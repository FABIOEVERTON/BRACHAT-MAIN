import re

with open('/Users/mac/brachat-main/portfolio/platform/site_oficial/academy/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace title and meta
content = re.sub(r'<title>.*?</title>', '<title>BRACHATEC Academy — Treinamentos e Cursos</title>', content)

# Modify Hero Section
hero_html = """
<section class="hero-inner" style="padding-top:160px;padding-bottom:100px;text-align:center;position:relative;overflow:hidden;">
  <div class="hero-glow"></div>
  <div class="section-inner" style="position:relative;z-index:2;">
    <div class="hero-tag" data-i18n="hero-tag">BRACHATEC Academy</div>
    <h1 class="hero-title" data-i18n="hero-title">Do problema ao domínio.<br>Capacitação Regulatória.</h1>
    <p class="hero-lead" data-i18n="hero-lead">Educação corporativa estruturada. Videoaulas, materiais de apoio e certificação para times que precisam dominar conformidade com profundidade técnica.</p>
    
    <!-- VIDEO PLACEHOLDER -->
    <div class="video-placeholder" style="max-width:800px; margin: 40px auto; background:#0e1525; border:1px solid rgba(201,168,76,.28); border-radius:12px; overflow:hidden; position:relative; aspect-ratio:16/9; display:flex; align-items:center; justify-content:center; box-shadow: 0 20px 40px rgba(0,0,0,0.4);">
      <div style="text-align:center;">
        <div style="width:64px;height:64px;background:var(--gold);border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 16px;cursor:pointer;box-shadow:0 0 20px var(--gold-dim);">
          <div style="width:0;height:0;border-top:10px solid transparent;border-bottom:10px solid transparent;border-left:16px solid var(--navy);margin-left:4px;"></div>
        </div>
        <div style="color:var(--white); font-weight:500;" data-i18n="vid-play">Assistir ao Trailer da Academia</div>
      </div>
    </div>
    
    <div class="hero-actions" style="justify-content:center;">
      <a href="#cursos" class="btn-primary" data-i18n="hero-btn">Explorar Cursos</a>
    </div>
  </div>
</section>
"""
content = re.sub(r'<section class="hero-inner".*?</section>', hero_html, content, flags=re.DOTALL)

# Modify Workflow/Curriculum Section
curriculum_html = """
<section id="cursos" class="section">
  <div class="section-inner">
    <div class="s-label" data-i18n="cur-lbl">Grade Curricular</div>
    <h2 class="s-title" data-i18n="cur-title">Módulos em Vídeo e Texto</h2>
    
    <div class="curriculum-list" style="margin-top:40px; display:flex; flex-direction:column; gap:16px; max-width:800px; margin-left:auto; margin-right:auto;">
      
      <!-- Module 1 -->
      <div style="background:var(--navy-2); border:1px solid var(--gold-border); border-radius:8px; padding:24px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
          <h3 style="margin:0; color:var(--white); font-size:20px;" data-i18n="mod1-title">Módulo 1: Conscientização Regulatória</h3>
          <span style="background:var(--gold-dim); color:var(--gold); padding:4px 12px; border-radius:12px; font-size:12px; font-weight:600;" data-i18n="mod-free">Gratuito</span>
        </div>
        <p style="color:var(--muted); font-size:14px; margin-bottom:16px;" data-i18n="mod1-desc">Fundamentos de conformidade, riscos de Shadow AI e introdução ao monitoramento de diários oficiais.</p>
        <div style="display:flex; gap:16px; font-size:13px; color:var(--muted-2);">
          <span style="display:flex; align-items:center; gap:4px;">▶ <span data-i18n="mod-vid">4 Aulas (Vídeo)</span></span>
          <span style="display:flex; align-items:center; gap:4px;">📄 <span data-i18n="mod-txt">2 Materiais de Apoio (PDF)</span></span>
        </div>
      </div>
      
      <!-- Module 2 -->
      <div style="background:var(--navy-2); border:1px solid var(--gold-border); border-radius:8px; padding:24px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
          <h3 style="margin:0; color:var(--white); font-size:20px;" data-i18n="mod2-title">Módulo 2: Governança Prática de IA</h3>
          <span style="background:var(--navy-4); color:var(--white-2); padding:4px 12px; border-radius:12px; font-size:12px; font-weight:600;" data-i18n="mod-pro">Pro</span>
        </div>
        <p style="color:var(--muted); font-size:14px; margin-bottom:16px;" data-i18n="mod2-desc">Como auditar endpoints, bloquear PII (dados sensíveis) em tempo real e construir relatórios forenses SHA-256.</p>
        <div style="display:flex; gap:16px; font-size:13px; color:var(--muted-2);">
          <span style="display:flex; align-items:center; gap:4px;">▶ <span data-i18n="mod-vid2">8 Aulas Práticas (Vídeo)</span></span>
          <span style="display:flex; align-items:center; gap:4px;">📄 <span data-i18n="mod-txt2">Scripts e Templates</span></span>
        </div>
      </div>

      <!-- Module 3 -->
      <div style="background:var(--navy-2); border:1px solid var(--gold-border); border-radius:8px; padding:24px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
          <h3 style="margin:0; color:var(--white); font-size:20px;" data-i18n="mod3-title">Módulo 3: Implantação e Certificação</h3>
          <span style="background:var(--navy-4); color:var(--white-2); padding:4px 12px; border-radius:12px; font-size:12px; font-weight:600;" data-i18n="mod-cert">Certificação</span>
        </div>
        <p style="color:var(--muted); font-size:14px; margin-bottom:16px;" data-i18n="mod3-desc">Exame final de múltipla escolha e avaliação prática para emissão do Certificado Oficial BRACHATEC Integrator.</p>
        <div style="display:flex; gap:16px; font-size:13px; color:var(--muted-2);">
          <span style="display:flex; align-items:center; gap:4px;">🏆 <span data-i18n="mod-badge">Badge Oficial</span></span>
        </div>
      </div>

    </div>
  </div>
</section>
"""
content = re.sub(r'<section id="dor".*?<section id="workflow".*?</section>', curriculum_html, content, flags=re.DOTALL)
content = re.sub(r'<section class="section" style="background:var\(--navy-2\)".*?</section>', '', content, flags=re.DOTALL)

# Dictionary update (removing old, inserting new)
dict_script = """
var T={
  pt:{
    'nav-login':'Acessar Plataforma',
    'nav-back':'← Voltar para home','nav-cta':'Ver Planos',
    'hero-tag':'BRACHATEC Academy',
    'hero-title':'Do problema ao domínio.<br>Capacitação Regulatória.',
    'hero-lead':'Educação corporativa estruturada. Videoaulas, materiais de apoio e certificação para times que precisam dominar conformidade com profundidade técnica.',
    'vid-play':'Assistir ao Trailer da Academia',
    'hero-btn':'Explorar Cursos',
    'cur-lbl':'Grade Curricular','cur-title':'Módulos em Vídeo e Texto',
    'mod1-title':'Módulo 1: Conscientização Regulatória',
    'mod-free':'Gratuito',
    'mod1-desc':'Fundamentos de conformidade, riscos de Shadow AI e introdução ao monitoramento de diários oficiais.',
    'mod-vid':'4 Aulas (Vídeo)','mod-txt':'2 Materiais de Apoio (PDF)',
    'mod2-title':'Módulo 2: Governança Prática de IA',
    'mod-pro':'Premium',
    'mod2-desc':'Como auditar endpoints, bloquear PII (dados sensíveis) em tempo real e construir relatórios forenses SHA-256.',
    'mod-vid2':'8 Aulas Práticas (Vídeo)','mod-txt2':'Scripts e Templates',
    'mod3-title':'Módulo 3: Implantação e Certificação',
    'mod-cert':'Certificação',
    'mod3-desc':'Exame final de múltipla escolha e avaliação prática para emissão do Certificado Oficial BRACHATEC Integrator.',
    'mod-badge':'Badge Oficial',
    'pr-lbl':'Acesso','pr-title':'Planos da Academia','pr-sub':'Comece a estudar gratuitamente ou forme todo o seu time de compliance.',
    'pr1-price':'R$ 0<span>/mês</span>',
    'pr-set1':'Acesso Imediato<br>Sem necessidade de cartão de crédito',
    'pr1-l1':'Módulo 1 completo (Vídeos)',
    'pr1-l2':'Material de apoio em PDF',
    'pr1-l3':'Participação em Webinars',
    'pr-btn-std':'Criar Conta Grátis',
    'pr2-price':'R$ 149<span>/usuário/mês</span>',
    'pr-set2':'Acesso total<br>Cancele quando quiser',
    'pr2-l1':'Todos os módulos em Vídeo',
    'pr2-l2':'Acesso a Scripts e Templates',
    'pr2-l3':'Emissão de Certificado',
    'pr2-l4':'Suporte direto com tutores',
    'pr-btn-ent':'Assinar Premium',
    'pr3-price':'Sob Consulta',
    'pr-set3':'Para empresas e agências',
    'pr3-l1':'Licenças em lote (10+ usuários)',
    'pr3-l2':'Painel de acompanhamento de alunos',
    'pr3-l3':'Treinamentos In-Company',
    'pr-btn-wl':'Falar com Vendas',
    'faq-title':'Dúvidas Frequentes',
    'faq1-q':'Os cursos emitem certificado?','faq1-a':'Sim, ao concluir os módulos pagos e passar na avaliação final, você recebe um certificado digital.',
    'faq2-q':'Posso baixar as videoaulas?','faq2-a':'As videoaulas devem ser assistidas na plataforma, mas os materiais de apoio (PDFs) podem ser baixados.',
    'faq3-q':'Como funciona para empresas?','faq3-a':'No plano corporativo, o gestor recebe um painel para acompanhar o progresso das aulas de toda a equipe.',
    'cta-title':'Pronto para dominar a governança?','cta-sub':'Crie sua conta gratuita agora e comece a assistir à primeira aula.','cta-btn':'Começar Agora',
    'f-copy':'© 2025 BRACHATEC Tecnologia Ltda. Todos os direitos reservados.'
  },
  es:{
    'nav-login':'Iniciar Sesión',
    'nav-back':'← Volver al inicio','nav-cta':'Ver Planes',
    'hero-tag':'BRACHATEC Academy',
    'hero-title':'Del problema al dominio.<br>Capacitación Regulatoria.',
    'hero-lead':'Educación corporativa estructurada. Videoclases, materiales de apoyo y certificación para equipos.',
    'vid-play':'Ver Trailer de la Academia',
    'hero-btn':'Explorar Cursos',
    'cur-lbl':'Plan de Estudios','cur-title':'Módulos en Video y Texto',
    'mod1-title':'Módulo 1: Conciencia Regulatoria',
    'mod-free':'Gratis',
    'mod1-desc':'Fundamentos de cumplimiento, riesgos de Shadow AI e introducción al monitoreo.',
    'mod-vid':'4 Clases (Video)','mod-txt':'2 Materiales de Apoyo (PDF)',
    'mod2-title':'Módulo 2: Gobernanza Práctica de IA',
    'mod-pro':'Premium',
    'mod2-desc':'Cómo auditar endpoints, bloquear PII (datos sensibles) en tiempo real y emitir reportes.',
    'mod-vid2':'8 Clases Prácticas (Video)','mod-txt2':'Scripts y Plantillas',
    'mod3-title':'Módulo 3: Implementación y Certificación',
    'mod-cert':'Certificación',
    'mod3-desc':'Examen final para emisión del Certificado Oficial BRACHATEC Integrator.',
    'mod-badge':'Insignia Oficial',
    'pr-lbl':'Acceso','pr-title':'Planes de la Academia','pr-sub':'Empiece a estudiar gratis o forme a todo su equipo de compliance.',
    'pr1-price':'$0<span>/mes</span>',
    'pr-set1':'Acceso Inmediato<br>Sin tarjeta de crédito',
    'pr1-l1':'Módulo 1 completo (Videos)',
    'pr1-l2':'Material de apoyo en PDF',
    'pr1-l3':'Participación en Webinars',
    'pr-btn-std':'Crear Cuenta Gratis',
    'pr2-price':'$29<span>/usuario/mes</span>',
    'pr-set2':'Acceso total<br>Cancele cuando quiera',
    'pr2-l1':'Todos los módulos en Video',
    'pr2-l2':'Acceso a Scripts y Plantillas',
    'pr2-l3':'Emisión de Certificado',
    'pr2-l4':'Soporte directo con tutores',
    'pr-btn-ent':'Suscribirse Premium',
    'pr3-price':'Bajo Consulta',
    'pr-set3':'Para empresas y agencias',
    'pr3-l1':'Licencias por volumen (10+ usuarios)',
    'pr3-l2':'Panel de seguimiento de alumnos',
    'pr3-l3':'Entrenamientos In-Company',
    'pr-btn-wl':'Hablar con Ventas',
    'faq-title':'Preguntas Frecuentes',
    'faq1-q':'¿Los cursos emiten certificado?','faq1-a':'Sí, al concluir los módulos pagos y aprobar la evaluación final, recibe un certificado digital.',
    'faq2-q':'¿Puedo descargar las videoclases?','faq2-a':'Las videoclases deben ser vistas en la plataforma, pero los materiales de apoyo (PDF) pueden descargarse.',
    'faq3-q':'¿Cómo funciona para empresas?','faq3-a':'En el plan corporativo, el gerente recibe un panel para rastrear el progreso de todo el equipo.',
    'cta-title':'¿Listo para dominar la gobernanza?','cta-sub':'Cree su cuenta gratis ahora y comience a ver la primera clase.','cta-btn':'Empezar Ahora',
    'f-copy':'© 2025 BRACHATEC Tecnologia Ltda. Todos los derechos reservados.'
  },
  en:{
    'nav-login':'Log In',
    'nav-back':'← Back to home','nav-cta':'View Plans',
    'hero-tag':'BRACHATEC Academy',
    'hero-title':'From problem to mastery.<br>Regulatory Training.',
    'hero-lead':'Structured corporate education. Video lessons, support materials, and certification for teams.',
    'vid-play':'Watch Academy Trailer',
    'hero-btn':'Explore Courses',
    'cur-lbl':'Curriculum','cur-title':'Video and Text Modules',
    'mod1-title':'Module 1: Regulatory Awareness',
    'mod-free':'Free',
    'mod1-desc':'Compliance fundamentals, Shadow AI risks, and introduction to gazette monitoring.',
    'mod-vid':'4 Lessons (Video)','mod-txt':'2 Support Materials (PDF)',
    'mod2-title':'Module 2: Practical AI Governance',
    'mod-pro':'Premium',
    'mod2-desc':'How to audit endpoints, block PII (sensitive data) in real-time, and build forensic reports.',
    'mod-vid2':'8 Practical Lessons (Video)','mod-txt2':'Scripts and Templates',
    'mod3-title':'Module 3: Implementation and Certification',
    'mod-cert':'Certification',
    'mod3-desc':'Final exam to earn the Official BRACHATEC Integrator Certificate.',
    'mod-badge':'Official Badge',
    'pr-lbl':'Access','pr-title':'Academy Plans','pr-sub':'Start studying for free or train your entire compliance team.',
    'pr1-price':'$0<span>/mo</span>',
    'pr-set1':'Instant Access<br>No credit card required',
    'pr1-l1':'Module 1 complete (Videos)',
    'pr1-l2':'Support material in PDF',
    'pr1-l3':'Webinar participation',
    'pr-btn-std':'Create Free Account',
    'pr2-price':'$29<span>/user/mo</span>',
    'pr-set2':'Full Access<br>Cancel anytime',
    'pr2-l1':'All video modules',
    'pr2-l2':'Access to Scripts and Templates',
    'pr2-l3':'Certificate issuance',
    'pr2-l4':'Direct support with tutors',
    'pr-btn-ent':'Subscribe Premium',
    'pr3-price':'On Demand',
    'pr-set3':'For companies and agencies',
    'pr3-l1':'Bulk licenses (10+ users)',
    'pr3-l2':'Student tracking dashboard',
    'pr3-l3':'In-Company training',
    'pr-btn-wl':'Talk to Sales',
    'faq-title':'Frequently Asked Questions',
    'faq1-q':'Do the courses issue a certificate?','faq1-a':'Yes, upon completing the paid modules and passing the final exam, you receive a digital certificate.',
    'faq2-q':'Can I download the video lessons?','faq2-a':'Video lessons must be watched on the platform, but support materials (PDFs) can be downloaded.',
    'faq3-q':'How does it work for companies?','faq3-a':'On the corporate plan, managers get a dashboard to track the progress of their entire team.',
    'cta-title':'Ready to master governance?','cta-sub':'Create your free account now and start watching the first lesson.','cta-btn':'Start Now',
    'f-copy':'© 2025 BRACHATEC Tecnologia Ltda. All rights reserved.'
  }
};
"""
content = re.sub(r'var T=\{.*?\n\};\nfunction setLang', dict_script + '\nfunction setLang', content, flags=re.DOTALL)

with open('/Users/mac/brachat-main/portfolio/platform/site_oficial/academy/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

