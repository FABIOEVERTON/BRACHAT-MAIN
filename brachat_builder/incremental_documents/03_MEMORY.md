# DIRETRIZ DE MEMÓRIA (BRACHÁT)

Este documento registra a configuração da camada de memória de longo prazo persistente utilizando a API do **Mem0** (modalidade gratuita).

---

## 1. Topologia de Escopos
A memória é dividida em namespaces específicos associados a cada diretoria:

* **`josue_ops`:** 
  * Acesso de leitura/escrita por Josué e seus gerentes.
  * Armazena preferências de clientes, cronogramas operacionais e métricas de delivery.

* **`gilmario_knowledge`:**
  * Acesso por Gilmário e seus gerentes.
  * Armazena materiais de estudo, cronogramas da UBA, notas de currículo e rascunhos de branding.

* **`aisio_governance`:**
  * Acesso por Aísio e seus gerentes.
  * Armazena assinaturas de anomalia de segurança e histórico de auditorias.

* **`nice_domestic`:**
  * Acesso por Nice sob coordenação de Dona Lu.
  * Armazena listas de mercado, histórico de contas e preferências domésticas.

---

## 2. Isolamento Jurídico (Jessica Isolated Memory)
* **`jessica_legal`:**
  * Escopo **estritamente isolado**.
  * Apenas Jéssica e seus gerentes possuem acesso de leitura e escrita.
  * Armazena minutas contratuais e análises de riscos de passivos legais.
