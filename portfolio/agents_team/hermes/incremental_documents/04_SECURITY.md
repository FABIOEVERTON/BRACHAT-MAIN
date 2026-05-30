# DIRETRIZ DE SEGURANÇA (BRACHÁT)

Este documento descreve as diretrizes de segurança Zero-Trust e restrições de sandbox para execução do ecossistema.

---

## 1. Arquitetura Zero-Trust
* **Validação por Transação:** Cada transação ou comando executado por gerentes é tratado como potencialmente hostil até que passe pelas validações de Aísio.
* **Sem Acesso de Escrita Direto:** Nenhum agente operacional pode alterar diretamente configurações críticas de infraestrutura ou códigos-fonte sem a revisão em conjunto com o CEO no Mac local.

---

## 2. Restrições do Sandbox
* **Nice Isolation:** O código em execução da Nice (`nice_core.py`) roda em sandbox separado da infraestrutura corporativa do Hugging Face.
* **APIs Seguras:** Todas as chaves e segredos de APIs devem ser carregadas em tempo de execução via `apis.env` (armazenadas em variáveis secretas do Hugging Face Spaces/GitHub Actions), nunca gravadas no código.
