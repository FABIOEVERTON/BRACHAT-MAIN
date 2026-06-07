const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');

const client = new Client({
  authStrategy: new LocalAuth(),
  puppeteer: { headless: true }
});

client.on('qr', (qr) => {
  console.log('=== ESCANEIE O QR CODE COM SEU WHATSAPP ===');
  qrcode.generate(qr, { small: true });
  console.log('===========================================');
});

client.on('ready', () => {
  console.log('[WHATSAPP] Conectado com sucesso!');
  console.log('[WHATSAPP] Para enviar mensagens: node send.js NUMERO "TEXTO"');
});

client.on('message', async (msg) => {
  console.log(`[RECEBIDO] De ${msg.from}: ${msg.body}`);
});

client.initialize();
