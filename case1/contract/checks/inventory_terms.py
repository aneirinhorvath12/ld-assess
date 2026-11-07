#!/usr/bin/env python3
"""Phase 0 inventory of capitalised defined terms used in the body.

For each term used in the operative body, record where it is defined:
Schedule 1 (directly, or by pointer to a body Section / other Schedule),
inline in the body, inline in another supplied schedule, or nowhere.
Also lists capitalised multi-word phrases in the body that match no definition.
Usage: python3 -I inventory_terms.py <source_clean_dir> <out_dir>
"""
import re, sys, pathlib, collections, json

src, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
HY = str.maketrans({'\u2011': '-', '\u2010': '-', '\u00ad': ''})
pa = (src / 'project_agreement.md').read_text().translate(HY)
body = pa[pa.index('THIS PROJECT AGREEMENT is made'):pa.index('IN WITNESS WHEREOF')]
s1 = (src / 's01_definitions.md').read_text().translate(HY)
app8 = s1.index('APPENDIX 8') if 'APPENDIX 8' in s1 else len(s1)
s1_main, s1_app8 = s1[:app8], s1[app8:]

Q = r'“([^”]{1,120})”'
defs = {}   # term -> (where, detail)

def add(term, where, detail=''):
    term = term.strip().strip(',')
    if term and term not in defs:
        defs[term] = (where, detail)

# Schedule 1 numbered entries
for m in re.finditer(r'^([0-9]+\.[0-9]+)\s+(.*)$', s1_main, re.M):
    num, rest = m.groups()
    terms = re.findall(Q, rest.split(' means')[0].split(' has the meaning')[0].split(' shall mean')[0])
    if not terms: continue
    pm = re.search(r'has the meaning (?:given|set out|ascribed)[^.]*?(?:in|to it in) ((?:Section|Article|Schedule|Part|Appendix)[^.;]*)', rest)
    for tm in terms:
        add(tm, 'Schedule 1 §' + num + (' → ' + pm.group(1).strip() if pm else ''), 'pointer' if pm else 'direct')
        if ' or ' in tm:
            for alt in tm.split(' or '): add(alt, 'Schedule 1 §' + num, 'alias')

# inline definitions in body:  (the “X”) / (“X”) / “X” means
for m in re.finditer(r'\((?:each, |each a |each an |collectively, |collectively the |the |a |an )?' + Q, body):
    add(m.group(1), 'body (inline)', '')
for m in re.finditer(Q + r' (?:means|shall mean|has the meaning)', body):
    add(m.group(1), 'body (inline)', '')

# other supplied schedules
for f in sorted(src.glob('s*.md')):
    if f.name.startswith('s01'): continue
    txt = f.read_text().translate(HY)
    tag = 'Schedule ' + f.stem.split('_')[0][1:].lstrip('0')
    for m in re.finditer(r'(?:^|\()(?:[0-9.]+\s+)?(?:the |each, |each a )?' + Q + r'(?:\)| means| shall mean| has the meaning)', txt, re.M):
        add(m.group(1), tag + ' (inline)', '')
    if f.stem.startswith('s15-1'):
        for m in re.finditer(r'^([A-Z][A-Za-z0-9’\'&/,\- ]{1,80}?) (?:means|has the meaning)', txt, re.M):
            add(m.group(1), tag, 'unquoted')

app8_terms = set(re.findall(r'^[0-9]+\.[0-9]+\s+' + Q, s1_app8, re.M))

# usage counts in body (longest terms first, masking matches)
masked = body
used = collections.Counter()
for term in sorted(defs, key=len, reverse=True):
    if not re.match(r'[A-Z0-9]', term): continue
    stem = re.escape(term[:-1]) + r's?' if term.endswith('s') and not term.endswith('ss') else re.escape(term)
    pat = re.compile(r'(?<![A-Za-z0-9])' + stem + r'(?:’s|\'s|s|es)?(?![A-Za-z0-9])')
    n = len(pat.findall(masked))
    if n:
        used[term] = n
        masked = pat.sub('▮', masked)

# capitalised phrases not covered by any definition
STOP = {'The','This','Such','If','In','Any','Each','No','For','All','Where','Subject','Without','Notwithstanding',
        'Upon','On','Unless','Except','To','Following','Within','Nothing','Provided','Prior','After','Where','Neither',
        'Further','Save','During','When','With','From','At','Should','Until','Pursuant','Both','Once','Where','It','A','An'}
masked = re.sub(r'^#{2,3} .*$', '', masked, flags=re.M)
masked = re.sub(r'(Schedules? [0-9]{1,2}(?:-[0-9])?\s*[−–-]\s*)((?:[A-Z][A-Za-z’\'\-]*|and|of|on|for|the|to|in)(?:\s+(?:[A-Z][A-Za-z’\'\-]*|and|of|on|for|the|to|in))*)', r'\1▮', masked)
cand = collections.Counter()
for m in re.finditer(r'(?<![.:;]\s)(?<!^)\b([A-Z][A-Za-z’\'\-]+(?:\s+(?:of|and|for|the|to|on|in|de|du|des|la|le|&)?\s*[A-Z][A-Za-z’\'\-]+)*)', masked, re.M):
    ph = m.group(1).strip()
    if ph.split()[0] in STOP or ph.isupper() and len(ph) > 25: continue
    if re.fullmatch(r'(Section|Sections|Article|Schedule|Schedules|Part|Appendix|Notice|Party|Parties)', ph): continue
    cand[ph] += 1

rows = []
for term, n in sorted(used.items(), key=lambda x: x[0].lower()):
    w, d = defs[term]
    rows.append({'term': term, 'uses': n, 'defined': w, 'kind': d, 'original_in_app8': term in app8_terms})
(out / 'defined_terms_used.json').write_text(json.dumps(rows, indent=1, ensure_ascii=False))
with open(out / 'defined_terms_used.md', 'w') as f:
    f.write('| Term | Uses in body | Defined at | App. 8 original |\n|---|---:|---|---|\n')
    for r in rows:
        f.write(f"| {r['term']} | {r['uses']} | {r['defined']} | {'yes' if r['original_in_app8'] else ''} |\n")
with open(out / 'undefined_capitalised.md', 'w') as f:
    f.write('| Phrase | Uses |\n|---|---:|\n')
    for ph, n in cand.most_common():
        f.write(f'| {ph} | {n} |\n')
by = collections.Counter(r['defined'].split(' §')[0].split(' →')[0] for r in rows)
print('definitions harvested:', len(defs), '| Schedule 1 entries:', sum(1 for v in defs.values() if v[0].startswith('Schedule 1')))
print('distinct defined terms used in body:', len(rows), dict(by))
print('S1 pointer defs used in body:', sum(1 for r in rows if r['kind']=='pointer'))
print('App 8 original terms:', len(app8_terms), '| used in body:', sum(r['original_in_app8'] for r in rows))
print('undefined capitalised phrase types:', len(cand), '| with >=3 uses:', sum(1 for v in cand.values() if v >= 3))
