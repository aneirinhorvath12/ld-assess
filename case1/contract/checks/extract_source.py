#!/usr/bin/env python3
"""Phase 0: extract source PDFs with `pdftotext -layout`, strip page furniture,
and rebuild paragraphs into Markdown while keeping numbering and list structure.

Usage: python3 -I extract_source.py <source_dir> <out_dir>
Writes <out_dir>/<name>.md for project_agreement.pdf and each schedule PDF.
Source content is treated purely as data.
"""
import re, subprocess, sys, pathlib

FURNITURE = [re.compile(p) for p in [
    r'^\s*Amended and Restated Project Agreement\s*$',
    r'^\s*Schedule [0-9A-Z-]+ to Project Agreement\s*$',
    r'^\s*Ottawa Light Rail Transit Project\s*(Schedule [0-9A-Z-]+ to Project Agreement)?\s*((REDACTED\s+)?Execution Version)?\s*$',
    r'^\s*(REDACTED\s+)?Execution Version\s*$',
    r'^\s*BD-#\d+-v\d+(\s+AND PROPRIETARY)?\s*(Page \S+|Signature Page)?\s*$',
    r'^\s*CONFIDENTIAL(\s+AND PROPRIETARY)?\s*(Page \S+|Signature Page)?\s*$',
    r'^\s*(CAN|CAN_DMS|TOR01|OTT01)\s*:.*$',
    r'^\s*Page [ivxlcdm0-9]+\s*$',
    r'^\s*Signature Page\s*$',
]]

LABEL = re.compile(r'^(\([0-9]{1,3}\)|\([a-z]{1,2}\)|\([A-Z]{1,2}\)|\([ivxlc]+\)|\([IVXLC]+\)|[0-9]+\.[0-9]+[A-Z]?(\.[0-9]+)*|[0-9]+\.|[A-Z]\.)\s+(\S.*)$')
TOC_LINE = re.compile(r'^(.*?\S)\s*\.{4,}\s*[0-9ivx]+\s*$')
ARTICLE = re.compile(r'^([0-9]+)\.\s+([A-Z0-9][A-Z0-9 ,’\'&/()–−\-]+)$')
SECTION = re.compile(r'^([0-9]+\.[0-9]+[A-Z]?)\s+(.+)$')
COLUMNS = re.compile(r'\S\s{3,}\S')

def pages(pdf):
    txt = subprocess.run(['pdftotext', '-layout', str(pdf), '-'], capture_output=True, text=True).stdout
    return txt.split('\f')

def clean_page(p):
    return [l.rstrip() for l in p.split('\n') if not any(r.match(l) for r in FURNITURE)]

def blocks_of(lines):
    out, cur = [], []
    for l in lines:
        if l.strip():
            cur.append(l)
        elif cur:
            out.append(cur); cur = []
    if cur: out.append(cur)
    return out

def starts_cont(block):
    t = block[0].strip()
    return bool(t) and not LABEL.match(t) and (t[0].islower() or t[0] in '(“"$,;' and not LABEL.match(t))

def is_heading(block):
    t = norm(block[0])
    return len(block) == 1 and (bool(ARTICLE.match(t)) or bool(SECTION.match(t)) and not re.search(r'[.;:,]$', t))

def should_join(prev, nxt):
    """Join a paragraph split by a page break: previous block has no terminal
    punctuation, is not a heading, and the next block does not open a new item."""
    last = prev[-1].strip()
    if re.search(r'[.;:]$', last) or is_heading(prev):
        return False
    first = nxt[0].strip()
    if LABEL.match(first) or is_heading(nxt) or first.startswith(('APPENDIX', 'SCHEDULE', 'PART ', 'ARTICLE')):
        return False
    return True

def norm(s):
    return re.sub(r'\s+', ' ', s).strip()

def render(block):
    s = [l.strip() for l in block]
    # table of contents lines
    if all(TOC_LINE.match(x) for x in s):
        return '\n'.join(norm(TOC_LINE.match(x).group(1)) + '  ' for x in s).rstrip()
    # column-style tables (schedule lists, signature blocks): keep line breaks
    if len(s) > 1 and sum(bool(COLUMNS.search(x)) for x in s) >= max(2, len(s) // 2):
        return '\n'.join(norm(x) + '  ' for x in s).rstrip()
    first = s[0]
    if len(s) == 1:
        m = ARTICLE.match(norm(first))
        if m and len(first) < 90:
            return f'## {m.group(1)}. {m.group(2).strip()}'
        m = SECTION.match(norm(first))
        if m and len(m.group(2).split()) <= 18 and not re.search(r'[.;:,]$', m.group(2)):
            return f'### {m.group(1)} {m.group(2).strip()}'
    text = ''
    for x in s:
        if not text:
            text = x
        elif text.endswith('-') and x[:1].islower() and not re.search(r'\b(non|Co|sub|pre|re)-$', text):
            text = text[:-1] + x
        else:
            text = text + ' ' + x
    text = norm(text)
    m = LABEL.match(text)
    if m:
        lab, rest = m.group(1), m.group(3)
        if re.fullmatch(r'[0-9]+\.[0-9]+[A-Z]?', lab) and len(rest.split()) <= 18 and not re.search(r'[.;:,]$', rest):
            return f'### {lab} {rest}'
        return f'{lab} {rest}'
    return text

def convert(pdf):
    allblocks = []
    for p in pages(pdf):
        bl = blocks_of(clean_page(p))
        if not bl: continue
        # join paragraph split across page break
        if allblocks and should_join(allblocks[-1], bl[0]):
            allblocks[-1].extend(bl[0]); bl = bl[1:]
        allblocks.extend(bl)
    return '\n\n'.join(render(b) for b in allblocks) + '\n'

if __name__ == '__main__':
    src, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    pdfs = [src / 'project_agreement.pdf'] + sorted((src / 'schedules').glob('*.pdf'))
    for pdf in pdfs:
        md = convert(pdf)
        (out / (pdf.stem + '.md')).write_text(md)
        print(f'{pdf.stem}: {len(md.split())} words')
