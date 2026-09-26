# WIZE GLOBAL ENFORCEMENT POLICY

Esta política estabelece os requisitos mandatórios universais de engenharia de software para todos os agentes do **Wize Developer Kit**. Ela tem precedência sobre preferências estilísticas e orienta toda e qualquer alteração de código.

---

## 1. Entendimento Antes da Alteração
O agente está terminantemente proibido de alterar qualquer código sem antes:
- Identificar o objetivo exato da tarefa e os requisitos explícitos.
- Localizar todos os arquivos envolvidos e mapear o fluxo de dados atual.
- Verificar testes existentes, comportamento esperado e convenções do projeto.
- Avaliar riscos de regressão, dependências e efeitos colaterais.
- Confirmar que a alteração pertence estritamente ao escopo da demanda.

## 2. Alteração Mínima Segura
O agente deve aplicar o princípio da menor alteração suficiente para resolver o problema com robustez.
**É expressamente proibido:**
- Refatorar arquivos ou trechos não relacionados à tarefa atual.
- Modificar contratos de APIs públicas ou interfaces sem necessidade explícita.
- Trocar bibliotecas, frameworks ou dependências por preferência pessoal.
- Alterar padrões arquiteturais consolidados sem uma ADR aprovada.
- Aplicar formatação em massa em código legado fora do escopo.
- Introduzir abstrações prematuras sem consumidores reais.
- Reescrever código funcional sem ganho mensurável e testado.

## 3. Preservação de Comportamento
Toda modificação deve preservar integralmente o comportamento observável existente, exceto quando a alteração comportamental for a meta declarada da tarefa.
Se houver qualquer risco de quebra:
- Criar testes de regressão antes de modificar a implementação.
- Mapear e validar todos os fluxos impactados.
- Declarar o risco e a alteração no relatório final de conformidade.

## 4. Testes Obrigatórios
Nenhuma tarefa que altere lógica de negócio ou persistência pode ser dada como concluída sem validação automatizada.
O agente deve criar ou atualizar testes ao:
- Corrigir bugs ou falhas de regressão.
- Implementar novas regras de negócio ou fluxos condicionais.
- Criar ou modificar endpoints de API e contratos de payload.
- Alterar validações de entrada, serialização ou esquemas de banco.
- Modificar fluxos de autenticação, autorização ou segurança.
- Tratar novos casos de erro ou exceções.

## 5. Proibição de Código Especulativo
O agente nunca deve escrever código baseado em suposições futuras ("YAGNI - You Aren't Gonna Need It").
É proibido criar:
- Funções, métodos ou classes sem chamadores ativos.
- Parâmetros opcionais "para uso futuro" sem caso de uso atual.
- Interfaces e camadas de abstração genéricas sem múltiplos clientes reais.
- Código "por precaução" não respaldado por requisitos.

## 6. Nomes Significativos e Intencionais
Nomes devem revelar expressamente a intenção do código.
- Proibido o uso de identificadores vagos (`data`, `result`, `item`, `val`, `temp`, `foo`, `bar`, `manager`, `helper`, `utils`, `process`, `handle`, `doSomething`) salvo em contextos matemáticos estritos devidamente comentados.
- Nomes de classes e entidades devem ser substantivos (`ForensicLedger`, `TenantResolver`).
- Nomes de funções e métodos devem iniciar por verbos de ação (`calculate_chained_hash`, `verify_signature`).

## 7. Funções Pequenas, Coesas e com Nível Único de Abstração
- Funções devem fazer apenas uma coisa e fazê-la com excelência (Single Responsibility).
- Manter nível único de abstração por função (evitar misturar I/O de baixo nível com regras de negócio de alto nível).
- Limitar parâmetros a no máximo 3 argumentos (acima disso, encapsular em objeto de configuração/DTO).
- Evitar efeitos colaterais ocultos (funções de consulta não devem alterar estado).
- Não dividir funções de forma mecânica apenas para reduzir linhas; a divisão deve produzir abstrações com significado semântico real.

## 8. Tratamento Robusto e Seguro de Erros
- Proibido ignorar exceções ou deixar blocos `except:` / `catch {}` vazios.
- Proibido engolir erros silenciosamente ou retornar valores mágicos (`null`, `-1`) sem documentação explícita de contrato.
- Erros devem ser capturados onde há capacidade de recuperação ou logados com contexto semântico detalhado (sem expor stack traces ou dados sensíveis ao usuário final).
- Toda exceção relançada deve preservar a causa raiz original.

## 9. Testabilidade & Injeção de Dependências
Código deve nascer testável por design:
- Evitar acoplamento direto a variáveis globais, relógios de sistema não mockáveis (`datetime.now()`) ou números aleatórios puros.
- Isolar acesso a I/O, banco de dados e APIs externas através de injeção de dependências ou adaptadores claros.
- Testes unitários devem ser independentes, determinísticos e executáveis em qualquer ordem sem estado compartilhado.

## 10. Segurança em Primeiro Lugar
Segurança é requisito não-funcional inegociável em 100% das alterações:
- Validação estrita de tipos e sanitização de toda entrada de usuário.
- Prevenção contra SQL Injection (uso obrigatório de queries parametrizadas/ORMs).
- Proibido hardcoding de credenciais, tokens JWT, senhas ou chaves de API no código-fonte.
- Mascaramento de dados pessoais (PII) em logs e armazenamento criptografado em repouso e trânsito.

## 11. Gestão Consciente de Dependências
- Não adicionar bibliotecas externas para resolver problemas triviais solucionáveis com a biblioteca padrão.
- Avaliar licença, vulnerabilidades conhecidas (CVEs), impacto no bundle/runtime e saúde do repositório antes de propor dependências.

## 12. Comentários Úteis vs Código Autoexplicativo
- O código deve ser tão claro que dispense comentários descritivos óbvios.
- Comentários devem existir exclusivamente para explicar **o porquê** de decisões não triviais, algoritmos complexos, requisitos regulatórios ou restrições de terceiros.
- Proibido deixar código comentado (código morto) no repositório.

## 13. Refatoração Disciplinada
- Toda refatoração deve possuir escopo delimitado, manter a compatibilidade da interface pública e ser respaldada por testes que garantam zero alteração de comportamento.
- Separar rigorosamente commits de refatoração de commits de novas features funcionais.

## 14. Análise Crítica da Duplicação (DRY Consciente)
- Antes de unificar código duplicado, avaliar se os trechos compartilham a mesma razão de mudança ou se a semelhança é meramente coincidente.
- Evitar acoplamento indevido entre módulos distintos através de abstrações artificiais criadas apenas para eliminar 2 linhas repetidas.

## 15. Resolução de Conflitos entre Regras (Ordem de Precedência)
Em caso de tensão entre diretrizes, a ordem estrita de desempate é:
1. **Segurança e Privacidade de Dados** (NIST / LGPD / OWASP)
2. **Correção Funcional e Integridade de Negócio**
3. **Requisitos Explícitos do Usuário**
4. **Compatibilidade e Preservação de Contratos**
5. **Testabilidade**
6. **Simplicidade (KISS / YAGNI)**
7. **Legibilidade e Coesão**
8. **Performance Otimizada**
9. **Preferências Estilísticas / Cosméticas**
