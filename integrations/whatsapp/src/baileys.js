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

if (!existsSync(AUTH_DIR)) mkdirSync(AUTH_DIR, { recursive: true });

const logger = pino({ level: "silent" });

async function start() {
  const { version } = await fetchLatestBaileysVersion();
  const { state, saveCreds } = await useMultiFileAuthState(AUTH_DIR);
  const sock = makeWASocket({
    version,
    auth: state,
    logger,
    browser: ["Brachat", "Chrome", "22.0"],
    syncFullHistory: false,
  });
  sock.ev.on("creds.update", saveCreds);
  sock.ev.on("messages.upsert", () => {});

  let qrCount = 0;
  sock.ev.on("connection.update", async ({ connection, lastDisconnect, qr }) => {
    if (qr) {
      qrCount++;
      process.stdout.write("\x1B[2J\x1B[0;0H");
      process.stdout.write("=== BRACHAT WHATSAPP ===\n\n");
      process.stdout.write(`QR Code #${qrCount} - Scan with your phone\n\n`);
      try {
        const { default: qrcode } = await import("qrcode-terminal");
        qrcode.generate(qr, { small: false });
      } catch {
        process.stdout.write(qr + "\n");
      }
      process.stdout.write("\nWhatsApp > Linked Devices > Link a Device\n\n");
      process.stdout.write("Waiting for scan...\n");
      return;
    }
    if (connection === "open") {
      process.stdout.write(`\n✅ CONNECTED: ${sock.user?.id}\n`);
      process.exit(0);
    }
    if (connection === "close") {
      const code = lastDisconnect?.error?.output?.statusCode;
      if (code === DisconnectReason.loggedOut) {
        process.stdout.write("\n🔴 Logged out\n");
        process.exit(2);
      }
      process.stdout.write(`\n⚠️ Reconnecting (${code})...\n`);
      start();
    }
  });
}

start().catch((e) => { process.stdout.write("Fatal: " + e.message + "\n"); process.exit(1); });
