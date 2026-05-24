# Agent Instructions

This repository contains a universal workflow pack for creating Bank of China style PPT decks.

When the user asks for PPT content pages, cover/chapter pages, or final assembly, read and follow:

```text
skills/boc-ppt-builder/AGENT.md
```

Key trigger phrases:

- `根据原始材料做内容页`
- `content页`
- `做PPT的封面和章节`
- `整合PPT`

The workflow pack is agent-neutral. Use it from Codex, OpenClaw, Claude Code, Cursor, VS Code + Copilot, CodeBuddy, or similar coding agents. Keep all edits inside this repository unless the user explicitly asks otherwise.

For deterministic checks and export, prefer the scripts under:

```text
skills/boc-ppt-builder/scripts/
```

The bundled `ppt-master` now requires explicit template directory paths. For Bank of China pages, use:

```text
ppt-master/skills/ppt-master/templates/decks/中国银行
```
