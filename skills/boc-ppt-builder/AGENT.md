# BOC PPT Builder Agent Guide

This is an agent-neutral workflow pack for creating Bank of China style PPT decks in this repository. It is not tied to one agent runtime. Codex, OpenClaw, Claude Code, Cursor, VS Code + Copilot, CodeBuddy, and similar coding agents should follow the same workflow here.

## Trigger Phrases

Use this workflow pack when the user says any of the following:

- `根据原始材料做内容页`
- `content页`
- `做PPT的封面和章节`
- `整合PPT`
- Any close paraphrase asking to create BOC-branded PPT content pages, chapters, or a final PPTX.

## Repository Contract

All paths are relative to the repository root unless an absolute path is required.

- Source material: `raw_files/`
- Content planning output: `ppt_plan/content_batch_N/pageM.md`
- Content assets: `ppt_plan/asset/`
- Content SVG output: `ppt_plan/svg/pageM.svg`
- Chapter workspace: `ppt_chapters/`
- Chapter assets: `ppt_chapters/asset/`
- Ordered final SVG input: `ppt_chapters/output_svg/`
- Final PPTX: `ppt_chapters/output_pptx/output.pptx`
- Underlying PPT engine: `ppt-master/skills/ppt-master`

## Workflow Selection

- For content-page work, read `skills/boc-ppt-builder/references/content-pages.md`.
- For cover, TOC, chapter, and ending pages, read `skills/boc-ppt-builder/references/chapter-pages.md`.
- For final deck assembly, read `skills/boc-ppt-builder/references/assemble-ppt.md`.

Load only the selected workflow file first. Load scripts only when you need exact behavior or need to modify them.

## Shared Operating Rules

- Use the bundled `ppt-master` 中国银行 template.
- Treat this wrapper's confirmed plan as the design confirmation. When invoking `ppt-master`, explicitly say to skip the eight blocking confirmations and continue directly.
- Preserve SVGs as the handoff format. Delete temporary `ppt-master` project folders after extracting the required SVG when the workflow says to keep only SVG.
- Run independent page generation in parallel when the active agent supports safe parallel work. Otherwise generate pages sequentially.
- Do not install this workflow pack globally. Keep it versioned in this repository.

## Deterministic Commands

Validate chapter structure and fix local asset references:

```powershell
python skills\boc-ppt-builder\scripts\validate_chapters.py --project-root C:\boc_ppt_master --fix-assets
```

Assemble SVGs and export the final PPTX:

```powershell
python skills\boc-ppt-builder\scripts\assemble_and_export.py --project-root C:\boc_ppt_master
```

## Human Interaction Rules

- Content pages: after reading `raw_files/`, propose a page split and stop for user confirmation before generating plans or SVGs.
- Cover/chapter workflow: if validation passes, ask for cover title and subtitle before generating cover/TOC/chapter/ending SVGs.
- Assembly workflow: do not export a partial deck. If validation fails, report the exact missing or malformed files and stop.
