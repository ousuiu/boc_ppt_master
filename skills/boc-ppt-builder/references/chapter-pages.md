# Cover, Chapter, TOC Workflow

Use this workflow when the user says "做PPT的封面和章节".

## Step 1 - Validate Chapter Workspace

Check `C:\boc_ppt_master\ppt_chapters`.

Required structure before continuing:

```text
ppt_chapters/
  asset/
  c1-章节标题/
    page1.svg
    page2.svg
  c2-章节标题/
    page1.svg
```

Run:

```powershell
python skills\boc-ppt-builder\scripts\validate_chapters.py --project-root C:\boc_ppt_master --fix-assets
```

The script checks:

- `ppt_chapters/` exists.
- Chapter directories are named `c[章节序号]-[章节标题]`.
- Chapter numbers are continuous from 1.
- Each chapter contains sequential `page[章节内页码序号].svg` files.
- Every local SVG asset reference can be matched by filename under `ppt_chapters/asset/`.
- When `--fix-assets` is set, SVG asset references are rewritten to the correct relative path.

If any check fails, report the exact issue and end the workflow. Continue only when the checks pass.

## Step 2 - Ask for Cover Text

Ask the user for:

- Cover title
- Cover subtitle

Do not generate cover/chapter/toc pages until both values are known.

## Step 3 - Generate Cover SVG

Invoke `ppt-master`:

```text
使用ppt-master技能,用中国银行模板cover页做1页PPT，标题是.....，副标题是.....。跳过ppt-master技能中强制停下的8项检查，直接往前走。
```

Keep only the SVG and save it as:

```text
C:\boc_ppt_master\ppt_chapters\cover.svg
```

Delete other temporary files.

## Step 4 - Generate Chapter, TOC, and Ending SVGs

Read chapter titles from `ppt_chapters/c[章节序号]-[章节标题]`. Let total chapter count be `[总章节数]`.

Generate chapter pages with:

```text
使用ppt-master技能,用中国银行模板chapter页做[总章节数]页PPT，第1页标题是：...., 第2页标题是....。跳过ppt-master技能中强制停下的8项检查，直接往前走。
```

Save each chapter SVG as:

```text
C:\boc_ppt_master\ppt_chapters\chapter[n].svg
```

Generate the TOC page with:

```text
使用ppt-master技能,用中国银行模板toc页做1页PPT，总共有[总章节数]个标题，标题为1...., 2...。跳过ppt-master技能中强制停下的8项检查，直接往前走。
```

Save it as:

```text
C:\boc_ppt_master\ppt_chapters\toc.svg
```

Generate the ending page with:

```text
使用ppt-master技能,用中国银行模板ending页做1页PPT，内容是"请批评指正"。跳过ppt-master技能中强制停下的8项检查，直接往前走。
```

Save it as:

```text
C:\boc_ppt_master\ppt_chapters\ending.svg
```

Keep only SVG outputs and delete all temporary `ppt-master` intermediate files.
