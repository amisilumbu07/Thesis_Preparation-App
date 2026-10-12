import re, json
raw = open('thesis/thesis.txt', encoding='utf-8').read()
clean = raw.replace('​', ' ').replace('­', '').replace('﻿', '')
lines = clean.split('\n')

# TOC: number -> title
toc = {}
for l in lines[180:250]:
    m = re.match(r'^\s*(\d+(?:\.\d+){1,3})\s+(.+?)\.{3,}\s*\d+\s*$', l)
    if m: toc[m.group(1)] = m.group(2).strip()

start = next(i for i, l in enumerate(lines) if l.strip() == 'Chapter One' and i > 250)
end = next(i for i, l in enumerate(lines) if l.strip() == 'References' and i > 2000)
body = lines[start:end]

def is_noise(l):
    s = l.strip()
    return s == '' and False

# sub-sections present in the body but not in the TOC
for i, l in enumerate(body):
    m = re.match(r'^\s*(\d+\.\d+\.\d+)\s+([A-Z].*)$', l)
    if m and m.group(1) not in toc and '.'.join(m.group(1).split('.')[:2]) in toc and len(l.strip()) < 110:
        t = m.group(2).strip()
        toc.setdefault(m.group(1), t)
order = sorted(toc, key=lambda n: [int(x) for x in n.split('.')])
pos = {}
cur = 0
for n in order:
    pat = re.compile(r'^\s*' + re.escape(n) + r'\.?\s+\S')
    for i in range(cur, len(body)):
        if pat.match(body[i]):
            pos[n] = i; cur = i + 1; break
missing = [n for n in order if n not in pos]

secs = {}
nums = [n for n in order if n in pos]
for k, n in enumerate(nums):
    a = pos[n]; b = pos[nums[k+1]] if k+1 < len(nums) else len(body)
    chunk = body[a+1:b]
    txt = []
    for l in chunk:
        if l.startswith('\f'): l = l.lstrip('\f')
        if re.fullmatch(r'\s*\d{1,3}\s*', l): continue  # page numbers
        txt.append(l.rstrip())
    text = '\n'.join(txt)
    text = re.split(r'\n\s*Chapter\s+(?:One|Two|Three|Four|Five)\s*\n', text)[0]
    text = re.sub(r'\n{3,}', '\n\n', text).strip()
    secs[n] = {'heading': toc[n], 'text': text}
json.dump(secs, open('thesis/sections.json', 'w'), ensure_ascii=False, indent=1)
print('toc', len(toc), 'found', len(secs), 'missing', missing)
for n in nums: print(n, len(secs[n]['text']), toc[n][:60])
