# Tech Vision — Plataforma BRACHATEC

## 1. Princípio de Arquitetura Core: Isolamento por Ramo (Branch-Level Isolation)
A plataforma **não** é um monólito. Devido à nossa estratégia agressiva de parcerias **White-Label**, é fundamental que os três grandes ramos da plataforma operem de forma 100% isolada e independente.

Se um escritório parceiro (White-Label) contratar apenas o módulo de Governança de IA, ele não pode compartilhar infraestrutura ou banco de dados com a Prefeitura que comprou o módulo de Setor Público.

### Diretriz Inviolável:
* **Frontend Próprio:** Cada ramo (IA, Público, RIG) possui sua própria interface logada. O site público atua apenas como funil de vendas e redirecionador para o gateway de pagamento.
* **Backend Separado:** OBRIGATÓRIO ter microsserviços e APIs isoladas para cada ramo. `backend/gov_ai`, `backend/gov_muni`, `backend/rig_tech`.
* **Banco de Dados Totalmente Independente:** Não há compartilhamento de base de dados entre os ramos. Cada cluster de backend aponta para o seu próprio banco de dados (e dentro de cada banco de dados, mantemos o *schema-per-tenant* para isolar os clientes).

## 2. Jornada e Integração
1. O usuário entra na Home Page (`site_oficial/index.html`).
2. Ele é direcionado para a página de vendas do produto (ex: `aigovernance/index.html`).
3. Da página do produto, ele é enviado ao Gateway de Pagamento.
4. Após o sucesso do pagamento (via Webhook Idempotente), o tenant é provisionado no banco de dados **específico** do ramo que ele comprou.
5. Ele recebe acesso ao App/Frontend exclusivo daquele ramo.

## 3. Padrões Tecnológicos (Stack)
* **Frontend:** Padrão Next.js / TypeScript.
* **Backend:** Python (FastAPI Assíncrono) totalmente modularizado nos 3 ramos.
* **Criptografia & Prova (AGCP & superXAi):** Implementados de maneira isolada no backend correspondente (ex: superXAi pertence apenas ao cluster de Governança de IA).
