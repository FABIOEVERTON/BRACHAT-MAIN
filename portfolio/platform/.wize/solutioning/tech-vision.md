# Visão Técnica de Engenharia — Plataforma BRACHATEC

## 1. Princípios de Arquitetura & Stack
* **Monorepo Estruturado (Turborepo):** Unificação de contratos de API (TypeScript/Pydantic), tipos compartilhados, portal web e microserviços.
* **Front-end Web & Portais:** Next.js 14+ (App Router), TypeScript strict mode, CSS nativo blindado com variáveis CSS consistentes com o design system do `site_oficial`.
* **Back-end & Motores de Negócio:** Python 3.12+ com **FastAPI** assíncrono para alto throughput e baixa latência.
* **Banco de Dados:** **PostgreSQL 16** com arquitetura de isolamento *schema-per-tenant* para garantir conformidade LGPD e sigilo governamental.
* **Segurança e Criptografia:**
  * Cadeia de custódia e laudos com hashes encadeados via **SHA-256**.
  * Armazenamento de laudos em **AWS S3 Object Lock (Compliance Mode / WORM)** em São Paulo (`sa-east-1`).
