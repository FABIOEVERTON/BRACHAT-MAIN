# Pontos de Risco (Risk Spots)

- **Sincronia Frontend/Backend:** O backend ainda precisa ser completamente implementado para alimentar os formulários de contato, login e cadastro do frontend em `site_oficial/app/`.
- **Rotas Relativas:** Os arquivos HTML de `app/` utilizam caminhos relativos que precisam ser mantidos íntegros se o sistema de roteamento (ex: Next.js) for introduzido depois.
- **Banco de Dados (Ledger):** A integridade das trilhas WORM e hashes SHA-256 (tabela `forensic_ledger`) é crítica e qualquer inconsistência na fase 11 pode corromper a promessa de imutabilidade.
