# Documentação Técnica: superXAi & AGCP

## O Paradigma de Interceptação em Runtime
Dashboards tradicionais falham porque analisam logs *após* o vazamento de dados. A **BrachaTec** resolve isso atuando na camada de rede através do **AGCP (Advanced Governance Control Proxy)**. 
O AGCP atua como um *Reverse Proxy Commit-Bound*. Isso significa que a requisição do usuário (ex: um prompt enviado ao ChatGPT) não vai para a OpenAI imediatamente. Ela bate no nosso proxy. O proxy "segura" a requisição por milissegundos, avalia e, só se estiver limpa, faz o "commit" para a nuvem. Caso contrário, ocorre o *fail-closed* imediato.

## A Engine superXAi (Antigo Cilis / Qilis)
Enquanto o proxy segura a requisição, ele aciona a engine **superXAi**.
O superXAi não é um LLM lento analisando texto. Ele é um motor de **Matemática Pura**.
1. **Vetorização Matemática:** Ele converte o prompt do usuário em vetores numéricos de alta densidade semântica.
2. **Cálculo de Intenção:** Em vez de procurar palavras proibidas, ele calcula a distância matemática entre o vetor do usuário e os clusters de "Risco" (Ex: Extração de PII, Injeção de Prompt, Viés Discriminatório).
3. **Decisão Binária (0 ou 1):** Se a equação identificar alta similaridade com uma infração da LGPD ou PL 2338/2023, a resposta matemática é 1 (Bloqueio). 

Como é um cálculo de álgebra linear e não geração de texto, a avaliação de todos os 129 filtros ocorre em **menos de 50 milissegundos**. É por isso que conseguimos auditar em *runtime* (tempo real) com latência imperceptível.

---

## Matriz de Soluções da Plataforma

### 1. Governança de IA
* **superXAi:** Engine central matemática que calcula a explicabilidade e detecta intenção maliciosa em *runtime*.
* **AGCP:** O proxy de controle e governança que intercepta as chamadas na rede.
* **BTScan:** Varredura assíncrona que mapeia endpoints na rede para descobrir *Shadow AI* escondida.
* **BTMonitor:** A interface de aplicação dos filtros L1 a L5 conectados ao AGCP.

### 2. Setor Público (Governo e Municípios)
* **BTGestor:** Monitoramento ativo da execução de obras. Assim que um projeto nasce, ele conecta no Transferegov e SIAFI, provendo documentos e respondendo diligências de forma autônoma para proteger o CPF do gestor.
* **BTLicita:** Assistente tático que acompanha o pregoeiro na montagem do edital, garantindo enquadramento na Lei 14.133.
* **BTCapta:** Motor de varredura que encontra dinheiro (convênios federais e emendas) exatamente nas fontes que a prefeitura indicar.

### 3. BTRig (Risco Legislativo Corporativo)
* **BTLex:** Crawler avançado focado em empresas que pagam caro por relatórios de risco. Monitora a Câmara dos Deputados, Senado e Diários Oficiais minuto a minuto.
* **BTAlerta:** Inteligência que cruza o BTLex com a matriz de risco da empresa, emitindo avisos precoces.
* **BTProva:** Emite o "Laudo Pericial Forense" final com carimbo criptográfico (Time-Stamp SHA-256), servindo de prova inalterável (WORM).
