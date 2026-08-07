# ezra_bot

Cerebro 24/7 do Ezra (opencode serve) + bridge Telegram + infraestrutura OCI.

## Estrutura
- `.opencode/` - cérebro (instructions, skills, plugin, reference, proposals, plugin.json Agent Plugins v1.0.0)
- `deploy/` - arquivos de produção
  - `ezra-serve.service` - opencode serve 127.0.0.1:3791
  - `bridge_telegram.service` + `bridge_telegram.js` - relay Telegram (sem lógica, timeout 240s)
  - `nblm-refresh.timer` - refresh diário 03:00 UTC do auth NotebookLM
  - `parashat-bot.service` - ver projeto parashat_bot
  - `anti-reclaim.service` + `anti-reclaim.py` - carga sintética anti-reclaim (idle protection)
  - `sync-ezra.sh` - pipeline Mac -> Drive -> GitHub -> VM

## Infra (OCI)
- ezra_bot_1 163.176.111.95: PRODUÇÃO (serve + bridge + parashat + nblm). IP reservado.
- ezra_bot_2 137.131.242.180: utilitários (acquirer A1.Flex, oci-capture). Sem cérebro.
- Auth serve: Basic, user `opencode`, senha = OPENCODE_SERVER_PASSWORD (.env da VM, chmod 600).
- Segredos: secrets.env SOMENTE no Mac. VM usa .env próprio. Nada de segredo em git.
- NotebookLM: notebooklm-py 0.8.0, cookies em ~/.notebooklm/profiles/default/storage_state.json. Caderno TORAH_STUDIES e4274837-7838-4bbb-a490-8fde601e5c7a (131 fontes).

## Praxe
Salvar tudo no Google Drive e comitar de lá. Fonte da verdade: brachat-main (Drive) -> GitHub -> VM.
