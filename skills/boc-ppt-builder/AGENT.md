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
- BOC deck template path: `ppt-master/skills/ppt-master/templates/decks/中国银行`

## Workflow Selection

- For content-page work, read `skills/boc-ppt-builder/references/content-pages.md`.
- For cover, TOC, chapter, and ending pages, read `skills/boc-ppt-builder/references/chapter-pages.md`.
- For final deck assembly, read `skills/boc-ppt-builder/references/assemble-ppt.md`.

Load only the selected workflow file first. When the selected workflow invokes `ppt-master`, also follow `skills/boc-ppt-builder/references/ppt-master-integration.md`.

## Shared Operating Rules

- Use the bundled `ppt-master` 中国银行 deck template by explicit path: `ppt-master/skills/ppt-master/templates/decks/中国银行`.
- Do not call the template by bare name. Newer `ppt-master` only activates templates when an explicit directory path is supplied.
- Do not use the old "skip eight confirmations" wording. Pass the wrapper-confirmed BOC constraints into `ppt-master`; if the active runtime treats the underlying Eight Confirmations gate as mandatory, present the compact confirmation bundle once and wait.
- Preserve SVGs as the handoff format. Delete temporary `ppt-master` project folders after extracting the required SVG when the workflow says to keep only SVG.
- Keep `ppt-master` SVG generation sequential inside each invoked project. Only run independent wrapper-level page jobs in parallel if the active agent supports isolated safe parallel work.
- Do not install this workflow pack globally. Keep it versioned in this repository.

## Deterministic Commands

Validate chapter structure and fix local asset references:

```powershell
python skills\boc-ppt-builder\scripts\validate_chapters.py --project-root C:\Apps\boc_ppt_master --fix-assets --include-top-level
```

Assemble SVGs and export the final PPTX:

```powershell
python skills\boc-ppt-builder\scripts\assemble_and_export.py --project-root C:\Apps\boc_ppt_master
```

## Human Interaction Rules

- Content pages: after reading `raw_files/`, propose a page split and stop for user confirmation before generating plans or SVGs.
- Cover/chapter workflow: if validation passes, ask for cover title, subtitle/team name, and report date before generating cover/TOC/chapter/ending SVGs.
- Assembly workflow: do not export a partial deck. If validation fails, report the exact missing or malformed files and stop.
