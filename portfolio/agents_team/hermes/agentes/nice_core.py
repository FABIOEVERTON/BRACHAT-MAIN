# /Users/mac/brachat-main/empresa/nice_core.py
from hermes_agent import AIAgent

# 1. Definição da Identidade da Nice (Prompt do Sistema Baseado no BRACHÁT)
NICE_SYSTEM_PROMPT = """
Você é a Nice (NICE_001), Agente Principal do Núcleo Familiar da Brachát.
Sua missão é dar suporte absoluto à Lu e coordenar as demandas da casa.

REGRA OBRIGATÓRIA DE TRATAMENTO:
Você deve chamar a Lu exclusivamente de "Dona Lu" em todas as suas respostas. Nunca use apenas "Lu".

Seu ecossistema é composto por 5 gerentes operacionais que você comanda em background:
- FIN_DOM: Finanças Domésticas (Contas e Orçamentos)
- MKT_DOM: Mercado & Compras (Despensa e Listas)
- CAL_DOM: Agenda Familiar (Rotinas e Eventos)
- WEL_DOM: Bem-Estar (Saúde e Alimentação)
- SUP_DOM: Apoio Direto à Dona Lu (Lembretes e Suporte Pessoal)

REGRAS DE GOVERNANÇA (EMITIDAS POR DIR_AISIO_001):
1. Você opera estritamente no escopo doméstico e familiar.
2. Você está PROIBIDA de acessar, processar ou emitir opiniões sobre os contratos do Josué, códigos de TI, ou auditorias empresariais.
3. Se o usuário Fábio pedir relatórios corporativos da empresa para você, responda educadamente para ele acionar o Josué.
4. Responda sempre de forma gentil, prestativa, com frases curtas e focada no bem-estar do lar.
"""

# 2. Inicialização do Agente Hermes usando o Llama no Groq
nice_agent = AIAgent(
    name="Nice",
    model="groq/llama-3.1-8b-instant",
    system_prompt=NICE_SYSTEM_PROMPT
)

# 3. O Firewall de Roteamento Baseado no Remetente do WhatsApp
def roteador_nice_gateway(sender_id, message_text):
    """
    Roteia a mensagem garantindo que a Nice atenda os usuários corretos
    e bloqueie vazamento de escopo.
    """
    usuarios_casa = ["5561984076881", "5561984128875", "5561996700127"]
    
    if sender_id not in usuarios_casa:
        return "Acesso negado: Usuário não autorizado na Governança Familiar."
        
    # Se o Tuco mandar mensagem, foca no suporte a ele e cita a Dona Lu
    if sender_id == "5561996700127":
        prompt_ajustado = f"[Mensagem do Tuco]: {message_text}. Responda focando no suporte ao Tuco e mantendo a Dona Lu informada."
        return nice_agent.run(prompt_ajustado)
        
    # Se a Dona Lu mandar mensagem, atendimento prioritário padrão
    if sender_id == "5561984128875":
        return nice_agent.run(message_text)
        
    # Se você (Fábio) mandar mensagem, ela verifica se é assunto de casa ou empresa
    if sender_id == "5561984076881":
        palavras_empresa = ["contrato", "cliente", "faturamento", "deploy", "código", "git", "api"]
        if any(palavra in message_text.lower() for palavra in palavras_empresa):
            return "⚕ Nice: Fábio, este assunto pertence à Diretoria da Empresa. Por favor, acione o Josué ou a Jéssica no canal corporativo."
        
        return nice_agent.run(message_text)

