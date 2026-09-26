# WIZE CODE REVIEW CHECKLIST

Checklist de validação obrigatório executado pelo **Hawkeye (`wize-agent-test-architect`)** e pelos agentes antes de considerar qualquer alteração concluída.

---

## 🔍 1. Entendimento & Escopo
- [ ] A alteração atende exatamente ao objetivo da tarefa e aos Critérios de Aceite (ACs)?
- [ ] O escopo foi mantido estritamente no necessário (sem alterações não solicitadas)?
- [ ] A compatibilidade retroativa e o comportamento existente foram preservados?

## 🏷️ 2. Nomenclatura & Legibilidade
- [ ] Todas as variáveis, classes e funções possuem nomes que revelam sua intenção?
- [ ] Foram eliminados nomes genéricos (`data`, `temp`, `manager`, `helper`, `process`)?
- [ ] O código é autoexplicativo, dispensando comentários descritivos redundantes?

## ⚙️ 3. Funções & Complexidade
- [ ] Cada função faz apenas uma coisa e possui nível único de abstração?
- [ ] A quantidade de parâmetros está limitada a no máximo 3 argumentos?
- [ ] A complexidade ciclomática está controlada com uso de cláusulas de guarda (*early returns*)?
- [ ] Não há aninhamento de condicionais superior a 2 níveis?

## 🛡️ 4. Segurança & Privacidade (LGPD / OWASP)
- [ ] Zero credenciais, chaves de API, senhas ou tokens hardcoded?
- [ ] Todas as consultas SQL utilizam queries parametrizadas / ORM blindado?
- [ ] Dados pessoais (PII) estão mascarados em logs e saídas de erro?
- [ ] Há validação estrita de tipos na entrada de dados?

## ⚠️ 5. Tratamento de Erros
- [ ] Não existem blocos `except:` / `catch {}` vazios que engolem exceções silenciosamente?
- [ ] As exceções lançadas são de domínio específico com mensagens contextuais claras?
- [ ] A causa original do erro é preservada ao relançar exceções?

## 🧪 6. Testes & Qualidade Automatizada
- [ ] Testes unitários e de integração foram criados ou atualizados para o trecho modificado?
- [ ] 100% dos testes disponíveis foram executados e passaram sem falhas?
- [ ] O linter e o formatter do projeto foram executados sem avisos pendentes?
- [ ] O diff final foi revisado linha por linha antes do commit?
