#!/usr/bin/env python3
"""
process_pci.py - Extrai texto dos PDFs, organiza por materia, gera arquivos para NotebookLM.
Gera: textos/parte_XXX.txt (max 500k palavras cada), metadados/metadados.csv, metadados/notebooklm_index.json
"""
import os, sys, re, json, pathlib, csv, math
from collections import defaultdict

BASE_DIR = pathlib.Path.home() / "Downloads" / "pci_concursos"
PDF_DIR = BASE_DIR / "pdfs"
TEXTOS_DIR = BASE_DIR / "textos"
METADADOS_DIR = BASE_DIR / "metadados"
MAX_WORDS_PER_FILE = 480_000

try:
    import fitz
except ImportError:
    os.system("pip3 install PyMuPDF"); import fitz

KEYWORDS = {
    "portugues": ["português", "língua portuguesa", "gramática", "ortografia", "interpretação de texto", "sintaxe", "crase"],
    "matematica": ["matemática", "raciocínio lógico", "álgebra", "geometria", "aritmética", "estatística", "probabilidade"],
    "informatica": ["informática", "computação", "linux", "windows", "word", "excel", "internet", "redes"],
    "direito_constitucional": ["direito constitucional", "constituição", "direitos fundamentais", "poder executivo", "poder legislativo"],
    "direito_administrativo": ["direito administrativo", "administração pública", "servidores públicos", "licitação"],
    "direito_penal": ["direito penal", "código penal", "crime", "pena", "tipicidade", "culpabilidade"],
    "direito_processual_penal": ["direito processual penal", "processo penal", "inquérito policial", "ação penal"],
    "direito_civil": ["direito civil", "código civil", "obrigações", "contratos", "responsabilidade civil"],
    "direito_tributario": ["direito tributário", "tributo", "imposto", "taxa", "ctn", "obrigação tributária"],
    "direito_do_trabalho": ["direito do trabalho", "clt", "contrato de trabalho", "remuneração", "jornada", "fgts"],
    "raciocinio_logico": ["raciocínio lógico", "lógica", "sequências", "diagramas", "proposições"],
    "administracao_geral": ["administração geral", "gestão", "planejamento", "organização", "liderança"],
    "administracao_publica": ["administração pública", "governo", "estado", "políticas públicas", "governança"],
    "contabilidade": ["contabilidade", "balanço", "demonstração contábil", "patrimônio", "ativo", "passivo"],
    "economia": ["economia", "microeconomia", "macroeconomia", "oferta", "demanda", "inflação", "pib"],
    "engenharia": ["engenharia", "cálculo", "física", "resistência dos materiais", "hidráulica", "topografia"],
    "conhecimentos_gerais": ["conhecimentos gerais", "atualidades", "história", "geografia", "meio ambiente"],
    "etica": ["ética", "moral", "deontologia", "conduta", "código de ética"],
    "legislacao_especifica": ["lei ", "decreto", "regulamento", "norma", "resolução", "portaria"],
}

def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = "\n".join(page.get_text() for page in doc if page.get_text().strip())
        doc.close()
        return re.sub(r"[ \t]+", " ", re.sub(r"\n{3,}", "\n\n", text)).strip()
    except Exception as e:
        print(f"  ! Erro extraindo {pdf_path.name}: {e}"); return ""

def extract_exam_metadata(pdf_path):
    name = pdf_path.stem
    parts = name.split("_", 2)
    page_num, exam_key = (parts[0], parts[1]) if len(parts) > 1 else ("?", name)
    tipo = "gabarito" if "gabarito" in name.lower() else "prova"
    exam_info = exam_key.replace("-", " ").title()
    orgao, cargo, ano = "", "", ""
    for i, p in enumerate(exam_info.split()):
        if re.match(r"^\d{4}$", p):
            ano = p; orgao = " ".join(exam_info.split()[:i]); cargo = " ".join(exam_info.split()[i+1:]) if i+1 < len(exam_info.split()) else ""; break
    if not ano:
        orgao = exam_info; m = re.search(r"(19|20)\d{2}", name)
        if m: ano = m.group()
    return {"filename": pdf_path.name, "exam_key": exam_key, "tipo": tipo, "orgao": orgao or exam_key, "cargo": cargo, "ano": ano, "page_num": page_num}

def guess_subject(text):
    text_lower = text.lower()
    scores = {subj: sum(1 for kw in kws if kw in text_lower) for subj, kws in KEYWORDS.items()}
    return max(scores, key=scores.get) if scores else "outros"

def split_into_questions(text):
    for pat in [r"(?=Quest[ãa]o\s+\d+)", r"(?=Q\.\s*\d+)", r"(?=^\s*\d+[\s\)\.])"]:
        parts = re.split(pat, text, flags=re.MULTILINE)
        if len(parts) > 3: return [p.strip() for p in parts if len(p.strip()) > 20]
    return [text]

def main():
    print("=== Processador PCI Concursos ===")
    TEXTOS_DIR.mkdir(parents=True, exist_ok=True); METADADOS_DIR.mkdir(parents=True, exist_ok=True)
    pdf_files = sorted(PDF_DIR.rglob("*.pdf"))
    print(f"PDFs encontrados: {len(pdf_files)}")
    all_entries, all_texts = [], []
    for idx, pdf_path in enumerate(pdf_files, 1):
        print(f"[{idx}/{len(pdf_files)}] {pdf_path.name}...", end=" ", flush=True)
        meta = extract_exam_metadata(pdf_path)
        text = extract_text_from_pdf(pdf_path)
        if len(text) < 30: print("vazio/pouco texto"); continue
        subject = guess_subject(text)
        meta.update({"subject": subject, "char_count": len(text), "word_count": len(text.split())})
        all_entries.append(meta); all_texts.append({"meta": meta, "text": text, "questions": split_into_questions(text), "subject": subject})
        print(f"{meta['word_count']} palavras, materia={subject}")
    print(f"\nProcessados: {len(all_texts)} PDFs com texto valido")
    by_subject = defaultdict(list)
    for item in all_texts: by_subject[item["subject"]].append(item)
    print(f"Materias encontradas: {len(by_subject)}")
    for subj, items in sorted(by_subject.items()):
        print(f"  {subj}: {len(items)} arquivos, ~{sum(it['meta']['word_count'] for it in items)} palavras")
    print("\nGerando arquivos para NotebookLM...")
    file_index, current_words, current_parts, generated_files = 1, 0, [], []
    def flush_current():
        nonlocal file_index, current_words, current_parts
        if not current_parts: return
        content = "\n\n=====\n\n".join(p["text"] for p in current_parts)
        fname = f"cebraspe_parte_{file_index:04d}.txt"
        with open(TEXTOS_DIR / fname, "w", encoding="utf-8") as f: f.write(content)
        wc = len(content.split())
        generated_files.append({"filename": fname, "word_count": wc, "char_count": len(content), "subjects": list(set(p["subject"] for p in current_parts))})
        print(f"  {fname}: {wc} palavras, {len(current_parts)} blocos")
        file_index += 1; current_words = 0; current_parts = []
    for subj in sorted(by_subject.keys()):
        for item in by_subject[subj]:
            block = f"=== MATERIA: {subj.upper()} ===\n=== CONCURSO: {item['meta']['orgao']} ===\n=== CARGO: {item['meta']['cargo']} ===\n=== ANO: {item['meta']['ano']} ===\n=== TIPO: {item['meta']['tipo']} ===\n\n{item['text']}"
            block_words = len(block.split())
            if current_words + block_words > MAX_WORDS_PER_FILE and current_words > 0: flush_current()
            current_parts.append({"subject": subj, "text": block}); current_words += block_words
    flush_current()
    print(f"\nArquivos gerados: {len(generated_files)} | Total palavras: {sum(f['word_count'] for f in generated_files)}")
    print("\nGerando metadados...")
    csv_path = METADADOS_DIR / "metadados.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["filename", "subject", "orgao", "cargo", "ano", "tipo", "word_count", "char_count", "exam_key"])
        writer.writeheader(); writer.writerows(all_entries)
    print(f"  CSV: {csv_path} ({len(all_entries)} linhas)")
    index_data = {
        "title": "CEBRASPE - Provas e Gabaritos (PCI Concursos)",
        "description": f"{len(all_texts)} PDFs processados de concursos CEBRASPE, organizados por materia",
        "total_files": len(generated_files), "total_pdfs_processed": len(all_texts),
        "total_words": sum(f["word_count"] for f in generated_files), "max_words_per_file": MAX_WORDS_PER_FILE,
        "files": generated_files,
        "subjects": {subj: {"count": len(items), "total_words": sum(it["meta"]["word_count"] for it in items)} for subj, items in sorted(by_subject.items())},
        "suggested_questions": ["Resuma as principais caracteristicas das provas CEBRASPE", "Quais os topicos mais cobrados em Direito Constitucional?", "Compare as abordagens de Portugues entre diferentes bancas", "Quais as principais diferencas entre provas de cargo administrativo vs tecnico?"],
    }
    index_path = METADADOS_DIR / "notebooklm_index.json"
    with open(index_path, "w", encoding="utf-8") as f: json.dump(index_data, f, indent=2, ensure_ascii=False)
    print(f"  JSON: {index_path}")
    print(f"\n=== CONCLUIDO ===\nTextos: {TEXTOS_DIR}\nMetadados: {METADADOS_DIR}")
    print(f"Instrucoes: 1. Va para https://notebooklm.google.com/  2. Abra caderno 'tcdf'  3. Adicione fontes de {TEXTOS_DIR}  4. Importe CSV {csv_path}")

if __name__ == "__main__":
    main()
