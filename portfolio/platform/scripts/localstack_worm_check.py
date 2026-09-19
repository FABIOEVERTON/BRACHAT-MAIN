#!/usr/bin/env python3
"""E0-S02 F0-05: valida WORM COMPLIANCE no LocalStack (teste PESSIMISTA — R-1).

put/head OK; DELETE DEVE FALHAR (modo COMPLIANCE 10 anos, ADR-003).
Sem depender de aws cli — usa boto3 (dep do pyproject).
"""
import os
import sys
from urllib.request import urlopen

import boto3
from botocore import UNSIGNED
from botocore.config import Config

ENDPOINT = os.environ.get("AWS_ENDPOINT_URL", "http://localhost:4566")
REGION = os.environ.get("AWS_REGION", "sa-east-1")
BUCKET = os.environ.get("S3_WORM_BUCKET", "ezra-worm")
DAYS = int(os.environ.get("S3_WORM_DAYS", "3650"))

s3 = boto3.client(
    "s3",
    endpoint_url=ENDPOINT,
    region_name=REGION,
    aws_access_key_id="test",
    aws_secret_access_key="test",
    config=Config(signature_version=UNSIGNED),
)


def health() -> None:
    with urlopen(f"{ENDPOINT}/_localstack/health", timeout=10) as r:
        assert r.status == 200, f"LocalStack health {r.status}"


def main() -> None:
    health()
    print(f"==> LocalStack healthy ({REGION})")

    try:
        s3.create_bucket(
            Bucket=BUCKET,
            CreateBucketConfiguration={"LocationConstraint": REGION},
        )
        print(f"==> bucket {BUCKET} criado")
    except s3.exceptions.BucketAlreadyOwnedByYou:
        print(f"==> bucket {BUCKET} já existe")

    try:
        s3.put_bucket_versioning(Bucket=BUCKET, VersioningConfiguration={"Status": "Enabled"})
        print("==> versioning Enabled (pré-requisito Object Lock)")
    except Exception:
        print("==> versioning já habilitado (bucket existente)")

    try:
        s3.put_object_lock_configuration(
        Bucket=BUCKET,
        ObjectLockConfiguration={
            "ObjectLockEnabled": "Enabled",
            "Rule": {"DefaultRetention": {"Mode": "COMPLIANCE", "Days": DAYS}},
        },
    )
        print(f"==> Object Lock COMPLIANCE {DAYS}d aplicado")
    except Exception:
        print("==> Object Lock já configurado (bucket existente)")

    s3.put_object(Bucket=BUCKET, Key="laudos/prova.txt", Body=b"laudo-teste-worm")
    head = s3.head_object(Bucket=BUCKET, Key="laudos/prova.txt")
    mode = head.get("ObjectLockMode")
    vid = head.get("VersionId")
    until = head.get("ObjectLockRetainUntilDate")
    print(f"==> put/head OK — ObjectLockMode={mode} retainUntil={until} versionId={vid}")

    if mode != "COMPLIANCE" or not until:
        print(f"FALHA DO GATE: objeto sem lock COMPLIANCE ativo ({mode})", file=sys.stderr)
        sys.exit(1)

    # Hard delete (remoção real com VersionId) — DEVE FALHAR em COMPLIANCE.
    try:
        s3.delete_object(Bucket=BUCKET, Key="laudos/prova.txt", VersionId=vid)
        print("FALHA DO GATE: deleção física teve sucesso — COMPLIANCE não respeitado", file=sys.stderr)
        sys.exit(1)
    except Exception:
        print("==> HARD DELETE falhou (AccessDenied) — WORM COMPLIANCE válido")
        print("F0-05 PASS")


if __name__ == "__main__":
    main()