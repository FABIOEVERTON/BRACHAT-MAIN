const { Client, LocalAuth } = require('whatsapp-web.js');

const numero = process.argv[2];
const texto = process.argv[3];

if (!numero || !texto) {
  console.log('Uso: node send.js NUMERO "MENSAGEM"');
  console.log('Ex: node send.js 5561998743226 "Olá!"');
  process.exit(1);
}

(async () => {
  const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: { headless: true }
  });

  let resolved = false;

  client.on('qr', () => {
    if (!resolved) {
      console.log('[ERRO] Nao autenticado. Execute node start.js primeiro e escaneie o QR.');
      resolved = true;
      process.exit(1);
    }
  });

  client.on('ready', async () => {
    if (resolved) return;
    resolved = true;
    try {
      const chatId = numero.includes('@c.us') ? numero : `${numero}@c.us`;
      const response = await client.sendMessage(chatId, texto);
      console.log(`[ENVIADO] Para ${numero}: ${texto.substring(0, 60)}`);
      console.log(`Message ID: ${response.id._serialized}`);
    } catch (err) {
      console.error(`[ERRO]`, err.message);
    }
    process.exit(0);
  });

  client.initialize();
})();
