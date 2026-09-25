import re

with open('/Users/mac/brachat-main/portfolio/platform/frontend/site_oficial/aigovernance/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the Arquitetura de Dados section
pattern = r'(<div class="s-label" data-i18n="arch-lbl">Arquitetura de Dados</div>\n\s*<h2 class="s-title" data-i18n="arch-title">.*?</section>)'

new_section = """<div class="s-label" data-i18n="arch-lbl">A Prateleira Enterprise</div>
    <h2 class="s-title" data-i18n="arch-title">Governança implacável. Dois produtos diretos.</h2>
    <div class="workflow-grid" style="margin-top:48px;">
      
      <!-- Passo 1: BTScan -->
      <div class="wf-step">
        <div class="wf-icon">1</div>
        <div class="wf-content">
          <div class="wf-title">BTScan (Discovery & Auditoria)</div>
          <p class="wf-desc" data-i18n="wf1-desc">Inventário e Discovery Retroativo. O BTScan varre sua infraestrutura corporativa mapeando Shadow AI e integrações oficiais. Ele aplica nosso framework de interpretabilidade matemática retrospectivamente para auditar o perfil de risco do que já aconteceu.</p>
        </div>
      </div>

      <!-- Passo 2: BTMonitor -->
      <div class="wf-step">
        <div class="wf-icon">2</div>
        <div class="wf-content">
          <div class="wf-title">BTMonitor (Segurança Inline)</div>
          <p class="wf-desc" data-i18n="wf2-desc">Proxy reverso Commit-Bound com latência zero. Em vez de usar IAs lentas para fiscalizar outras IAs, o BTMonitor aplica o <strong>QILIS Framework</strong> "em voo". Ele calcula a assinatura matemática da intenção do usuário no espaço vetorial, bloqueando instantaneamente vazamentos (PII) e ataques (Jailbreak).</p>
        </div>
      </div>

      <!-- Passo 3: O Relatório -->
      <div class="wf-step">
        <div class="wf-icon">3</div>
        <div class="wf-content">
          <div class="wf-title">O Diferencial Absoluto: O Laudo Pericial Inalterável</div>
          <p class="wf-desc" data-i18n="wf3-desc">A verdadeira blindagem jurídica. Todas as interceptações do BTMonitor e auditorias do BTScan são trancadas em um <strong>Cofre Criptográfico WORM (SHA-256)</strong>. O sistema emite automaticamente um Relatório de Explicabilidade (RIPD) impossível de ser fraudado, garantindo prova pericial imediata para juízes e conselhos de compliance em caso de litígio.</p>
        </div>
      </div>

    </div>
  </div>
</section>"""

content = re.sub(pattern, new_section, content, flags=re.DOTALL)

with open('/Users/mac/brachat-main/portfolio/platform/frontend/site_oficial/aigovernance/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
