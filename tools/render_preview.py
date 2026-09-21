#!/usr/bin/env python3
"""Render README previews (SVG mock-ups of a VS Code window) from the theme's colours."""
import json, os, re, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DARK = dict(FG='#f8f8f2', K='#f92672', S='#e6db74', N='#ae81ff', F='#a7ec21', CL='#66d9ef', CM='#75715e', P='#f9faf4',
            PV='#00c0b0', PF='#98ffe0', PP='#e9ff65', PC='#ff0057', PI='#00ffa6',
            JL='#51f611', JG='#2293ff', JP='#00d7ff', JM='#f88908', JF='#fff21c', TI='#e30000')
import importlib.util
_bl = importlib.util.spec_from_file_location('bl', os.path.join(ROOT, 'tools', 'build_light.py'))
LIGHT_MAP = dict(re.findall(r"'(#[0-9a-f]{6})': '(#[0-9a-f]{6})'", open(_bl.origin).read()))
LIGHT = {k: LIGHT_MAP.get(v, v) for k, v in DARK.items()}

def t(text, color='FG', style=''):
    return (text, color, style)

PHP = [
    [t('<?php', 'K')],
    [],
    [t('namespace ', 'K'), t('App\\Service', 'FG'), t(';', 'K')],
    [],
    [t('/**', 'CM')],
    [t(' * Recalculates camera fees for the billing period.', 'CM')],
    [t(' */', 'CM')],
    [t('final class ', 'K'), t('FeeCalculator', 'CL', 'italic'), t(' implements ', 'K'), t('Calculator', 'PI', 'italic')],
    [t('{', 'P')],
    [t('    const ', 'K'), t('DEFAULT_RATE', 'PC'), t(' = ', 'K'), t('0.15', 'N'), t(';', 'K')],
    [],
    [t('    private ', 'K'), t('array', 'CL', 'italic'), t(' ', 'FG'), t('$cache', 'PV'), t(' = [];', 'K')],
    [],
    [t('    public function ', 'K'), t('calculate', 'F'), t('(', 'P'), t('Account', 'CL', 'italic'), t(' ', 'FG'), t('$account', 'PP'), t(', ', 'K'), t('int', 'CL', 'italic'), t(' ', 'FG'), t('$days', 'PP'), t('): ', 'K'), t('float', 'CL', 'italic')],
    [t('    {', 'P')],
    [t('        if ', 'K'), t('(', 'P'), t('isset', 'F'), t('(', 'P'), t('$this', 'PV'), t('->', 'K'), t('cache', 'PF'), t('[', 'P'), t('$account', 'PP'), t('->', 'K'), t('id', 'PF'), t(']', 'P'), t('))', 'P'), t(' {', 'P')],
    [t('            return ', 'K'), t('$this', 'PV'), t('->', 'K'), t('cache', 'PF'), t('[', 'P'), t('$account', 'PP'), t('->', 'K'), t('id', 'PF'), t('];', 'K')],
    [t('        }', 'P')],
    [],
    [t('        ', 'FG'), t('$rate', 'PV'), t(' = ', 'K'), t('$account', 'PP'), t('->', 'K'), t('rate', 'PF'), t(' ?? ', 'K'), t('self', 'K'), t('::', 'K'), t('DEFAULT_RATE', 'PC'), t(';', 'K')],
    [t('        ', 'FG'), t('$total', 'PV'), t(' = ', 'K'), t('round', 'F'), t('(', 'P'), t('$rate', 'PV'), t(' * ', 'K'), t('$days', 'PP'), t(', ', 'K'), t('2', 'N'), t(');', 'K')],
    [t('        ', 'FG'), t('$this', 'PV'), t('->', 'K'), t('log', 'F'), t('(', 'P'), t('"fee for {$account->id}: $total"', 'S'), t(');', 'K')],
    [],
    [t('        return ', 'K'), t('$this', 'PV'), t('->', 'K'), t('cache', 'PF'), t('[', 'P'), t('$account', 'PP'), t('->', 'K'), t('id', 'PF'), t('] = ', 'K'), t('$total', 'PV'), t(';', 'K')],
    [t('    }', 'P')],
    [t('}', 'P')],
]

TS = [
    [t('import ', 'K'), t('{ ', 'P'), t('EventEmitter', 'CL', 'italic'), t(' }', 'P'), t(' from ', 'K'), t("'events'", 'S'), t(';', 'K')],
    [],
    [t('// Device state pushed by the hub over websocket', 'CM')],
    [t('export interface ', 'K'), t('DeviceState', 'TI', 'italic'), t(' {', 'P')],
    [t('  id', 'FG'), t(': ', 'K'), t('string', 'CL', 'italic'), t(';', 'K')],
    [t('  armed', 'FG'), t(': ', 'K'), t('boolean', 'CL', 'italic'), t(';', 'K')],
    [t('  battery', 'FG'), t('?: ', 'K'), t('number', 'CL', 'italic'), t(';', 'K')],
    [t('}', 'P')],
    [],
    [t('const ', 'K'), t('RETRY_MS', 'JG', 'bold italic'), t(' = ', 'K'), t('5_000', 'N'), t(';', 'K')],
    [],
    [t('export function ', 'K'), t('connect', 'JF', 'italic'), t('(', 'P'), t('url', 'JP', 'underline'), t(': ', 'K'), t('string', 'CL', 'italic'), t(', ', 'K'), t('bus', 'JP', 'underline'), t(': ', 'K'), t('EventEmitter', 'CL', 'italic'), t(') {', 'P')],
    [t('  let ', 'K'), t('attempt', 'JL'), t(' = ', 'K'), t('0', 'N'), t(';', 'K')],
    [t('  const ', 'K'), t('socket', 'JL'), t(' = ', 'K'), t('new ', 'K'), t('WebSocket', 'CL', 'italic'), t('(', 'P'), t('url', 'JP', 'underline'), t(');', 'K')],
    [],
    [t('  socket', 'JL'), t('.', 'K'), t('onmessage', 'JM'), t(' = ', 'K'), t('(', 'P'), t('ev', 'JP', 'underline'), t(') => {', 'P')],
    [t('    const ', 'K'), t('state', 'JL'), t(': ', 'K'), t('DeviceState', 'TI', 'italic'), t(' = ', 'K'), t('JSON', 'CL', 'italic'), t('.', 'K'), t('parse', 'JM'), t('(', 'P'), t('ev', 'JP', 'underline'), t('.', 'K'), t('data', 'PF'), t(');', 'K')],
    [t('    bus', 'JP', 'underline'), t('.', 'K'), t('emit', 'JM'), t('(', 'P'), t('`device:${', 'S'), t('state', 'JL'), t('.', 'K'), t('id', 'PF'), t('}`', 'S'), t(', ', 'K'), t('state', 'JL'), t(');', 'K')],
    [t('  };', 'P')],
    [],
    [t('  socket', 'JL'), t('.', 'K'), t('onclose', 'JM'), t(' = ', 'K'), t('() => ', 'P'), t('setTimeout', 'JF', 'italic'), t('(', 'P'), t('() => ', 'P'), t('connect', 'JF', 'italic'), t('(', 'P'), t('url', 'JP', 'underline'), t(', ', 'K'), t('bus', 'JP', 'underline'), t('), ', 'P'), t('RETRY_MS', 'JG', 'bold italic'), t(' * ', 'K'), t('++', 'K'), t('attempt', 'JL'), t(');', 'K')],
    [t('}', 'P')],
]

FONT = "'JetBrains Mono','SF Mono',Menlo,Consolas,monospace"
CH, LH, FS = 8.4, 22, 14  # char width, line height, font size

def render(C, PAL, lines, filename, tree, out):
    FG, BG = C['editor.foreground'], C['editor.background']
    SIDE, ACT, BORDER, ACC = C['sideBar.background'], C['activityBar.background'], C['sideBar.border'], C['tab.activeBorderTop']
    DIM, LN = C['sideBar.foreground'], C['editorLineNumber.foreground']
    W, ACTW, SIDEW, TABH, STATH = 1080, 48, 210, 36, 24
    H = TABH + LH * (len(lines) + 1) + 20 + STATH
    EX = ACTW + SIDEW  # editor x
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}" font-size="{FS}">',
           f'<rect width="{W}" height="{H}" rx="10" fill="{BG}"/>',
           f'<rect width="{ACTW}" height="{H - STATH}" fill="{ACT}"/>',
           f'<rect x="{ACTW}" width="{SIDEW}" height="{H - STATH}" fill="{SIDE}"/>',
           f'<rect x="{ACTW + SIDEW}" width="1" height="{H - STATH}" fill="{BORDER}"/>']
    # activity bar icons
    for i, col in enumerate([FG, DIM, DIM, DIM, DIM]):
        y = 14 + i * 46
        svg.append(f'<rect x="14" y="{y}" width="20" height="20" rx="4" fill="none" stroke="{col}" stroke-width="1.8"/>')
    svg.append(f'<rect x="0" y="12" width="2" height="24" fill="{ACC}"/>')
    # sidebar tree
    svg.append(f'<text x="{ACTW + 14}" y="24" fill="{DIM}" font-size="11" letter-spacing="1">EXPLORER</text>')
    for i, (depth, name, active) in enumerate(tree):
        y = 52 + i * 22
        if active:
            svg.append(f'<rect x="{ACTW}" y="{y - 15}" width="{SIDEW}" height="22" fill="{C["list.activeSelectionBackground"]}"/>')
        svg.append(f'<text x="{ACTW + 14 + depth * 14}" y="{y}" fill="{FG if active else DIM}" font-size="13">{html.escape(name)}</text>')
    # tabs
    svg.append(f'<rect x="{EX}" width="{W - EX}" height="{TABH}" fill="{C["editorGroupHeader.tabsBackground"]}"/>')
    svg.append(f'<rect x="{EX}" y="{TABH - 1}" width="{W - EX}" height="1" fill="{BORDER}"/>')
    tabw = 12 + len(filename) * CH + 24
    svg.append(f'<rect x="{EX}" width="{tabw}" height="{TABH}" fill="{BG}"/>')
    svg.append(f'<rect x="{EX}" width="{tabw}" height="2" fill="{ACC}"/>')
    svg.append(f'<text x="{EX + 12}" y="23" fill="{FG}" font-size="13">{filename}</text>')
    svg.append(f'<text x="{EX + tabw + 12}" y="23" fill="{DIM}" font-size="13">README.md</text>')
    # code
    y0 = TABH + 16
    svg.append(f'<rect x="{EX}" y="{y0 + LH * 2 + 4}" width="{W - EX}" height="{LH}" fill="{C["editor.lineHighlightBackground"]}"/>')
    for i, line in enumerate(lines):
        y = y0 + LH * (i + 1)
        svg.append(f'<text x="{EX + 42}" y="{y}" fill="{LN}" text-anchor="end" font-size="12">{i + 1}</text>')
        x = EX + 60
        for text, color, style in line:
            attrs = f' fill="{PAL[color]}"'
            if 'bold' in style: attrs += ' font-weight="bold"'
            if 'italic' in style: attrs += ' font-style="italic"'
            if 'underline' in style: attrs += ' text-decoration="underline"'
            svg.append(f'<text x="{x:.1f}" y="{y}"{attrs} xml:space="preserve">{html.escape(text)}</text>')
            x += len(text) * CH
    # status bar
    svg.append(f'<rect y="{H - STATH}" width="{W}" height="{STATH}" fill="{C["statusBar.background"]}"/>')
    svg.append(f'<rect y="{H - STATH}" width="{W}" height="1" fill="{BORDER}"/>')
    svg.append(f'<text x="14" y="{H - 8}" fill="{DIM}" font-size="11">⎇ develop   ✓ 0  ⚠ 0</text>')
    svg.append(f'<text x="{W - 14}" y="{H - 8}" fill="{DIM}" font-size="11" text-anchor="end">Ln 12, Col 18   UTF-8   {filename.split(".")[-1].upper()}   Monokai Navy</text>')
    svg.append('</svg>')
    open(os.path.join(ROOT, 'assets', out), 'w').write('\n'.join(svg))

PHP_TREE = [(0, '▾ pulse', False), (1, '▾ src', False), (2, '▾ Service', False), (3, 'FeeCalculator.php', True), (3, 'Calculator.php', False), (2, '▸ Http', False), (1, '▸ tests', False), (1, 'composer.json', False)]
TS_TREE = [(0, '▾ garm-hub-web', False), (1, '▾ src', False), (2, 'socket.ts', True), (2, 'state.ts', False), (2, 'main.ts', False), (1, '▸ public', False), (1, 'package.json', False), (1, 'tsconfig.json', False)]
VARIANTS = json.load(open(os.path.join(ROOT, 'tools', 'variants.json')))   # dark workbench variants
JOBS = [('' if vid == 'blue' else '-' + vid, DARK, v['file']) for vid, v in VARIANTS.items() if not vid.startswith('$')]
JOBS.append(('-light', LIGHT, 'monokai-navy-light-color-theme.json'))
for suffix, PAL, fn in JOBS:
    C = json.load(open(os.path.join(ROOT, 'themes', fn)))['colors']
    render(C, PAL, PHP, 'FeeCalculator.php', PHP_TREE, f'preview-php{suffix}.svg')
    render(C, PAL, TS, 'socket.ts', TS_TREE, f'preview-ts{suffix}.svg')

# palette strip (dark)
C = json.load(open(os.path.join(ROOT, 'themes', 'monokai-navy-color-theme.json')))['colors']
BG, SIDE, ACT, BORDER, FG = C['editor.background'], C['sideBar.background'], C['activityBar.background'], C['sideBar.border'], C['editor.foreground']
CM, K, S, N, F, CL, PV, PF, PP, PC, PI = (DARK[k] for k in 'CM K S N F CL PV PF PP PC PI'.split())
sw = [('bg', BG), ('sidebar', SIDE), ('chrome', ACT), ('border', BORDER), ('fg', FG), ('comment', CM), ('keyword', K), ('string', S),
      ('number', N), ('function', F), ('class', CL), ('php $var', PV), ('php field', PF), ('php param', PP), ('php const', PC), ('php iface', PI)]
n = len(sw); cw = 60; W, H = cw * n, 74
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}" font-size="9">']
for i, (name, col) in enumerate(sw):
    x = i * cw
    svg.append(f'<rect x="{x}" width="{cw}" height="46" fill="{col}"/>')
    svg.append(f'<text x="{x + cw / 2}" y="58" fill="#c9d1da" text-anchor="middle">{html.escape(name)}</text>')
    svg.append(f'<text x="{x + cw / 2}" y="69" fill="#8a97a8" text-anchor="middle">{col}</text>')
svg.append('</svg>')
open(os.path.join(ROOT, 'assets', 'palette.svg'), 'w').write('\n'.join(svg))

# Marketplace (vsce) rejects SVG images in README -> rasterise to PNG at 2x (needs rsvg-convert: brew install librsvg)
import shutil, subprocess
if shutil.which('rsvg-convert'):
    for f in sorted(os.listdir(os.path.join(ROOT, 'assets'))):
        if f.endswith('.svg'):
            src = os.path.join(ROOT, 'assets', f)
            subprocess.run(['rsvg-convert', '-z', '2', '-o', src[:-4] + '.png', src], check=True)
    print('ok (svg + png)')
else:
    print('ok (svg only; install librsvg for png)')
