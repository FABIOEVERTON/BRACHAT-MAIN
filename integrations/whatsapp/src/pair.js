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
const PHONE = process.argv[2] || "5561998743226";

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

let codePrinted = false;

sock.ev.on("connection.update", async ({ connection, lastDisconnect }) => {
  if (connection === "open") {
    console.log(`CONNECTED:${sock.user?.id}`);
    setTimeout(() => process.exit(0), 2000);
  }
  if (connection === "close") {
    const reason = lastDisconnect?.error?.output?.statusCode;
    if (reason === DisconnectReason.loggedOut) {
      if (codePrinted) {
        console.log("LOGGED_OUT");
        process.exit(2);
      }
    } else {
      setTimeout(() => process.exit(1), 1000);
    }
  }
});

sock.ev.on("messages.upsert", () => {});

await new Promise((r) => setTimeout(r, 3000));
const raw = await sock.requestPairingCode(PHONE);
const code = raw?.match(/.{1,4}/g)?.join("-") || raw;
codePrinted = true;
console.log(code);

setTimeout(() => process.exit(1), 120000);
