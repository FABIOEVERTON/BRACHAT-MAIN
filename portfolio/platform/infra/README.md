# Infra — Plataforma EZRA

- `terraform/` — IaC AWS **sa-east-1** (ADR-008): RDS Multi-AZ, S3 Object Lock COMPLIANCE (WORM 10a), SQS, ECS Fargate, CloudFront. Região fixa + AWS Config rule (sair de sa-east-1 = alerta). Real na E0-S10/CI.
- `docker/` — Dockerfile services + compose (dev LocalStack). Real na E0-S02.