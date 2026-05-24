# Final PPT Assembly Workflow

Use this workflow when the user says "整合PPT".

## Step 1 - Validate Completeness

Run:

```powershell
python skills\boc-ppt-builder\scripts\assemble_and_export.py --project-root C:\Apps\boc_ppt_master
```

The script checks:

- `ppt_chapters/cover.svg`, `toc.svg`, and `ending.svg` exist.
- Top-level `chapter[n].svg` files exist.
- `chapter[n].svg` count and numbering match the `c[章节序号]-[章节标题]` folders.
- Every chapter folder contains sequential `page[章节内页码序号].svg` files.
- Every local SVG asset reference can be matched by filename under `ppt_chapters/asset/`.

Before checking asset references, the script attempts to copy missing referenced BOC template assets from `ppt-master/skills/ppt-master/templates/decks/中国银行/assets/` into `ppt_chapters/asset/`.

If validation fails, report the errors and end the workflow. Do not export a partial deck.

## Step 2 - Organize SVGs

The script organizes pages into this order:

```text
[页号]_cover.svg
[页号]_toc.svg
[页号]_chapter[章节序号].svg
[页号]_content[章节内页码序号].svg
[页号]_content[章节内页码序号].svg
...
[页号]_chapter[章节序号].svg
[页号]_content[章节内页码序号].svg
[页号]_content[章节内页码序号].svg
...
[页号]_ending.svg
```

It writes the organized SVGs to:

```text
C:\Apps\boc_ppt_master\ppt_chapters\final_svg
C:\Apps\boc_ppt_master\ppt_chapters\output_svg
```

Page numbers are zero-padded to keep filesystem sorting stable, for example `01_cover.svg`.

## Step 3 - Repair Page Numbers

The script checks every file in `output_svg/`:

- Filename page number must match the visible page number inside the SVG.
- Total page count inside each SVG must match the number of SVG files.
- If a page number is missing, the script inserts a BOC-style page number at the bottom center.

## Step 4 - Export PPTX

The script calls:

```powershell
python ppt-master\skills\ppt-master\scripts\svg_to_pptx.py C:\Apps\boc_ppt_master\ppt_chapters -s output_svg -o C:\Apps\boc_ppt_master\ppt_chapters\output_pptx\output.pptx
```

The upgraded `svg_to_pptx.py` exports native editable PPTX by default and applies default transitions / element entrance animations. Use `assemble_and_export.py --export-arg=...` to pass through advanced `ppt-master` export flags when the user asks for custom animation, SVG snapshot output, paragraph merging, auto-advance, or recorded narration.

The expected primary output is:

```text
C:\Apps\boc_ppt_master\ppt_chapters\output_pptx\output.pptx
```
