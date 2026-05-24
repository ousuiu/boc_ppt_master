# Content Pages Workflow

Use this workflow when the user says "根据原始材料做内容页", "content页", or equivalent wording.

## Step 1 - Read Raw Materials

Read every file under `C:\Apps\boc_ppt_master\raw_files` as source material. Convert Office/PPT/PDF/Excel/Web files to Markdown when needed by using the source conversion tools in `C:\Apps\boc_ppt_master\ppt-master\skills\ppt-master\scripts\source_to_md`.

Relevant upgraded converters include `pdf_to_md.py`, `doc_to_md.py`, `ppt_to_md.py`, `excel_to_md.py`, and `web_to_md.py`.

Keep each batch small. Prefer no more than about 5 content pages per run; reduce the number if the source is dense or the base model is weak.

## Step 2 - Propose Page Split and Stop

Organize the raw material into a proposed page split, then stop and wait for the user.

Use this response shape:

```text
建议做成 N 页PPT。
第1页内容是：...
第2页内容是：...
...
请问这样是否可以？
```

The stop is mandatory. The user may change total pages, page order, page titles, or page content. Do not create planning files or SVGs until the user confirms the split.

## Step 3 - Create Page Planning Markdown

After confirmation, create a new batch folder under `C:\Apps\boc_ppt_master\ppt_plan`.

Batch numbering rule:

- If no `content_batch_N` folder exists, use `content_batch_0`.
- Otherwise find the largest existing `N` and use `N + 1`.

Write one Markdown file per page:

```text
C:\Apps\boc_ppt_master\ppt_plan\content_batch_N\page1.md
C:\Apps\boc_ppt_master\ppt_plan\content_batch_N\page2.md
...
```

Use this instruction when drafting the plan files:

```text
参考/raw_files/里的文件，规划[总页面数]页PPT。
第1页是.....。
第2页是.....。

输出这[总页面数]页的PPT的详细规划的md文件到这个文件夹的/ppt_plan/content_batch_[批次序号]/目录下，每个页面的规划存一个md文件，md的文件名为page[页码序号].md，如果ppt_plan文件夹下面还没有content_batch_[批次序号]子文件夹则当前[批次序号]为0，如果有的话就找到已经存在的子文件夹中最大的[批次序号]，然后+1，从而决定这次的[批次序号]是什么。

用详尽的语言描述[总页面数]页PPT设计，涵盖每页的内容，内容页面结构，用字符的形式表达文字结构、箭头走向、图标和布局，精确描述所有表格内容和数字。如果页面比较空，使用image gen生图，也可以引用查找资料的过程中找到有价值的图片。图片或者其它要引用的资产放到/ppt_plan/asset/目录下，同时在PPT设计md文件中详细注明图片引用信息。
```

Include this color scheme in every page plan, unless a user explicitly replaces the brand system:

```markdown
### Color Scheme

| Role | HEX | Purpose |
| ---- | --- | ------- |
| **Background** | #FFFFFF | Content-page base background |
| **Primary** | #A50021 | BOC red for rules, structural emphasis and brand accents |
| **Primary dark / cover red** | #B40029 | Cover title, chapter section label and chapter rule |
| **Body text** | #1F2328 | Main titles and high-emphasis text |
| **Secondary text** | #5F6368 / #6B727C | Supporting text, labels and descriptions |
| **Tertiary text** | #7C838C / #8A9099 | English labels and page numbers |
| **Divider / border** | #E4E7EB / #E8EAED | Footer divider, TOC separators and dashed content boundary |
| **Placeholder text** | #9AA0A6 / #D8D8D8 / #E6E6E6 | Template-only content-area markers |
| **Reverse text** | #FFFFFF | Text on red or dark overlays when needed |
| **Reference data blue** | #4285F4 | Optional data-number color suggested in content SVG note |
```

## Step 4 - Generate Content SVGs

For each page plan, follow `skills/boc-ppt-builder/references/ppt-master-integration.md`, then call `ppt-master` with this prompt shape. The explicit deck template path is mandatory for the upgraded `ppt-master`:

```text
使用ppt-master技能。请读取 C:\Apps\boc_ppt_master\ppt-master\skills\ppt-master\SKILL.md，并按新版ppt-master流程执行。
显式使用deck模板路径：C:\Apps\boc_ppt_master\ppt-master\skills\ppt-master\templates\decks\中国银行
按照 C:\Apps\boc_ppt_master\ppt_plan\content_batch_[批次序号]\page[页码序号].md 的要求，只生成1页中国银行content页，继承 03_content.svg 的内容页结构。
本wrapper已完成分页确认，请把以下内容作为BOC确认束：canvas=ppt169；page_count=1；audience=中国银行管理层/业务条线汇报；style=稳健、克制、金融可信；colors/fonts/template均继承上述deck模板；formula_policy=mixed；image acquisition按该page md显式要求执行。
不要使用旧的“跳过八项确认”指令。如果当前运行环境仍强制ppt-master Eight Confirmations硬停，请只展示上述紧凑确认束并等待一次确认；确认后继续生成。
这一步不生成最终PPTX，只需要保留该页最终SVG，并把该SVG引用的本地模板资产复制到 C:\Apps\boc_ppt_master\ppt_plan\asset。
```

Save the resulting SVG to:

```text
C:\Apps\boc_ppt_master\ppt_plan\svg\page[页码序号].svg
```

Delete temporary `ppt-master` intermediate folders after extracting the final SVG and required local assets. When content SVGs are later moved into `ppt_chapters/cN-.../`, copy any non-template assets from `ppt_plan/asset/` into `ppt_chapters/asset/` as well. Keep `ppt-master` generation sequential inside each temporary project; only run independent page jobs in parallel if the active runtime can isolate them safely.
