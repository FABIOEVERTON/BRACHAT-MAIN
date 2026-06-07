# 🛡️ OPTIMIZED_POLICIES: Manual de Políticas Otimizadas e Mapeamento Cruzado

Este documento unifica e consolida as políticas de governança e desenvolvimento originadas das configurações do **Claude Code** (`.claude.json`), do **Workflow de 8 Fases**, da governança **AGCP/QUILIS** e das diretrizes gerais do **GEMINI.md**. O objetivo é garantir a máxima eficiência operacional do **Brachat Construtor** com foco em: **Rapidez, Economia de Tokens e Segurança**.

---

## 📊 1. Tabela de Mapeamento Cruzado de Políticas

| Origem | Regra de Negócio / Configuração | Pilar Impactado | Aplicação Prática no Construtor |
| :--- | :--- | :--- | :--- |
| **`.claude.json`** | Timeout estrito de ferramentas (Bash 30s, Grep 20s) | ⚡ Rapidez | O daemon aborta execuções de comandos locais longos ou travados imediatamente. |
| **`GEMINI.md`** | Leitura restrita por delimitadores (`StartLine`/`EndLine`) | 🪙 Economia de Tokens | Proibido ler arquivos de código inteiros. Apenas trechos úteis entram no contexto. |
| **`GEMINI.md`** | Edição cirúrgica via `multi_replace_file_content` | 🪙 Economia de Tokens | Proibido reescrever arquivos completos. Modificações são aplicadas bloco a bloco. |
| **`GOVERNANCE`** | Workspace Guard (`chmod 444` por padrão) | 🔒 Segurança | Código-fonte permanece travado como somente-leitura, imune a injeções acidentais. |
| **`GOVERNANCE`** | Invariante de Rastreabilidade (Plano Técnico Aprovado) | 🔒 Segurança / Rastreabilidade | Bloqueia modificações em arquivos que não foram pré-declarados no plano. |
| **`.claude.json`** | Compactação de Contexto (Limite de 150k tokens) | 🪙 Economia de Tokens | O daemon compacta o histórico para manter a esteira rápida e de baixo consumo. |
| **`GEMINI.md`** | Exclusão de indexação de pastas como `node_modules` | ⚡ Rapidez / Economia | O `Grep` e `Find` ignoram diretórios gigantes de dependências para não estourar o prompt. |
| **`GOVERNANCE`** | Git Pre-Commit Hook local ativo | 🔒 Segurança | Valida se a esteira passou por planejamento antes de autorizar o commit. |
| **`GEMINI.md`** | Uso de Llama 3.3 e Groq como fallback gratuito | ⚡ Rapidez / Custo | Evita limites rígidos de cota e queda na latência do processamento. |

---

## ⚡ 2. Pilar da Rapidez (Speed Optimization)

Para manter a velocidade das interações e execução das ferramentas no terminal:
1. **Comando Timeout:** Toda execução física de scripts no macOS através do Hermes deve rodar com timeout máximo de **30 segundos**.
2. **Varredura Otimizada:** Varreduras de buscas em diretórios devem usar o comando `grep` apontando para tipos específicos de arquivos (ex: `--include="*.py"`), reduzindo o tempo de CPU.
3. **Inference Routing:** O runtime do Hermes e Ezra prioriza conexões rápidas por sockets ou chamadas HTTP para o roteador Llama 3.3 no Hugging Face (tempo médio de resposta <1.5s).

---

## 🪙 3. Pilar da Economia de Tokens (Context & Token Economy)

Para mitigar o estouro de contexto e o desperdício financeiro de chamadas de LLM:
1. **Constituição de Leitura de Arquivo:**
   * Nunca abrir arquivos inteiros maiores que **50 linhas** se apenas um método/bloco for relevante.
   * Utilizar buscas `grep` pontuais primeiro para localizar os números das linhas (`StartLine`/`EndLine`).
2. **Compactação de Turno:**
   * O estado local do chat e do daemon é reavaliado a cada **10 chamadas de ferramentas**. Sessões de desenvolvimento longas disparam um resumo intermediário e limpam os logs de execução da memória RAM.
3. **Escopos de Busca Ignorados:**
   * Estão permanentemente banidos de indexação ou leituras:
     * `node_modules/`, `bower_components/`, `dist/`, `build/`, `.next/`, `.nuxt/`
     * Arquivos de lock (`package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`)
     * Bancos de dados locais (`.db`, `.db-wal`, `.db-shm`) e caches (`.mypy_cache`, `__pycache__`).

---

## 🔒 4. Pilar da Segurança (Zero Trust & Compliance)

Para mitigar riscos regulatórios e cibersegurança nos ambientes de produção e Mac local:
1. **Princípio de Menor Privilégio (Least Privilege):**
   * Agentes de desenvolvimento (`Coder`, `Researcher`) não possuem acesso às chaves de API do ecossistema principal.
   * O acesso a variáveis sensíveis no arquivo `/Users/mac/apis/apis.env` é ocultado através de rotinas de sanitização de logs.
2. **Lock de Workspace:**
   * O destravamento dinâmico para gravação física do `Coder` (`chmod 644`) expira imediatamente após o encerramento da Fase 5 (Development). O Hermes executa `chmod 444` recursivo de forma automática.
3. **Git Pre-Commit Gatekeeping:**
   * O gancho Git físico localizado em `hooks/pre-commit` bloqueia qualquer commit direto que contenha logs ou variáveis confidenciais, ou que não possua metadados válidos assinados no `.brachat-state.json`.
