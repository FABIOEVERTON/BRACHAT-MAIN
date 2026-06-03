# Skills Library — 1475 Skills Especializados

Catálogo de skills para agente de IA, indexados e pesquisáveis sob demanda.

## Índice

O índice em `skills-cache/index.json` contém todos os 1475 skills com:
- **name** — Nome do diretório
- **desc** — Descrição curta extraída do SKILL.md / README.md
- **tags** — Palavras-chave derivadas do nome

## Como funciona

1. Usuário faz uma pergunta
2. Automaticamente busca no índice por match de tags/name/desc
3. Se achar skill relevante, carrega o conteúdo e aplica
4. Sem custo de tokens — consulta sob demanda

## Exemplos de skills

| Skill | Descrição |
|-------|-----------|
| `kubernetes-deployment` | Kubernetes deployment workflow |
| `devops-deploy` | DevOps e deploy — Docker, CI/CD |
| `accessibility-compliance` | Auditoria de acessibilidade |
| `zod-validation-expert` | Validação Zod TypeScript |
| `zustand-store-ts` | Estado global com Zustand |

## Estrutura

```
.agents/skills 13.58.16/
├── 00-andruia-consultant/
├── 3d-web-experience/
├── kubernetes-deployment/
├── zod-validation-expert/
├── ... (1475 diretórios)
└── zustand-store-ts/
```
