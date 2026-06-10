#!/usr/bin/env python3
"""Yahoo Mail CLI - leitura e envio de emails via IMAP/SMTP"""
import imaplib, smtplib, email, json, sys, getpass
from email.mime.text import MIMEText
from email.header import decode_header

IMAP_SERVER = "imap.mail.yahoo.com"
SMTP_SERVER = "smtp.mail.yahoo.com"
SMTP_PORT = 587

def decode_str(s):
    if not s: return ""
    parts = decode_header(s)
    return "".join(
        part.decode(charset or "utf-8") if isinstance(part, bytes) else part
        for part, charset in parts
    )

def list_emails(mail, n=10):
    mail.select("INBOX")
    status, msgs = mail.search(None, "ALL")
    ids = msgs[0].split()[-n:]
    results = []
    for eid in ids:
        status, data = mail.fetch(eid, "(RFC822)")
        for part in data:
            if isinstance(part, tuple):
                msg = email.message_from_bytes(part[1])
                results.append({
                    "id": eid.decode(),
                    "from": decode_str(msg["From"]),
                    "subject": decode_str(msg["Subject"]),
                    "date": msg["Date"]
                })
    return results

def send_email(smtp, user, pw, to, subject, body):
    msg = MIMEText(body)
    msg["From"] = user
    msg["To"] = to
    msg["Subject"] = subject
    smtp.sendmail(user, [to], msg.as_string())
    return {"sent": True, "to": to, "subject": subject}

def main():
    print("=== Yahoo Mail CLI ===")
    user = "fabioeverton@yahoo.com.br"
    pw = getpass.getpass(f"Senha de app para {user}: ")

    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(user, pw)
        print("✅ Conectado via IMAP\n")
    except Exception as e:
        print(f"❌ Falha: {e}. Use senha de app (Yahoo > Segurança > Senhas de app)")
        sys.exit(1)

    smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    smtp.starttls()
    smtp.login(user, pw)

    while True:
        print("\n--- MENU ---")
        print("1. Listar últimos emails")
        print("2. Enviar email")
        print("0. Sair")
        op = input("> ").strip()

        if op == "1":
            n = input("Quantos? (padrao 10): ").strip()
            for e in list_emails(mail, int(n) if n else 10):
                print(f"\n[{e['id']}] {e['date']}")
                print(f"    De: {e['from']}")
                print(f"    Assunto: {e['subject']}")
        elif op == "2":
            to = input("Para: ").strip()
            subject = input("Assunto: ").strip()
            print("Corpo (Ctrl+D ou linha com . pra finalizar):")
            lines = []
            while True:
                try:
                    line = input()
                    if line.strip() == ".":
                        break
                    lines.append(line)
                except EOFError:
                    break
            body = "\n".join(lines)
            r = send_email(smtp, user, pw, to, subject, body)
            print(f"✅ Email enviado para {r['to']}")
        elif op == "0":
            break

    mail.logout()
    smtp.quit()
    print("Desconectado.")

if __name__ == "__main__":
    main()
