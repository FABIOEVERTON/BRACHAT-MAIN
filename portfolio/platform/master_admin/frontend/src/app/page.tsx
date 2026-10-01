import { 
  Activity, Users, Database, Shield, Zap, TrendingUp,
  Server, HardDrive, CheckCircle2, AlertCircle 
} from "lucide-react";

export default function MasterAdminDashboard() {
  return (
    <div className="min-h-screen bg-[#0a0e17] text-gray-100 flex font-sans">
      
      {/* SIDEBAR */}
      <aside className="w-64 border-r border-white/5 bg-[#0a0e17] flex-col hidden md:flex">
        <div className="h-16 flex items-center px-6 border-b border-white/5">
          <h1 className="text-xl font-bold tracking-widest text-white">
            <span className="text-[#3ecfbe]">B</span>racha<span className="text-[#3ecfbe]">T</span>ec<span className="text-xs text-white/40 ml-2 font-normal">HUB</span>
          </h1>
        </div>
        <nav className="flex-1 p-4 space-y-2">
          <a href="#" className="flex items-center gap-3 px-3 py-2 bg-white/5 text-[#3ecfbe] rounded-lg border border-[#3ecfbe]/20">
            <Activity size={18} /> <span className="text-sm font-medium">Visão Global</span>
          </a>
          <a href="#" className="flex items-center gap-3 px-3 py-2 text-gray-400 hover:text-white hover:bg-white/5 rounded-lg transition-colors">
            <Users size={18} /> <span className="text-sm font-medium">Gestão de Clientes</span>
          </a>
          <a href="#" className="flex items-center gap-3 px-3 py-2 text-gray-400 hover:text-white hover:bg-white/5 rounded-lg transition-colors">
            <Shield size={18} /> <span className="text-sm font-medium">Parceiros WL</span>
          </a>
          <a href="#" className="flex items-center gap-3 px-3 py-2 text-gray-400 hover:text-white hover:bg-white/5 rounded-lg transition-colors">
            <Database size={18} /> <span className="text-sm font-medium">Cofre WORM</span>
          </a>
        </nav>
        <div className="p-4 border-t border-white/5">
          <div className="flex items-center gap-3 text-xs text-gray-400">
            <div className="w-2 h-2 rounded-full bg-[#3ecfbe] animate-pulse"></div>
            System Online (sa-east-1)
          </div>
        </div>
      </aside>

      {/* MAIN CONTENT */}
      <main className="flex-1 flex flex-col h-screen overflow-hidden">
        {/* TOP NAV */}
        <header className="h-16 border-b border-white/5 bg-[#0a0e17] flex items-center justify-between px-8">
          <h2 className="text-lg font-medium text-gray-200">Painel de Controle Central</h2>
          <div className="flex items-center gap-4">
            <span className="text-sm text-gray-400">Admin</span>
            <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-[#3ecfbe] to-blue-600"></div>
          </div>
        </header>

        {/* SCROLLABLE AREA */}
        <div className="flex-1 overflow-y-auto p-8 bg-[#0a0e17] bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-[#101622] to-[#0a0e17]">
          
          {/* KPI ROW */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div className="bg-[#141c2b]/60 border border-white/5 p-6 rounded-xl backdrop-blur-sm shadow-xl">
              <div className="flex justify-between items-start mb-4">
                <span className="text-gray-400 text-sm font-medium">Receita Mensal (MRR)</span>
                <TrendingUp size={18} className="text-[#3ecfbe]" />
              </div>
              <div className="text-3xl font-bold text-white mb-1">R$ 1.482.500</div>
              <div className="text-xs text-[#3ecfbe]">+12.4% comparado ao mês passado</div>
            </div>

            <div className="bg-[#141c2b]/60 border border-white/5 p-6 rounded-xl backdrop-blur-sm shadow-xl">
              <div className="flex justify-between items-start mb-4">
                <span className="text-gray-400 text-sm font-medium">Clientes Ativos</span>
                <Users size={18} className="text-blue-400" />
              </div>
              <div className="text-3xl font-bold text-white mb-1">428</div>
              <div className="text-xs text-gray-400 flex gap-2 mt-2">
                <span className="bg-blue-500/10 text-blue-400 px-1.5 py-0.5 rounded text-[10px] border border-blue-500/20">Gov AI: 112</span>
                <span className="bg-yellow-500/10 text-yellow-400 px-1.5 py-0.5 rounded text-[10px] border border-yellow-500/20">Muni: 204</span>
                <span className="bg-purple-500/10 text-purple-400 px-1.5 py-0.5 rounded text-[10px] border border-purple-500/20">Rig: 112</span>
              </div>
            </div>

            <div className="bg-[#141c2b]/60 border border-white/5 p-6 rounded-xl backdrop-blur-sm shadow-xl">
              <div className="flex justify-between items-start mb-4">
                <span className="text-gray-400 text-sm font-medium">Assessorias WL</span>
                <Shield size={18} className="text-yellow-400" />
              </div>
              <div className="text-3xl font-bold text-white mb-1">64</div>
              <div className="text-xs text-gray-400 mt-2">Atendendo 1.200 pontas finais</div>
            </div>

            <div className="bg-[#141c2b]/60 border border-white/5 p-6 rounded-xl backdrop-blur-sm shadow-xl relative overflow-hidden">
              <div className="absolute top-0 right-0 p-4 opacity-10"><Database size={64} /></div>
              <div className="flex justify-between items-start mb-4">
                <span className="text-gray-400 text-sm font-medium">Hashes SHA-256 / 24h</span>
                <Activity size={18} className="text-[#3ecfbe]" />
              </div>
              <div className="text-3xl font-bold text-white mb-1">1.2M</div>
              <div className="text-xs text-[#3ecfbe] flex items-center gap-1 mt-2">
                <span className="w-1.5 h-1.5 rounded-full bg-[#3ecfbe] animate-pulse"></span>
                Gravando no Cofre WORM em tempo real
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            {/* AWS HEALTH & WORM STATUS */}
            <div className="lg:col-span-2 bg-[#141c2b]/60 border border-white/5 rounded-xl backdrop-blur-sm shadow-xl flex flex-col">
              <div className="p-6 border-b border-white/5 flex justify-between items-center">
                <h3 className="text-sm font-medium text-white flex items-center gap-2">
                  <Server size={16} className="text-gray-400" /> Status da Infraestrutura
                </h3>
                <span className="text-[10px] uppercase tracking-widest text-[#3ecfbe] border border-[#3ecfbe]/30 px-2 py-1 rounded bg-[#3ecfbe]/10">AWS SA-EAST-1</span>
              </div>
              <div className="p-6 grid grid-cols-3 gap-4 flex-1">
                <div className="flex flex-col gap-2 p-4 border border-white/5 rounded-lg bg-[#0a0e17]/50">
                  <div className="text-xs text-gray-400 uppercase tracking-wider">Controlador CPT (IA)</div>
                  <div className="flex items-center gap-2">
                    <CheckCircle2 size={16} className="text-[#3ecfbe]" />
                    <span className="text-sm font-medium text-white">Operacional</span>
                  </div>
                  <div className="text-[10px] text-gray-500 mt-2">Latência: 12ms</div>
                </div>
                <div className="flex flex-col gap-2 p-4 border border-white/5 rounded-lg bg-[#0a0e17]/50">
                  <div className="text-xs text-gray-400 uppercase tracking-wider">Rastreador LEX (Rig)</div>
                  <div className="flex items-center gap-2">
                    <CheckCircle2 size={16} className="text-[#3ecfbe]" />
                    <span className="text-sm font-medium text-white">Operacional</span>
                  </div>
                  <div className="text-[10px] text-gray-500 mt-2">Buscando 89 diários/s</div>
                </div>
                <div className="flex flex-col gap-2 p-4 border border-white/5 rounded-lg bg-[#0a0e17]/50 border-orange-500/20 relative overflow-hidden">
                  <div className="absolute top-0 right-0 w-1 h-full bg-orange-500/50"></div>
                  <div className="text-xs text-gray-400 uppercase tracking-wider">Transferegov API</div>
                  <div className="flex items-center gap-2">
                    <AlertCircle size={16} className="text-orange-400" />
                    <span className="text-sm font-medium text-orange-100">Carga Alta</span>
                  </div>
                  <div className="text-[10px] text-orange-400 mt-2">Processando editais...</div>
                </div>
              </div>
            </div>

            {/* LIVE SYSTEM LOG */}
            <div className="bg-[#141c2b]/60 border border-white/5 rounded-xl backdrop-blur-sm shadow-xl flex flex-col h-[300px]">
              <div className="p-6 border-b border-white/5">
                <h3 className="text-sm font-medium text-white flex items-center gap-2">
                  <Zap size={16} className="text-gray-400" /> Terminal de Eventos
                </h3>
              </div>
              <div className="flex-1 p-6 overflow-y-auto space-y-4">
                <div className="flex flex-col gap-1">
                  <span className="text-[10px] text-gray-500">Há 2 min</span>
                  <div className="text-sm text-gray-300"><span className="text-yellow-400 font-medium">[Muni]</span> Nova licitação auditada: Pref. São Paulo</div>
                  <div className="text-[10px] text-gray-600 font-mono">hash: 9f86d081884c7d65...</div>
                </div>
                <div className="flex flex-col gap-1">
                  <span className="text-[10px] text-gray-500">Há 5 min</span>
                  <div className="text-sm text-gray-300"><span className="text-blue-400 font-medium">[Gov AI]</span> Shadow AI bloqueada: Hospital Albert E.</div>
                  <div className="text-[10px] text-gray-600 font-mono">hash: 52c92b23a9d701e6...</div>
                </div>
                <div className="flex flex-col gap-1">
                  <span className="text-[10px] text-gray-500">Há 12 min</span>
                  <div className="text-sm text-gray-300"><span className="text-purple-400 font-medium">[Rig]</span> Push disparado: Impacto tributário PL-22</div>
                  <div className="text-[10px] text-gray-600 font-mono">hash: 10a173873499426f...</div>
                </div>
                <div className="flex flex-col gap-1">
                  <span className="text-[10px] text-gray-500">Há 45 min</span>
                  <div className="text-sm text-gray-300"><span className="text-[#3ecfbe] font-medium">[Billing]</span> Nova Assinatura: Assessoria WL Alpha</div>
                </div>
              </div>
            </div>
          </div>

        </div>
      </main>
    </div>
  );
}
