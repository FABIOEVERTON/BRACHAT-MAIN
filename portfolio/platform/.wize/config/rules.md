# Regras Fixas de Engenharia e Roteamento de LLMs (BRACHATEC Platform)

## 1. Política de Conservação Contínua de Créditos
Para garantir operação ininterrupta e nunca esgotar créditos ou atingir rate limits:
1. **Atividades de Baixa/Média Complexidade (Padrão):**
   - Utilizar **Flash / Flash (Medium)** para navegação, criação de arquivos, testes unitários e codificação padrão (Shuri / Pepper / Peggy).
2. **Atividades de Alta Densidade / Raciocínio Crítico:**
   - Acionar modelos **Pro** ou **Big Pickle LLM via OpenCode / MCP** para:
     - Análise arquitetural profunda (Tony Stark).
     - Auditoria adversarial e gate final (Hawkeye).
     - Varredura de segurança / DAST / SAST complexo (Natasha Romanoff).
     - Resolução de ambiguidades técnicas críticas.
3. **Regra de Fallback e Troca:**
   - Ao menor sinal de saturação de contexto ou aproximação de limite de taxa, alternar a delegação de sub-tarefas para o modelo mais leve ou acionar o Big Pickle via MCP.
   - Sempre reutilizar artefatos em `.wize/` para evitar reprocessamento redundante de prompts.

## 2. Padrões de Integridade do Código
- **Fonte da Verdade:** `site_oficial/` é a referência canônica visual e de regras comerciais.
- **Rastreabilidade:** Toda alteração significativa deve ser registrada no `.wize/` correspondente.
