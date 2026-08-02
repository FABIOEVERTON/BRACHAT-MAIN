---
name: osint-security-assessment
id: S24
cluster: seguranca
description: Executa investigação OSINT metódica com verificação cruzada obrigatória e relatório com confidence levels.
---

### Objetivo
Executar investigação OSINT metódica em pessoas físicas, pessoas jurídicas, domínios, IPs, emails e usernames para due diligence, background check para contratação, investigação defensiva, e auditoria de segurança. Aplica coleta silenciosa em fontes públicas, verificação cruzada obrigatória, e emissão de relatório com confidence levels.

### 1. Regras Fundamentais

**Documentação** — cada fonte consultada deve ser registrada com URL, data/hora, e conteúdo capturado.

**Verificação cruzada** — nenhum dado isolado constitui fato; exige corroboração mínima de duas fontes independentes.

**Separação de camadas** — distinguir sempre: FATO VERIFICADO / INFERÊNCIA / HIPÓTESE / ESPECULAÇÃO.

**Postura do Agente:**
- Modo coleta silenciosa: não interagir com o alvo, não criar contas para acessar dados restritos.
- Registrar TODOS os passos em log estruturado.
- Emitir relatório final com confidence levels: HIGH / MEDIUM / LOW / INSUFFICIENT.
- Sinalizar explicitamente quando uma informação não puder ser verificada.

### 2. Fases da Investigação

#### FASE 0 — Definição do Alvo (Mandatory)

Antes de qualquer ação, registrar:

| Campo | Exemplo |
|---|---|
| ALVO_TIPO | pessoa_fisica, pessoa_juridica, dominio, IP, handle, organizacao |
| ALVO_ID | nome, CPF/CNPJ, dominio, IP, username |
| OBJETIVO | due_diligence, contratacao, investigacao_jornalistica, seguranca_defensiva, pesquisa |
| ESCOPO | Brasil, internacional, digital, fisico, todos |
| RESTRICOES | o que NAO investigar |

Se qualquer campo estiver ausente, solicitar ao operador antes de prosseguir.

#### FASE 1 — Reconhecimento Passivo (Footprinting)

**1.A — Pessoas Físicas**

| Fonte | Dado Alvo | Ferramenta / Método |
|---|---|---|
| Google Dorks | Menções públicas, documentos vazados | site:, filetype:, inurl:, intext: |
| Redes Sociais | Perfis, conexões, localização, rotina | Busca manual + sherlock / maigret |
| LinkedIn | Histórico profissional, vínculos corporativos | Busca direta + dorks site:linkedin.com |
| SERASA/SPC público | Restrições (não acessa dados privados) | Verificação de disponibilidade pública |
| Cartórios (Brasil) | Registros imobiliários públicos | Portais estaduais de cartório |
| Diário Oficial | Cargos públicos, nomeações, licitações | diariooficial.net, portais gov.br, DOU (in.gov.br) |
| Processos judiciais | Litígios, execuções, falências | CNJ, TJDFT, TJSP, TJRJ, TRFs, TST — consulta pública |
| PF/Polícia Federal | Inquéritos (via MPF/transparência) | Transparência MPF, site da PF |
| MPF | Inquéritos civis e criminais | transparencia.mpf.mp.br |
| CPF (parcial) | Validação de formato e situação | Receita Federal (consulta pública de situação) |

Google Dorks de alta eficácia para pessoas:
```
"[nome completo]" filetype:pdf site:gov.br
"[nome completo]" CPF OR cnpj
"[nome completo]" site:linkedin.com OR site:facebook.com
"[nome completo]" "telefone" OR "endereço" OR "email" site:br
"[nome]" inurl:licitacao OR inurl:pregao
```

**1.B — Pessoas Jurídicas / CNPJs**

| Fonte | Dado Alvo | Acesso |
|---|---|---|
| Receita Federal | Situação cadastral, sócios, capital | gov.br/receitafederal |
| SINTEGRA / SEFAZ | Situação estadual, IE | Por UF |
| Simples Nacional | Enquadramento tributário | Portal Simples Nacional |
| BrasilAPI | CNPJ consolidado, QSA | brasilapi.com.br (API gratuita, sem auth) |
| Portal da Transparência | Fornecedores, valores recebidos | portaltransparencia.gov.br |
| Junta Comercial | Estatutos, alterações, procurações | Por UF (ex: JUCESP, JUCEES) |
| TCU | Irregularidades, sanções, inidôneos | portal.tcu.gov.br |
| CGU (CEIS, CNEP, CEPIM) | Sanções, impedimentos, punições | portaldatransparencia.gov.br/sancoes |

Comandos:
```bash
curl "https://brasilapi.com.br/api/cnpj/v1/[CNPJ_SEM_PONTUACAO]" | jq .
curl "https://brasilapi.com.br/api/cnpj/v1/[CNPJ]" | jq '.qsa[]'
```

**1.C — Domínios e Infraestrutura**

```bash
whois dominio.com.br
whois -h whois.registro.br dominio.com.br   # .br
dig dominio.com.br ANY
dig +short MX dominio.com.br
dig +short TXT dominio.com.br
nslookup -type=NS dominio.com.br

# Certificados SSL — enumeração de subdomínios
curl "https://crt.sh/?q=%.dominio.com.br&output=json" | jq '.[].name_value' | sort -u

# Tecnologias do site
curl -s -I https://dominio.com.br
# Verificar headers: Server, X-Powered-By, Set-Cookie, CSP
```

**1.D — Endereços IP**

```bash
curl "https://ipapi.co/[IP]/json/" | jq .
curl "https://ipinfo.io/[IP]/json" | jq .

# Reputação (navegador): Shodan, AbuseIPDB, VirusTotal
```

#### FASE 2 — Enumeração de Identidade Digital

**2.A — Usernames / Handles**
```bash
sherlock [username] --timeout 10 --output sherlock_[username].txt
maigret [username] --html
```
Catálogo de sites por categoria: https://whatsmyname.app/

**2.B — E-mails**
```bash
# HIBP — breaches
curl "https://haveibeenpwned.com/api/v3/breachedaccount/[email]" -H "hibp-api-key: [KEY]"

# Hunter.io — verificação de formato e domínio corporativo
curl "https://api.hunter.io/v2/email-verifier?email=[email]&api_key=[KEY]"

# Google Dorks para e-mail
# site:pastebin.com "[email]"
# site:github.com "[email]"
```

**2.C — Telefones (Brasil)**
| Fonte | Método |
|---|---|
| Google | "[DDD] [NÚMERO]" + nome esperado |
| TrueCaller web | truecaller.com/search/br/[numero] |
| ANATEL | Consulta de Portabilidade |
| Processos judiciais | CNJ + nome do alvo |

#### FASE 3 — Análise de Vínculos e Grafo Relacional

**3.A — Mapeamento de Sócios (Brasil)**
```bash
# Para cada CNPJ, extrair QSA
curl "https://brasilapi.com.br/api/cnpj/v1/[CNPJ]" | jq '.qsa[] | {nome: .nome_socio, cpf: .cnpj_cpf_do_socio, qualificacao: .qualificacao_socio}'

# Para cada CPF de sócio, buscar outros CNPJs vinculados
```

**3.B — Grafo de Relacionamentos**
```
ENTIDADE_A | TIPO_VÍNCULO | ENTIDADE_B | FONTE | DATA | CONFIANÇA
```

**3.C — Ferramentas de Grafo**
| Ferramenta | Categoria | Uso Primário | Acesso |
|---|---|---|---|
| Maltego | Grafo visual | Conectar entidades (pessoas, empresas, domínios, IPs), identificar padrões ocultos e redes de influência via transforms automáticos | CE gratuito; Pro/Enterprise pago |
| i2 Analyst's Notebook | Grafo criminal | Padrão ouro em forças policiais; mapeia fluxo de eventos e relações complexas entre alvos ao longo do tempo | Licença corporativa (IBM) |
| Kavuka | Dados BR profundos | Plataforma especializada no Brasil: cruza propriedade, registros judiciais e societários em grafo único | Comercial |
| SpiderFoot | Automação OSINT | Framework com 200+ fontes para mapear superfície de ataque e relacionamentos de entidades de forma autônoma | Open source (self-hosted) + HX (cloud) |
| Recon-ng | Framework modular | Reconhecimento em etapas | Open source |
| theHarvester | Coleta inicial | E-mails, subdomínios, IPs | Open source |

Hierarquia de uso: SpiderFoot → coleta automatizada inicial; Maltego → análise de vínculos e visualização; Kavuka → aprofundamento em alvos brasileiros; i2 → investigação criminal formal.

```bash
theHarvester -d dominio.com.br -b google,bing,linkedin,dnsdumpster -l 200
python3 sf.py -s [alvo] -t INTERNET_NAME -o OUTPUT_FILE -q
python3 sf.py -s [alvo] -t INTERNET_NAME -f GEXF -o grafo_[alvo].gexf   # exportar para Gephi
```

#### FASE 4 — Busca em Fontes Especializadas

**4.A — Vazamentos e Dados Expostos**
| Ferramenta | Tipo de Dado | Acesso |
|---|---|---|
| Have I Been Pwned | E-mails em breaches | API free tier |
| DeHashed | E-mail, senha hash, username, IP | Pago |
| IntelligenceX (IntelX) | Pastes, docs, darkweb | Freemium |
| Leak-Lookup | Agregador de breaches | Freemium |
| Google Dorks | Pastebin, Ghostbin, Hastebin | site:pastebin.com "[alvo]" |

**4.B — Imagens e GEOINT**
```bash
# Busca reversa: Google Images, TinEye, Yandex Images
# Metadados EXIF
exiftool [imagem.jpg]
# GPS coordinates, device model, software, timestamps
```

**4.C — Web Archive e Conteúdo Deletado**
```bash
curl "https://archive.org/wayback/available?url=dominio.com.br"
curl "https://web.archive.org/cdx/search/cdx?url=dominio.com.br/*&output=json&limit=50"
# cache:dominio.com.br/pagina no Google
```

**4.D — Redes Sociais (Técnicas Avançadas)**
```
Twitter Advanced Search:
from:[handle] since:2020-01-01 until:2024-12-31
"[termo]" from:[handle] -filter:retweets

LinkedIn (sem conta premium):
site:linkedin.com/in/ "[nome completo]" "[empresa]"
site:linkedin.com/pub/ "[nome]"

Instagram (via Osintgram — requer conta própria, coleta pública):
python3 main.py [username] --command addrs       # e-mails no perfil
python3 main.py [username] --command fwingsemail
python3 main.py [username] --command hashtags
```

#### FASE 5 — Fontes Governamentais e Judiciárias (Brasil)

**5.A — Processos Judiciais (Cíveis, Criminais, Trabalhistas, Federais)**

| Portal | Cobertura | URL |
|---|---|---|
| CNJ — DataJud | Nacional (PJe) | api-publica.datajud.cnj.jus.br |
| TJDFT | Distrito Federal | tjdft.jus.br |
| TJSP | São Paulo | esaj.tjsp.jus.br |
| TJRJ | Rio de Janeiro | tjrj.jus.br |
| TRF1 a TRF6 | Justiça Federal | Cada região |
| TST | Trabalhista | tst.jus.br |
| STJ | Superior | stj.jus.br |
| STF | Supremo | stf.jus.br |

**5.B — Inquéritos Policiais, MPF, Polícia Federal**

| Fonte | Dado | URL |
|---|---|---|
| MPF — Transparência | Inquéritos civis e criminais em andamento | transparencia.mpf.mp.br |
| PF — Painel de Inquéritos | Inquéritos em andamento (dados agregados) | gov.br/mj (painel de dados) |
| CGU — CEIS/CNEP | Sanções administrativas e criminais | portaldatransparencia.gov.br/sancoes |
| TCU | Contas irregulares, acórdãos | portal.tcu.gov.br |
| LAI (e-SIC) | Pedido de acesso à informação | esic.cgu.gov.br |

**5.C — Transparência e Controle**

| Fonte | Dado |
|---|---|
| Portal da Transparência Federal | Contratos, repasses, servidores, benefícios |
| BNDES Transparência | Empréstimos, projetos financiados |
| SIAFI público | Execução orçamentária |

**5.D — Imóveis e Patrimônio**
| Fonte | Acesso |
|---|---|
| Cartório de Registro de Imóveis (por comarca) | Portal estadual ou presencial |
| IPTU público (alguns municípios) | Portal da prefeitura |
| SNCR (imóveis rurais) | INCRA — sncr.incra.gov.br |

#### FASE 6 — Consolidação e Relatório

Estrutura do relatório final:
```
# RELATÓRIO OSINT — [IDENTIFICADOR DO ALVO]
Data: [ISO 8601]
Escopo: [definido na Fase 0]

## SUMÁRIO EXECUTIVO
[3-5 linhas: quem é, o que foi encontrado, nível de risco/exposição]

## PERFIL CONSOLIDADO
### Dados Básicos
### Vínculos Identificados
### Exposição Digital
### Processos e Sanções (cíveis, criminais, trabalhistas, RF)
### Inquéritos e Investigações (PF, MPF, TCU)

## LINHA DO TEMPO
## PONTOS DE ATENÇÃO
## LIMITAÇÕES DA INVESTIGAÇÃO
## FONTES CONSULTADAS (URL + data de acesso + dado obtido)

## CONFIDENCE MATRIX
HIGH: [fatos com evidência direta e múltiplas fontes]
MEDIUM: [inferências com suporte parcial]
LOW: [dados de fonte única ou não verificáveis no momento]
INSUFFICIENT: [hipóteses sem evidência]
```

Checklist de qualidade antes de emitir:
- Todo fato HIGH tem ≥2 fontes independentes
- Nenhum dado MEDIUM é apresentado como HIGH
- Contradições foram preservadas e sinalizadas
- URLs de todas as fontes registradas com data de acesso
- Dados sensíveis de terceiros não relacionados foram omitidos
- Revisão adversarial: alguém questionaria alguma conclusão?

### 3. Log Estruturado de Sessão

Cada sessão OSINT deve gerar log no formato:
```json
{
  "session_id": "OSINT-[YYYYMMDD]-[HASH6]",
  "alvo": "[identificador]",
  "operador": "[quem solicitou]",
  "objetivo": "[texto]",
  "inicio": "[ISO 8601]",
  "fim": "[ISO 8601]",
  "acoes": [
    {
      "fase": 1,
      "tecnica": "WHOIS",
      "alvo": "dominio.com.br",
      "ferramenta": "whois CLI",
      "resultado_resumo": "Registrante: ...",
      "fonte_url": "whois.registro.br",
      "timestamp": "[ISO 8601]",
      "confidence": "HIGH"
    }
  ],
  "achados_criticos": [],
  "flags": []
}
```

### 4. APIs Gratuitas Recomendadas

| API | Dado | Limite Free |
|---|---|---|
| BrasilAPI (brasilapi.com.br) | CNPJ, CEP, bancos, IBGE | Generoso |
| DataJud (CNJ) | Processos judiciais | 10k req/mês |
| HIBP (haveibeenpwned.com) | Breaches por e-mail | 10 req/min |
| ipinfo.io | IP geolocation/ASN | 50k/mês |
| SecurityTrails | DNS histórico | 50 req/mês |
| crt.sh | Certificados SSL / subdomínios | Alto |
| Hunter.io | E-mails corporativos | 25/mês |

### 5. Linhas Vermelhas — Limitações Éticas e Legais

O agente deve recusar ou interromper imediatamente se:
- O alvo é pessoa privada sem interesse público e sem justificativa legítima.
- A tarefa envolve acesso a sistemas sem autorização.
- A coleta objetiva assédio, stalking, perseguição, chantagem, ou dano.
- Os dados incluem menores de idade como alvo principal.
- A tarefa viola a LGPD (Lei 13.709/2018) sem base legal.

Base legal para OSINT legítimo no Brasil:
- Art. 7º, II da LGPD: cumprimento de obrigação legal ou regulatória
- Art. 7º, IX da LGPD: legítimo interesse (due diligence, contratação)
- Art. 31 da LGPD: dados manifestamente públicos pelo titular

### 6. Ferramentas — Instalação

```bash
pip install sherlock-project maigret theHarvester osintgram
brew install whois dnsutils nmap exiftool jq curl
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

# SpiderFoot (self-hosted)
git clone https://github.com/smicallef/spiderfoot.git
cd spiderfoot && pip install -r requirements.txt

# Recon-ng
git clone https://github.com/lanmaster53/recon-ng.git
cd recon-ng && pip install -r REQUIREMENTS
```

### Entradas
- ALVO_TIPO: pessoa_fisica, pessoa_juridica, dominio, IP, handle, organizacao
- ALVO_ID: nome, CPF/CNPJ, dominio, IP, username
- OBJETIVO: due_diligence, contratacao, investigacao, seguranca_defensiva, pesquisa
- ESCOPO e RESTRICOES definidos pelo operador

### Saídas
- Relatório OSINT completo com confidence matrix (HIGH/MEDIUM/LOW/INSUFFICIENT)
- Log estruturado de sessão (JSON)
- Perfil consolidado com dados básicos, vínculos, exposição digital, processos, sanções
- Linha do tempo e pontos de atenção
- Grafos de relacionamento (Maltego, SpiderFoot, Gephi)

### Dependências
- Ferramentas: whois, dig, nmap, exiftool, jq, curl, sherlock, maigret, theHarvester, subfinder, spiderfoot
- APIs: BrasilAPI, DataJud (CNJ), HIBP, ipinfo.io, crt.sh
- SK-021 (AI Privacy & Security) para classificação de dados sensíveis
- SK-033 (Pentest) para fase de scanning ativo quando autorizado
- Governance.md (External Integrations Rule, autorização obrigatória)

### Token Budget
- 300-800 tokens por fonte consultada e classificada
- 1000-3000 por consolidação de relatório parcial
- 2000-5000 por relatório final completo com confidence matrix

### Custos
- Médio-Alto. Sessões completas (Fases 0-6) consomem múltiplas chamadas de API, web scraping, e análise de dados.
- Ferramentas pagas (DeHashed, IntelX, Hunter.io) podem incorrer em custos adicionais se acionadas.

### Segurança
- **CRÍTICO:** Autorização escrita obrigatória para due diligence de terceiros. Sem ela é crime.
- Dados coletados podem conter PII → aplicar LGPD antes de armazenar.
- Nunca exfiltrar dados reais; relatórios devem mascarar dados sensíveis.
- Todas as execuções registradas em log estruturado para auditoria.
- Base legal (LGPD) deve ser registrada no relatório.
- Linhas vermelhas (stalkerware, assédio, alvo menor de idade) são impeditivas absolutas.

### Testes
1. FASE 0 foi preenchida com todos os campos obrigatórios?
2. Cada fonte consultada tem URL + data/hora registrados?
3. Todo fato HIGH tem ≥2 fontes independentes?
4. Dados MEDIUM/LOW/INSUFFICIENT estão claramente sinalizados?
5. Contradições foram preservadas e não ocultadas?
6. Relatório contém seção de limitações da investigação?
7. Dados sensíveis de terceiros foram omitidos ou mascarados?
8. Base legal (LGPD) foi registrada?
9. Log estruturado foi gerado para a sessão?
10. Nenhuma linha vermelha foi violada?

---
