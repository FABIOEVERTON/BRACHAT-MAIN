#!/usr/bin/env python3
"""
baixar_tudo_v2.py - Baixa TODAS as provas CEBRASPE do PCI Concursos (1592 exames).

FLUXO:
1. Abre navegador para voce resolver o captcha UMA vez
2. Tenta usar o token para obter URLs de TODOS os 1592 exames
3. Se o token funcionar para + de 1, baixa tudo em paralelo
4. Se falhar, baixa um por um pedindo captcha quando necessario
"""

import os, sys, json, re, time, pathlib, cloudscraper, math
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE = pathlib.Path.home() / "Downloads" / "pci_concursos"
PDF_DIR = BASE / "pdfs"
STATE_FILE = BASE / "progresso.json"
CODES_FILE = BASE / "all_codes.json"
URLS_FILE = BASE / "urls_totais.json"
MAX_WORKERS = 10

PDF_DIR.mkdir(parents=True, exist_ok=True)


def resolver_captcha(mensagem="Resolva o captcha no navegador"):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False, args=["--no-sandbox"])
        ctx = browser.new_context(viewport={"width": 1280, "height": 800}, locale="pt-BR")
        page = ctx.new_page()
        page.goto("https://www.pciconcursos.com.br/provas/download/administracao-petrobras-cebraspe-2022")
        print(f"\n{'='*60}")
        print(f"  {mensagem}")
        print(f"  Clique em 'Nao sou um robo' (ou resolva o desafio)")
        print(f"  O script detectara automaticamente e continuara")
        print(f"{'='*60}\n")
        for i in range(300):
            time.sleep(1)
            try:
                t = page.evaluate("() => { try { return turnstile.getResponse(); } catch(e) { return null; } }")
                if t:
                    print(f"\nCaptcha resolvido! Token obtido.")
                    page.close()
                    browser.close()
                    return t
            except:
                pass
            if i % 15 == 0:
                print(f"  Aguardando captcha... ({i+1}s)")
        print("Timeout aguardando captcha.")
        page.close()
        browser.close()
        return None


def obter_urls_exame(slug, code, token):
    scraper = cloudscraper.create_scraper()
    try:
        r = scraper.post(
            "https://www.pciconcursos.com.br/provas/link",
            data={"prova_code": code, "cf-turnstile-response": token},
            timeout=15,
        )
        resp = r.json()
        if resp.get("ok") and resp.get("arquivos"):
            urls = {}
            for arq in resp["arquivos"]:
                url_raw = arq["baixar"]
                url_full = url_raw if url_raw.startswith("http") else "https://www.pciconcursos.com.br" + url_raw
                urls[arq["arquivo"]] = url_full
            return urls, None
        return None, resp.get("erro", "falha")
    except Exception as e:
        return None, str(e)


def baixar_pdf(url, dest):
    if dest.exists() and dest.stat().st_size > 1000:
        return True
    try:
        scraper = cloudscraper.create_scraper()
        r = scraper.get(url, timeout=60)
        if r.status_code == 200 and len(r.content) > 1000:
            dest.parent.mkdir(parents=True, exist_ok=True)
            with open(dest, "wb") as f:
                f.write(r.content)
            return True
        return False
    except:
        return False


def main():
    print("=== BAIXAR TODAS AS PROVAS CEBRASPE (1592 exames) ===")
    
    if not CODES_FILE.exists():
        print("ERRO: all_codes.json nao encontrado!")
        sys.exit(1)
    
    with open(CODES_FILE) as f:
        codes = json.load(f)
    
    slugs = list(codes.keys())
    print(f"\nTotal de exames: {len(slugs)}")
    
    # Carrega progresso
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            completos = set(json.load(f))
    else:
        completos = set()
    
    pendentes = [s for s in slugs if s not in completos]
    print(f"Ja baixados: {len(completos)}")
    print(f"Pendentes:   {len(pendentes)}")
    
    # Carrega ou constroi mapa de URLs
    urls_map = {}
    if URLS_FILE.exists():
        with open(URLS_FILE) as f:
            urls_map = json.load(f)
        print(f"URLs ja conhecidas: {len(urls_map)}")
    
    # FASE 1: Obter URLs pendentes
    slugs_precisam_url = [s for s in pendentes if s not in urls_map]
    if slugs_precisam_url:
        print(f"\nFASE 1: Obter URLs para {len(slugs_precisam_url)} exames")
        
        while slugs_precisam_url:
            token = resolver_captcha()
            if not token:
                print("Falha no captcha!")
                break
            
            # Tenta em lote com este token
            lote = slugs_precisam_url[:50]
            acertos = 0
            for slug in lote:
                urls, erro = obter_urls_exame(slug, codes[slug], token)
                if urls:
                    urls_map[slug] = urls
                    acertos += 1
                elif erro and "captcha" in erro.lower():
                    print(f"  Token expirou apos {acertos} acertos")
                    break
                time.sleep(0.3)  # rate limit
            
            with open(URLS_FILE, "w") as f:
                json.dump(urls_map, f, indent=2)
            
            slugs_precisam_url = [s for s in pendentes if s not in urls_map]
            print(f"  Acertos neste lote: {acertos}/{len(lote)}")
            print(f"  URLs totais: {len(urls_map)}, ainda faltam: {len(slugs_precisam_url)}")
    
    # FASE 2: Baixar PDFs
    ainda_pendentes = [s for s in slugs if s not in completos and s in urls_map]
    if ainda_pendentes:
        print(f"\nFASE 2: Baixar PDFs de {len(ainda_pendentes)} exames")
        
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = []
            for slug in ainda_pendentes:
                for nome_arq, url in urls_map[slug].items():
                    tipo = "gabarito" if "gabarito" in nome_arq.lower() else "prova"
                    slug_clean = slug.replace("/", "_")[:80]
                    dest = PDF_DIR / slug_clean / f"{tipo}.pdf"
                    futures.append((slug, tipo, executor.submit(baixar_pdf, url, dest)))
            
            for i, (slug, tipo, future) in enumerate(futures):
                ok = future.result()
                if ok:
                    completos.add(slug)
                if (i+1) % 20 == 0:
                    with open(STATE_FILE, "w") as f:
                        json.dump(sorted(completos), f)
                    print(f"  Progresso: {len(completos)}/{len(slugs)}")
        
        with open(STATE_FILE, "w") as f:
            json.dump(sorted(completos), f)
        
        print(f"\nBaixados: {len(completos)}/{len(slugs)}")
    
    # Mostra estatisticas finais
    total_pdfs = sum(len(v) for v in urls_map.values())
    print(f"\n=== RESUMO ===")
    print(f"Exames com URL: {len(urls_map)}")
    print(f"Exames baixados: {len(completos)}")
    print(f"Total de PDFs esperados: ~{total_pdfs}")
    print(f"PDFs em: {PDF_DIR}")


if __name__ == "__main__":
    main()
