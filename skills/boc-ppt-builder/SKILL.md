---
name: boc-ppt-builder
description: >
  Agent-neutral orchestration skill for Bank of China PPT production in this
  repository. Use when the user says 根据原始材料做内容页, content页,
  做PPT的封面和章节, or 整合PPT. It plans content pages from raw_files,
  calls ppt-master with the explicit 中国银行 deck template path, validates ppt_chapters assets,
  organizes SVGs, fixes page numbers, and exports
  ppt_chapters/output_pptx/output.pptx.
---

# BOC PPT Builder

## Overview

This is an agent-neutral workflow pack for `C:\Apps\boc_ppt_master`. It is an orchestration layer over the bundled `ppt-master` skill at `C:\Apps\boc_ppt_master\ppt-master\skills\ppt-master`.

For non-Codex agents, the canonical entry is `AGENT.md` in this same folder. This `SKILL.md` is retained for agents that support skill-style folders.

This package contains three workflows:

- Content pages: read `raw_files`, ask for page split confirmation, create page-level planning Markdown, then generate content SVGs.
- Cover and chapters: validate `ppt_chapters`, ask for cover title/subtitle, then generate cover, TOC, chapter, and ending SVGs.
- Final assembly: validate all pages, organize SVGs, fix page numbers, and export one PPTX.

## Repository Paths

Use these paths relative to `C:\Apps\boc_ppt_master`:

- Raw materials: `raw_files/`
- Content planning output: `ppt_plan/content_batch_N/pageM.md`
- Content assets: `ppt_plan/asset/`
- Content SVG output: `ppt_plan/svg/pageM.svg`
- Chapter workspace: `ppt_chapters/`
- Chapter assets: `ppt_chapters/asset/`
- Final SVG inputs for export: `ppt_chapters/output_svg/`
- Final PPTX: `ppt_chapters/output_pptx/output.pptx`
- BOC deck template: `ppt-master/skills/ppt-master/templates/decks/中国银行`

## Workflow Selection

- If the user asks "根据原始材料做内容页" or "content页", read `references/content-pages.md`.
- If the user asks "做PPT的封面和章节", read `references/chapter-pages.md`.
- If the user asks "整合PPT", read `references/assemble-ppt.md`.

Load only the selected reference file unless another workflow is explicitly needed. When the selected workflow invokes `ppt-master`, also follow `references/ppt-master-integration.md`.

## Shared Rules

- Use the 中国银行 deck template from `ppt-master` by explicit path: `ppt-master/skills/ppt-master/templates/decks/中国银行`.
- Do not call the template by bare name. Newer `ppt-master` only activates templates when an explicit directory path is supplied.
- Do not use the old "skip eight confirmations" wording. Pass the wrapper-confirmed BOC constraints into `ppt-master`; if the active runtime treats the underlying Eight Confirmations gate as mandatory, present the compact confirmation bundle once and wait.
- Preserve generated SVG as the handoff artifact. Delete temporary `ppt-master` project folders after extracting the required SVG when the workflow says to keep only SVG.
- Keep `ppt-master` SVG generation sequential inside each invoked project. Only run independent wrapper-level page jobs in parallel if the active agent/runtime supports isolated safe parallel work.
- Do not install this workflow pack globally; keep it versioned in this project folder.

## Deterministic Helpers

Use the bundled scripts for checks and assembly:

```powershell
python skills\boc-ppt-builder\scripts\validate_chapters.py --project-root C:\Apps\boc_ppt_master --fix-assets --include-top-level
python skills\boc-ppt-builder\scripts\assemble_and_export.py --project-root C:\Apps\boc_ppt_master
```

`validate_chapters.py` checks the chapter directory shape and local asset references. `assemble_and_export.py` validates the complete deck, writes `final_svg/` and `output_svg/`, repairs page numbers, and calls `ppt-master`'s `svg_to_pptx.py`.
