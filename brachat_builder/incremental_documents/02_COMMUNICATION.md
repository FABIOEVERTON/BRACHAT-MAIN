# DIRETRIZ DE COMUNICAÇÃO (BRACHÁT)

Este documento descreve as regras de roteamento de eventos e o formato padrão de comunicação entre os agentes gerenciados pelo Hermes.

---

## 1. Regras de Roteamento (Hermes)
* Toda comunicação deve possuir um `context_id` único gerado na origem.
* O Hermes valida se o remetente tem permissão explícita para enviar mensagens ao destinatário (de acordo com a matriz de permissões do Registry).
* Mensagens não autenticadas ou com desvio de domínio são bloqueadas e reportadas imediatamente para Aísio.

---

## 2. Formato Padrão de Mensagem (JSON Schema)
```json
{
  "context_id": "string (ex: CTX_20260529_001)",
  "sender_id": "string (ex: DIR_JOSUE_001)",
  "receiver_id": "string (ex: DIR_JESSICA_001)",
  "timestamp": "ISO 8601 string",
  "payload": {
    "action": "string",
    "data": "object"
  },
  "signature": "string"
}
```
