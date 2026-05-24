# ppt-master Integration Notes

Use this note whenever a BOC workflow invokes the bundled `ppt-master` skill.

## Current ppt-master Contract

- Underlying skill root: `C:\Apps\boc_ppt_master\ppt-master\skills\ppt-master`
- Canonical skill file: `ppt-master/skills/ppt-master/SKILL.md`
- BOC template kind: `deck`
- BOC template path: `C:\Apps\boc_ppt_master\ppt-master\skills\ppt-master\templates\decks\中国银行`
- Core BOC SVG layouts: `01_cover.svg`, `02_toc.svg`, `02_chapter.svg`, `03_content.svg`, `04_ending.svg`
- Required BOC template assets: `assets/cover_bg.png`, `assets/toc_bg.png`, `assets/end_bg.png`, `assets/boc_full_logo.png`

Read `ppt-master/skills/ppt-master/SKILL.md` before invoking the underlying workflow if it has not already been loaded in the current turn.

## Invocation Rules

1. Always provide the explicit BOC deck template directory path in the first `ppt-master` request.
2. Do not rely on the bare name `中国银行`; newer `ppt-master` deliberately ignores bare template names.
3. Do not tell `ppt-master` to "skip the eight confirmations". Instead, pass a compact BOC confirmation bundle:
   - Canvas: `ppt169`, 1280 x 720.
   - Template: `C:\Apps\boc_ppt_master\ppt-master\skills\ppt-master\templates\decks\中国银行`.
   - Page count and page type: exactly what the wrapper workflow requested.
   - Audience/tone: BOC executive reporting, official, restrained, financially credible.
   - Color/typography: inherited from the BOC deck `design_spec.md`.
   - Source/content outline: the wrapper-confirmed page plan or chapter list.
   - Formula policy: `mixed` unless the user says otherwise.
   - Image acquisition: use only user/source assets unless the page plan explicitly asks for AI or web images.
4. If the active runtime treats the underlying Eight Confirmations as a mandatory hard stop, present that compact bundle once and wait for confirmation. After confirmation, continue the remaining non-blocking `ppt-master` steps.
5. Preserve `ppt-master`'s new execution discipline inside each project: `spec_lock.md`, live preview startup, sequential page SVG generation, quality check, and post-processing are part of the underlying workflow.

## Asset Handoff

When extracting an SVG from a temporary `ppt-master` project, also copy every local asset referenced by that SVG into the target asset directory:

- Content-page workflow target: `C:\Apps\boc_ppt_master\ppt_plan\asset`
- Chapter workflow target: `C:\Apps\boc_ppt_master\ppt_chapters\asset`

The helper scripts can also repair references and copy missing BOC template assets from the deck template:

```powershell
python skills\boc-ppt-builder\scripts\validate_chapters.py --project-root C:\Apps\boc_ppt_master --fix-assets --include-top-level
python skills\boc-ppt-builder\scripts\assemble_and_export.py --project-root C:\Apps\boc_ppt_master
```

## New Capabilities To Surface

- `spec_lock.md`: when hand-authoring or revising SVGs, use BOC colors, fonts, icons, images, page layout, rhythm, and chart selections from `spec_lock.md`; re-read it per page in long runs.
- Live preview: allow `ppt-master` to start `svg_editor/server.py --live` during generation. Do not suppress it.
- Chart verification: if generated pages contain bar/line/pie/radar or similar data charts, run `ppt-master/skills/ppt-master/workflows/verify-charts.md` before export.
- Visual review: run `ppt-master/skills/ppt-master/workflows/visual-review.md` only when the user explicitly asks for a visual re-pass.
- Export features: final assembly uses the upgraded `svg_to_pptx.py`, which now defaults to native editable PPTX plus transitions/element animations. Use `assemble_and_export.py --export-arg=...` to pass through advanced export flags such as `-a none`, `--svg-snapshot`, `--merge-paragraphs`, `--auto-advance`, or recorded narration options.
