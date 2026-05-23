# CVPR Paper Research Skill

A cross-platform Codex and Claude Code skill/plugin for researching, writing, and preparing top-tier conference papers, especially CVPR/ICCV/ECCV/NeurIPS/ICML/ICLR-style submissions.

Repository: `yuanchuzhiyuan-JLGuo/cvpr-paper-research-skill`

Skill invocation name: `$cvpr-paper-writing`

It helps you move from a research idea to an Overleaf-ready LaTeX paper project with:

- official conference template setup;
- `main.tex` as the Overleaf root and `paper.tex` as the manuscript body;
- multi-agent enhanced planning, writing, auditing, and review;
- claim/evidence/experiment traceability;
- reviewer-risk analysis and submission-readiness checks.

## TL;DR

In Codex or Claude Code, ask:

```text
Use $cvpr-paper-writing in multi-agent-enhanced mode to help me turn my research idea into a CVPR-style paper.

Target venue: CVPR
Research topic: [your topic]
Core method: [your method]
Main contributions: [2-4 bullets]
Current evidence: [datasets, baselines, metrics, results, figures, logs]
Output: official LaTeX project, paper.tex draft, experiment plan, and reviewer-risk report.
Do not invent unsupported results.
```

For a template-only setup:

```bash
python skills/cvpr-paper-writing/scripts/setup_official_template.py --output paper_cvpr --venue CVPR
```

## 中文快速用法

最常用的启动指令：

```text
请使用 $cvpr-paper-writing 的 multi-agent-enhanced 模式，针对我的研究思路生成一篇 CVPR 风格论文。

目标会议：CVPR
研究方向：
核心问题：
方法思路：
主要创新点：
已有实验：
已有结果：
相关论文：
希望输出：官方 LaTeX 模板工程、paper.tex 初稿、实验规划、reviewer 风险分析。
要求：不要编造不存在的实验结果；没有证据的 claim 标记为待验证或 limitations。
```

如果你还没有准备好完整论文，可以先让它只做规划：

```text
请使用 $cvpr-paper-writing 的 multi-agent-enhanced 模式，先基于当前研究思路生成 paper-positioning、method-contract、experiment-protocol 和 agent-workplan，暂时不要写完整 paper.tex。
```

## What This Skill Produces

When setting up a paper project, the skill creates or guides creation of:

```text
paper_cvpr/
  main.tex                    # Overleaf root
  paper.tex                   # manuscript body to edit
  main_template_original.tex  # original root backup if main.tex was adapted
  preamble.tex
  main.bib
  cvpr.sty
  sec/
  figures/
  tables/
  TEMPLATE_AUDIT.md
  plan/
    agent-workplan.md
    venue-profile.md
    paper-positioning.md
    evidence-map.md
    method-contract.md
    experiment-protocol.md
    method-experiment-traceability.md
    section-blueprints/
    review/
```

`paper.tex` is intentionally not standalone. Keep `main.tex` as the root file in Overleaf.

## Installation

### Codex

Install from GitHub with the Codex skill installer:

```bash
python scripts/install-skill-from-github.py --repo yuanchuzhiyuan-JLGuo/cvpr-paper-research-skill --path skills/cvpr-paper-writing
```

Then restart Codex so the skill is discovered.

This repository also includes Codex plugin metadata:

```text
.codex-plugin/plugin.json
skills/cvpr-paper-writing/agents/openai.yaml
```

### Claude Code

For local development:

```bash
claude --plugin-dir .
```

For plugin installation:

```text
/plugin marketplace add yuanchuzhiyuan-JLGuo/cvpr-paper-research-skill
/plugin install cvpr-paper-research-skill@cvpr-paper-writing
/reload-plugins
```

The skill is exposed as:

```text
/cvpr-paper-research-skill:cvpr-paper-writing
```

## Start A New Paper

### 1. Generate The Official Template

CVPR/ICCV/3DV-style default:

```bash
python skills/cvpr-paper-writing/scripts/setup_official_template.py --output paper_cvpr --venue CVPR
```

Another venue with an official LaTeX zip:

```bash
python skills/cvpr-paper-writing/scripts/setup_official_template.py --output paper_topconf --venue NeurIPS --template-url <official-template-zip-url>
```

The script preserves the official template files and adds `paper.tex`. If it needs to adapt `main.tex` to include `paper.tex`, it saves the original as `main_template_original.tex`.

### 2. Give The Skill Your Research Materials

Use this intake template:

```text
Use $cvpr-paper-writing in multi-agent-enhanced mode.

Target venue:
Paper title or working title:
Research problem:
Core idea:
Method summary:
Main contributions:
Closest prior work:
Datasets:
Baselines:
Metrics:
Ablations:
Existing results:
Figures/tables available:
Code/logs/configs available:
Claims that must be avoided or treated carefully:
Output folder:
```

### 3. Ask For Planning Before Drafting

Recommended first pass:

```text
Use $cvpr-paper-writing in multi-agent-enhanced mode. First create the positioning, evidence map, method contract, experiment protocol, and agent workplan. Do not write the full paper yet.
```

Expected outputs:

```text
plan/agent-workplan.md
plan/paper-positioning.md
plan/evidence-map.md
plan/method-contract.md
plan/experiment-protocol.md
```

### 4. Draft `paper.tex`

After the plan is approved:

```text
Continue with $cvpr-paper-writing. Use draft_editor_agent to write paper.tex based on the approved plan. Start with Abstract, Introduction, Related Work, and Method. Mark unsupported claims as TODO evidence instead of inventing results.
```

Then continue section by section:

```text
Now write the Experiments section using the experiment protocol. Only include real results that are present in the result ledger or user-provided tables.
```

### 5. Run Integrity And Review

Before polishing:

```text
Run the integrity_agent and review_panel. Produce claim-registry, result-ledger, integrity-audit, submission-risk-review, and revision-roadmap. Reviewers must not edit paper.tex directly.
```

### 6. Run Static Submission Checks

```bash
python skills/cvpr-paper-writing/scripts/check_submission_static.py --paper-dir paper_cvpr
```

Use `--fail-on-warn` if you want warnings to fail CI:

```bash
python skills/cvpr-paper-writing/scripts/check_submission_static.py --paper-dir paper_cvpr --fail-on-warn
```

## Multi-Agent Workflow

For complete papers and major revisions, use `multi-agent-enhanced` mode.

| Role | Responsibility | Typical output |
|---|---|---|
| `orchestrator` | workflow state, checkpoints, synthesis | `plan/agent-workplan.md` |
| `venue_template_agent` | official rules and template setup | `TEMPLATE_AUDIT.md`, `plan/venue-profile.md` |
| `positioning_agent` | problem, gap, contribution boundary | `plan/paper-positioning.md` |
| `evidence_agent` | related work and source support | `plan/evidence-map.md` |
| `method_experiment_agent` | method/experiment traceability | `plan/method-contract.md`, `plan/experiment-protocol.md` |
| `draft_editor_agent` | manuscript prose | `paper.tex` |
| `integrity_agent` | claim/result/config verification | `plan/review/integrity-audit.md` |
| `review_panel` | independent reviewer reports | `plan/review/reviewer-*.md` |
| `format_agent` | LaTeX, anonymity, static checks | `plan/review/format-audit.md` |

Use single-agent mode only for small edits, quick explanations, or environments without delegated-agent support.

## Common Prompts

Set up a CVPR paper:

```text
Use $cvpr-paper-writing to create a CVPR official LaTeX project in ./paper_cvpr and prepare paper.tex for writing.
```

Plan from a research idea:

```text
Use $cvpr-paper-writing in multi-agent-enhanced mode to turn this research idea into a top-conference paper plan. Create paper-positioning, evidence-map, method-contract, experiment-protocol, and agent-workplan.
```

Write the Introduction:

```text
Use $cvpr-paper-writing to write the Introduction in paper.tex. Follow the section recipe: problem pressure, prior route, unresolved gap, method insight, and contributions. Do not overclaim beyond current evidence.
```

Audit experiments:

```text
Use $cvpr-paper-writing to audit whether the experiments support the claimed contributions. Create method-experiment-traceability and result-ledger.
```

Simulate reviewers:

```text
Use $cvpr-paper-writing review_panel to run independent area-chair, closest-work, methodology, reproducibility, skeptical, and visual reviewers. Produce reviewer reports and a revision roadmap. Do not edit paper.tex directly.
```

Prepare for submission:

```text
Use $cvpr-paper-writing to run final integrity, anonymity, LaTeX, and Overleaf-readiness checks for this paper directory.
```

## What To Provide For Best Results

The skill works best when you provide:

- a clear target venue and year;
- your actual research idea and contribution list;
- closest prior work or related papers;
- datasets, baselines, metrics, and ablations;
- real result tables, logs, configs, or screenshots;
- figures or figure descriptions;
- constraints such as "do not claim SOTA" or "experiments are pilot only".

If evidence is missing, the skill should weaken the wording, create a TODO, or move the point to limitations. It should not invent results.

## Repository Layout

```text
.codex-plugin/
.claude-plugin/
skills/
  cvpr-paper-writing/
    SKILL.md
    agents/
    references/
    scripts/
AGENTS.md
CLAUDE.md
VERSION
```

## Validation

Run from the repository root:

```bash
python C:\Users\admin\.codex\skills\.system\skill-creator\scripts\quick_validate.py .\skills\cvpr-paper-writing
python -Werror -m py_compile .\skills\cvpr-paper-writing\scripts\setup_official_template.py .\skills\cvpr-paper-writing\scripts\check_submission_static.py
```

Smoke test:

```powershell
$out = Join-Path $env:TEMP ("cvpr-skill-test-" + [guid]::NewGuid().ToString("N"))
python .\skills\cvpr-paper-writing\scripts\setup_official_template.py --output $out --venue CVPR
python .\skills\cvpr-paper-writing\scripts\check_submission_static.py --paper-dir $out
```

## Current Release

`v0.4.1`
