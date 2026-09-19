"""Cofre WORM — S3 Object Lock COMPLIANCE (PRD §3.5, ADR-003).

- store: put_object COMPLIANCE + retain 10 anos (LGPD Art. 37) + SSE-KMS (prod)
- fetch: get_object — 404 → WORMVaultNotFoundError (RFC 7807, F0-28)
- get_signed_url: 1h (AWS) / URL direta (LocalStack dev)
"""

import os
from datetime import datetime, timedelta, timezone

import boto3
from botocore import UNSIGNED
from botocore.config import Config


class WORMVaultNotFoundError(Exception):
    """Chave ausente no cofre — converter em 404 RFC 7807 (F0-28)."""

    def __init__(self, key: str):
        self.key = key
        self.status_code = 404
        self.title = "Not Found"
        self.detail = f"objeto WORM não encontrado: {key}"
        super().__init__(self.detail)


class WORMVault:
    def __init__(self, *, endpoint_url: str | None = None, bucket: str | None = None,
                 region: str = "sa-east-1", retention_years: int = 10,
                 kms_key_id: str | None = None):
        self.endpoint = endpoint_url or os.environ.get("AWS_ENDPOINT_URL")
        self.bucket = bucket or os.environ.get("S3_WORM_BUCKET", "ezra-worm")
        self.retention_years = retention_years
        self.kms_key_id = kms_key_id or os.environ.get("S3_WORM_KMS_KEY")

        client_kwargs: dict = {"region_name": region}
        if self.endpoint:
            client_kwargs["endpoint_url"] = self.endpoint
            client_kwargs["aws_access_key_id"] = "test"
            client_kwargs["aws_secret_access_key"] = "test"
        else:
            client_kwargs["aws_access_key_id"] = os.environ.get("AWS_ACCESS_KEY_ID")
            client_kwargs["aws_secret_access_key"] = os.environ.get("AWS_SECRET_ACCESS_KEY")
            client_kwargs["config"] = Config(signature_version=UNSIGNED)

        self.s3 = boto3.client("s3", **client_kwargs)

    async def store(self, *, tenant_id: str, laudo_type: str, content: bytes,
                    metadata: dict) -> str:
        """F0-25: COMPLIANCE + retain +10y (+ SSE-KMS quando configurado)."""
        key = self._key(tenant_id, laudo_type)
        retain_until = datetime.now(timezone.utc) + timedelta(days=365 * self.retention_years)

        put_kwargs: dict = dict(
            Bucket=self.bucket,
            Key=key,
            Body=content,
            ContentType="application/pdf",
            Metadata={k: str(v) for k, v in metadata.items() if v},
            ObjectLockMode="COMPLIANCE",
            ObjectLockRetainUntilDate=retain_until,
        )
        if self.kms_key_id:
            put_kwargs["ServerSideEncryption"] = "aws:kms"
            put_kwargs["SSEKMSKeyId"] = self.kms_key_id

        self.s3.put_object(**put_kwargs)
        return key

    async def fetch(self, key: str) -> bytes:
        try:
            obj = self.s3.get_object(Bucket=self.bucket, Key=key)
        except Exception as e:
            if "404" in str(e) or "NoSuchKey" in str(e) or "not found" in str(e).lower():
                raise WORMVaultNotFoundError(key) from e
            raise
        return obj["Body"].read()

    async def get_signed_url(self, key: str) -> str:
        """URL assinada 1h (AWS); URL direta no LocalStack dev (F0-27)."""
        if self.endpoint:
            return f"{self.endpoint}/{self.bucket}/{key}"
        return self.s3.generate_presigned_url(
            "get_object", Params={"Bucket": self.bucket, "Key": key}, ExpiresIn=3600
        )

    @staticmethod
    def _key(tenant_id: str, laudo_type: str) -> str:
        ts = datetime.now(timezone.utc).isoformat(timespec="seconds").replace(":", "-")
        return f"{tenant_id}/{laudo_type}/{ts}.pdf"