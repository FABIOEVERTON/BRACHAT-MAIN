const { Client, LocalAuth } = require('whatsapp-web.js');
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3456;
const client = new Client({
  authStrategy: new LocalAuth({ dataPath: path.join(__dirname, '.wwebjs_auth') }),
  puppeteer: { headless: true }
});

let currentQr = null;
let connected = false;

const server = http.createServer((req, res) => {
  if (connected) {
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(`<html><body style="font-family:sans-serif;text-align:center;padding-top:100px"><h1>✅ Conectado!</h1><p>WhatsApp conectado com sucesso. Pode fechar esta janela.</p><script>setTimeout(()=>window.close(),2000)</script></body></html>`);
    return;
  }
  if (!currentQr) {
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(`<html><body style="font-family:sans-serif;text-align:center;padding-top:100px"><h1>⏳ Aguardando QR...</h1><p>Recarregue a página em alguns segundos.</p></body></html>`);
    return;
  }
  const url = `https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=${encodeURIComponent(currentQr)}`;
  res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
  res.end(`<html><body style="font-family:sans-serif;text-align:center;padding-top:50px">
    <h1>Escaneie o QR Code</h1>
    <img src="${url}" alt="QR Code" style="width:300px;height:300px;image-rendering:pixelated"/>
    <p style="color:#666">Abra WhatsApp > Menu > WhatsApp Web > Escaneie</p>
    <script>setTimeout(()=>location.reload(),3000)</script>
  </body></html>`);
});

server.listen(PORT, () => {
  console.log(`[QR-VIEWER] Servidor rodando em http://localhost:${PORT}`);
  console.log(`[QR-VIEWER] Abra o navegador em http://localhost:${PORT} para ver o QR`);
});

client.on('qr', (qr) => {
  currentQr = qr;
  console.log('[QR] QR Code atualizado');
});

client.on('ready', () => {
  connected = true;
  console.log('[QR-VIEWER] WhatsApp conectado!');
  fs.writeFileSync(path.join(__dirname, 'connected.flag'), 'ok');
  setTimeout(() => { server.close(); process.exit(0); }, 3000);
});

client.on('auth_failure', (msg) => {
  console.error('[QR-VIEWER] Falha de autenticação:', msg);
});

client.initialize();
