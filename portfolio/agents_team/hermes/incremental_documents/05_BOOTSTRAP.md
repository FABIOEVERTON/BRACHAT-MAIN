# DIRETRIZ DE INICIALIZAÇÃO / BOOTSTRAP (BRACHÁT)

Este documento registra a ordem cronológica obrigatória para inicialização segura do ecossistema BRACHÁT.

---

## 1. Sequência de Inicialização
Para evitar inconsistências ou acessos indevidos antes da ativação do firewall de segurança, siga esta ordem:

```text
Passo 0: Carregar APIs (apis.env) ➔ Validar Mem0
   ▼
Passo 1: Iniciar Aísio (Governança & Auditoria)
   ▼
Passo 2: Iniciar Hermes (Mensageria & Roteador)
   ▼
Passo 3: Iniciar Diretores (Josué, Gilmário, Jéssica)
   ▼
Passo 4: Iniciar Nice (Núcleo Familiar / Sandbox Doméstico)
```

---

## 2. Critério de Sucesso
O sistema só é considerado **100% Operacional** quando:
1. Conexão com o Mem0 for estabelecida com sucesso.
2. Aísio estiver ouvindo e registrando eventos sem falhas.
3. O bot do Telegram do Josué estiver respondendo no chat ID autorizado.
