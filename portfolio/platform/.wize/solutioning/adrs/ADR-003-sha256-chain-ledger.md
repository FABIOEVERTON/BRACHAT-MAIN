# ADR-003: Cadeia de Custódia Probatória SHA-256 com Custódia WORM

* **Status:** Aceito
* **Contexto:** Os laudos periciais e eventos de auditoria precisam de validade jurídica inquestionável perante tribunais e órgãos reguladores (ANPD, TCE, TCU).
* **Decisão:** Cada registro no ledger vincula o hash do registro anterior criando uma cadeia de blocos sequencial e imutável, exportada para S3 Object Lock (WORM).
* **Consequências:** Integridade matemática verificável por qualquer auditor independente; lock-in técnico de alto valor para o cliente.
