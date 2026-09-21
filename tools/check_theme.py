#!/usr/bin/env python3
"""Lint the theme: duplicate TextMate scopes, low-contrast token colours, olive leftovers."""
import json, os, re, sys
from collections import Counter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import glob
OLIVE = re.compile(r'^#(41433|27282|38383|49483|46474|76777|20212|18171|02020|00005|1e1f1c|34352f|3e3d32|90908a|ccccc7)', re.I)

def lum(h):
    h = h.lstrip('#')[:6]; r, g, b = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)
def contrast(a, b):
    x, y = sorted((lum(a), lum(b)), reverse=True); return (x + 0.05) / (y + 0.05)

def check(path):
    T = json.load(open(path)); BG = T['colors']['editor.background']
    bad = 0
    cnt = Counter()
    for r in T['tokenColors']:
        sc = r.get('scope')
        for x in ([sc] if isinstance(sc, str) else (sc or [])):
            cnt[x.strip()] += 1
    for k, v in cnt.items():
        if v > 1: print('DUP scope:', k); bad += 1

    seen = set()
    for r in T['tokenColors']:
        c = r['settings'].get('foreground')
        if c and c.lower() not in seen:
            seen.add(c.lower())
            if contrast(c, BG) < 3.0: print(f'LOW contrast {c} {contrast(c, BG):.1f}:1  {r.get("name") or r.get("scope")}'); bad += 1
    for k, v in T['semanticTokenColors'].items():
        c = v.get('foreground')
        if c and contrast(c, BG) < 3.0: print(f'LOW contrast {c} {contrast(c, BG):.1f}:1  semantic {k}'); bad += 1

    for k, v in T['colors'].items():
        if OLIVE.match(v): print('OLIVE leftover:', k, v); bad += 1
    for k in ('editorIndentGuide.background', 'editorIndentGuide.activeBackground'):
        if k in T['colors']: print('DEPRECATED key:', k); bad += 1

    print(os.path.basename(path), '|', 'colors', len(T['colors']), '| tokenColors', len(T['tokenColors']), '| semantic', len(T['semanticTokenColors']), '|', 'OK' if not bad else f'{bad} issue(s)')
    return bad
total = sum(check(p) for p in sorted(glob.glob(os.path.join(ROOT, 'themes', '*.json'))))
sys.exit(1 if total else 0)
