# Cover, Chapter, TOC Workflow

Use this workflow when the user says "做PPT的封面和章节".

## Step 1 - Validate Chapter Workspace

Check `C:\Apps\boc_ppt_master\ppt_chapters`.

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
python skills\boc-ppt-builder\scripts\validate_chapters.py --project-root C:\Apps\boc_ppt_master --fix-assets --include-top-level
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
- Cover subtitle or reporting organization (this maps to the BOC template's `{{TEAM_NAME}}` slot)
- Report date or reporting period (this maps to `{{DATE}}`; if the user does not care, use today's date)

Do not generate cover/chapter/toc pages until these values are known.

## Step 3 - Generate Cover SVG

Follow `skills/boc-ppt-builder/references/ppt-master-integration.md`, then invoke `ppt-master`. The explicit deck template path is mandatory for the upgraded `ppt-master`:

```text
使用ppt-master技能。请读取 C:\Apps\boc_ppt_master\ppt-master\skills\ppt-master\SKILL.md，并按新版ppt-master流程执行。
显式使用deck模板路径：C:\Apps\boc_ppt_master\ppt-master\skills\ppt-master\templates\decks\中国银行
只生成1页中国银行cover页，继承 01_cover.svg。标题写入 {{TITLE}}：.....；副标题/汇报单位写入 {{TEAM_NAME}}：.....；日期写入 {{DATE}}：.....。
本wrapper已完成封面信息确认，请把这些内容作为BOC确认束；不要使用旧的“跳过八项确认”指令。如果当前运行环境仍强制ppt-master Eight Confirmations硬停，请只展示紧凑确认束并等待一次确认；确认后继续生成。
```

Keep only the SVG and save it as:

```text
C:\Apps\boc_ppt_master\ppt_chapters\cover.svg
```

Copy any referenced local template assets into `C:\Apps\boc_ppt_master\ppt_chapters\asset`, then delete other temporary files.

## Step 4 - Generate Chapter, TOC, and Ending SVGs

Read chapter titles from `ppt_chapters/c[章节序号]-[章节标题]`. Let total chapter count be `[总章节数]`.

The bundled BOC TOC template has six indexed TOC slots. If there are more than six chapters, stop and ask the user whether to merge chapters or allow a custom TOC layout.

Generate chapter pages with:

```text
使用ppt-master技能。显式使用deck模板路径：C:\Apps\boc_ppt_master\ppt-master\skills\ppt-master\templates\decks\中国银行
生成[总章节数]页中国银行chapter页，继承 02_chapter.svg。第1页 {{CHAPTER_NUM}}=01，{{CHAPTER_TITLE}}=....；第2页 {{CHAPTER_NUM}}=02，{{CHAPTER_TITLE}}=....。
使用wrapper已确认的BOC确认束；不要使用旧的“跳过八项确认”指令。如果当前运行环境仍强制ppt-master Eight Confirmations硬停，请只展示紧凑确认束并等待一次确认；确认后继续生成。
```

Save each chapter SVG as:

```text
C:\Apps\boc_ppt_master\ppt_chapters\chapter[n].svg
```

Generate the TOC page with:

```text
使用ppt-master技能。显式使用deck模板路径：C:\Apps\boc_ppt_master\ppt-master\skills\ppt-master\templates\decks\中国银行
生成1页中国银行toc页，继承 02_toc.svg。总共有[总章节数]个章节标题：1....，2....。为每个TOC项补充一句简短说明，空余TOC槽删除或保持不可见。
使用wrapper已确认的BOC确认束；不要使用旧的“跳过八项确认”指令。如果当前运行环境仍强制ppt-master Eight Confirmations硬停，请只展示紧凑确认束并等待一次确认；确认后继续生成。
```

Save it as:

```text
C:\Apps\boc_ppt_master\ppt_chapters\toc.svg
```

Generate the ending page with:

```text
使用ppt-master技能。显式使用deck模板路径：C:\Apps\boc_ppt_master\ppt-master\skills\ppt-master\templates\decks\中国银行
生成1页中国银行ending页，继承 04_ending.svg，{{THANK_YOU}} 写入 "请批评指正"。
使用wrapper已确认的BOC确认束；不要使用旧的“跳过八项确认”指令。如果当前运行环境仍强制ppt-master Eight Confirmations硬停，请只展示紧凑确认束并等待一次确认；确认后继续生成。
```

Save it as:

```text
C:\Apps\boc_ppt_master\ppt_chapters\ending.svg
```

Keep only SVG outputs and required local assets in `C:\Apps\boc_ppt_master\ppt_chapters\asset`; delete all temporary `ppt-master` intermediate files.
