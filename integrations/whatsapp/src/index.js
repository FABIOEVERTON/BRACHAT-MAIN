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

const logger = pino({
  level: process.env.LOG_LEVEL || "info",
  transport: {
    target: "pino-pretty",
    options: { colorize: true },
  },
});

async function start() {
  const { version, isLatest } = await fetchLatestBaileysVersion();
  logger.info(`Baileys v${version} (latest: ${isLatest})`);

  const { state, saveCreds } = await useMultiFileAuthState(AUTH_DIR);

  const sock = makeWASocket({
    version,
    auth: state,
    logger,
    browser: ["Brachat", "Chrome", "22.0"],
    markOnlineOnConnect: true,
    syncFullHistory: false,
  });

  sock.ev.on("creds.update", saveCreds);

  sock.ev.on("connection.update", async ({ connection, lastDisconnect, qr }) => {
    if (qr) {
      try {
        const { default: qrcode } = await import("qrcode-terminal");
        qrcode.generate(qr, { small: true });
      } catch {
        console.log("\nQR Code:\n" + qr);
      }
      console.log("\n📱 Scan the QR Code with your WhatsApp (Settings > Linked Devices)");
      return;
    }

    if (connection === "open") {
      console.log(`✅ WhatsApp connected! Logged in as: ${sock.user?.id}`);
    }

    if (connection === "close") {
      const reason = lastDisconnect?.error?.output?.statusCode;
      const shouldReconnect = reason !== DisconnectReason.loggedOut;
      console.log(
        `❌ Disconnected (${reason}). ${shouldReconnect ? "Reconnecting..." : "Logged out."}`
      );
      if (shouldReconnect) {
        setTimeout(start, 1000);
      }
    }
  });

  sock.ev.on("messages.upsert", ({ messages }) => {
    for (const msg of messages) {
      if (!msg.key.fromMe && msg.message?.conversation) {
        console.log(`💬 ${msg.key.remoteJid}: ${msg.message.conversation}`);
      }
    }
  });

  process.on("SIGINT", () => {
    console.log("\nDisconnecting...");
    sock.end(undefined);
    process.exit(0);
  });
}

start().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});
