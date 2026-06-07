const { makeWASocket, useMultiFileAuthState, Browsers, DisconnectReason } = require('@whiskeysockets/baileys');
const http = require('http');
const fs = require('fs');
const path = require('path');
const pino = require('pino');

const PORT = 3456;
const QUEUE_FILE = path.join(__dirname, 'queue.json');
const STATUS_FILE = path.join(__dirname, 'status.json');
const AUTH_DIR = path.join(__dirname, 'auth_baileys');
const CONTACTS_FILE = path.join(__dirname, 'contacts.json');

let sock = null;
let currentQr = null;
const contactMap = {};

function setStatus(s) {
  fs.writeFileSync(STATUS_FILE, JSON.stringify({ status: s, updated_at: new Date().toISOString() }, null, 2));
}

function log(m) {
  const ts = new Date().toISOString();
  process.stdout.write(`[${ts}] ${m}\n`);
}

async function processQueue() {
  if (!sock) return;
  try {
    if (!fs.existsSync(QUEUE_FILE)) return;
    const queue = JSON.parse(fs.readFileSync(QUEUE_FILE, 'utf-8'));
    const pending = queue.filter(q => q.status === 'pending');
    if (pending.length === 0) return;

    for (const item of pending) {
      try {
        const jid = item.to.includes('@') ? item.to : `${item.to}@s.whatsapp.net`;
        await sock.sendMessage(jid, { text: item.text });
        item.status = 'sent';
        item.sent_at = new Date().toISOString();
        log(`Mensagem enviada para ${item.to} [from: ${item.from}]`);
      } catch (err) {
        item.status = 'failed';
        item.error = err.message;
        log(`Falha ao enviar para ${item.to}: ${err.message}`);
      }
    }
    fs.writeFileSync(QUEUE_FILE, JSON.stringify(queue, null, 2));
  } catch (e) {
    log(`Erro na fila: ${e.message}`);
  }
}

function saveContacts() {
  const list = Object.entries(contactMap)
    .filter(([jid]) => !jid.includes('@g.us') && !jid.includes('status@broadcast'))
    .map(([jid, info]) => ({ jid, ...info }))
    .sort((a, b) => (a.name || a.number).localeCompare(b.name || b.number));
  fs.writeFileSync(CONTACTS_FILE, JSON.stringify(list, null, 2));
}

async function listContacts() {
  return Object.entries(contactMap)
    .filter(([jid]) => !jid.includes('@g.us') && !jid.includes('status@broadcast'))
    .map(([jid, info]) => ({ jid, ...info }))
    .sort((a, b) => (a.name || a.number).localeCompare(b.name || b.number));
}

async function startBot() {
  const { state, saveCreds } = await useMultiFileAuthState(AUTH_DIR);

  sock = makeWASocket({
    auth: state,
    printQRInTerminal: true,
    browser: Browsers.macOS('Chrome'),
    logger: pino({ level: 'warn' }),
    syncFullHistory: true,
    markOnlineOnConnect: false
  });

  sock.ev.on('contacts.upsert', async (contacts) => {
    for (const c of contacts) {
      if (c.id && c.id.includes('@s.whatsapp.net')) {
        contactMap[c.id] = { name: c.name || c.notify || c.verifiedName || null, number: c.id.split('@')[0] };
      }
    }
    saveContacts();
  });

  sock.ev.on('contacts.update', async (contacts) => {
    for (const c of contacts) {
      if (c.id && contactMap[c.id]) {
        Object.assign(contactMap[c.id], { name: c.name || c.notify || c.verifiedName || null });
      }
    }
    saveContacts();
  });

  sock.ev.on('connection.update', async (update) => {
    const { connection, lastDisconnect, qr } = update;

    if (qr) {
      currentQr = qr;
      setStatus('qr_required');
      log('Novo QR Code gerado');
    }

    if (connection === 'connecting') {
      setStatus('connecting');
      log('Conectando...');
    }

    if (connection === 'open') {
      currentQr = null;
      setStatus('connected');
      log('WhatsApp conectado com sucesso!');
      fs.writeFileSync(path.join(__dirname, 'connected.flag'), new Date().toISOString());

      // Salvar contatos periodicamente
      setTimeout(async () => {
        try {
          const contacts = await listContacts();
          fs.writeFileSync(CONTACTS_FILE, JSON.stringify(contacts, null, 2));
          log(`Contatos salvos: ${contacts.length}`);
        } catch (e) {
          log(`Erro ao salvar contatos: ${e.message}`);
        }
      }, 10000);

      // Processar fila com delay inicial
      setTimeout(() => {
        processQueue();
        setInterval(processQueue, 5000);
      }, 5000);
    }

    if (connection === 'close') {
      const reason = lastDisconnect?.error?.output?.statusCode;
      const shouldReconnect = reason !== DisconnectReason.loggedOut;
      log(`Desconectado (${reason}). Reconnectar: ${shouldReconnect}`);
      setStatus('disconnected');
      sock = null;

      if (shouldReconnect) {
        setTimeout(startBot, 3000);
      } else {
        log('Deslogado permanentemente — remova auth_baileys e escaneie QR de novo');
        setStatus('logged_out');
      }
    }
  });

  sock.ev.on('messages.upsert', async (m) => {
    for (const msg of m.messages) {
      if (!msg.key.fromMe && msg.key.remoteJid) {
        log(`[RECEBIDO] De ${msg.key.remoteJid}: ${msg.message?.conversation || msg.message?.extendedTextMessage?.text || '(mídia)'}`);
      }
    }
  });

  sock.ev.on('creds.update', saveCreds);
}

const server = http.createServer((req, res) => {
  if (req.url === '/status') {
    const s = JSON.parse(fs.readFileSync(STATUS_FILE, 'utf-8') || '{}');
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(s));
    return;
  }

  if (req.url === '/contacts') {
    try {
      const c = JSON.parse(fs.readFileSync(CONTACTS_FILE, 'utf-8') || '[]');
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(c, null, 2));
    } catch (e) {
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: e.message }));
    }
    return;
  }

  try {
    const s = JSON.parse(fs.readFileSync(STATUS_FILE, 'utf-8') || '{}');
    if (s.status === 'connected' || s.status === 'disconnected' || s.status === 'logged_out') {
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(`<html><body style="font-family:sans-serif;text-align:center;padding-top:100px">
        <h1>✅ ${s.status === 'connected' ? 'Conectado!' : s.status === 'logged_out' ? 'Deslogado' : 'Desconectado'}</h1>
        <p>WhatsApp ${s.status === 'connected' ? 'conectado' : 'não conectado'}.</p>
        <a href="/contacts">Ver contatos</a>
      </body></html>`);
      return;
    }
  } catch (e) {}

  if (!currentQr) {
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(`<html><body style="font-family:sans-serif;text-align:center;padding-top:100px">
      <h1>⏳ Aguardando QR...</h1>
      <p>Recarregue em alguns segundos.</p>
      <script>setTimeout(()=>location.reload(),3000)</script>
    </body></html>`);
    return;
  }

  const url = `https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=${encodeURIComponent(currentQr)}`;
  res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
  res.end(`<html><body style="font-family:sans-serif;text-align:center;padding-top:50px">
    <h1>Escaneie o QR Code</h1>
    <img src="${url}" alt="QR Code" style="width:300px;height:300px"/>
    <p style="color:#666">Abra WhatsApp > Menu > Aparelhos vinculados > Vincular um dispositivo</p>
    <script>setTimeout(()=>location.reload(),3000)</script>
  </body></html>`);
});

server.listen(PORT, () => {
  log(`Servidor Baileys rodando em http://localhost:${PORT}`);
  setStatus('starting');
  startBot();
});

process.on('SIGTERM', () => { if (sock) sock.end(undefined); process.exit(0); });
process.on('SIGINT', () => { if (sock) sock.end(undefined); process.exit(0); });
