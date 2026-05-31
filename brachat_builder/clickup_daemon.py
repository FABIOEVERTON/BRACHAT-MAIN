import os
import sys
import time
import requests
import json
import subprocess

# Setup de seguranca e variaveis de ambiente
def load_env():
    env_path = "/Users/mac/apis/apis.env"
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip()
                    
                    # Remove comentarios ao final do valor
                    raw_val = val
                    if " - " in val:
                        raw_val = val.split(" - ", 1)[0].strip()
                    elif " #" in val:
                        raw_val = val.split(" #", 1)[0].strip()
                    elif " " in val:
                        raw_val = val.split(" ", 1)[0].strip()
                        
                    os.environ[key] = raw_val
                    
                    # Mapeia chaves especificas baseadas no comentario original
                    if key == "TELEGRAM_API_KEY":
                        if "HERMES" in val.upper():
                            os.environ["TELEGRAM_HERMES_TOKEN"] = raw_val
                        elif "ANTIGRAVITY" in val.upper():
                            os.environ["TELEGRAM_ANTIGRAVITY_TOKEN"] = raw_val

load_env()
CLICKUP_API_KEY = os.environ.get("CLICKUP_API_KEY")
TELEGRAM_HERMES_TOKEN = os.environ.get("TELEGRAM_HERMES_TOKEN")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
ALLOWED_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "8035491919")

def call_gemini(system_prompt, user_content):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GOOGLE_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"role": "user", "parts": [{"text": user_content}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 1000
        }
    }
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=25)
        if res.status_code == 200:
            return res.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        return f"⚠️ Erro de API do Gemini: HTTP {res.status_code} - {res.text}"
    except Exception as e:
        return f"⚠️ Erro de conexão com Gemini: {str(e)}"

def call_llm_with_fallback(system_prompt, user_content):
    res_gemini = call_gemini(system_prompt, user_content)
    if not res_gemini.startswith("⚠️ Erro"):
        return res_gemini
        
    print(f"⚠️ Falha no Gemini: {res_gemini}. Tentando fallback no Claude...")
    claude_key = os.environ.get("CLAUDE_API_KEY")
    if claude_key:
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": claude_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        payload = {
            "model": "claude-3-5-sonnet-20241022",
            "max_tokens": 1000,
            "temperature": 0.2,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_content}]
        }
        try:
            res = requests.post(url, headers=headers, json=payload, timeout=25)
            if res.status_code == 200:
                print("✅ Fallback no Claude executado com sucesso.")
                return res.json()["content"][0]["text"].strip()
            print(f"⚠️ Falha no Claude: HTTP {res.status_code} - {res.text}")
        except Exception as e:
            print(f"⚠️ Erro ao conectar com o Claude: {str(e)}")
            
    # Fallback 3: Groq (CUSTOM_API_KEY)
    print("⚠️ Gemini/Claude indisponiveis. Tentando fallback no Groq...")
    groq_key = os.environ.get("CUSTOM_API_KEY")
    if groq_key:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {groq_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            "temperature": 0.2,
            "max_tokens": 1000
        }
        try:
            res = requests.post(url, headers=headers, json=payload, timeout=25)
            if res.status_code == 200:
                print("✅ Fallback no Groq (Llama 3.1) executado com sucesso.")
                return res.json()["choices"][0]["message"]["content"].strip()
            print(f"⚠️ Falha no Groq: HTTP {res.status_code} - {res.text}")
        except Exception as e:
            print(f"⚠️ Erro ao conectar com o Groq: {str(e)}")
            
    return res_gemini

# ==========================================
# FRAMEWORK DE AGENTES: BRACHAT CREW (LangChain/CrewAI Style)
# ==========================================

class BrachatAgent:
    def __init__(self, agent_id, name, role, mission, system_instruction, memory_scope=None):
        self.agent_id = agent_id
        self.name = name
        self.role = role
        self.mission = mission
        self.system_instruction = system_instruction
        self.memory_scope = memory_scope or f"scope_{agent_id.lower()}"

    def retrieve_memories(self):
        # Tenta buscar memorias locais salvas no formato JSON correspondentes ao escopo do agente
        mem_file = f"/Users/mac/brachat-main/brachat_builder/memories/{self.memory_scope}.json"
        if os.path.exists(mem_file):
            try:
                with open(mem_file, "r") as f:
                    mems = json.load(f)
                    if isinstance(mems, list):
                        return "\n".join([f"- {m}" for m in mems])
            except:
                pass
        return ""

    def execute(self, prompt_text):
        memories = self.retrieve_memories()
        
        # Formata o prompt do sistema no padrão CrewAI (Role, Mission, Backstory)
        full_system_prompt = (
            f"Você é o {self.name} ({self.role}).\n"
            f"Identificador de Governança: {self.agent_id}\n"
            f"Missão Principal: {self.mission}\n\n"
            f"Instruções Técnicas:\n{self.system_instruction}\n"
        )
        if memories:
            full_system_prompt += f"\nMemórias persistentes de contexto:\n{memories}\n"
            
        return call_llm_with_fallback(full_system_prompt, prompt_text)

# ==========================================
# DECLARAÇÃO DOS AGENTES CONFORME O REGISTRY.MD
# ==========================================

# 1. Agente AI Research (Pesquisador local)
agent_researcher = BrachatAgent(
    agent_id="AGT_AI_001",
    name="Agente AI Research",
    role="Pesquisador Técnico do Mac",
    mission="Investigar a estrutura física do repositório ativo e mapear arquivos e dependências.",
    system_instruction=(
        "Analise a instrução de desenvolvimento e a árvore de diretórios fornecida.\n"
        "Retorne um relatório curto contendo:\n"
        "- Arquivos relacionados à mudança.\n"
        "- Bibliotecas/dependências envolvidas.\n"
        "- Potenciais conflitos arquiteturais.\n"
        "Seja estritamente técnico e evite conversas casuais."
    ),
    memory_scope="gilmario_knowledge"
)

# 2. Arquiteto de Soluções (Especificador)
agent_spec = BrachatAgent(
    agent_id="MGR_ARCH_001",
    name="Arquiteto de Soluções",
    role="Especificador Técnico de Sistemas",
    mission="Desenhar planos de implementação detalhados, limpos e seguros em implementation_plan.md.",
    system_instruction=(
        "Escreva o arquivo Markdown implementation_plan.md para orientar o desenvolvimento.\n"
        "O plano deve descrever exatamente:\n"
        "- Quais arquivos criar ([NEW]) ou editar ([MODIFY]).\n"
        "- A lógica exata, endpoints ou funções necessárias.\n"
        "- Plano de verificação com comandos de testes locais (ex: pytest).\n"
        "Apenas retorne o Markdown completo do plano."
    ),
    memory_scope="aisio_governance"
)

# 3. Agente Python (Coder / Operário)
agent_coder = BrachatAgent(
    agent_id="AGT_PYTHON_001",
    name="Agente Python Coder",
    role="Operário Programador",
    mission="Codificar e aplicar alterações físicas de arquivos seguindo as diretrizes da especificação.",
    system_instruction=(
        "Gere o novo conteúdo atualizado para o arquivo de código solicitado com base no plano de implementação.\n"
        "Importante: Retorne APENAS o código puro e completo do arquivo, sem tags de markdown (como ```python) ou explicações adicionais."
    ),
    memory_scope="gilmario_knowledge"
)

# 4. Gerente de Documentação (Documentador)
agent_documenter = BrachatAgent(
    agent_id="MGR_DOC_001",
    name="Gerente de Documentação",
    role="Responsável por Documentação Técnica e Wikis",
    mission="Garantir a atualização do README.md e logs históricos do repositório.",
    system_instruction=(
        "Com base na feature criada, escreva um log técnico sucinto contendo o que mudou no projeto para anexar no README.md."
    ),
    memory_scope="aisio_governance"
)

# ==========================================
# LOGICA DE EXECUÇÃO DE TESTES E COMANDOS
# ==========================================

def run_project_tests(project_path, config):
    test_cmd = config.get("test_command", "")
    if not test_cmd:
        if os.path.exists(os.path.join(project_path, "package.json")):
            test_cmd = "npm run test"
        else:
            test_cmd = "pytest"
            
    print(f"  [Teste] Executando comando: {test_cmd}")
    try:
        res = subprocess.run(
            test_cmd,
            shell=True,
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=40
        )
        return res.returncode == 0, f"STDOUT:\n{res.stdout}\n\nSTDERR:\n{res.stderr}"
    except Exception as e:
        return False, f"Falha ao executar testes: {str(e)}"

# ==========================================
# UTILITÁRIOS GERAIS
# ==========================================

def send_telegram_reply(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_HERMES_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        res = requests.post(url, json=payload, timeout=10)
        if res.status_code not in [200, 201]:
            payload.pop("parse_mode", None)
            requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Erro ao enviar Telegram: {str(e)}")

def manage_clickup_tag(task_id, tag_name, action="add"):
    method = "POST" if action == "add" else "DELETE"
    url = f"https://api.clickup.com/api/v2/task/{task_id}/tag/{tag_name}"
    headers = {"Authorization": CLICKUP_API_KEY}
    try:
        res = requests.request(method, url, headers=headers, timeout=10)
        return res.status_code in [200, 201, 204]
    except Exception as e:
        print(f"Erro ao gerenciar tag {tag_name}: {str(e)}")
        return False

def update_clickup_status(task_id, status_name):
    url = f"https://api.clickup.com/api/v2/task/{task_id}"
    headers = {
        "Authorization": CLICKUP_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {"status": status_name}
    try:
        requests.put(url, headers=headers, json=payload, timeout=10)
    except Exception as e:
        print(f"Erro ao atualizar status: {str(e)}")

def add_clickup_comment(task_id, comment_text):
    url = f"https://api.clickup.com/api/v2/task/{task_id}/comment"
    headers = {
        "Authorization": CLICKUP_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {"comment_text": comment_text}
    try:
        requests.post(url, headers=headers, json=payload, timeout=10)
    except Exception as e:
        print(f"Erro ao adicionar comentário: {str(e)}")

def lock_project_files(project_path, read_only=True):
    mode = 0o444 if read_only else 0o644
    for root, dirs, files in os.walk(project_path):
        if any(ignored in root for ignored in [".git", "node_modules", "__pycache__", ".venv", "dist", "build"]):
            continue
        for file in files:
            if file.endswith((".py", ".js", ".ts", ".html", ".css", ".json", ".md")) and file not in [".brachat-state.json", ".brachat"]:
                try:
                    os.chmod(os.path.join(root, file), mode)
                except:
                    pass

def get_active_project():
    active_path = "/Users/mac/brachat_builder/active_project.json"
    if os.path.exists(active_path):
        try:
            with open(active_path, "r") as f:
                data = json.load(f)
                return data.get("active_project_path")
        except:
            pass
    return None

def get_clickup_task(task_id):
    url = f"https://api.clickup.com/api/v2/task/{task_id}"
    headers = {"Authorization": CLICKUP_API_KEY}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            return res.json()
    except Exception as e:
        print(f"Erro ao ler tarefa {task_id}: {str(e)}")
    return None

def scan_clickup_for_active_task(list_id):
    url = f"https://api.clickup.com/api/v2/list/{list_id}/task?subtasks=true&statuses[]=to do&tags[]=brachat_researcher"
    headers = {"Authorization": CLICKUP_API_KEY}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            tasks = res.json().get("tasks", [])
            if tasks:
                return tasks[0]
    except Exception as e:
        print(f"Erro ao escanear tarefas ClickUp: {str(e)}")
    return None

def save_project_state(project_path, state):
    state_path = os.path.join(project_path, ".brachat-state.json")
    try:
        os.chmod(state_path, 0o644)
    except:
        pass
    try:
        with open(state_path, "w") as f:
            json.dump(state, f, indent=2)
        os.chmod(state_path, 0o444)
    except Exception as e:
        print(f"Erro ao salvar estado: {str(e)}")

# ==========================================
# ORQUESTRADOR CODER AGENT LOCAL
# ==========================================

def run_coder_agent(project_path, instruction, plan):
    target_files = []
    lines = plan.split("\n")
    for line in lines:
        if "/Users/mac/" in line:
            parts = line.split()
            for part in parts:
                if "/Users/mac/" in part:
                    clean_path = part.strip("`*[]()\"'")
                    if os.path.exists(clean_path) or clean_path.endswith((".py", ".js", ".ts", ".html", ".css", ".json", ".md")):
                        target_files.append(clean_path)
                        
    if not target_files:
        for line in lines:
            if "file:///" in line:
                clean_path = line.split("file:///")[-1].split(")")[0].strip()
                target_files.append(clean_path)

    if not target_files:
        return "⚠️ Não consegui mapear os arquivos alvos no plano de implementação."

    target_files = list(set(target_files))
    print(f"  [Coder] Arquivos alvos identificados para edição: {target_files}")
    
    for file_path in target_files:
        file_content = ""
        is_new = True
        if os.path.exists(file_path):
            is_new = False
            try:
                with open(file_path, "r") as f:
                    file_content = f.read()
            except Exception as e:
                return f"⚠️ Erro ao ler arquivo alvo {file_path}: {str(e)}"
                
        user_prompt = (
            f"Plano de Implementação:\n{plan}\n\n"
            f"Instrução do Usuário: {instruction}\n\n"
            f"Arquivo Alvo: {file_path}\n"
            f"Novo arquivo? {'Sim' if is_new else 'Não'}\n"
            f"Conteúdo atual do arquivo:\n```\n{file_content}\n```\n\n"
            f"Gere o novo conteúdo completo para o arquivo {file_path}."
        )
        
        reply = agent_coder.execute(user_prompt)
        
        if reply.startswith("```"):
            lines = reply.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            reply = "\n".join(lines).strip()
            
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as f:
                f.write(reply)
            print(f"  [Coder] Arquivo modificado com sucesso: {file_path}")
        except Exception as e:
            return f"⚠️ Erro ao gravar alterações no arquivo {file_path}: {str(e)}"
            
    return "✅ Código desenvolvido e aplicado localmente com sucesso."

# ==========================================
# PROCESSAMENTO DE WORKFLOW
# ==========================================

def process_workflow(project_path):
    conf_path = os.path.join(project_path, ".brachat")
    state_path = os.path.join(project_path, ".brachat-state.json")
    
    if not os.path.exists(conf_path) or not os.path.exists(state_path):
        return
        
    try:
        with open(conf_path, "r") as f:
            conf = json.load(f)
        with open(state_path, "r") as f:
            state = json.load(f)
    except Exception as e:
        print(f"Erro ao ler configuracoes do projeto: {str(e)}")
        return
        
    task_id = state.get("active_task_id")
    phase = state.get("phase", "backlog")
    
    if not task_id:
        task = scan_clickup_for_active_task(conf.get("clickup_list_id", "901714169490"))
        if task:
            task_id = task.get("id")
            state["active_task_id"] = task_id
            state["active_task_name"] = task.get("name")
            state["phase"] = "researcher"
            state["plan_approved"] = False
            state["tests_passed"] = False
            save_project_state(project_path, state)
            print(f"\n[Workflow] Nova tarefa ativada: {task.get('name')} (ID: {task_id})")
            sys.stdout.flush()
        else:
            return
            
    task_data = get_clickup_task(task_id)
    if not task_data:
        print(f"Tarefa {task_id} nao encontrada no ClickUp. Resetando estado local.")
        state["active_task_id"] = None
        state["phase"] = "backlog"
        save_project_state(project_path, state)
        return
        
    task_name = task_data.get("name")
    desc = task_data.get("description", "")
    tags = task_data.get("tags", [])
    
    print(f"\n[Fila] Projeto: {conf.get('project_name')} | Tarefa: {task_name} | Fase Local: {phase.upper()}")
    sys.stdout.flush()
    
    # 1. FASE: RESEARCHER (AI Research Agent)
    if phase == "researcher":
        send_telegram_reply(ALLOWED_CHAT_ID, f"🔍 **Fase 1/8 - Researcher ({agent_researcher.name}):** Analisando arquivos de `{conf.get('project_name')}`...")
        
        project_tree = ""
        for root, dirs, files in os.walk(project_path):
            if any(ignored in root for ignored in [".git", "node_modules", "__pycache__", ".venv", "dist", "build"]):
                continue
            depth = root.replace(project_path, "").count(os.sep)
            indent = "  " * depth
            project_tree += f"{indent}📁 {os.path.basename(root)}/\n"
            for file in files[:5]:
                project_tree += f"{indent}  📄 {file}\n"
                
        user_content = f"Instrução: {desc}\n\nEstrutura de pastas do projeto:\n{project_tree}"
        research_result = agent_researcher.execute(user_content)
        
        add_clickup_comment(task_id, f"📝 **Relatório de Pesquisa Técnica (Researcher):**\n\n{research_result}")
        send_telegram_reply(ALLOWED_CHAT_ID, f"📝 **Resultado da Pesquisa Técnica:**\n\n{research_result}")
        
        state["phase"] = "specification"
        save_project_state(project_path, state)
        manage_clickup_tag(task_id, "brachat_researcher", "remove")
        manage_clickup_tag(task_id, "brachat_spec", "add")
        print("  Fase Researcher concluida. Avancando para Specification.")
        sys.stdout.flush()
        
    # 2. FASE: SPECIFICATION (Arquiteto de Soluções)
    elif phase == "specification":
        plan_file = os.path.join(project_path, "implementation_plan.md")
        
        if not os.path.exists(plan_file):
            send_telegram_reply(ALLOWED_CHAT_ID, f"📋 **Fase 2/8 - Specification ({agent_spec.name}):** Gerando o plano de implementação...")
            
            user_content = f"Instrução: {desc}\n\nPor favor, escreva o implementation_plan.md detalhando as modificacoes de arquivos no Mac."
            spec_result = agent_spec.execute(user_content)
            
            os.chmod(project_path, 0o755)
            with open(plan_file, "w") as f:
                f.write(spec_result)
                
            add_clickup_comment(task_id, f"📋 **Plano de Implementação Proposto (Antigravity):**\n\n{spec_result}")
            send_telegram_reply(
                ALLOWED_CHAT_ID, 
                f"📋 **Plano de Implementação Criado!**\n"
                f"Caminho local: `{plan_file}`\n\n"
                f"Para prosseguir, aprove alterando a Tag do ClickUp para `brachat_dev`."
            )
            
        if "brachat_dev" in tags or state.get("plan_approved"):
            state["plan_approved"] = True
            state["phase"] = "development"
            save_project_state(project_path, state)
            
            lock_project_files(project_path, read_only=False)
            
            manage_clickup_tag(task_id, "brachat_spec", "remove")
            manage_clickup_tag(task_id, "brachat_dev", "add")
            
            send_telegram_reply(
                ALLOWED_CHAT_ID, 
                f"🔓 **Plano de Implementação Aprovado!**\n"
                f"Arquivos locais de código em `{conf.get('project_name')}` destravados para edição.\n"
                f"Iniciando fase de codificação técnica (Development)..."
            )
            print("  Fase Specification aprovada. Iniciando Development.")
            sys.stdout.flush()
            
    # 3. FASE: DEVELOPMENT (Python Coder Agent)
    elif phase == "development":
        if "brachat_test" in tags:
            state["phase"] = "testing"
            save_project_state(project_path, state)
            lock_project_files(project_path, read_only=True)
            print("  Fase Development concluida pelo usuario. Iniciando Testing.")
            sys.stdout.flush()
            return
            
        plan_file = os.path.join(project_path, "implementation_plan.md")
        if os.path.exists(plan_file):
            send_telegram_reply(ALLOWED_CHAT_ID, f"⚙️ **Fase 3/8 - Development ({agent_coder.name}):** Codificando alterações no Mac local...")
            with open(plan_file, "r") as f:
                plan_content = f.read()
                
            dev_result = run_coder_agent(project_path, desc, plan_content)
            
            add_clickup_comment(task_id, f"💻 **Código Desenvolvido (Coder):**\n\n{dev_result}")
            send_telegram_reply(ALLOWED_CHAT_ID, f"💻 **Resultado do Coder:** {dev_result}")
            
            state["phase"] = "testing"
            save_project_state(project_path, state)
            
            lock_project_files(project_path, read_only=True)
            
            manage_clickup_tag(task_id, "brachat_dev", "remove")
            manage_clickup_tag(task_id, "brachat_test", "add")
            print("  Desenvolvimento concluido. Avancando para Testing.")
            sys.stdout.flush()
            
    # 4. FASE: TESTING (Qualidade / Execucao local)
    elif phase == "testing":
        send_telegram_reply(ALLOWED_CHAT_ID, f"🧪 **Fase 4/8 - Testing (Testes):** Executando testes automatizados...")
        
        success, log = run_project_tests(project_path, conf)
        
        if success:
            state["tests_passed"] = True
            state["phase"] = "validation"
            save_project_state(project_path, state)
            
            wt_file = os.path.join(project_path, "walkthrough.md")
            os.chmod(project_path, 0o755)
            with open(wt_file, "w") as f:
                f.write(f"# Walkthrough de Validação\n\n✅ Todos os testes passaram com sucesso no Mac local!\n\n## Logs dos Testes\n```\n{log}\n```\n")
                
            add_clickup_comment(task_id, f"✅ **Testes Concluídos com Sucesso!**\n\nWalkthrough criado em local.\n{log[:1000]}")
            send_telegram_reply(
                ALLOWED_CHAT_ID, 
                f"🧪 **Testes passaram com sucesso!**\n"
                f"walkthrough.md criado na raiz do projeto.\n"
                f"Aprove o avanço mudando a Tag para `brachat_doc` ou movendo no ClickUp."
            )
            
            manage_clickup_tag(task_id, "brachat_test", "remove")
            manage_clickup_tag(task_id, "brachat_validate", "add")
            print("  Testes bem-sucedidos. Avancando para Validation.")
            sys.stdout.flush()
        else:
            state["tests_passed"] = False
            state["phase"] = "development"
            save_project_state(project_path, state)
            
            lock_project_files(project_path, read_only=False)
            
            add_clickup_comment(task_id, f"❌ **Testes Falharam no Mac!**\n\nRetornando para a fase de Desenvolvimento para correções.\n\n{log[:1000]}")
            send_telegram_reply(
                ALLOWED_CHAT_ID, 
                f"❌ **Testes falharam!**\n"
                f"Logs de erro enviados para o ClickUp.\n"
                f"Arquivos locais destravados para correção. Retornando para Desenvolvimento..."
            )
            
            manage_clickup_tag(task_id, "brachat_test", "remove")
            manage_clickup_tag(task_id, "brachat_dev", "add")
            print("  Testes falharam. Retornando para Development.")
            sys.stdout.flush()
            
    # 5. FASE: VALIDATION (Portao Humano)
    elif phase == "validation":
        if "brachat_doc" in tags:
            state["phase"] = "documentation"
            save_project_state(project_path, state)
            manage_clickup_tag(task_id, "brachat_validate", "remove")
            print("  Feature validada pelo usuario. Iniciando Documentation.")
            sys.stdout.flush()
            
    # 6. FASE: DOCUMENTATION (Gerente de Documentação)
    elif phase == "documentation":
        send_telegram_reply(ALLOWED_CHAT_ID, f"📝 **Fase 7/8 - Documentation ({agent_documenter.name}):** Gerando notas e documentação incremental...")
        
        user_content = f"Instrução: {desc}\n\nEscreva a nota de documentacao curta do que mudou no projeto."
        doc_result = agent_documenter.execute(user_content)
        
        # 1. Atualiza o README.md
        readme_path = os.path.join(project_path, "README.md")
        try:
            os.chmod(project_path, 0o755)
            if os.path.exists(readme_path):
                os.chmod(readme_path, 0o644)
                with open(readme_path, "a") as f:
                    f.write(f"\n\n### 🚀 Nova Feature: {task_name}\n\n{doc_result}\n")
                os.chmod(readme_path, 0o444) # Trava como read-only
        except Exception as e:
            print(f"Erro ao atualizar README.md: {str(e)}")
            
        # 2. Cria Documento Incremental no padrão agents_team (QUILIS/AGCP)
        inc_docs_dir = os.path.join(project_path, "incremental_documents")
        try:
            os.makedirs(inc_docs_dir, exist_ok=True)
            existing_files = [f for f in os.listdir(inc_docs_dir) if f.endswith(".md")]
            next_seq = len(existing_files) + 1
            clean_name = "".join([c if c.isalnum() else "_" for c in task_name]).strip("_")
            clean_name = clean_name.replace("__", "_")
            doc_filename = f"{next_seq:02d}_{clean_name[:30].lower()}.md"
            doc_filepath = os.path.join(inc_docs_dir, doc_filename)
            
            doc_prompt = (
                f"Feature: {task_name}\n"
                f"Escopo original: {desc}\n\n"
                f"Escreva um arquivo markdown de documentação incremental no padrão QUILIS/AGCP do BRACHÁT.\n"
                f"Detalhe a finalidade do código, a estrutura de arquivos criada/alterada, critérios de cibersegurança do MITRE/NIST aplicados, e o status final de validação."
            )
            incremental_content = agent_documenter.execute(doc_prompt)
            
            with open(doc_filepath, "w") as f:
                f.write(f"# Documentação Incremental: {task_name}\n\n"
                        f"**ID da Tarefa ClickUp:** `{task_id}`\n"
                        f"**Data:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                        f"{incremental_content}\n")
            os.chmod(doc_filepath, 0o444) # Trava como read-only
            print(f"  [Documentacao] Arquivo incremental criado: {doc_filepath}")
        except Exception as e:
            print(f"Erro ao gravar documentacao incremental: {str(e)}")
                
        add_clickup_comment(task_id, f"📝 **Documentação Adicionada:**\n\n{doc_result}")
        send_telegram_reply(ALLOWED_CHAT_ID, f"📝 **Documentação Criada:**\n{doc_result}")
        
        state["phase"] = "done"
        save_project_state(project_path, state)
        
        manage_clickup_tag(task_id, "brachat_doc", "remove")
        manage_clickup_tag(task_id, "brachat_done", "add")
        update_clickup_status(task_id, "complete")
        
        state["active_task_id"] = None
        state["active_task_name"] = ""
        state["phase"] = "backlog"
        state["plan_approved"] = False
        state["tests_passed"] = False
        save_project_state(project_path, state)
        
        send_telegram_reply(ALLOWED_CHAT_ID, f"✅ **Fase 8/8 - Concluído:** A funcionalidade foi completamente integrada, testada e documentada com sucesso no Mac local!")
        print("  Workflow concluido. Estado resetado.")
        sys.stdout.flush()

def main():
    print("🚀 BRACHÁT ClickUp Daemon de 8 Fases Iniciado (CrewAI/LangChain Style).")
    sys.stdout.flush()
    
    while True:
        project_path = get_active_project()
        if project_path and os.path.exists(project_path):
            try:
                process_workflow(project_path)
            except Exception as e:
                print(f"Erro ao processar workflow do projeto ativo: {str(e)}")
                sys.stdout.flush()
        else:
            print("⏳ Aguardando configuracao de projeto ativo via `/switch` no Telegram...", end="\r")
            sys.stdout.flush()
            
        time.sleep(10)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nDaemon encerrado.")
