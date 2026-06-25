import {
  makeWASocket,
  useMultiFileAuthState,
  DisconnectReason,
  fetchLatestBaileysVersion,
} from "@whiskeysockets/baileys";
import pino from "pino";
import { existsSync, mkdirSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const AUTH_DIR = join(__dirname, "..", "auth");

if (!existsSync(AUTH_DIR)) {
  mkdirSync(AUTH_DIR, { recursive: true });
}

const { version } = await fetchLatestBaileysVersion();
const { state, saveCreds } = await useMultiFileAuthState(AUTH_DIR);

const sock = makeWASocket({
  version,
  auth: state,
  logger: pino({ level: "silent" }),
  browser: ["Brachat", "Chrome", "22.0"],
  markOnlineOnConnect: true,
  syncFullHistory: false,
});

sock.ev.on("creds.update", saveCreds);

let qrShown = false;

sock.ev.on("connection.update", async ({ connection, lastDisconnect, qr }) => {
  if (qr && !qrShown) {
    qrShown = true;
    try {
      const { default: qrcode } = await import("qrcode-terminal");
      qrcode.generate(qr, { small: true });
    } catch {
      console.log(qr);
    }
    console.log("SCAN_ME");
    return;
  }

  if (connection === "open") {
    console.log("CONNECTED");
    console.log(JSON.stringify({ user: sock.user?.id }));
    setTimeout(() => process.exit(0), 1000);
  }

  if (connection === "close") {
    const reason = lastDisconnect?.error?.output?.statusCode;
    if (reason === DisconnectReason.loggedOut) {
      console.log("LOGGED_OUT");
      process.exit(1);
    }
  }
});

sock.ev.on("messages.upsert", () => {});

setTimeout(() => {
  if (!qrShown) {
    console.log("QR_EXPIRED_RESTART");
    process.exit(1);
  }
}, 25000);
