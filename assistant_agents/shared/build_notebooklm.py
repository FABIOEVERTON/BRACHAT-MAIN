#!/usr/bin/env python3
"""Build NotebookLM-ready markdown volumes from all SKILL.md files."""
import os, re, json
from pathlib import Path

SKILLS_DIR = Path(__file__).parent / "general_skills"
OUT_DIR = Path(__file__).parent / "notebooklm"
OUT_DIR.mkdir(exist_ok=True)

def parse_frontmatter(text):
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n', text, re.DOTALL)
    if not m:
        return {}, text
    fm = {}
    for line in m.group(1).split('\n'):
        if ':' in line:
            k, v = line.split(':', 1)
            fm[k.strip()] = v.strip().strip('"\'')
    return fm, text[m.end():]

def extract_skills():
    skills = []
    for sk_path in sorted(SKILLS_DIR.rglob("*")):
        if not sk_path.is_dir():
            continue
        sk_file = sk_path / "SKILL.md"
        if not sk_file.exists():
            continue
        text = sk_file.read_text(encoding='utf-8', errors='replace')
        fm, body = parse_frontmatter(text)
        name = fm.get('name', sk_path.name)
        desc = fm.get('description', '')
        cat = fm.get('category', 'uncategorized')
        skills.append({
            'name': name,
            'dir': sk_path.name,
            'desc': desc,
            'category': cat,
            'body_len': len(body),
            'body': body,
            'frontmatter': fm,
        })
    return skills

def categorize(skill):
    cat = skill['category']
    domain_map = {
        'development': 'eng-dev',
        'frontend': 'eng-dev',
        'framework': 'eng-dev',
        'devops': 'eng-dev',
        'testing': 'eng-dev',
        'data': 'eng-dev',
        'data-ai': 'eng-dev',
        'design': 'design-creative',
        'content': 'design-creative',
        'writing': 'design-creative',
        'marketing': 'business-growth',
        'growth': 'business-growth',
        'productivity': 'business-growth',
        'planning': 'business-growth',
        'security': 'security-infra',
        'andruia': 'andruia',
        'meta': 'system-core',
        'granular-workflow-bundle': 'workflow',
        'workflow-bundle': 'workflow',
    }
    return domain_map.get(cat, 'other')

def main():
    skills = extract_skills()
    print(f"Found {len(skills)} skills")

    domain_skills = {}
    for s in skills:
        dom = categorize(s)
        domain_skills.setdefault(dom, []).append(s)

    # 1. Master Index
    idx_lines = ["# BRACHÁT Skill Library — Master Index", "",
                 f"Total: {len(skills)} skills", "---", ""]
    for dom, items in sorted(domain_skills.items()):
        idx_lines.append(f"## {dom.upper()} ({len(items)} skills)")
        idx_lines.append("")
        for s in items:
            idx_lines.append(f"- **{s['name']}** — {s['desc']}")
        idx_lines.append("")
    (OUT_DIR / "00-MASTER-INDEX.md").write_text("\n".join(idx_lines), encoding='utf-8')
    print(f"Master index: {len(idx_lines)} lines")

    # 2. Thematic Volumes (full content)
    vol_names = {
        'eng-dev': 'Engineering & Development',
        'design-creative': 'Design & Creative',
        'business-growth': 'Business & Growth',
        'security-infra': 'Security & Infrastructure',
        'andruia': 'Andruia Framework',
        'system-core': 'System & Core',
        'workflow': 'Workflow Automation',
        'other': 'Other Specialized Skills',
    }

    def write_volume(fname, vname, items):
        lines = [f"# {vname}", f"## {len(items)} skills", "---", ""]
        for s in items:
            lines.append(f"## {s['name']}")
            if s['desc']:
                lines.append(f"*{s['desc']}*")
            lines.append("")
            fm = s['frontmatter']
            if fm.get('tags'):
                lines.append(f"Tags: {fm.get('tags')}")
            if fm.get('tools'):
                lines.append(f"Tools: {fm.get('tools')}")
            if fm.get('risk'):
                lines.append(f"Risk: {fm.get('risk')}")
            lines.append("")
            body = s['body'].strip()
            lines.append(body)
            lines.append("")
            lines.append("---")
            lines.append("")
        (OUT_DIR / fname).write_text("\n".join(lines), encoding='utf-8')
        print(f"Volume {fname}: {len(lines)} lines for {len(items)} skills")
        return len(lines)

    vol_counts = {}
    for dom, items in sorted(domain_skills.items()):
        if dom == 'other':
            alpha_groups = {
                'A-F': lambda s: s['name'][0].upper() <= 'F',
                'G-L': lambda s: 'G' <= s['name'][0].upper() <= 'L',
                'M-S': lambda s: 'M' <= s['name'][0].upper() <= 'S',
                'T-Z': lambda s: s['name'][0].upper() >= 'T',
            }
            for suffix, filt in alpha_groups.items():
                sub = [s for s in items if filt(s)]
                if sub:
                    vname = f"Other Skills ({suffix})"
                    fname = f"01-OTHER-{suffix}.md"
                    vol_counts[f"other-{suffix}"] = write_volume(fname, vname, sub)
        else:
            vname = vol_names.get(dom, dom)
            fname = f"01-{dom.upper()}.md"
            vol_counts[dom] = write_volume(fname, vname, items)

    # Stats
    total_lines = sum(vol_counts.values())
    print(f"\nDone! {len(skills)} skills across {len(domain_skills)} domains")
    print(f"Files in {OUT_DIR}/")
    for f in sorted(OUT_DIR.iterdir()):
        size = f.stat().st_size
        print(f"  {f.name}: {size/1024:.0f}KB")

if __name__ == "__main__":
    main()
