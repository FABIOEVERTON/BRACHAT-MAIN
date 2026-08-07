const BASE = process.env.OPENCODE_URL || "http://127.0.0.1:3791";
const TOKEN = process.env.TELEGRAM_BOT_TOKEN;
const PASS = process.env.OPENCODE_SERVER_PASSWORD;
const TIMEOUT = 240000;
if (!TOKEN || !PASS) { console.error("missing TELEGRAM_BOT_TOKEN or OPENCODE_SERVER_PASSWORD"); process.exit(1); }
const AUTH = "Basic " + Buffer.from("opencode:" + PASS).toString("base64");
const TG = "https://api.telegram.org/bot" + TOKEN;
const sessions = {};
let offset = 0;
async function tg(method, body) {
  const r = await fetch(TG + "/" + method, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body || {}) });
  return r.json();
}
async function send(chatId, text) {
  const s = String(text || "");
  for (const chunk of s.match(/[\s\S]{1,4000}/g) || []) await tg("sendMessage", { chat_id: chatId, text: chunk });
}
async function post(url, body) {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), TIMEOUT);
  try {
    return await fetch(url, { method: "POST", headers: { Authorization: AUTH, "Content-Type": "application/json" }, body: JSON.stringify(body), signal: ctrl.signal });
  } finally { clearTimeout(t); }
}
async function ask(chatId, text) {
  let sid = sessions[chatId];
  if (!sid) {
    const r = await post(BASE + "/session", {});
    if (!r || !r.ok) return send(chatId, "(erro ao abrir sessão)");
    const j = await r.json();
    sid = sessions[chatId] = j.id;
  }
  const r = await post(BASE + "/session/" + sid + "/message", { parts: [{ type: "text", text }] });
  if (!r || !r.ok) return send(chatId, "(falha no processamento)");
  const j = await r.json();
  const out = (j.parts || []).filter(p => p.type === "text" && p.text).map(p => p.text).join("\n").trim();
  await send(chatId, out || "(sem resposta)");
}
async function poll() {
  const up = await tg("getUpdates", { offset, timeout: 50, allowed_updates: ["message"] });
  for (const u of up.result || []) {
    offset = u.update_id + 1;
    const m = u.message;
    if (!m || !m.text) continue;
    await ask(m.chat.id, m.text);
  }
}
(async () => {
  console.log("bridge_telegram: relay", TOKEN.slice(0, 9) + "...", "->", BASE, "(timeout", TIMEOUT + "ms)");
  for (;;) {
    try { await poll(); } catch (e) { console.error("poll", e.message); }
    await new Promise(r => setTimeout(r, 250));
  }
})();
