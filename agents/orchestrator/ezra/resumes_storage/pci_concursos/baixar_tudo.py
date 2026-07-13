#!/usr/bin/env python3
"""
baixar_tudo.py - Baixa TODAS as provas CEBRASPE do PCI Concursos (1592 exames).
Uso: python3 baixar_tudo.py

FLUXO:
1. Abre o navegador numa pagina de exame
2. VC resolve o captcha (clicando no checkbox "Nao sou um robo")
3. O script captura o token e tenta reutilizar para baixar TUDO
4. Se o token expirar, pede pra resolver de novo
"""

import os, sys, json, re, time, pathlib, cloudscraper
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE = pathlib.Path.home() / "Downloads" / "pci_concursos"
PDF_DIR = BASE / "pdfs"
STATE_FILE = BASE / "progresso.json"
CODES_FILE = BASE / "all_codes.json"
MAX_WORKERS = 5

PDF_DIR.mkdir(parents=True, exist_ok=True)
scraper = cloudscraper.create_scraper()

def carregar_codes():
    with open(CODES_FILE) as f:
        return json.load(f)

def carregar_progresso():
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return set(json.load(f))
    return set()

def salvar_progresso(feitos):
    with open(STATE_FILE, "w") as f:
        json.dump(sorted(feitos), f)

def resolver_captcha():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False, args=["--no-sandbox", "--disable-blink-features=AutomationControlled"])
        context = browser.new_context(viewport={"width": 1280, "height": 800}, locale="pt-BR")
        page = context.new_page()
        page.goto("https://www.pciconcursos.com.br/provas/download/administracao-petrobras-cebraspe-2022")
        print("\n=== RESOLVA O CAPTCHA no navegador que abriu ===")
        print("Clique em 'Nao sou um robo' e aguarde...\n")
        token = None
        for i in range(120):
            time.sleep(1)
            try:
                t = page.evaluate("() => { try { return turnstile.getResponse(); } catch(e) { return null; } }")
                if t:
                    token = t
                    print(f"Captcha resolvido! Token obtido ({len(token)} chars)")
                    break
            except:
                pass
            if i % 10 == 0:
                print(f"  Aguardando captcha... ({i+1}s)")
        page.close()
        browser.close()
        return token

def baixar_url_direto(slug, token_tentativa):
    codes = carregar_codes()
    if slug not in codes:
        return None, "slug nao encontrado nos codes"
    code = codes[slug]
    try:
        r = scraper.post("https://www.pciconcursos.com.br/provas/link", data={"prova_code": code, "cf-turnstile-response": token_tentativa}, timeout=15)
        resp = r.json()
        if resp.get("ok") and resp.get("arquivos"):
            urls = {}
            for arq in resp["arquivos"]:
                urls[arq["arquivo"]] = "https://www.pciconcursos.com.br" + arq["baixar"] if arq["baixar"].startswith("/") else arq["baixar"]
            return urls, None
        return None, resp.get("erro", "resposta invalida")
    except Exception as e:
        return None, str(e)

def baixar_pdf(url, dest):
    if dest.exists() and dest.stat().st_size > 1000:
        return True
    try:
        r = scraper.get(url, timeout=60)
        if r.status_code == 200 and len(r.content) > 100:
            dest.parent.mkdir(parents=True, exist_ok=True)
            with open(dest, "wb") as f:
                f.write(r.content)
            return True
        return False
    except:
        return False

def main():
    print("=== BAIXAR TODAS AS PROVAS CEBRASPE (PCI Concursos) ===")
    print(f"Diretorio: {PDF_DIR}")
    if not CODES_FILE.exists():
        print("ERRO: all_codes.json nao encontrado! Execute primeiro: python3 extrair_codes.py")
        sys.exit(1)
    token = resolver_captcha()
    if not token:
        print("Falha ao obter token do captcha!")
        sys.exit(1)
    codes = carregar_codes()
    slugs = list(codes.keys())
    feitos = carregar_progresso()
    pendentes = [s for s in slugs if s not in feitos]
    print(f"\nTotal: {len(slugs)} exames | Ja baixados: {len(feitos)} | Pendentes: {len(pendentes)}")
    falhas_token = 0
    batch_size = 30
    while pendentes:
        batch = pendentes[:batch_size]
        print(f"\n--- Processando lote de {len(batch)} exames ---")
        lote_urls = {}
        for slug in batch:
            urls, erro = baixar_url_direto(slug, token)
            if urls:
                lote_urls[slug] = urls
            elif erro and "captcha" in str(erro).lower():
                falhas_token += 1
                if falhas_token >= 3:
                    print(f"\nToken expirou apos {len(feitos)} downloads. Precisa resolver o captcha NOVAMENTE...")
                    token = resolver_captcha()
                    if not token:
                        print("Falha no captcha!")
                        break
                    falhas_token = 0
                    continue
            else:
                print(f"  ! {slug[:40]}: {erro}")
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = []
            for slug, urls in lote_urls.items():
                for nome_arq, url in urls.items():
                    tipo = "gabarito" if "gabarito" in nome_arq.lower() else "prova"
                    slug_clean = slug.replace("/", "_")[:60]
                    dest = PDF_DIR / slug_clean / f"{tipo}.pdf"
                    futures.append((slug, executor.submit(baixar_pdf, url, dest)))
            for slug, future in futures:
                future.result()
        for slug in batch:
            feitos.add(slug)
        salvar_progresso(feitos)
        pendentes = [s for s in slugs if s not in feitos]
        print(f"Progresso: {len(feitos)}/{len(slugs)}")
        time.sleep(1)
    print(f"\n=== CONCLUIDO! {len(feitos)} exames baixados ===")
    print(f"PDFs em: {PDF_DIR}")

if __name__ == "__main__":
    main()
