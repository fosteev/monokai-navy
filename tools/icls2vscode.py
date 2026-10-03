#!/usr/bin/env python3
"""Convert a JetBrains .icls scheme into a VS Code color-theme extension.
Layers, later wins: VS Code built-in Monokai (chrome + TextMate fallback)
  -> values from the .icls  -> tools/navy.json (hand-made navy workbench + fixes).
Usage: icls2vscode.py SCHEME.icls BUILTIN_MONOKAI.json OUT_DIR [navy.json]"""
import json, os, re, sys, xml.etree.ElementTree as ET

ICLS, BASE, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
NAVY = sys.argv[4] if len(sys.argv) > 4 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'navy.json')
root = ET.parse(ICLS).getroot()

def hexc(v):  # JetBrains strips leading zeros: '55' -> '#000055'; '0' / '' mean "inherit"
    v = (v or '').strip()
    if not v or v == '0':
        return None
    return '#' + v.zfill(6).lower()

colors = {o.get('name'): hexc(o.get('value')) for o in root.find('colors')}
attrs = {}
for o in root.find('attributes'):
    v = o.find('value')
    if v is None:
        continue
    attrs[o.get('name')] = {x.get('name'): x.get('value') for x in v}

def style(name):
    # name may be a tuple: first attribute that defines a foreground wins
    names = name if isinstance(name, tuple) else (name,)
    a = next((attrs[n] for n in names if hexc(attrs.get(n, {}).get('FOREGROUND'))), attrs.get(names[0], {}))
    s = {}
    if hexc(a.get('FOREGROUND')): s['foreground'] = hexc(a['FOREGROUND'])
    ft = int(a.get('FONT_TYPE', 0)); fs = []
    if ft & 1: fs.append('bold')
    if ft & 2: fs.append('italic')
    if a.get('EFFECT_TYPE') == '1': fs.append('underline')
    if fs: s['fontStyle'] = ' '.join(fs)
    return s

# JetBrains attribute -> TextMate scopes
TM = [
    ('DEFAULT_LINE_COMMENT', 'Comment', ['comment', 'punctuation.definition.comment']),
    ('DEFAULT_DOC_COMMENT', 'Doc comment', ['comment.block.documentation']),
    ('DEFAULT_DOC_COMMENT_TAG', 'Doc tag', ['keyword.other.phpdoc', 'storage.type.class.jsdoc', 'punctuation.definition.block.tag.jsdoc']),
    ('DOC_COMMENT_TAG_VALUE', 'Doc tag value', ['comment.block.documentation variable', 'comment.block.documentation entity.name.type']),
    ('DEFAULT_KEYWORD', 'Keyword', ['keyword', 'storage', 'storage.type', 'storage.modifier', 'keyword.control', 'keyword.other']),
    ('DEFAULT_OPERATION_SIGN', 'Operator', ['keyword.operator']),
    ('DEFAULT_COMMA', 'Comma', ['punctuation.separator.delimiter', 'punctuation.separator.comma']),
    ('DEFAULT_DOT', 'Dot / arrow', ['keyword.operator.class', 'keyword.operator.accessor', 'punctuation.accessor']),
    ('DEFAULT_SEMICOLON', 'Semicolon', ['punctuation.terminator']),
    ('DEFAULT_BRACES', 'Braces', ['punctuation.section.scope', 'punctuation.definition.block', 'meta.brace.curly', 'punctuation.section.block']),
    ('DEFAULT_BRACKETS', 'Brackets', ['punctuation.section.array', 'meta.brace.square', 'punctuation.definition.array']),
    ('DEFAULT_PARENTHS', 'Parens', ['punctuation.definition.parameters', 'punctuation.definition.arguments', 'meta.brace.round', 'punctuation.definition.begin.bracket.round', 'punctuation.definition.end.bracket.round']),
    ('DEFAULT_STRING', 'String', ['string', 'punctuation.definition.string']),
    ('DEFAULT_VALID_STRING_ESCAPE', 'String escape', ['constant.character.escape']),
    ('DEFAULT_INVALID_STRING_ESCAPE', 'Bad escape', ['invalid.illegal.character.escape']),
    ('DEFAULT_NUMBER', 'Number', ['constant.numeric']),
    ('DEFAULT_CONSTANT', 'Constant', ['constant.language', 'constant.other', 'support.constant', 'variable.other.constant']),
    ('DEFAULT_PREDEFINED_SYMBOL', 'Predefined symbol', ['support.variable', 'variable.language']),
    ('DEFAULT_FUNCTION_CALL', 'Function call', ['entity.name.function', 'support.function', 'meta.function-call entity.name.function', 'variable.function']),
    ('DEFAULT_FUNCTION_DECLARATION', 'Function decl', ['meta.function entity.name.function']),
    ('DEFAULT_CLASS_NAME', 'Class', ['entity.name.type', 'entity.name.class', 'support.class', 'entity.other.inherited-class', 'entity.name.type.class', 'support.type']),
    (('DEFAULT_INTERFACE_NAME', 'INTERFACE_NAME_ATTRIBUTES'), 'Interface', ['entity.name.type.interface']),
    ('DEFAULT_PARAMETER', 'Parameter', ['variable.parameter']),
    ('DEFAULT_LOCAL_VARIABLE', 'Variable', ['variable', 'variable.other', 'variable.other.readwrite']),
    ('DEFAULT_INSTANCE_FIELD', 'Field', ['variable.other.property', 'variable.other.object.property']),
    ('DEFAULT_TAG', 'Tag', ['entity.name.tag', 'punctuation.definition.tag']),
    ('DEFAULT_ATTRIBUTE', 'Attribute', ['entity.other.attribute-name']),
    ('DEFAULT_ENTITY', 'HTML entity', ['constant.character.entity']),
    ('ANNOTATION_NAME_ATTRIBUTES', 'Annotation / decorator', ['meta.decorator', 'punctuation.decorator', 'meta.attribute.php', 'support.attribute']),
    ('DEFAULT_METADATA', 'Metadata', ['meta.tag.metadata']),
    ('DEFAULT_LABEL', 'Label', ['entity.name.label']),
    ('BAD_CHARACTER', 'Invalid', ['invalid.illegal']),
    ('DEPRECATED_ATTRIBUTES', 'Deprecated', ['invalid.deprecated']),
    ('TODO_DEFAULT_ATTRIBUTES', 'TODO', ['comment keyword.codetag']),
    # PHP
    ('PHP_VAR', 'PHP variable', ['variable.other.php', 'punctuation.definition.variable.php', 'variable.language.this.php']),
    ('PHP_PARAMETER', 'PHP parameter', ['meta.function.parameters.php variable.other.php']),
    ('PHP_INSTANCE_FIELD', 'PHP field', ['variable.other.property.php']),
    ('PHP_CONSTANT', 'PHP constant', ['constant.other.php', 'support.constant.core.php', 'support.constant.ext.php', 'support.constant.std.php', 'constant.other.class.php', 'constant.language.php']),
    ('PHP_INTERFACE', 'PHP interface', ['entity.name.type.interface.php', 'meta.interface.php entity.name.type']),
    # JS / TS (TextMate fallback; semantic tokens below are more precise)
    ('JS.LOCAL_VARIABLE', 'JS variable', ['variable.other.readwrite.js', 'variable.other.readwrite.ts', 'variable.other.readwrite.tsx']),
    ('JS.PARAMETER', 'JS parameter', ['variable.parameter.js', 'variable.parameter.ts', 'variable.parameter.tsx']),
    ('JS.GLOBAL_FUNCTION', 'JS function', ['entity.name.function.js', 'entity.name.function.ts', 'support.function.js']),
    ('JS.INSTANCE_MEMBER_FUNCTION', 'JS method', ['meta.method.declaration entity.name.function.js', 'meta.method.declaration entity.name.function.ts', 'support.function.dom', 'meta.function-call.js support.function']),
    ('JS.INTERFACE', 'JS interface', ['entity.name.type.interface.js']),
    ('TS.INTERFACE', 'TS interface', ['entity.name.type.interface.ts', 'entity.name.type.interface.tsx']),
    # CSS
    ('CSS.PROPERTY_NAME', 'CSS property', ['support.type.property-name.css', 'support.type.property-name.scss', 'meta.property-name.css']),
    ('CSS.SEMICOLON', 'CSS semicolon', ['punctuation.terminator.rule.css', 'punctuation.terminator.rule.scss']),
]

token_colors = []
for key, name, scopes in TM:
    s = style(key)
    if s:
        token_colors.append({'name': name, 'scope': scopes, 'settings': s})

# Semantic tokens (TS server / any LSP that provides them)
SEM = {
    'variable': 'DEFAULT_LOCAL_VARIABLE', 'parameter': 'DEFAULT_PARAMETER',
    'property': 'DEFAULT_INSTANCE_FIELD', 'function': 'DEFAULT_FUNCTION_CALL',
    'method': 'DEFAULT_INSTANCE_METHOD', 'class': 'DEFAULT_CLASS_NAME',
    'interface': ('DEFAULT_INTERFACE_NAME', 'INTERFACE_NAME_ATTRIBUTES'), 'enum': 'ENUM_NAME_ATTRIBUTES',
    'typeParameter': 'TYPE_PARAMETER_NAME_ATTRIBUTES',
    'variable.readonly': 'DEFAULT_CONSTANT', 'property.static': 'DEFAULT_STATIC_FIELD',
    'method.static': 'DEFAULT_STATIC_METHOD',
    # JS / TS
    'variable:javascript': 'JS.GLOBAL_VARIABLE', 'variable.local:javascript': 'JS.LOCAL_VARIABLE',
    'variable:typescript': 'JS.GLOBAL_VARIABLE', 'variable.local:typescript': 'JS.LOCAL_VARIABLE',
    'parameter:javascript': 'JS.PARAMETER', 'parameter:typescript': 'JS.PARAMETER',
    'function:javascript': 'JS.GLOBAL_FUNCTION', 'function:typescript': 'JS.GLOBAL_FUNCTION',
    'method:javascript': 'JS.INSTANCE_MEMBER_FUNCTION', 'method:typescript': 'JS.INSTANCE_MEMBER_FUNCTION',
    'interface:javascript': 'JS.INTERFACE', 'interface:typescript': 'TS.INTERFACE',
    # PHP (Intelephense / PHP Tools, if installed)
    'variable:php': 'PHP_VAR', 'parameter:php': 'PHP_PARAMETER', 'property:php': 'PHP_INSTANCE_FIELD',
    'interface:php': 'PHP_INTERFACE', 'enumMember:php': 'PHP_CONSTANT', 'variable.readonly:php': 'PHP_CONSTANT',
}
semantic = {}
for sel, key in SEM.items():
    s = style(key)
    if s: semantic[sel] = s

base = json.load(open(BASE))
c = colors
bg = hexc(attrs['TEXT']['BACKGROUND']); fg = hexc(attrs['TEXT']['FOREGROUND'])
def bgof(k): a = attrs.get(k, {}); return hexc(a['BACKGROUND']) if a.get('BACKGROUND') else None
def fgof(k): a = attrs.get(k, {}); return hexc(a['FOREGROUND']) if a.get('FOREGROUND') else None
def ecof(k): a = attrs.get(k, {}); return hexc(a['EFFECT_COLOR']) if a.get('EFFECT_COLOR') else None

ui = {
    'editor.background': bg, 'editor.foreground': fg,
    'editorCursor.foreground': c['CARET_COLOR'],
    'editor.lineHighlightBackground': bg,  # CARET_ROW_COLOR empty in scheme
    'editor.selectionBackground': c['SELECTION_BACKGROUND'],
    'editor.selectionForeground': c['SELECTION_FOREGROUND'],
    'editor.inactiveSelectionBackground': c['SELECTION_BACKGROUND'] + '99',
    'editorIndentGuide.background1': c['INDENT_GUIDE'],
    'editorIndentGuide.activeBackground1': c['SELECTED_INDENT_GUIDE'],
    'editorWhitespace.foreground': c['WHITESPACES'],
    'editorRuler.foreground': c['RIGHT_MARGIN_COLOR'],
    'editorGutter.background': c['GUTTER_BACKGROUND'],
    'editorLineNumber.foreground': '#90908a',
    'editorGutter.addedBackground': c['ADDED_LINES_COLOR'],
    'editorGutter.modifiedBackground': c['MODIFIED_LINES_COLOR'],
    'editorBracketMatch.border': fgof('MATCHED_BRACE_ATTRIBUTES'),
    'editorBracketMatch.background': bg,
    'editor.wordHighlightBackground': bgof('IDENTIFIER_UNDER_CARET_ATTRIBUTES'),
    'editor.wordHighlightStrongBackground': bgof('WRITE_IDENTIFIER_UNDER_CARET_ATTRIBUTES'),
    'editor.findMatchHighlightBackground': bgof('SEARCH_RESULT_ATTRIBUTES'),
    'editor.findMatchBackground': bgof('TEXT_SEARCH_RESULT_ATTRIBUTES'),
    'editor.foldBackground': bgof('FOLDED_TEXT_ATTRIBUTES'),
    'editorInlayHint.foreground': fgof('INLINE_PARAMETER_HINT'),
    'editorInlayHint.background': bgof('INLINE_PARAMETER_HINT'),
    'editorError.foreground': ecof('ERRORS_ATTRIBUTES'),
    'editorWarning.foreground': ecof('GENERIC_SERVER_ERROR_OR_WARNING'),
    'editorInfo.foreground': ecof('INFO_ATTRIBUTES'),
    'editorUnnecessaryCode.opacity': '#00000080',
    'diffEditor.insertedTextBackground': bgof('DIFF_INSERTED') + '80',
    'diffEditor.removedTextBackground': bgof('DIFF_DELETED') + '80',
    'diffEditor.insertedLineBackground': bgof('DIFF_INSERTED') + '55',
    'diffEditor.removedLineBackground': bgof('DIFF_DELETED') + '55',
    'merge.currentContentBackground': bgof('DIFF_CONFLICT') + '80',
    'editor.stackFrameHighlightBackground': bgof('EXECUTIONPOINT_ATTRIBUTES'),
    'debugIcon.breakpointForeground': '#e51400',
    'editorHoverWidget.background': c['DOCUMENTATION_COLOR'],
    'editorSuggestWidget.background': c['LOOKUP_COLOR'],
    'terminal.background': c['CONSOLE_BACKGROUND_KEY'],
    'terminal.foreground': fgof('CONSOLE_NORMAL_OUTPUT'),
    'terminal.ansiBlack': fgof('CONSOLE_BLACK_OUTPUT'),
    'terminal.ansiRed': fgof('CONSOLE_RED_OUTPUT'),
    'terminal.ansiBlue': fgof('CONSOLE_BLUE_OUTPUT'),
    'terminal.ansiCyan': fgof('CONSOLE_CYAN_OUTPUT'),
    'terminal.ansiMagenta': fgof('CONSOLE_MAGENTA_OUTPUT'),
    'terminal.ansiWhite': fgof('CONSOLE_WHITE_OUTPUT'),
    'terminal.ansiBrightBlue': bgof('CONSOLE_BLUE_BRIGHT_OUTPUT'),
    'gitDecoration.addedResourceForeground': c['FILESTATUS_ADDED'],
    'gitDecoration.modifiedResourceForeground': c['FILESTATUS_MODIFIED'],
    'gitDecoration.deletedResourceForeground': c['FILESTATUS_DELETED'],
    'gitDecoration.untrackedResourceForeground': c['FILESTATUS_UNKNOWN'],
    'gitDecoration.ignoredResourceForeground': c['FILESTATUS_IDEA_FILESTATUS_IGNORED'],
    'gitDecoration.conflictingResourceForeground': c['FILESTATUS_IDEA_FILESTATUS_MERGED_WITH_CONFLICTS'],
    'textLink.foreground': fgof('HYPERLINK_ATTRIBUTES'),
    'editorLink.activeForeground': fgof('HYPERLINK_ATTRIBUTES'),
}
ui = {k: v for k, v in ui.items() if v}

def scopes_of(rule):
    sc = rule.get('scope')
    if sc is None: return None
    return [x.strip() for x in (sc if isinstance(sc, list) else sc.split(',')) if x.strip()]

def merge_tokens(base_rules, overrides):
    """Later layer wins: strip its scopes out of earlier rules, drop rules left empty."""
    taken = {x for r in overrides for x in (scopes_of(r) or [])}
    out = []
    for r in base_rules:
        sc = scopes_of(r)
        if sc is None:
            out.append(r); continue
        keep = [x for x in sc if x not in taken]
        if keep:
            out.append({**r, 'scope': keep})
    return out + overrides

navy = json.load(open(NAVY)) if os.path.exists(NAVY) else {}
colors_out = {**base['colors'], **ui, **navy.get('colors', {})}
for k in navy.get('drop', []):
    colors_out.pop(k, None)

theme = {
    '$schema': 'vscode://schemas/color-theme',
    'name': 'Monokai Navy',
    'type': 'dark',
    'semanticHighlighting': True,
    'colors': colors_out,
    'tokenColors': merge_tokens(merge_tokens(base['tokenColors'], token_colors), navy.get('tokenColors', [])),
    'semanticTokenColors': {**semantic, **navy.get('semanticTokenColors', {})},
}
VARIANTS = os.path.join(os.path.dirname(NAVY), 'variants.json')
variants = json.load(open(VARIANTS)) if os.path.exists(VARIANTS) else {'blue': {'label': 'Monokai Navy', 'file': 'monokai-navy-color-theme.json', 'map': {}}}
HEX = re.compile(r'#([0-9a-fA-F]{6})([0-9a-fA-F]{2})?$')
def recolour(value, cmap):
    m = HEX.match(value)
    if not m: return value
    return cmap.get('#' + m.group(1).lower(), '#' + m.group(1)) + (m.group(2) or '')
def resolved(v):  # "extends": inherit map / tokens / colors from another variant, own entries win
    p = resolved(variants[v['extends']]) if v.get('extends') else {}
    return {**p, **v, **{f: {**p.get(f, {}), **v.get(f, {})} for f in ('map', 'tokens', 'colors')}}
os.makedirs(os.path.join(OUT, 'themes'), exist_ok=True)
for vid, v in variants.items():
    if vid.startswith('$') or v.get('base'): continue   # light-based variants: tools/build_light.py
    v = resolved(v)
    cmap = {k.lower(): val for k, val in v['map'].items()}
    tmap = {k.lower(): val for k, val in v.get('tokens', {}).items()}   # optional: the variant's own syntax palette
    out = {**theme, 'name': v['label'], 'colors': {**{k: recolour(val, {**tmap, **cmap}) for k, val in theme['colors'].items()}, **v.get('colors', {})}}
    if tmap:
        st = lambda s: {**s, **{f: recolour(s[f], tmap) for f in ('foreground', 'background') if f in s}}
        out['tokenColors'] = [{**r, 'settings': st(r['settings'])} for r in theme['tokenColors']]
        out['semanticTokenColors'] = {k: st(s) for k, s in theme['semanticTokenColors'].items()}
    with open(os.path.join(OUT, 'themes', v['file']), 'w') as f:
        json.dump(out, f, indent=2); f.write('\n')
pkg = os.path.join(OUT, 'package.json')
if not os.path.exists(pkg):  # never clobber a hand-maintained manifest
    json.dump({
        'name': 'monokai-navy', 'displayName': 'Monokai Navy',
        'publisher': 'fosteev', 'version': '1.0.0',
        'engines': {'vscode': '^1.80.0'}, 'categories': ['Themes'],
        'contributes': {'themes': [{'label': 'Monokai Navy', 'uiTheme': 'vs-dark',
                                    'path': './themes/monokai-navy-color-theme.json'}]},
    }, open(pkg, 'w'), indent=2)
print('tokenColors:', len(theme['tokenColors']), 'semantic:', len(theme['semanticTokenColors']),
      'colors:', len(colors_out), 'navy overrides:', len(navy.get('colors', {})),
      'variants:', ', '.join(k for k, v in variants.items() if not k.startswith('$') and not v.get('base')))
