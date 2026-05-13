from __future__ import annotations

from pathlib import Path
from textwrap import dedent
import html


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "projects" / "同业落地案例_中国银行_ppt169_20260508_ppt169_20260508"

W, H = 1280, 720
TITLE_FONT = "SimHei, Arial, sans-serif"
BODY_FONT = "SimHei, Microsoft YaHei, Arial, sans-serif"
EMPH_FONT = "Arial, SimHei, sans-serif"

COLORS = {
    "background": "#FFFFFF",
    "secondary_bg": "#F8F9FA",
    "tint_bg": "#FFF7F7",
    "primary": "#A50021",
    "primary_dark": "#B40029",
    "accent_blue": "#4285F4",
    "accent_green": "#2E7D32",
    "body_text": "#1F2328",
    "secondary_text": "#5F6368",
    "tertiary_text": "#8A9099",
    "border": "#E4E7EB",
    "divider": "#E8EAED",
    "pale_red": "#F3D7DC",
    "white": "#FFFFFF",
    "shadow": "#000000",
}


def esc(text: str) -> str:
    return html.escape(str(text), quote=True)


def text(x, y, content, size=14, fill="body_text", weight="400", family=BODY_FONT,
         anchor=None, extra=""):
    anchor_attr = f' text-anchor="{anchor}"' if anchor else ""
    return (
        f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
        f'font-weight="{weight}" fill="{COLORS.get(fill, fill)}"{anchor_attr}{extra}>'
        f'{esc(content)}</text>'
    )


def multiline(x, y, lines, size=14, fill="body_text", weight="400", line_h=20,
              family=BODY_FONT, anchor=None):
    anchor_attr = f' text-anchor="{anchor}"' if anchor else ""
    tspans = []
    for i, line in enumerate(lines):
        dy = 0 if i == 0 else line_h
        tspans.append(f'<tspan x="{x}" dy="{dy}">{esc(line)}</tspan>')
    return (
        f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
        f'font-weight="{weight}" fill="{COLORS.get(fill, fill)}"{anchor_attr}>'
        f'{"".join(tspans)}</text>'
    )


def chrome(title: str, page: int, source: str) -> str:
    return f"""
  <g id="header">
    <image href="../templates/assets/boc_full_logo.png" x="1000" y="44" width="250" height="60" preserveAspectRatio="xMidYMid meet"/>
    {text(72, 80, title, 30, "body_text", "700", TITLE_FONT)}
    <line x1="72" y1="98" x2="300" y2="98" stroke="{COLORS["primary"]}" stroke-width="3"/>
    {text(1208, 128, "03 同业落地实践", 12, "tertiary_text", "400", BODY_FONT, anchor="end")}
  </g>
  <g id="footer">
    <line x1="72" y1="660" x2="1208" y2="660" stroke="{COLORS["border"]}" stroke-width="1.2"/>
    {text(72, 690, source, 11, "tertiary_text", "400", BODY_FONT)}
    {text(640, 690, f"{page} / 6", 14, "tertiary_text", "400", BODY_FONT, anchor="middle")}
    {text(1208, 690, "内部资料整理", 11, "tertiary_text", "400", BODY_FONT, anchor="end")}
  </g>
"""


def svg(title: str, page: int, source: str, body: str) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="3" stdDeviation="6" flood-color="#000000" flood-opacity="0.08"/>
    </filter>
  </defs>
  <rect x="0" y="0" width="{W}" height="{H}" fill="{COLORS["background"]}"/>
  {chrome(title, page, source)}
  {body}
</svg>
"""


def rounded_rect(x, y, w, h, fill="white", stroke="border", sw=1, rx=8, extra=""):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
        f'fill="{COLORS.get(fill, fill)}" stroke="{COLORS.get(stroke, stroke)}" '
        f'stroke-width="{sw}"{extra}/>'
    )


def tag(x, y, label, fill="tint_bg", color="primary"):
    return f'<g>{rounded_rect(x, y - 16, 74, 22, fill, "pale_red", 1, 11)}{text(x + 37, y, label, 12, color, "700", BODY_FONT, "middle")}</g>'


def metric_box(x, y, w, label, value):
    return f"""
      <g>
        <rect x="{x}" y="{y}" width="{w}" height="46" rx="6" fill="{COLORS["tint_bg"]}" stroke="{COLORS["pale_red"]}" stroke-width="1"/>
        {text(x + 12, y + 18, label, 11, "secondary_text", "400")}
        {text(x + 12, y + 37, value, 15, "primary_dark", "700", EMPH_FONT)}
      </g>
    """


def small_flow(x, y, steps, w=520):
    gap = 8
    step_w = (w - gap * (len(steps) - 1)) / len(steps)
    parts = []
    for i, step in enumerate(steps):
        sx = x + i * (step_w + gap)
        parts.append(
            f'<rect x="{sx:.1f}" y="{y}" width="{step_w:.1f}" height="32" rx="5" fill="{COLORS["secondary_bg"]}" stroke="{COLORS["divider"]}" stroke-width="1"/>'
        )
        parts.append(text(round(sx + step_w / 2, 1), y + 21, step, 11, "secondary_text", "700", BODY_FONT, "middle"))
        if i < len(steps) - 1:
            ax = sx + step_w + 1
            parts.append(f'<line x1="{ax:.1f}" y1="{y + 16}" x2="{ax + gap - 2:.1f}" y2="{y + 16}" stroke="{COLORS["primary"]}" stroke-width="1.5"/>')
            parts.append(f'<polygon points="{ax + gap - 2:.1f},{y + 16} {ax + gap - 8:.1f},{y + 12} {ax + gap - 8:.1f},{y + 20}" fill="{COLORS["primary"]}"/>')
    return "".join(parts)


def case_panel(x, y, bank, case_name, tagline, img, metrics, flow, insight):
    mx = x + 18
    return f"""
    <g id="case-{esc(bank).replace(' ', '-')}">
      {rounded_rect(x, y, 570, 508, "white", "border", 1, 8)}
      <rect x="{x}" y="{y}" width="5" height="508" rx="2.5" fill="{COLORS["primary"]}"/>
      {text(mx, y + 31, bank, 18, "body_text", "700", TITLE_FONT)}
      {text(mx, y + 55, case_name, 13, "primary_dark", "700")}
      {multiline(mx, y + 81, tagline, 12, "secondary_text", "400", 17)}
      <image href="../images/case_images/{img}" x="{mx}" y="{y + 112}" width="250" height="141" preserveAspectRatio="xMidYMid slice"/>
      <rect x="{mx}" y="{y + 112}" width="250" height="141" fill="none" stroke="{COLORS["border"]}" stroke-width="1"/>
      <g id="metrics-{esc(bank).replace(' ', '-')}">
        {metric_box(mx + 270, y + 112, 128, metrics[0][0], metrics[0][1])}
        {metric_box(mx + 410, y + 112, 128, metrics[1][0], metrics[1][1])}
        {metric_box(mx + 270, y + 170, 128, metrics[2][0], metrics[2][1])}
        {metric_box(mx + 410, y + 170, 128, metrics[3][0], metrics[3][1])}
      </g>
      {text(mx, y + 284, "能力链路", 13, "body_text", "700")}
      {small_flow(mx, y + 300, flow, 530)}
      <rect x="{mx}" y="{y + 354}" width="530" height="72" rx="6" fill="{COLORS["secondary_bg"]}" stroke="{COLORS["divider"]}" stroke-width="1"/>
      {text(mx + 14, y + 379, "对本行启示", 13, "primary_dark", "700")}
      {multiline(mx + 95, y + 379, insight, 12, "secondary_text", "400", 17)}
    </g>
    """


def overview_page():
    stages = [
        ("知识资产沉淀", "制度、研报、流程、问答"),
        ("语义检索/RAG", "向量切片、证据召回"),
        ("大模型助手", "员工提效、文档智能"),
        ("智能体闭环", "工具调用、流程执行"),
    ]
    axis = []
    for i, (label, desc) in enumerate(stages):
        cx = 178 + i * 300
        axis.append(f'<circle cx="{cx}" cy="156" r="13" fill="{COLORS["primary"]}"/>')
        axis.append(text(cx, 190, label, 17, "body_text", "700", BODY_FONT, "middle"))
        axis.append(text(cx, 215, desc, 12, "secondary_text", "400", BODY_FONT, "middle"))
        if i < 3:
            x1 = cx + 18
            x2 = cx + 282
            axis.append(f'<line x1="{x1}" y1="156" x2="{x2}" y2="156" stroke="{COLORS["border"]}" stroke-width="3"/>')
            axis.append(f'<polygon points="{x2},156 {x2 - 9},151 {x2 - 9},161" fill="{COLORS["border"]}"/>')
    cases = [
        ("JPMorgan", "员工入口"), ("Morgan Stanley", "投顾 RAG"), ("Citi", "文档智能"),
        ("HSBC", "全行平台"), ("工行", "模型矩阵"), ("建行", "场景覆盖"),
        ("农行", "知识增强"), ("邮储", "基层助手"), ("招行", "投研知识库"), ("兴业", "智能体"),
    ]
    grid = []
    for i, (name, kw) in enumerate(cases):
        col = i % 5
        row = i // 5
        x = 76 + col * 225
        y = 258 + row * 70
        grid.append(rounded_rect(x, y, 190, 48, "white", "border", 1, 6))
        grid.append(text(x + 16, y + 21, name, 15, "body_text", "700"))
        grid.append(text(x + 16, y + 39, kw, 12, "primary_dark", "700"))
    rows = [
        ("员工级通用助手", "JPMorgan / Citi / HSBC", "20万用户、175,000+员工、20,000+开发者", "统一入口与安全环境"),
        ("专业知识库/RAG", "Morgan Stanley / 招行 / 农行", "10万文档、>98%顾问团队采用、数万用户", "找得准、答得出、可追溯"),
        ("业务流程智能化", "建行 / 邮储 / 工行", "46领域、3.9万+网点、200+场景", "授信、客服、网点、研发"),
        ("企业级智能体平台", "兴业 / JPMorgan agents / Citi Squad", "200+智能体、260+场景", "模型服务、评测、运营"),
    ]
    table = []
    y0 = 426
    table.append(f'<rect x="72" y="{y0}" width="1136" height="184" rx="6" fill="{COLORS["white"]}" stroke="{COLORS["border"]}" stroke-width="1"/>')
    table.append(f'<rect x="72" y="{y0}" width="1136" height="34" rx="6" fill="{COLORS["secondary_bg"]}"/>')
    headers = [("路径", 92), ("代表案例", 296), ("公开数字", 590), ("体现能力", 910)]
    for label, x in headers:
        table.append(text(x, y0 + 23, label, 13, "body_text", "700"))
    for i, row in enumerate(rows):
        yy = y0 + 34 + i * 37
        table.append(f'<line x1="72" y1="{yy}" x2="1208" y2="{yy}" stroke="{COLORS["divider"]}" stroke-width="1"/>')
        table.append(text(92, yy + 24, row[0], 12, "body_text", "700"))
        table.append(text(296, yy + 24, row[1], 12, "secondary_text"))
        table.append(text(590, yy + 24, row[2], 12, "primary_dark", "700"))
        table.append(text(910, yy + 24, row[3], 12, "secondary_text"))
    body = f"""
  <g id="takeaway">
    <rect x="72" y="116" width="1136" height="44" rx="6" fill="{COLORS["tint_bg"]}" stroke="{COLORS["pale_red"]}" stroke-width="1"/>
    {text(92, 144, "核心判断：银行 AI 落地正在从“知识问答”升级为“企业级智能体与流程闭环”。", 17, "primary_dark", "700")}
  </g>
  <g id="evolution-axis">{"".join(axis)}</g>
  <g id="case-matrix">
    {text(72, 246, "10 个公开案例覆盖四类落地路径", 16, "body_text", "700")}
    {"".join(grid)}
  </g>
  <g id="overview-table">{"".join(table)}</g>
"""
    return svg("同业落地概况：银行 AI 正从知识问答走向企业级智能体", 1,
               "Sources: JPMorgan, OpenAI, Citi, HSBC, ICBC, CCB, ABC, PSBC, CMB, CIB", body)


def page2():
    body = case_panel(
        72, 128, "JPMorgan Chase", "LLM Suite",
        ["把大模型先做成员工级安全入口", "再逐步接入内部数据和 AI agents"],
        "case_01_jpmorgan_llm_suite.png",
        [("上线节奏", "2024 夏季"), ("采用规模", "200,000 users"), ("时间口径", "8个月内"), ("后续方向", "AI agents")],
        ["员工入口", "安全套件", "内容生成", "内部数据", "Agents"],
        ["先建立合规统一入口，再把知识库、工作流和智能体逐步接入。"],
    ) + case_panel(
        638, 128, "Morgan Stanley", "AI Assistant / Debrief",
        ["以财富管理投顾知识库为核心", "用 evals、复核和零留存建立信任"],
        "case_02_morgan_stanley_ai_assistant.png",
        [("采用率", ">98%团队"), ("语料规模", "100,000文档"), ("访问率", "20%→80%"), ("安全", "零数据留存")],
        ["投顾问题", "知识库", "RAG回答", "人工复核", "CRM跟进"],
        ["专业知识库的价值不在“能问”，而在可信、可复核、可持续扩展。"],
    )
    return svg("国际大行实践（一）：员工级入口与投顾知识库", 2,
               "Sources: JPMorgan Chase Tech Blog; OpenAI Morgan Stanley customer story", body)


def page3():
    body = case_panel(
        72, 128, "Citi", "Citi Assist / Stylus / Squad",
        ["全球扩展员工 AI 工具矩阵", "覆盖政策查询、文档智能和协同工作流"],
        "case_03_citi_assist_stylus.png",
        [("市场覆盖", "80个国家/地区"), ("员工覆盖", "175,000+"), ("工具1", "Assist"), ("工具2", "Stylus")],
        ["内部政策", "Assist", "文档智能", "Stylus", "Squad"],
        ["制度、文档、流程类知识可按任务拆成工具矩阵，而非单一聊天入口。"],
    ) + case_panel(
        638, 128, "HSBC", "Enterprise GenAI",
        ["以全行平台和责任 AI 治理承接多条线场景", "从研发助手扩展到客户服务与信贷分析"],
        "case_04_hsbc_genai_platform.png",
        [("运行用例", "600+"), ("开发者", "20,000+"), ("编码效率", "15%"), ("客户交互", "300万/年")],
        ["平台底座", "开发助手", "服务助手", "信贷分析", "生命周期治理"],
        ["平台治理要和场景扩展同步建设，否则规模化会先遭遇责任 AI 与生命周期管理瓶颈。"],
    )
    return svg("国际大行实践（二）：文档智能、上下文搜索与全行 GenAI 平台", 3,
               "Sources: Citi Perspectives; HSBC Transforming HSBC with AI", body)


def page4():
    body = case_panel(
        72, 128, "工商银行", "“工银智涌”企业级金融大模型体系",
        ["全栈自主可控、全域场景赋能", "构建模型矩阵、知识架构和算力云体系"],
        "case_05_icbc_gongyin_zhiyong.png",
        [("模型矩阵", "十余个大模型"), ("传统模型", "2000+"), ("业务领域", "20+"), ("落地场景", "200+")],
        ["算力云", "模型矩阵", "五级知识", "工具安全", "业务场景"],
        ["知识库需要进入模型、工具、安全和运营的企业级体系，而不是独立组件。"],
    ) + case_panel(
        638, 128, "建设银行", "DeepSeek-R1 金融大模型",
        ["以金融推理底座覆盖全集团场景", "将 AI 助手、工具箱、代码解释器和向量知识库组合落地"],
        "case_06_ccb_financial_llm.png",
        [("员工覆盖", "一半以上"), ("业务领域", "46个"), ("场景", "200+"), ("2024应用", "168个")],
        ["R1底座", "私有部署", "AI助手", "向量知识库", "业务提效"],
        ["业务收益要用分钟级压缩、覆盖率和场景数表达，管理层才容易判断投入价值。"],
    )
    return svg("国内大行实践（一）：企业级金融大模型与全行场景覆盖", 4,
               "Sources: 工商银行/中国电子银行网；新华财经/新浪财经", body)


def page5():
    body = case_panel(
        72, 128, "农业银行", "ChatABC",
        ["较早披露的金融大模型应用", "以知识增强、检索增强和 RLHF 转化行内知识"],
        "case_07_abc_chatabc.png",
        [("发布节点", "2023-03-31"), ("模型规模", "百亿级参数"), ("技术路线", "RAG+RLHF"), ("平台化", "MaaS")],
        ["内部知识", "精调提示", "检索增强", "ChatABC", "工单辅助"],
        ["知识增强需要与模型调优、反馈机制、人工标注共同设计。"],
    ) + case_panel(
        638, 128, "邮储银行", "“小邮助手”",
        ["面向全国网点和员工的企业级业务助手", "形成问答、SOP、AI 陪练和知识社区闭环"],
        "case_08_psbc_xiaoyou_assistant.png",
        [("覆盖网点", "3.9万+"), ("覆盖员工", "33万+"), ("效率提升", "80%以上"), ("日均问题", "5万+")],
        ["员工提问", "精准解答", "SOP指引", "知识沉淀", "效率提升"],
        ["基层推广价值适合用员工覆盖、日均处理和效率提升三类指标证明。"],
    )
    return svg("国内大行实践（二）：金融知识增强与基层员工助手", 5,
               "Sources: 农业银行微信/中国电子银行网；中国邮政集团", body)


def page6():
    body = case_panel(
        72, 128, "招商银行", "招银智库 AI 小研",
        ["依托招银智库研究资源平台", "把投研内容升级为问答、摘要和热点追踪入口"],
        "case_09_cmb_ai_xiaoyan.png",
        [("公开节点", "2025-01-17"), ("底座", "通义千问"), ("服务用户", "数万名"), ("功能", "问答/研报/热点")],
        ["研究资源", "金融语义", "智能问答", "Chat研报", "一线研判"],
        ["可优先选择高价值知识资产，做专业问答入口并嵌入一线工作流。"],
    ) + case_panel(
        638, 128, "兴业银行", "“智慧兴业”智能体体系",
        ["围绕统一模型服务平台构建智能体和员工 AI 助手", "推动数字兴业向智慧兴业升级"],
        "case_10_cib_ai_agents.png",
        [("公开节点", "2026-04-30"), ("智能体", "200+"), ("场景", "260+"), ("工程", "数据/知识/模型")],
        ["数据工程", "知识工程", "模型平台", "智能体", "场景运营"],
        ["智能体规模化需要统一模型服务、评测运营和知识工程共同支撑。"],
    )
    return svg("国内银行实践（三）：投研知识库与智能体体系化运营", 6,
               "Sources: 招商银行招银智库项目组/金融电子化；兴业银行官网", body)


def write_specs():
    design_spec = dedent("""
    # 同业落地案例 - Design Spec

    ## I. Project Information

    | Item | Value |
    | ---- | ----- |
    | **Project Name** | 同业落地案例_中国银行 |
    | **Canvas Format** | ppt169 (1280×720) |
    | **Page Count** | 6 |
    | **Design Style** | Top Consulting, Bank of China branded executive report |
    | **Target Audience** | 中国银行内部管理层、AI/知识库/数字化相关部门负责人 |
    | **Use Case** | 同业 AI 落地实践汇报，接续原文件“同业落地实践”章节 |
    | **Created Date** | 2026-05-08 |

    ## II. Canvas Specification

    | Property | Value |
    | -------- | ----- |
    | **Format** | PPT 16:9 |
    | **Dimensions** | 1280 × 720 px |
    | **viewBox** | `0 0 1280 720` |
    | **Margins** | 内容页主安全边界 40 px；标题锚点 x=72/y=80 |
    | **Content Area** | x=40, y=112, w=1200, h=538 |

    ## III. Visual Theme

    ### Theme Style

    - **Style**: 中国银行红白内容页 + 管理层咨询汇报
    - **Theme**: Light theme
    - **Tone**: 稳健、可信、克制、结论先行；以浅灰秩序线、BOC 红强调和左右对标结构形成专业感。

    ### Color Scheme

    | Role | HEX | Purpose |
    | ---- | --- | ------- |
    | **Background** | `#FFFFFF` | 内容页背景 |
    | **Secondary bg** | `#F8F9FA` | 表头、流程节点、启示区背景 |
    | **Tint bg** | `#FFF7F7` | 关键判断、指标背景 |
    | **Primary** | `#A50021` | 品牌线条、竖线、节点 |
    | **Primary dark** | `#B40029` | 关键数字、案例名 |
    | **Accent blue** | `#4285F4` | 可选对比指标 |
    | **Accent green** | `#2E7D32` | 正向结果提示 |
    | **Body text** | `#1F2328` | 主标题与高强调文本 |
    | **Secondary text** | `#5F6368` | 支持性描述 |
    | **Tertiary text** | `#8A9099` | 页脚、章节标签 |
    | **Border / Divider** | `#E4E7EB` / `#E8EAED` | 边界和分隔线 |

    ## IV. Typography System

    ### Font Plan

    **Typography direction**: CJK-primary corporate sans; maintain BOC template compatibility.

    | Role | Chinese | English | Fallback tail |
    | ---- | ------- | ------- | ------------- |
    | **Title** | SimHei | Arial | sans-serif |
    | **Body** | SimHei, Microsoft YaHei | Arial | sans-serif |
    | **Emphasis** | SimHei | Arial | sans-serif |
    | **Code** | — | Consolas, Courier New | monospace |

    **Per-role font stacks**

    - Title: `SimHei, Arial, sans-serif`
    - Body: `SimHei, Microsoft YaHei, Arial, sans-serif`
    - Emphasis: `Arial, SimHei, sans-serif`
    - Code: `Consolas, Courier New, monospace`

    ### Font Size Hierarchy

    **Baseline**: Body font size = 18px. Page titles use 30px; body text ranges 12–18px; footnotes 11–14px.

    ## V. Layout Principles

    ### Page Structure

    - **Header area**: upper-right BOC logo, left title, BOC red underline, right section label.
    - **Content area**: `x=40, y=112, w=1200, h=538`；第 1 页为总览轴 + 案例矩阵 + 路径表；第 2–6 页为左右双栏案例卡。
    - **Footer area**: source note, page number, “内部资料整理”。

    ### Layout Pattern Library

    | Pattern | Suitable Scenarios |
    | ------- | ----------------- |
    | Process flow | 第 1 页演进轴、案例能力链路 |
    | Basic table | 第 1 页路径归类总览 |
    | Symmetric split | 第 2–6 页双案例对标 |
    | Case card | 每个银行案例的图片、指标、流程和启示 |

    ### Spacing Specification

    | Element | Current Project |
    | ------- | --------------- |
    | Safe margin | 40–72 px |
    | Card gap | 24 px |
    | Card padding | 18 px |
    | Card radius | 6–8 px |
    | Footer baseline | y=690 |

    ## VI. Icon Usage Specification

    ### Source

    - **Chosen library**: `tabler-filled`
    - **Usage**: 本 deck 主要以文字、图片、流程块呈现；图标仅作为备选，不强制使用。

    | Purpose | Icon Path | Page |
    | ------- | --------- | ---- |
    | Knowledge database | `tabler-filled/database` | 1–6 |
    | Search / RAG | `tabler-filled/search` | 1–6 |
    | AI assistant | `tabler-filled/message-chatbot` | 1–6 |
    | Platform / operation | `tabler-filled/settings` | 1–6 |
    | Security / governance | `tabler-filled/shield-check` | 2–4 |

    ## VII. Visualization Reference List

    **Read-audit**:

    ```
    Catalog read: 70 templates / 10 categories
    Per-page selection:
      P01 process_flow | summary-quote: "Pick for 3-8 sequential steps connected by simple arrows."
      P01 basic_table  | summary-quote: "Pick for plain tabular text/number grid, 3-8 columns."
      P02-P06 no-template-match | fallback: custom symmetric case comparison; each page has image + KPI strip + process mini-flow
    Runners-up considered:
      kpi_cards rejected for P02-P06: metrics are paired with narrative and images, not standalone dashboard KPIs.
      comparison_table rejected for P02-P06: each page compares only two cases with unequal narrative detail; dense matrix would reduce scanability.
      pipeline_with_stages rejected for P01: overview uses a simple maturity flow, not stage outputs/artifacts.
    ```

    | Visualization Type | Reference Template | Used In |
    | ------------------ | ------------------ | ------- |
    | process_flow | `templates/charts/process_flow.svg` | Slide 01 and mini-flows on Slides 02–06 |
    | basic_table | `templates/charts/basic_table.svg` | Slide 01 |
    | custom case comparison | no-template-match | Slides 02–06 |

    ## VIII. Image Resource List

    | Filename | Dimensions | Ratio | Purpose | Type | Status | Generation Description |
    | -------- | ---------- | ----- | ------- | ---- | ------ | ---------------------- |
    | case_01_jpmorgan_llm_suite.png | 1600×900 | 1.78 | JPMorgan case visual | Illustration | Existing | User-provided case asset |
    | case_02_morgan_stanley_ai_assistant.png | 1600×900 | 1.78 | Morgan Stanley case visual | Illustration | Existing | User-provided case asset |
    | case_03_citi_assist_stylus.png | 1600×900 | 1.78 | Citi case visual | Illustration | Existing | User-provided case asset |
    | case_04_hsbc_genai_platform.png | 1600×900 | 1.78 | HSBC case visual | Illustration | Existing | User-provided case asset |
    | case_05_icbc_gongyin_zhiyong.png | 1600×900 | 1.78 | ICBC case visual | Illustration | Existing | User-provided case asset |
    | case_06_ccb_financial_llm.png | 1600×900 | 1.78 | CCB case visual | Illustration | Existing | User-provided case asset |
    | case_07_abc_chatabc.png | 1600×900 | 1.78 | ABC case visual | Illustration | Existing | User-provided case asset |
    | case_08_psbc_xiaoyou_assistant.png | 1600×900 | 1.78 | PSBC case visual | Illustration | Existing | User-provided case asset |
    | case_09_cmb_ai_xiaoyan.png | 1600×900 | 1.78 | CMB case visual | Screenshot / Illustration | Existing | User-provided case asset |
    | case_10_cib_ai_agents.png | 1600×900 | 1.78 | CIB case visual | Diagram | Existing | User-provided case asset |

    ## IX. Content Outline

    ### Part 1: 同业落地实践

    #### Slide 01 - 同业落地概况
    - **Layout**: 顶部演进轴 + 2×5 案例矩阵 + 底部路径归类表
    - **Title**: 同业落地概况：银行 AI 正从知识问答走向企业级智能体
    - **Visualization**: process_flow + basic_table
    - **Content**: 四条路径：员工助手、专业知识库/RAG、业务流程智能化、企业级智能体平台。

    #### Slide 02 - 国际案例一
    - **Layout**: 左右双栏案例卡
    - **Title**: 国际大行实践（一）：员工级入口与投顾知识库
    - **Content**: JPMorgan LLM Suite 与 Morgan Stanley AI Assistant / Debrief。

    #### Slide 03 - 国际案例二
    - **Layout**: 左右双栏案例卡
    - **Title**: 国际大行实践（二）：文档智能、上下文搜索与全行 GenAI 平台
    - **Content**: Citi Assist / Stylus / Squad 与 HSBC Enterprise GenAI。

    #### Slide 04 - 国内案例一
    - **Layout**: 左右双栏案例卡
    - **Title**: 国内大行实践（一）：企业级金融大模型与全行场景覆盖
    - **Content**: 工商银行“工银智涌”与建设银行 DeepSeek-R1 金融大模型。

    #### Slide 05 - 国内案例二
    - **Layout**: 左右双栏案例卡
    - **Title**: 国内大行实践（二）：金融知识增强与基层员工助手
    - **Content**: 农业银行 ChatABC 与邮储银行“小邮助手”。

    #### Slide 06 - 国内案例三
    - **Layout**: 左右双栏案例卡
    - **Title**: 国内银行实践（三）：投研知识库与智能体体系化运营
    - **Content**: 招商银行“招银智库 AI 小研”与兴业银行“智慧兴业”智能体体系。

    ## X. Speaker Notes Requirements

    One speaker note file per page, saved to `notes/`; `notes/total.md` uses `#` headings and is split by `total_md_split.py`. Notes should be formal, conclusion-first, and written in Chinese.

    ## XI. Technical Constraints Reminder

    1. All SVG files keep `width="1280" height="720" viewBox="0 0 1280 720"`.
    2. Use explicit HEX colors from `spec_lock.md`.
    3. Use `<text>` and `<tspan>` only for text; no `foreignObject`, no CSS, no script.
    4. Image references are local under `../images/case_images/`.
    5. Preserve Chinese Bank template chrome: logo, title anchor, red underline, footer.
    """).strip() + "\n"

    spec_lock = dedent("""
    # Execution Lock - 同业落地案例

    ## canvas
    - format: ppt169
    - width: 1280
    - height: 720
    - viewbox: 0 0 1280 720
    - content_x: 40
    - content_y: 112
    - content_w: 1200
    - content_h: 538

    ## colors
    - background: #FFFFFF
    - secondary_bg: #F8F9FA
    - tint_bg: #FFF7F7
    - primary: #A50021
    - primary_dark: #B40029
    - accent_blue: #4285F4
    - accent_green: #2E7D32
    - body_text: #1F2328
    - secondary_text: #5F6368
    - tertiary_text: #8A9099
    - border: #E4E7EB
    - divider: #E8EAED
    - pale_red: #F3D7DC
    - white: #FFFFFF
    - shadow: #000000

    ## typography
    - font_family: SimHei, Microsoft YaHei, Arial, sans-serif
    - title_family: SimHei, Arial, sans-serif
    - body_family: SimHei, Microsoft YaHei, Arial, sans-serif
    - emphasis_family: Arial, SimHei, sans-serif
    - code_family: Consolas, Courier New, monospace
    - body: 18
    - title: 30
    - subtitle: 24
    - section_label: 20
    - kpi_number: 40
    - hero_number: 44
    - annotation: 14
    - footnote: 11
    - page_number: 14

    ## icons
    - library: tabler-filled
    - database: tabler-filled/database
    - search: tabler-filled/search
    - message_chatbot: tabler-filled/message-chatbot
    - settings: tabler-filled/settings
    - shield_check: tabler-filled/shield-check

    ## images
    - boc_logo: ../templates/assets/boc_full_logo.png
    - case_01: ../images/case_images/case_01_jpmorgan_llm_suite.png
    - case_02: ../images/case_images/case_02_morgan_stanley_ai_assistant.png
    - case_03: ../images/case_images/case_03_citi_assist_stylus.png
    - case_04: ../images/case_images/case_04_hsbc_genai_platform.png
    - case_05: ../images/case_images/case_05_icbc_gongyin_zhiyong.png
    - case_06: ../images/case_images/case_06_ccb_financial_llm.png
    - case_07: ../images/case_images/case_07_abc_chatabc.png
    - case_08: ../images/case_images/case_08_psbc_xiaoyou_assistant.png
    - case_09: ../images/case_images/case_09_cmb_ai_xiaoyan.png
    - case_10: ../images/case_images/case_10_cib_ai_agents.png

    ## page_rhythm
    - P01: dense
    - P02: dense
    - P03: dense
    - P04: dense
    - P05: dense
    - P06: dense

    ## page_layouts
    - P01: 03_content
    - P02: 03_content
    - P03: 03_content
    - P04: 03_content
    - P05: 03_content
    - P06: 03_content

    ## page_charts
    - P01: process_flow
    """).strip() + "\n"

    PROJECT.joinpath("design_spec.md").write_text(design_spec, encoding="utf-8")
    PROJECT.joinpath("spec_lock.md").write_text(spec_lock, encoding="utf-8")


def write_notes():
    notes = dedent("""
    # 01_同业落地概况

    这一页先给出整体判断：银行 AI 的公开落地已经不只是知识问答，而是在向企业级智能体和流程闭环推进。国际大行和国内头部银行的案例可以归纳为四条路径：员工级通用助手、专业知识库与 RAG、业务流程智能化、企业级智能体平台。对本行而言，关键不是单点试验多少，而是能否把知识资产、模型入口、工具调用和运营机制连成体系。

    ---

    # 02_国际案例一

    在国外案例中，JPMorgan 和 Morgan Stanley 代表了两个典型入口。JPMorgan 的 LLM Suite 先把大模型做成员工级安全入口，八个月内 onboard 二十万用户，再逐步接入内部数据和 AI agents。Morgan Stanley 则以投顾知识库和 RAG 为核心，超过百分之九十八的顾问团队采用，说明专业知识库只有在可信、可复核、可治理时，才会真正进入一线工作。

    ---

    # 03_国际案例二

    接着看 Citi 和 HSBC，它们共同说明 AI 工具正在从单一问答走向工具矩阵和平台治理。Citi 将 Assist、Stylus、Squad 扩展到八十个国家和地区、覆盖十七万五千多名员工，重点是政策查询、文档智能和协同工作流。HSBC 则强调全行 GenAI 平台和责任 AI 治理，六百多个运行中用例背后，是开发、客服、信贷分析和生命周期管理的同步推进。

    ---

    # 04_国内案例一

    国内大型银行的落地更强调企业级体系化能力。工商银行的“工银智涌”把算力云、模型矩阵、金融数据集、工具和安全放在同一个体系里，公开材料披露覆盖二十多个业务领域和二百多个落地场景。建设银行以 DeepSeek-R1 金融大模型为底座，覆盖四十六个业务领域和二百多个场景，并把向量知识库作为基础应用之一，这说明知识库要进入业务场景，必须和模型、工具、指标一起表达价值。

    ---

    # 05_国内案例二

    农业银行和邮储银行展示的是知识增强与基层员工助手两类路径。农业银行 ChatABC 的重点在于精调、提示工程、知识增强、检索增强和 RLHF，把内部知识转化为行内问答、摘要和工单辅助能力。邮储银行“小邮助手”则面向三点九万多个网点和三十三万多名员工，以知识社区、智能辅助、AI 陪练和 SOP 指引形成运营闭环，公开口径显示业务办理效率提升百分之八十以上。

    ---

    # 06_国内案例三

    最后一页看招商银行和兴业银行。招商银行“招银智库 AI 小研”说明，高价值知识资产可以优先做成一线工作流入口，服务投研、零售、对公和风险条线。兴业银行“智慧兴业”则展示了智能体规模化的方向，公开披露二百多个智能体、二百六十多个应用场景，背后需要统一模型服务平台、知识工程、评测和运营能力共同支撑。
    """).strip() + "\n"
    notes_dir = PROJECT / "notes"
    notes_dir.mkdir(exist_ok=True)
    (notes_dir / "total.md").write_text(notes, encoding="utf-8")


def main():
    for dirname in ("svg_output", "svg_final", "notes"):
        (PROJECT / dirname).mkdir(exist_ok=True)
    write_specs()
    pages = [overview_page(), page2(), page3(), page4(), page5(), page6()]
    names = [
        "01_同业落地概况.svg",
        "02_国际案例一.svg",
        "03_国际案例二.svg",
        "04_国内案例一.svg",
        "05_国内案例二.svg",
        "06_国内案例三.svg",
    ]
    for name, content in zip(names, pages):
        (PROJECT / "svg_output" / name).write_text(content, encoding="utf-8")
    write_notes()
    print(f"Generated {len(pages)} SVG pages and specs under {PROJECT}")


if __name__ == "__main__":
    main()
