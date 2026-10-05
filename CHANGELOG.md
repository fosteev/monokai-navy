# Changelog

## 1.4.1

- Extension icon: a Monokai-coloured “M” on the navy tile (`assets/icon.svg` → `icon.png`).

## 1.4.0

- Monokai Navy Claude: the near-black neutral workbench of the Claude desktop app (`#111111` → `#212121`, colours sampled from the app) with a clay `#d97757` accent and its own syntax palette — clay keywords, manilla strings, olive functions, blue classes, heather numbers. Variants in `tools/variants.json` can now carry `"tokens"` (syntax palette), `"colors"` (per-key overrides) and `"extends"` (inherit another variant).
- Monokai Navy Claude Blue / Claude Green: the Claude variant with a blue `#6394e4` or green `#5dbb74` workbench accent instead of clay.

## 1.3.0

- Monokai Navy White: pure white editor with neutral grey chrome, derived from Light (`tools/variants.json`, `"base": "light"`).

## 1.2.0

- Grey and Pink (plum) workbench variants next to Blue: same syntax colours, different ramp (`tools/variants.json`).

- Workbench ramp inverted: the editor stays `#0b1823` and is now the darkest surface; sidebar/panels `#112232`, activity/title/status bars `#152a3d`, popups/inputs `#183044`, borders `#24425c` (the chrome used to be darker than the editor).

- Interfaces were black (`#000000`) — the scheme's `DEFAULT_INTERFACE_NAME` is "inherit"; now cyan italic like classes.
- JS/TS interfaces lifted from `#c70000`/`#e30000` (unreadable on navy) to `#ff5555`.
- Find matches, word highlights and the current match were near-invisible (`#020202`, `#000055`); now orange/yellow/cyan translucent, plus overview-ruler marks.
- Selection (editor, inactive, terminal, widgets) moved from olive `#383830` to navy `#22405c`.
- ~25 olive/grey leftovers from the built-in Monokai chrome repainted (drop targets, peek view, panel borders, inactive status bar, inlay hints, fold background, whitespace).
- Grey `editor.lineHighlightBorder` from vs-dark defaults removed.
- Theme file deduplicated: built-in Monokai rules whose scopes the scheme overrides are dropped (99 → 82 rules).
- Deprecated `editorIndentGuide.background`/`activeBackground` removed.
- README previews rendered to PNG as well (vsce refuses SVG images in README, so the package could not be built).
- Tooling: navy layer moved to `tools/navy.json`, converter merges layers instead of appending, `tools/check_theme.py` lint.

## 1.1.0

- Monokai Navy Light: the same scopes and hues re-tuned for a white page (`tools/build_light.py`).

## 1.0.0

- Initial port from PhpStorm scheme.
