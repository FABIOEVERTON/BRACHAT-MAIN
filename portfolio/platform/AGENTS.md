# Wize Developer Kit — Diretrizes Globais de Agentes

Todos os agentes de IA atuando neste repositório (Shuri, Tony Stark, Hawkeye, Maria Hill, Natasha Romanoff, Mantis, Pepper Potts, Peggy Carter, Nick Fury e Wizer) devem obrigatoriamente:

1. **Ler e Obedecer às Políticas Oficiais:**
   - [`WIZE_GLOBAL_ENFORCEMENT_POLICY.md`](./WIZE_GLOBAL_ENFORCEMENT_POLICY.md)
   - [`WIZE_CLEAN_CODE_POLICY.md`](./WIZE_CLEAN_CODE_POLICY.md)
2. **Respeitar Rigorosamente o Escopo:** Aplicar a menor alteração segura necessária para resolver a tarefa sem refatorar código alheio fora do escopo.
3. **Prioridade de Segurança:** Tratar regras `BLOCKER` e `CRITICAL` (como [WCC-05] e [WCC-06] sobre tratamento de erros e segurança/segredos) com tolerância zero.
4. **Testabilidade Obrigatória:** Nenhuma alteração de código ou regra de negócio está concluída sem testes automatizados correspondentes ([WCC-07]).
5. **Relatório Final Padrão:** Toda alteração de código deve ser finalizada com o Relatório de Conformidade preenchido conforme [`WIZE_AGENT_SYSTEM_PROMPT.md`](./WIZE_AGENT_SYSTEM_PROMPT.md).
6. **Cérebro de Alto Capítulo (Automático):** Para QUALQUER implementação de código (gerar, modificar, testar ou criar arquivos), chamar a ferramenta MCP `ask_bigpickle` (OpenCode BigPickle). Ela executa com capacidade superior à do Gemini local. Usar SEMPRE que a tarefa exigir código real — nunca implementar direto no Gemini local. Aguardar o retorno do BigPickle e aplicar o resultado no repositório, mantendo as regras 1-5.
