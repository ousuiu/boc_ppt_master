---
label: 中国银行汇报模板
summary: A Bank of China branded executive reporting template for high-end consulting, work briefings, product presentations, operating analysis, and executive communication to state-owned bank leadership.
keywords:
  - Bank of China
  - BOC
  - Executive briefing
  - Consulting
  - Finance
category: Brand
primary_color: "#A50021"
use_cases: 高端咨询、工作汇报、产品宣讲、经营分析、战略沟通、管理层汇报、国有银行内部沟通
placeholders:
  01_cover: ["{{TITLE}}", "{{TEAM_NAME}}", "{{DATE}}"]
  02_toc:
    - "{{TOC_ITEM_1_TITLE}}"
    - "{{TOC_ITEM_1_DESC}}"
    - "{{TOC_ITEM_2_TITLE}}"
    - "{{TOC_ITEM_2_DESC}}"
    - "{{TOC_ITEM_3_TITLE}}"
    - "{{TOC_ITEM_3_DESC}}"
    - "{{TOC_ITEM_4_TITLE}}"
    - "{{TOC_ITEM_4_DESC}}"
    - "{{TOC_ITEM_5_TITLE}}"
    - "{{TOC_ITEM_5_DESC}}"
    - "{{TOC_ITEM_6_TITLE}}"
    - "{{TOC_ITEM_6_DESC}}"
    - "{{PAGE_NUM}}"
    - "{{TOTAL_PAGES}}"
  02_chapter: ["{{CHAPTER_NUM}}", "{{CHAPTER_TITLE}}", "{{PAGE_NUM}}", "{{TOTAL_PAGES}}"]
  03_content: ["{{PAGE_TITLE}}", "{{CONTENT_AREA}}", "{{PAGE_NUM}}", "{{TOTAL_PAGES}}"]
  04_ending: ["{{THANK_YOU}}"]
---

# 中国银行汇报模板 - Design Specification

> A Bank of China branded executive reporting template. This specification is regenerated from the current SVG files and reflects the manually revised layout filenames, placeholders, and local assets under `assets/`.

## I. Template Overview

- **Template ID**: `中国银行`
- **Display Name**: 中国银行汇报模板
- **Category**: Brand
- **Applicable Scenarios**: 高端咨询、工作汇报、产品宣讲、经营分析、战略沟通、管理层汇报、国有银行内部沟通
- **Target Audience**: 非业务背景体制内国有银行高管、部门负责人、经营管理与产品条线管理者
- **Design Tone**: 稳健、权威、克制、金融可信、国有大行品牌感；以中国银行红、官方标识、浅灰秩序线、留白和品牌背景图建立庄重专业气质。
- **Theme Mode**: Light theme. Cover / TOC / chapter / ending pages use local brand backgrounds; content pages use clean white reporting canvas.
- **Core Layout Files**: `01_cover.svg`, `02_toc.svg`, `02_chapter.svg`, `03_content.svg`, `04_ending.svg`
- **Required Local Assets**: `assets/cover_bg.png`, `assets/toc_bg.png`, `assets/end_bg.png`, `assets/boc_full_logo.png`
- **Optional Packaged Asset**: `assets/boc_logo.png` is present but not referenced by current SVG templates.

## II. Canvas Specification

| Property | Value |
| -------- | ----- |
| **Format** | `ppt169` |
| **Dimensions** | 1280 × 720 px |
| **viewBox** | `0 0 1280 720` |
| **Primary Safe Margin** | 40 px on content pages; 72 px remains the title anchor |
| **Content Boundary** | `x=40, y=112, w=1200, h=538` in `03_content.svg` |
| **TOC Flexible Area** | `x=72, y=190, w=1138, h=450` for the indexed TOC item matrix in `02_toc.svg` |
| **Brand Zone** | `x=1000, y=44, w=250, h=60` for `assets/boc_full_logo.png` |
| **Footer** | Page number baseline `y=690`; content divider `y=660` |

## III. Visual Theme

### Theme Style

- **Style**: Bank of China branded executive report
- **Theme**: Light theme with asset-backed brand pages
- **Tone**: official, financially credible, restrained, presentation-ready, structured for management communication

### Color Scheme

| Role | HEX | Purpose |
| ---- | --- | ------- |
| **Background** | `#FFFFFF` | Content-page base background |
| **Primary** | `#A50021` | BOC red for rules, structural emphasis and brand accents |
| **Primary dark / cover red** | `#B40029` | Cover title, chapter section label and chapter rule |
| **Body text** | `#1F2328` | Main titles and high-emphasis text |
| **Secondary text** | `#5F6368` / `#6B727C` | Supporting text, labels and descriptions |
| **Tertiary text** | `#7C838C` / `#8A9099` | English labels and page numbers |
| **Divider / border** | `#E4E7EB` / `#E8EAED` | Footer divider, TOC separators and dashed content boundary |
| **Placeholder text** | `#9AA0A6` / `#D8D8D8` / `#E6E6E6` | Template-only content-area markers |
| **Reverse text** | `#FFFFFF` | Text on red or dark overlays when needed |
| **Reference data blue** | `#4285F4` | Optional data-number color suggested in content SVG note |

### Shadow Style

- **Migrated card/page-element shadow**: use `filter="url(#cardShadow)"` for cards or elevated page elements that need depth.
- **Shadow filter definition**: `dx="0"`, `dy="4"`, `stdDeviation="8"`, `flood-color="#000"`, `flood-opacity="0.1"`; filter bounds `x="-10%" y="-10%" width="120%" height="120%"`.
- **Scope rule**: this is the only migrated style from `examples/ppt169_高端咨询风_汽车认证五年战略规划`; keep all BOC colors, typography, layout anchors, logo placement and background assets unchanged.

### Image Resource List

| Asset | Used By | Role |
| ----- | ------- | ---- |
| `assets/cover_bg.png` | `01_cover.svg` | Full-canvas cover background |
| `assets/toc_bg.png` | `02_toc.svg`, `02_chapter.svg` | TOC and chapter background |
| `assets/end_bg.png` | `04_ending.svg` | Full-canvas ending background |
| `assets/boc_full_logo.png` | All SVG layouts | Official upper-right BOC logo lockup |
| `assets/boc_logo.png` | Not currently referenced | Optional standalone logo mark for variants |

## IV. Typography System

**Typography direction**: CJK-primary corporate sans; clean PPT-safe stacks for Chinese executive communication.

| Role | Stack |
| ---- | ----- |
| **Title** | `SimHei, Arial, sans-serif` |
| **Body** | `SimHei, PingFang SC, Arial, sans-serif` |
| **Emphasis / Numeric** | `Arial, SimHei, sans-serif` |
| **Code** | `Consolas, Courier New, monospace` |

**Baseline**: Body font size = 18 px for content-heavy corporate pages.

| Purpose | Size | Weight | Current Usage |
| ------- | ---- | ------ | ------------- |
| Cover title | 60 px | 700 | `{{TITLE}}` |
| Cover team / presenter | 30 px | 700 | `{{TEAM_NAME}}` |
| Cover date | 15 px | 700 | `{{DATE}}` |
| TOC Chinese heading | 34 px | 700 | Fixed `目录` |
| TOC English label | 13 px | Regular | Fixed `CONTENTS` |
| Chapter section label | 16 px | 500 | `第 {{CHAPTER_NUM}}节` |
| Chapter title | 48 px | Bold | `{{CHAPTER_TITLE}}` |
| Content title | 30 px | 700 | `{{PAGE_TITLE}}` |
| TOC item number | 42 px | 700 | `01` to `06` fixed item numbers |
| TOC item title | 23 px | 700 | `{{TOC_ITEM_N_TITLE}}` |
| TOC item description | 14 px | Regular | `{{TOC_ITEM_N_DESC}}` |
| Content placeholder | 18 px / 14 px | Regular | `{{CONTENT_AREA}}` and viewport note |
| Page number | 14 px | Regular | `{{PAGE_NUM}} / {{TOTAL_PAGES}}` |
| Ending headline | 50 px | 700 | `{{THANK_YOU}}` |

## V. Layout Principles

### Page Structure

- **Brand lockup**: all five templates use `assets/boc_full_logo.png` at `x=1000, y=44, width=250, height=60`.
- **Cover**: full-page background, upper-right logo, right-aligned title/team/date block anchored at `x=1170` (`1280 - 110`) with `text-anchor="end"` for PPTX-safe right alignment.
- **TOC**: fixed title area and logo, with a 2-column × 3-row indexed agenda matrix. Unused items may be removed by the downstream project executor.
- **Chapter**: centered section label and chapter title over `assets/toc_bg.png`.
- **Content**: white working canvas with fixed page title, BOC-red underline, maximized dashed flexible content boundary and centered pagination.
- **Ending**: `assets/end_bg.png`, upper-right logo and simple red closing headline.

### Layout Pattern Library

| Pattern | Suitable Scenarios |
| ------- | ------------------ |
| **Indexed TOC matrix** | 1–6 chapters; default 2×3 matrix, remove unused entries or collapse to one column for 1–3 chapters |
| **KPI grid** | 2×2 or 2×3 metrics on content pages |
| **Left text / right visual** | Product, policy, case or strategy explanation |
| **Three-column cards** | Parallel points, comparison dimensions, initiative lists |
| **Four-quadrant matrix** | Classifications, risk/opportunity mapping, portfolio view |
| **Dashboard style** | Operating analysis with KPI cards plus chart/table evidence |
| **List + explanation** | Management recommendations, work plans, action items |

## VI. Icon Usage Specification

- **Source**: `templates/icons/` may be used by project pages when needed.
- **Template default**: current SVG layouts do not include icon placeholders or `<use data-icon="...">` references.
- **Style rule**: use BOC red icon accents sparingly and avoid decorative clutter in official bank presentations.

| Purpose | Suggested Icon Type |
| ------- | ------------------- |
| Status / completion | check-circle |
| Risk / warning | alert-triangle |
| Trend / growth | trending-up |
| Finance / data | bar-chart |

## VII. Visualization Reference List

The base package keeps `03_content.svg` generic. Use visualization templates only when source content requires data or structured analysis.

`03_content.svg` provides a maximized content viewport at `x=40, y=112, w=1200, h=538`. Every visualization listed in `templates/charts/charts_index.json` must target this viewport when used with this template. Prefer adapting the visualization's internal layout to fill the viewport. If a full 1280 × 720 visualization template must be preserved, scale it by `min(1200/1280, 538/720) = 0.7472` and center it inside the viewport.

| Visualization Type | Recommended Use | Placement |
| ------------------ | --------------- | --------- |
| KPI cards | Executive summary, performance highlights | Inside `x=40, y=112, w=1200, h=538` |
| Bar / column chart | Performance comparison, product metrics | Inside content boundary |
| Line chart | Trends over time | Inside content boundary |
| Table | Operating analysis, risk list, work plan | Inside content boundary |
| Matrix / quadrant | Strategy, segmentation, priority mapping | Inside content boundary |
| Timeline / roadmap | Implementation plan, milestone tracking | Inside content boundary |

## VIII. Spacing Specification

| Page | Anchor Rules |
| ---- | ------------ |
| Cover | Right-aligned block uses fixed PPTX-safe `x=1170` and `text-anchor="end"`; baselines y=320, 375, 415 |
| TOC | Heading x=92/y=112; English x=94/y=145; red rule x=92–320/y=166; indexed entries occupy x=92–1186/y=202–612 |
| Chapter | Label x=640/y=290; title x=640/y=400 |
| Content | Title x=72/y=80; underline x=72–300/y=98; boundary x=40/y=112/w=1200/h=538; divider y=660 |
| Ending | Closing headline starts at x=500/y=350 |

## IX. SVG Technical Constraints

- All SVG files must keep `width="1280" height="720" viewBox="0 0 1280 720"`.
- Each SVG layout defines the reusable `cardShadow` filter for migrated card/page-element depth; apply it with `filter="url(#cardShadow)"` only to cards or elevated elements, not to brand logo/background assets.
- Keep all asset references local and relative (`assets/...`) so copied project templates remain functional.
- Avoid external CSS, script, animation, `foreignObject`, remote URLs and non-local image references.
- Use HEX colors and explicit opacity attributes when transparency is needed.
- Keep placeholders as editable SVG `<text>` nodes wherever possible.
- Current SVG asset references:
  - `01_cover.svg`: `assets/cover_bg.png`, `assets/boc_full_logo.png`
  - `02_toc.svg`: `assets/toc_bg.png`, `assets/boc_full_logo.png`
  - `02_chapter.svg`: `assets/toc_bg.png`, `assets/boc_full_logo.png`
  - `03_content.svg`: `assets/boc_full_logo.png`
  - `04_ending.svg`: `assets/end_bg.png`, `assets/boc_full_logo.png`
- `02_chapter.svg` intentionally uses only the centered section label and chapter title; do not add divider rules unless the chapter layout is intentionally redesigned.
- Escape XML-reserved characters such as `&amp;`, `<`, `>`, `&quot;`, `&apos;` when adding text.

## X. Placeholder Specification

| Placeholder | Purpose | Pages | Current SVG |
| ----------- | ------- | ----- | ----------- |
| `{{TITLE}}` | Main presentation title | Cover | Present |
| `{{TEAM_NAME}}` | Presenter team / reporting organization | Cover | Present |
| `{{DATE}}` | Date / reporting period | Cover | Present |
| `{{TOC_ITEM_1_TITLE}}`–`{{TOC_ITEM_6_TITLE}}` | Indexed TOC item titles | TOC | Present |
| `{{TOC_ITEM_1_DESC}}`–`{{TOC_ITEM_6_DESC}}` | Indexed TOC item descriptions | TOC | Present |
| `{{CONTENT_AREA}}` | Flexible generated content marker | Content | Present |
| `{{PAGE_NUM}}` | Current page number | TOC, Chapter, Content | Present |
| `{{TOTAL_PAGES}}` | Total page count | TOC, Chapter, Content | Present |
| `{{CHAPTER_NUM}}` | Chapter number | Chapter | Present |
| `{{CHAPTER_TITLE}}` | Chapter title | Chapter | Present |
| `{{PAGE_TITLE}}` | Content page title | Content | Present |
| `{{THANK_YOU}}` | Closing headline | Ending | Present |
| `{{SUBTITLE}}` | Optional canonical cover subtitle | Cover | Not present |
| `{{AUTHOR}}` | Optional canonical author/presenter | Cover | Not present; use `{{TEAM_NAME}}` in this template |
| `{{CONTACT_INFO}}` | Optional closing contact block | Ending | Not present |
| `{{SECTION_NAME}}` | Optional content section label | Content | Not present |
| `{{KEY_MESSAGE}}` | Optional executive takeaway | Content | Not present |
| `{{SOURCE}}` | Optional source / footnote | Content | Not present |

## XI. Usage Guide

- Use this template when the deck must feel official, financially credible, executive-ready and clearly aligned with Bank of China identity.
- Copy all SVG files, `design_spec.md`, and the entire `assets/` directory when using this template in a project.
- Keep generated content inside `03_content.svg`'s flexible bounds unless creating a project-specific custom page.
- For TOC pages, replace the indexed `{{TOC_ITEM_N_TITLE}}` / `{{TOC_ITEM_N_DESC}}` placeholders with chapter text and remove unused agenda entries.
- Use BOC red sparingly for structure, key numbers and critical conclusions; avoid long red paragraphs.
- Preserve `assets/boc_full_logo.png` as the default brand lockup source. Use `assets/boc_logo.png` only for variants that need the standalone mark.
- Preserve the current file names exactly: `01_cover.svg`, `02_toc.svg`, `02_chapter.svg`, `03_content.svg`, `04_ending.svg`.
