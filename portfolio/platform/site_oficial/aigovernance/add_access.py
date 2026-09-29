import re

with open('/Users/mac/brachat-main/portfolio/platform/site_oficial/aigovernance/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

access_html = """
<section id="acesso" class="section" style="background:var(--navy-2);">
  <div class="section-inner">
    <div class="s-label" data-i18n="acc-lbl">Formas de Integração</div>
    <h2 class="s-title" style="margin-bottom:48px;" data-i18n="acc-title">A governança onde você precisa.</h2>
    
    <div class="pricing-grid" style="grid-template-columns: repeat(3, 1fr); gap: 24px;">
      
      <!-- MCP -->
      <div class="price-card" style="text-align:left; padding:32px;">
        <div class="pc-name" style="font-size:24px; color:var(--white);" data-i18n="acc1-title">No seu Agente (MCP)</div>
        <p style="color:var(--muted); font-size:14px; margin:16px 0;" data-i18n="acc1-desc">A conformidade viva dentro das suas ferramentas. Nativo para Claude, Cursor, Windsurf e clientes MCP. Seus robôs consultam as matrizes de risco e bloqueiam vazamentos (PII) direto no código.</p>
        <div class="pc-price" style="font-size:24px; margin-bottom:0;" data-i18n="acc1-price">Plano Pro (Add-on)</div>
      </div>

      <!-- Terminal -->
      <div class="price-card popular" style="text-align:left; padding:32px;">
        <div class="popular-badge" data-i18n="acc-rec">Recomendado</div>
        <div class="pc-name" style="font-size:24px; color:var(--white);" data-i18n="acc2-title">No seu Navegador (Terminal)</div>
        <p style="color:var(--muted); font-size:14px; margin:16px 0;" data-i18n="acc2-desc">A auditoria em um painel visual. Histórico completo, trilhas SHA-256 e emissão de laudos. Ideal para gestores de compliance e diretores que precisam de respostas rápidas.</p>
        <div class="pc-price" style="font-size:24px; margin-bottom:0;" data-i18n="acc2-price">Portal Dashboard</div>
      </div>

      <!-- Feed / API -->
      <div class="price-card" style="text-align:left; padding:32px;">
        <div class="pc-name" style="font-size:24px; color:var(--white);" data-i18n="acc3-title">Na sua Infraestrutura (Feed/API)</div>
        <p style="color:var(--muted); font-size:14px; margin:16px 0;" data-i18n="acc3-desc">O motor BRACHATEC plugado nos seus sistemas. Filtros inline de milissegundos conectados via API. Bloqueie dados antes de chegarem à OpenAI no nível do seu servidor.</p>
        <div class="pc-price" style="font-size:24px; margin-bottom:0;" data-i18n="acc3-price">Integração API Rest</div>
      </div>

    </div>
  </div>
</section>
"""

content = re.sub(r'</section>\n\n<section id="precos"', '</section>\n\n' + access_html + '\n<section id="precos"', content)

dict_additions_pt = """
    'acc-lbl':'Formas de Integração','acc-title':'A governança onde você precisa.','acc-rec':'Recomendado',
    'acc1-title':'No seu Agente (MCP)','acc1-desc':'A conformidade viva dentro das suas ferramentas. Nativo para Claude, Cursor, Windsurf e clientes MCP. Seus robôs consultam as matrizes de risco e bloqueiam vazamentos (PII) direto no código.','acc1-price':'Plano Pro (Add-on)',
    'acc2-title':'No seu Navegador (Terminal)','acc2-desc':'A auditoria em um painel visual. Histórico completo, trilhas SHA-256 e emissão de laudos. Ideal para gestores de compliance e diretores que precisam de respostas rápidas.','acc2-price':'Portal Dashboard',
    'acc3-title':'Na sua Infraestrutura (Feed/API)','acc3-desc':'O motor BRACHATEC plugado nos seus sistemas. Filtros inline de milissegundos conectados via API. Bloqueie dados antes de chegarem à OpenAI no nível do seu servidor.','acc3-price':'Integração API Rest',
"""
content = re.sub(r"'pr-lbl':'Investimento',", dict_additions_pt + "\n    'pr-lbl':'Investimento',", content)

dict_additions_es = """
    'acc-lbl':'Formas de Integración','acc-title':'Gobernanza donde la necesita.','acc-rec':'Recomendado',
    'acc1-title':'En su Agente (MCP)','acc1-desc':'Conformidad viva en sus herramientas. Nativo para Claude, Cursor y clientes MCP. Sus robots consultan matrices de riesgo y bloquean fugas en tiempo real.','acc1-price':'Plan Pro (Add-on)',
    'acc2-title':'En su Navegador (Terminal)','acc2-desc':'Auditoría en un panel visual. Historial completo, huellas SHA-256 e informes. Ideal para gerentes de compliance que necesitan respuestas rápidas.','acc2-price':'Portal Dashboard',
    'acc3-title':'En su Infraestructura (Feed/API)','acc3-desc':'El motor conectado a sus sistemas. Filtros inline de milisegundos vía API. Bloquee datos antes de llegar a OpenAI desde su propio servidor.','acc3-price':'Integración API Rest',
"""
content = re.sub(r"'pr-lbl':'Inversión',", dict_additions_es + "\n    'pr-lbl':'Inversión',", content)

dict_additions_en = """
    'acc-lbl':'Integration Methods','acc-title':'Governance where you need it.','acc-rec':'Recommended',
    'acc1-title':'In your Agent (MCP)','acc1-desc':'Live compliance inside your tools. Native to Claude, Cursor, and MCP clients. Your bots query risk matrices and block PII leaks directly in the code.','acc1-price':'Pro Plan (Add-on)',
    'acc2-title':'In your Browser (Terminal)','acc2-desc':'Auditing on a visual dashboard. Full history, SHA-256 ledger, and report generation. Ideal for compliance managers needing fast answers.','acc2-price':'Dashboard Portal',
    'acc3-title':'In your Stack (Feed/API)','acc3-desc':'The engine piped into your systems. Millisecond inline filters via API. Block data before it hits OpenAI at your server level.','acc3-price':'REST API Integration',
"""
content = re.sub(r"'pr-lbl':'Investment',", dict_additions_en + "\n    'pr-lbl':'Investment',", content)


with open('/Users/mac/brachat-main/portfolio/platform/site_oficial/aigovernance/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

