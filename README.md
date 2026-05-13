# BOC PPT Master

这是一个用于制作中国银行风格汇报 PPT 的本地项目。项目里已经包含 `ppt-master`、中国银行模板、样例原始材料，以及一个面向主流 Agent 工具的通用工作流包：`boc-ppt-builder`。

它适合这样使用：先把材料拆成一批内容页，再把内容页按章节整理，最后自动补齐封面、目录、章节页、结束页并导出一个完整的 PPTX。

## 目录结构

```text
C:\boc_ppt_master
├─ raw_files\                 原始材料，做内容页时从这里读取
├─ ppt_plan\                  内容页规划和中间产物
├─ ppt_chapters\              最终组装 PPT 的工作区
├─ ppt-master\                底层 PPT/SVG 生成工具和中国银行模板
└─ skills\boc-ppt-builder\    本项目专用的 PPT 编排工作流包
```

常用输出位置：

```text
ppt_plan\content_batch_N\pageM.md      每一页内容页的设计规划
ppt_plan\svg\pageM.svg                 生成好的内容页 SVG
ppt_chapters\cover.svg                 封面
ppt_chapters\toc.svg                   目录
ppt_chapters\chapterN.svg              第 N 个章节页
ppt_chapters\ending.svg                结束页
ppt_chapters\output_svg\               最终排序后的 SVG
ppt_chapters\output_pptx\output.pptx   最终 PPTX
```

## 推荐工作流

### 1. 根据原始材料做内容页

把本批要处理的材料放进 `raw_files\`。一次建议只放适合生成 3 到 5 页内容页的材料，材料太多时分批处理效果更稳。

对当前使用的 Agent 说：

```text
根据原始材料做内容页
```

流程会先读取 `raw_files\`，提出分页建议，例如“建议做成 5 页 PPT，第 1 页内容是……”。这里会停下来等你确认。你可以改页数、改顺序、改每页内容。

确认后，会生成：

```text
ppt_plan\content_batch_N\page1.md
ppt_plan\content_batch_N\page2.md
...
ppt_plan\svg\page1.svg
ppt_plan\svg\page2.svg
...
```

### 2. 整理章节并生成封面、目录、章节页

把内容页 SVG 按章节放进 `ppt_chapters\`，格式如下：

```text
ppt_chapters\
├─ asset\
├─ c1-第一章标题\
│  ├─ page1.svg
│  └─ page2.svg
├─ c2-第二章标题\
│  └─ page1.svg
```

如果 SVG 引用了图片、logo 或其他资产，把这些文件放进：

```text
ppt_chapters\asset\
```

然后对当前使用的 Agent 说：

```text
做PPT的封面和章节
```

它会先检查章节目录和资产引用是否完整。检查通过后，会向你要封面标题和副标题，然后生成：

```text
ppt_chapters\cover.svg
ppt_chapters\toc.svg
ppt_chapters\chapter1.svg
ppt_chapters\chapter2.svg
ppt_chapters\ending.svg
```

### 3. 整合 PPT

章节内容和封面/目录/章节页都准备好后，对当前使用的 Agent 说：

```text
整合PPT
```

它会检查所有文件是否齐全，然后按下面顺序组织页面：

```text
封面
目录
第 1 章章节页
第 1 章内容页...
第 2 章章节页
第 2 章内容页...
结束页
```

最终输出：

```text
ppt_chapters\output_pptx\output.pptx
```

## 手动检查命令

如果只想检查章节结构和资产引用：

```powershell
python skills\boc-ppt-builder\scripts\validate_chapters.py --project-root C:\boc_ppt_master --fix-assets
```

如果想直接整理并导出最终 PPTX：

```powershell
python skills\boc-ppt-builder\scripts\assemble_and_export.py --project-root C:\boc_ppt_master
```

## 支持的 Agent 工具

`boc-ppt-builder` 不是 Codex 专用 skill。核心说明统一放在：

```text
skills\boc-ppt-builder\AGENT.md
```

各主流工具入口如下：

```text
AGENTS.md                                  OpenClaw / Codex / AGENTS.md 兼容工具
CLAUDE.md                                  Claude Code
.cursor\rules\boc-ppt-builder.mdc          Cursor
.cursorrules                               Cursor 旧版规则入口
.github\copilot-instructions.md            VS Code + GitHub Copilot
CODEBUDDY.md                               CodeBuddy
.codebuddy\CODEBUDDY.md                    CodeBuddy workspace memory
.codebuddy\rules\boc-ppt-builder\RULE.mdc  CodeBuddy project rule
.codebuddy\skills\boc-ppt-builder\SKILL.md CodeBuddy skill adapter
skills\boc-ppt-builder\SKILL.md            Skill-folder 兼容入口
```

后续如果要改工作流，优先改 `skills\boc-ppt-builder\AGENT.md` 和对应 `references\` 文件；其它入口文件只保留轻量指向，避免多处内容不一致。

## 使用建议

- `raw_files\` 里放当前批次需要处理的材料，不要一次塞完整大报告。
- 内容页生成后，先人工看一下 `ppt_plan\svg\` 的 SVG，再放进 `ppt_chapters\`。
- 章节目录必须按 `c1-标题`、`c2-标题` 这样的格式命名。
- 章节内内容页必须命名为 `page1.svg`、`page2.svg`。
- 所有 SVG 引用的本地图片资产，尽量统一放进 `ppt_chapters\asset\`。
- `ppt-master\` 是底层工具目录，通常不用手动改。

## 当前状态

项目已经包含中国银行模板和样例 `raw_files`。`ppt_chapters` 当前可以作为最终组装区使用；当其中内容页和章节结构准备好后，就可以运行“整合PPT”生成最终文件。
