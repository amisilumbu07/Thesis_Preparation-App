import sys, os, json, importlib, traceback
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'content'))
import content_lib as L
mods = sys.argv[1:] or ['p_ab', 'p_c', 'p_d', 'p_e', 'p_f', 'p_reg']
for m in mods:
    if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'content', m + '.py')):
        importlib.import_module(m)
out = os.path.join(L.ROOT, 'content')
src = L.build_sources()
json.dump(src, open(os.path.join(out, 'sources.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(L.CONCEPTS, open(os.path.join(out, 'concepts.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(L.CARDS, open(os.path.join(out, 'cards.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(L.REGISTER, open(os.path.join(out, 'register.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(src), 'sources,', len(L.CONCEPTS), 'concepts,', len(L.CARDS), 'cards,', len(L.REGISTER), 'register')
