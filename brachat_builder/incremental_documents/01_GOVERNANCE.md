# DIRETRIZ DE GOVERNANÇA (BRACHÁT)

Este documento registra as regras invariantes de compliance e governança do ecossistema.

---

## 1. Regras Invariantes (Absolutas)
1. **Auditoria por Aísio:** Toda ação e tráfego de mensagens podem ser auditados por Aísio em tempo real.
2. **Poder de Veto:** Aísio (`DIR_AISIO_001`) possui poder de veto universal sobre qualquer ação ou mensagem não autorizada ou que apresente comportamento anômalo.
3. **Kill Switch:** Um interruptor geral de emergência que desativa todos os agentes em nuvem. Requer comando de Aísio com dupla confirmação do CEO Fábio.
4. **Isolamento de Domínio:** Agentes domésticos (Nice) não podem sob nenhuma circunstância acessar bancos de dados corporativos ou dados contratuais.

---

## 2. Níveis de Risco e Auditoria
* **CRITICAL:** Logs com assinatura hash imutável gravados a cada evento (MGR_CTRL).
* **HIGH:** Auditoria com logs estruturados completos (Josué, Jéssica).
* **MEDIUM:** Logs operacionais padrões (Gilmário, Nice).
* **LOW:** Registros básicos de execução.
