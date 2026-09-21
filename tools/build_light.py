#!/usr/bin/env python3
"""Derive the light variant from the dark theme: same scopes, palette re-tuned for a white page."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dark = json.load(open(os.path.join(ROOT, 'themes', 'monokai-navy-color-theme.json')))

# dark token colour -> light token colour (contrast-checked against #f8fafc)
MAP = {
    '#f8f8f2': '#1b2733', '#f9faf4': '#1b2733', '#cfcfc2': '#1b2733', '#000000': '#1b2733', '#f9eff9': '#1b2733',
    '#75715e': '#8a94a0', '#88846f': '#8a94a0',
    '#f92672': '#d81b60', '#e6db74': '#9a7d0a', '#ae81ff': '#6f42c1', '#ae81ffa0': '#6f42c1a0', '#b267e6': '#6f42c1',
    '#a6e22e': '#4f8a10', '#a7ec21': '#4f8a10', '#a8c023': '#4f8a10',
    '#66d9ef': '#0b7fa5', '#65d8ee': '#0b7fa5', '#6796e6': '#1565c0', '#fd971f': '#c25e00', '#cd9731': '#c25e00',
    '#f44747': '#c62828', '#ff0000': '#c62828',
    # php
    '#00c0b0': '#00897b', '#98ffe0': '#2e7d6e', '#e9ff65': '#8d6e00', '#ff0057': '#c50045', '#00ffa6': '#00875a',
    # js / ts
    '#51f611': '#2e8b00', '#2293ff': '#1565c0', '#00d7ff': '#0277bd', '#f88908': '#e65100', '#fff21c': '#b58a00',
    '#c70000': '#c62828', '#e30000': '#c62828',
}
def m(v): return MAP.get(v.lower(), v) if isinstance(v, str) else v

tokens = []
for r in dark['tokenColors']:
    s = dict(r['settings'])
    if 'foreground' in s: s['foreground'] = m(s['foreground'])
    if 'background' in s: s.pop('background')  # css property bg etc. — not wanted on light
    tokens.append({**r, 'settings': s})
semantic = {k: {**v, **({'foreground': m(v['foreground'])} if 'foreground' in v else {})} for k, v in dark['semanticTokenColors'].items()}

BG, FG = '#f8fafc', '#1b2733'; SIDE, ACT, WID, BR, ACC, DIM = '#eef2f6', '#e3e9ef', '#ffffff', '#d3dce6', '#0b7fa5', '#5b6875'
SEL, LH, LN = '#cfe3f5', '#eef3f8', '#a0aab4'
colors = {
    'editor.background': BG, 'editor.foreground': FG, 'editorCursor.foreground': '#1b2733',
    'editor.lineHighlightBackground': LH, 'editor.selectionBackground': SEL, 'editor.inactiveSelectionBackground': '#cfe3f599',
    'editor.selectionHighlightBackground': '#cfe3f580', 'editor.wordHighlightBackground': '#ffe9a850', 'editor.wordHighlightStrongBackground': '#ffd47a70',
    'editor.findMatchBackground': '#ffd47a', 'editor.findMatchHighlightBackground': '#ffe9a880', 'editor.foldBackground': '#e3e9ef80',
    'editorLineNumber.foreground': LN, 'editorLineNumber.activeForeground': FG, 'editorGutter.background': BG,
    'editorGutter.addedBackground': '#7cc47f', 'editorGutter.modifiedBackground': '#6fa8dc', 'editorGutter.deletedBackground': '#e57373',
    'editorIndentGuide.background1': '#dfe6ee', 'editorIndentGuide.activeBackground1': '#9fb0c2', 'editorWhitespace.foreground': '#d3dce6', 'editorRuler.foreground': '#dfe6ee',
    'editorBracketMatch.border': '#e65100', 'editorBracketMatch.background': BG,
    'editorInlayHint.foreground': '#7a8794', 'editorInlayHint.background': '#eef2f6',
    'editorError.foreground': '#c62828', 'editorWarning.foreground': '#c25e00', 'editorInfo.foreground': '#0b7fa5',
    'editorUnnecessaryCode.opacity': '#00000080',
    'diffEditor.insertedTextBackground': '#a5d6a760', 'diffEditor.removedTextBackground': '#ef9a9a60',
    'diffEditor.insertedLineBackground': '#a5d6a730', 'diffEditor.removedLineBackground': '#ef9a9a30',
    'editorWidget.background': WID, 'editorWidget.border': BR, 'editorSuggestWidget.background': WID, 'editorSuggestWidget.border': BR,
    'editorSuggestWidget.selectedBackground': SEL, 'editorHoverWidget.background': WID, 'editorHoverWidget.border': BR,
    'editorStickyScroll.background': BG, 'editorStickyScrollHover.background': LH, 'editorOverviewRuler.border': BR,
    'minimap.background': BG, 'scrollbarSlider.background': '#9fb0c250', 'scrollbarSlider.hoverBackground': '#9fb0c280', 'scrollbarSlider.activeBackground': '#9fb0c2b0',
    'activityBar.background': ACT, 'activityBar.foreground': FG, 'activityBar.inactiveForeground': '#8a94a0', 'activityBar.border': BR,
    'activityBarBadge.background': ACC, 'activityBarBadge.foreground': '#ffffff',
    'sideBar.background': SIDE, 'sideBar.foreground': '#2f3d4a', 'sideBar.border': BR,
    'sideBarSectionHeader.background': SIDE, 'sideBarSectionHeader.foreground': DIM, 'sideBarSectionHeader.border': BR, 'sideBarTitle.foreground': DIM,
    'titleBar.activeBackground': ACT, 'titleBar.inactiveBackground': ACT, 'titleBar.activeForeground': FG, 'titleBar.border': BR,
    'statusBar.background': ACT, 'statusBar.foreground': DIM, 'statusBar.border': BR, 'statusBar.noFolderBackground': ACT, 'statusBar.debuggingBackground': '#c25e00', 'statusBar.debuggingForeground': '#ffffff',
    'statusBarItem.hoverBackground': '#d3dce6', 'statusBarItem.remoteBackground': ACC, 'statusBarItem.remoteForeground': '#ffffff',
    'panel.background': BG, 'panel.border': BR, 'panelTitle.activeForeground': FG, 'panelTitle.inactiveForeground': DIM, 'panelTitle.activeBorder': ACC,
    'editorGroupHeader.tabsBackground': SIDE, 'editorGroupHeader.tabsBorder': BR, 'editorGroupHeader.noTabsBackground': BG, 'editorGroup.border': BR,
    'tab.activeBackground': BG, 'tab.activeForeground': FG, 'tab.activeBorderTop': ACC, 'tab.inactiveBackground': SIDE, 'tab.inactiveForeground': DIM, 'tab.border': BR,
    'tab.unfocusedActiveBackground': BG, 'tab.unfocusedInactiveBackground': SIDE, 'tab.hoverBackground': LH,
    'breadcrumb.background': BG, 'breadcrumb.foreground': DIM, 'breadcrumb.focusForeground': FG, 'breadcrumbPicker.background': WID,
    'list.hoverBackground': LH, 'list.activeSelectionBackground': SEL, 'list.activeSelectionForeground': FG, 'list.inactiveSelectionBackground': '#e3e9ef', 'list.focusBackground': SEL, 'list.highlightForeground': ACC,
    'tree.indentGuidesStroke': BR,
    'input.background': WID, 'input.border': BR, 'input.foreground': FG, 'input.placeholderForeground': '#8a94a0', 'inputOption.activeBackground': SEL, 'inputOption.activeBorder': ACC,
    'dropdown.background': WID, 'dropdown.border': BR, 'dropdown.listBackground': WID,
    'quickInput.background': WID, 'quickInputList.focusBackground': SEL, 'quickInputTitle.background': SIDE,
    'menu.background': WID, 'menu.foreground': FG, 'menu.selectionBackground': SEL, 'menu.selectionForeground': FG, 'menu.border': BR, 'menu.separatorBackground': BR,
    'widget.shadow': '#00000022', 'focusBorder': ACC, 'checkbox.background': WID, 'checkbox.border': BR,
    'button.background': ACC, 'button.foreground': '#ffffff', 'button.hoverBackground': '#096a8a', 'button.secondaryBackground': '#d3dce6', 'button.secondaryForeground': FG,
    'badge.background': '#d3dce6', 'badge.foreground': FG, 'progressBar.background': ACC,
    'notifications.background': WID, 'notifications.border': BR, 'notificationCenterHeader.background': SIDE,
    'pickerGroup.foreground': ACC, 'pickerGroup.border': BR, 'settings.headerForeground': FG, 'settings.modifiedItemIndicator': ACC,
    'textLink.foreground': '#1565c0', 'editorLink.activeForeground': '#1565c0',
    'commandCenter.background': WID, 'commandCenter.border': BR, 'debugToolBar.background': WID,
    'welcomePage.background': BG, 'walkThrough.embeddedEditorBackground': SIDE, 'textBlockQuote.background': SIDE, 'textCodeBlock.background': SIDE,
    'gitDecoration.addedResourceForeground': '#2e7d32', 'gitDecoration.modifiedResourceForeground': '#1565c0', 'gitDecoration.deletedResourceForeground': '#8a94a0',
    'gitDecoration.untrackedResourceForeground': '#c25e00', 'gitDecoration.ignoredResourceForeground': '#a0aab4', 'gitDecoration.conflictingResourceForeground': '#c62828',
    'terminal.background': BG, 'terminal.foreground': FG, 'terminal.border': BR, 'terminalCursor.foreground': FG, 'terminal.selectionBackground': SEL,
    'terminal.ansiBlack': '#1b2733', 'terminal.ansiRed': '#d81b60', 'terminal.ansiGreen': '#4f8a10', 'terminal.ansiYellow': '#9a7d0a',
    'terminal.ansiBlue': '#0b7fa5', 'terminal.ansiMagenta': '#6f42c1', 'terminal.ansiCyan': '#00897b', 'terminal.ansiWhite': '#c9d1da',
    'terminal.ansiBrightBlack': '#5b6875', 'terminal.ansiBrightRed': '#e53935', 'terminal.ansiBrightGreen': '#2e7d32', 'terminal.ansiBrightYellow': '#c25e00',
    'terminal.ansiBrightBlue': '#1565c0', 'terminal.ansiBrightMagenta': '#8e24aa', 'terminal.ansiBrightCyan': '#00796b', 'terminal.ansiBrightWhite': '#f8fafc',
}
light = {'$schema': 'vscode://schemas/color-theme', 'name': 'Monokai Navy Light', 'type': 'light', 'semanticHighlighting': True,
         'colors': colors, 'tokenColors': tokens, 'semanticTokenColors': semantic}
json.dump(light, open(os.path.join(ROOT, 'themes', 'monokai-navy-light-color-theme.json'), 'w'), indent=2)
print('light theme written', len(tokens), 'rules')
