# ADR-002: Isolamento de Dados Schema-per-Tenant no PostgreSQL 16

* **Status:** Aceito
* **Contexto:** Atendemos prefeituras municipais e clientes corporativos de compliance com rigorosas exigências de segregação de dados.
* **Decisão:** Implementar PostgreSQL 16 com criação dinâmica de schemas isolados (`tenant_{slug_ou_id}`) para cada organização cadastrada.
* **Consequências:** Isolamento físico lógico absoluto, facilidade de backup/restauração individual e garantia contra vazamentos cross-tenant.
