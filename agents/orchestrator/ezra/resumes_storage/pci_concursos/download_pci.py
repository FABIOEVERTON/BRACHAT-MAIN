#!/usr/bin/env python3
"""
download_pci.py - Baixa todas as provas CEBRASPE do PCI Concursos (páginas 1 a 32)
Uso: python3 download_pci.py [--resume]
"""
import os, sys, json, time, pathlib, traceback
from urllib.parse import urljoin

BASE_DIR = pathlib.Path.home() / "Downloads" / "pci_concursos"
PDF_DIR = BASE_DIR / "pdfs"
STATE_FILE = BASE_DIR / "download_state.json"
BASE_URL = "https://www.pciconcursos.com.br"
TOTAL_PAGES = 32
PDF_DIR.mkdir(parents=True, exist_ok=True)

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PwTimeout
except ImportError:
    os.system("pip3 install playwright && playwright install chromium")
    from playwright.sync_api import sync_playwright, TimeoutError as PwTimeout

def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE) as f: return json.load(f)
    return {"completed_exams": [], "pages_done": []}

def save_state(state):
    with open(STATE_FILE, "w") as f: json.dump(state, f, indent=2)

def get_exam_links(page, page_num):
    url = f"{BASE_URL}/provas/cebraspe" + (f"/{page_num}" if page_num > 1 else "")
    page.goto(url, wait_until="networkidle"); time.sleep(2)
    links = page.eval_on_selector_all("a[href*='/provas/download/']", "els => els.map(el => ({href: el.href, text: el.innerText.trim()}))")
    seen, unique = set(), []
    for l in links:
        h = l["href"]
        if h not in seen and "/provas/download/" in h:
            seen.add(h); unique.append(l)
    return unique

def wait_for_download_links(page, timeout=30000):
    try:
        page.wait_for_function("() => { const links = document.querySelectorAll('.prova-pdf-link[data-acao=\"baixar\"]'); return links.length > 0 && links[0].href && links[0].href !== 'javascript:void(0);'; }", timeout=timeout)
        return True
    except PwTimeout:
        return False

def get_download_urls(page):
    return page.eval_on_selector_all('a.prova-pdf-link[data-acao="baixar"]', 'els => els.map(el => ({arquivo: el.dataset.arquivo, url: el.href}))')

def try_solve_captcha(page):
    for attempt in range(30):
        solved = page.evaluate("() => { try { if (typeof liberado !== 'undefined' && liberado) return true; if (typeof turnstile !== 'undefined') { var resp = turnstile.getResponse(); if (resp) { if (typeof provasCaptchaOk === 'function') provasCaptchaOk(resp); return true; } } return false; } catch(e) { return false; } }")
        if solved:
            time.sleep(2); return True
        time.sleep(1)
    return False

def download_pdf(page, url, filepath):
    if filepath.exists() and filepath.stat().st_size > 1000: return True
    try:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with page.expect_download(timeout=60000) as download_info:
            page.goto(url, wait_until="domcontentloaded")
        download_info.value.save_as(str(filepath))
        return True
    except Exception as e:
        print(f"  ! Erro download {url}: {e}"); return False

def process_exam(page, exam_href, exam_text, page_num, exam_idx, state):
    exam_key = exam_href.split("/provas/download/")[-1]
    if exam_key in state["completed_exams"]:
        print(f"  [{exam_idx}] Já baixado: {exam_text}"); return True
    page_dir = PDF_DIR / f"page_{page_num:03d}"
    page_dir.mkdir(parents=True, exist_ok=True)
    print(f"  [{exam_idx}] {exam_text}...", end=" ", flush=True)
    page.goto(exam_href, wait_until="domcontentloaded"); time.sleep(3)
    links_ready = wait_for_download_links(page, timeout=15000)
    if not links_ready:
        solved = try_solve_captcha(page)
        if solved:
            time.sleep(2); links_ready = wait_for_download_links(page, timeout=15000)
        else:
            print("captcha nao resolvido automaticamente"); return False
    if not links_ready:
        print("links nao disponiveis"); return False
    urls = get_download_urls(page)
    if not urls:
        print("sem urls de download"); return False
    all_ok = True
    for item in urls:
        fname, url = item["arquivo"], item["url"]
        tipo = "gabarito" if "gabarito" in fname.lower() else "prova"
        safe_name = exam_key.replace("/", "_")[:80]
        dest = page_dir / f"{exam_idx:03d}_{safe_name}_{tipo}.pdf"
        ok = download_pdf(page, url, dest)
        print(f"{tipo}{'(OK)' if ok else '(FAIL)'} ", end="", flush=True)
        if not ok: all_ok = False
    if all_ok:
        state["completed_exams"].append(exam_key); save_state(state)
    print(); return all_ok

def main():
    resume = "--resume" in sys.argv
    state = {"completed_exams": [], "pages_done": []} if not resume else load_state()
    print(f"PCI Concursos Downloader - {TOTAL_PAGES} páginas | Resume: {'SIM' if resume else 'NAO'} | Completos: {len(state['completed_exams'])} exames\n")
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"])
        context = browser.new_context(user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", viewport={"width": 1280, "height": 1024})
        page = context.new_page()
        try:
            for p in range(1, TOTAL_PAGES + 1):
                if p in state["pages_done"]:
                    print(f"Pagina {p}/{TOTAL_PAGES} - ja concluida"); continue
                print(f"\n=== Pagina {p}/{TOTAL_PAGES} ===")
                exams = get_exam_links(page, p)
                print(f"Encontrados {len(exams)} exames")
                if not exams:
                    print("Sem exames - pulando"); state["pages_done"].append(p); save_state(state); continue
                success_count = sum(1 for idx, exam in enumerate(exams, 1) if process_exam(page, exam["href"], exam["text"], p, idx, state))
                state["pages_done"].append(p); save_state(state)
                print(f"Pagina {p}: {success_count}/{len(exams)} ok")
        except Exception as e:
            print(f"\nERRO: {e}"); traceback.print_exc()
        finally:
            browser.close()
    print(f"\nConcluido! {len(state['completed_exams'])} exames baixados em {PDF_DIR}")

if __name__ == "__main__":
    main()
