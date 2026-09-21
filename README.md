# PhpStorm Monokai Navy — VS Code theme

Monokai (Sublime Text 3 flavour) as it looks in my PhpStorm, ported to VS Code:
the editor and the whole workbench sit on a dark navy `#0b1823` instead of the classic `#272822`.

- Token colours come straight from the PhpStorm `.icls` scheme (PHP variables, fields,
  parameters, constants and interfaces have their own colours; JS/TS locals, globals,
  parameters, methods and interfaces are coloured via semantic tokens).
- Workbench chrome (sidebar, tabs, status bar, panels, inputs, terminal) is a navy family
  derived from the editor background; Monokai cyan `#66d9ef` is the accent.
- Terminal uses a proper Monokai ANSI palette.

## Install

Marketplace: not published yet. From source:

```sh
git clone https://github.com/fosteev/vscode-phpstorm-monokai ~/.vscode/extensions/fosteev.phpstorm-monokai
```

Restart VS Code, then `Cmd+K Cmd+T` → **PhpStorm Monokai**.

Or build a `.vsix` with `npx @vscode/vsce package` and install it via
`code --install-extension phpstorm-monokai-1.0.0.vsix`.

## Regenerating from PhpStorm

`tools/icls2vscode.py` converts a JetBrains `.icls` scheme into this extension, using
VS Code's built-in Monokai as the base for anything the scheme does not define:

```sh
python3 tools/icls2vscode.py \
  ~/Library/Application\ Support/JetBrains/PhpStorm*/colors/My\ Scheme.icls \
  /Applications/Visual\ Studio\ Code.app/Contents/Resources/app/extensions/theme-monokai/themes/monokai-color-theme.json \
  ./build
```

`tools/source.icls` is the scheme this theme was generated from. The navy workbench
colours were added on top of the generated file by hand.

## Notes

- PHP is highlighted by the TextMate grammar unless a language server (Intelephense,
  PHP Tools) is installed — semantic rules for `php` are already in the theme.
- The scheme's font (JetBrains Mono 14) is not part of a colour theme; set
  `editor.fontFamily` yourself.
