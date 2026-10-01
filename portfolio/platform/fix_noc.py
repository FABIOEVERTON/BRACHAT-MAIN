import re

with open("master_admin/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Add an infrastructure separation widget
infra_html = """
      <!-- SHARED-NOTHING INFRASTRUCTURE VISUALIZATION -->
      <h3 class="text-xs font-mono text-gray-400 uppercase tracking-widest border-b border-white/5 pb-2 mt-8 mb-4">Topologia Shared-Nothing (Isolamento Físico)</h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        
        <div class="bg-[#3ecfbe]/5 border border-[#3ecfbe]/20 p-4 rounded-lg flex flex-col justify-between">
          <div class="flex items-center gap-2 mb-3">
            <i data-lucide="server" class="w-4 h-4 text-[#3ecfbe]"></i>
            <span class="text-sm font-bold text-white">Cluster AI (Isolado)</span>
          </div>
          <div class="text-[10px] font-mono text-gray-400 space-y-1">
            <div class="flex justify-between"><span>DB: RDS PostgreSQL</span><span class="text-[#3ecfbe]">db-ai-prd-01</span></div>
            <div class="flex justify-between"><span>Compute: EKS Node</span><span class="text-[#3ecfbe]">eks-ai-cls</span></div>
            <div class="flex justify-between"><span>Vault: S3 Glacier</span><span class="text-[#3ecfbe]">vault-ia-hash</span></div>
            <div class="flex justify-between mt-2 pt-2 border-t border-white/5 text-gray-300"><span>MRR Isolado:</span><span>R$ 480.000</span></div>
          </div>
        </div>

        <div class="bg-yellow-500/5 border border-yellow-500/20 p-4 rounded-lg flex flex-col justify-between">
          <div class="flex items-center gap-2 mb-3">
            <i data-lucide="server" class="w-4 h-4 text-yellow-400"></i>
            <span class="text-sm font-bold text-white">Cluster Muni (Isolado)</span>
          </div>
          <div class="text-[10px] font-mono text-gray-400 space-y-1">
            <div class="flex justify-between"><span>DB: RDS PostgreSQL</span><span class="text-yellow-400">db-mn-prd-02</span></div>
            <div class="flex justify-between"><span>Compute: EKS Node</span><span class="text-yellow-400">eks-mn-cls</span></div>
            <div class="flex justify-between"><span>Vault: S3 Glacier</span><span class="text-yellow-400">vault-mn-hash</span></div>
            <div class="flex justify-between mt-2 pt-2 border-t border-white/5 text-gray-300"><span>MRR Isolado:</span><span>R$ 610.000</span></div>
          </div>
        </div>

        <div class="bg-purple-500/5 border border-purple-500/20 p-4 rounded-lg flex flex-col justify-between">
          <div class="flex items-center gap-2 mb-3">
            <i data-lucide="server" class="w-4 h-4 text-purple-400"></i>
            <span class="text-sm font-bold text-white">Cluster Rig (Isolado)</span>
          </div>
          <div class="text-[10px] font-mono text-gray-400 space-y-1">
            <div class="flex justify-between"><span>DB: RDS PostgreSQL</span><span class="text-purple-400">db-rg-prd-03</span></div>
            <div class="flex justify-between"><span>Compute: EKS Node</span><span class="text-purple-400">eks-rg-cls</span></div>
            <div class="flex justify-between"><span>Vault: S3 Glacier</span><span class="text-purple-400">vault-rg-hash</span></div>
            <div class="flex justify-between mt-2 pt-2 border-t border-white/5 text-gray-300"><span>MRR Isolado:</span><span>R$ 392.500</span></div>
          </div>
        </div>

      </div>
"""

# Insert right after the Telemetry Matrix
html = html.replace(
    '<!-- BOTTOM ROW: BUGS / EXCEPTIONS & SECURITY AUDIT -->',
    infra_html + '\n      <!-- BOTTOM ROW: BUGS / EXCEPTIONS & SECURITY AUDIT -->'
)

with open("master_admin/index.html", "w", encoding="utf-8") as f:
    f.write(html)
