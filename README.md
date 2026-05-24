# CVPR Paper Research Skill

A cross-platform Codex and Claude Code skill/plugin for moving a research idea toward a top-tier conference paper. It supports CVPR/ICCV/ECCV/NeurIPS/ICML/ICLR-style workflows, from baseline and dataset research through code execution, result analysis, paper writing, and reviewer-risk auditing.

Repository: `yuanchuzhiyuan-JLGuo/cvpr-paper-research-skill`

Skill invocation name: `$cvpr-paper-writing`

## What It Does

This skill has two complementary modes:

- `research-experiment-paper`: a full research loop for surveying recent baselines/datasets, finding official baseline code, ingesting existing results, profiling compute, planning/running experiments, aggregating metrics, generating figures/tables, and drafting the paper.
- `multi-agent-enhanced`: a manuscript-focused loop for official template setup, paper positioning, evidence maps, experiment protocols, `paper.tex` drafting, integrity audits, and simulated reviewer review.

Core principle:

```text
Claim -> Evidence -> Experiment/Table/Figure -> Allowed Wording -> Reviewer Risk
```

The skill treats a project as an ongoing research codebase, not a blank notebook. It first looks for existing code, configs, checkpoints, logs, raw metric files, official baseline repositories, and reusable evaluation scripts before designing new experiments or writing new code.

## TL;DR

Full research-to-paper workflow:

```text
Use $cvpr-paper-writing in research-experiment-paper mode.

Target venue: CVPR
Research topic: [your topic]
Core idea: [your method]
Current project folder: [path]
Available compute: [local GPU / server name / cluster]
Output: baseline and dataset survey, official baseline source registry, existing result ledger, compute-aware experiment matrix, missing code implementation plan, training/evaluation runbook, top-conference figures/tables, paper.tex draft, and reviewer-risk audit.

Do not invent unsupported results. Reuse official baseline code where possible. Label planned, executed, and submission-grade evidence separately.
```

Paper-only workflow:

```text
Use $cvpr-paper-writing in multi-agent-enhanced mode to prepare a CVPR-style paper from my existing method and results.

Target venue: CVPR
Research topic: [your topic]
Core method: [your method]
Main contributions: [2-4 bullets]
Current evidence: [datasets, baselines, metrics, results, figures, logs]
Output: official LaTeX project, paper.tex draft, experiment plan, and reviewer-risk report.
Do not invent unsupported results.
```

Template-only setup:

```bash
python skills/cvpr-paper-writing/scripts/setup_official_template.py --output paper_cvpr --venue CVPR
```

## Research-to-Paper Workflow

Use `research-experiment-paper` when the project needs actual research work, not just prose.

The workflow:

1. Define the research question and claim boundary.
2. Survey recent baselines and datasets, usually emphasizing the last three years for fast-moving fields.
3. Find official baseline source code, checkpoints, licenses, commits, and reproduction status.
4. Ingest existing project assets: code, configs, logs, checkpoints, metric JSON/CSV files, figures, and previous result ledgers.
5. Ask or infer whether experiments run locally or on a server; profile GPU, CUDA/PyTorch, disk, network, and job runner.
6. Build a compute-aware experiment matrix: smoke, pilot, main, and submission-grade runs.
7. Implement or adapt only missing method, dataset, baseline wrapper, training, evaluation, and plotting code.
8. Run or resume experiments when requested and feasible.
9. Aggregate results into a traceable ledger.
10. Generate top-conference-style tables, plots, qualitative panels, and failure cases.
11. Draft and audit the paper.

Key artifacts:

```text
plan/research-question.md
plan/baseline-dataset-survey.md
baselines/source-registry.md
baselines/reproduction-log.md
baselines/adaptation-notes.md
baselines/license-audit.md
plan/existing-asset-index.md
plan/compute-profile.md
plan/experiment-matrix.yaml
plan/experiment-runbook.md
plan/experiment-gap-analysis.md
plan/method-code-contract.md
plan/review/result-ledger.md
analysis/result-summary.md
tables/*.tex
figures/*.pdf
```

## Baseline Policy

Baselines must be traceable. The skill searches for baseline sources in this order:

1. Original paper.
2. Official project page.
3. Author-maintained GitHub repository.
4. Official checkpoints on HuggingFace, ModelScope, Google Drive, or similar hosts.
5. Maintained third-party reproduction.
6. Lightweight reimplementation only when no usable source exists.

Baseline classes:

| Class | Meaning |
|---|---|
| `official` | Official code/checkpoint used with documented settings. |
| `reproduced` | Official code retrained or reevaluated by us. |
| `adapted` | Official code modified for our task/data/metrics. |
| `reimplemented` | We implemented the idea ourselves; never present it as official. |
| `reported-only` | Number copied from a paper or leaderboard; keep separate from unified evaluation. |
| `excluded` | Too costly, incompatible, unavailable, or out of scope; record the reason. |

Hard gates:

- A baseline without a source cannot enter the main comparison.
- A number without a raw metric/log file cannot enter a paper table.
- Smoke results cannot be described as main results.
- Official reported numbers and unified-evaluation numbers must not be mixed in one table without clear labeling.

## Evidence Levels

The skill distinguishes:

| Evidence state | Allowed wording |
|---|---|
| Planned experiment | Future work or experiment plan only. |
| Smoke run | Pipeline/plumbing verification. |
| Pilot run | Feasibility or diagnostic claim. |
| Single-dataset fair comparison | Bounded empirical claim. |
| Multi-seed, fair baselines, ablations | Stronger result claim. |
| Rich external validation | Broader generalization claim, still scoped. |

## Official LaTeX Workflow

For CVPR/ICCV/3DV-style venues:

```bash
python skills/cvpr-paper-writing/scripts/setup_official_template.py --output paper_cvpr --venue CVPR
```

For another venue with an official LaTeX zip:

```bash
python skills/cvpr-paper-writing/scripts/setup_official_template.py --output paper_topconf --venue NeurIPS --template-url <official-template-zip-url>
```

The script preserves the official template files and adds `paper.tex`. Keep `main.tex` as the Overleaf root file.

Generated project layout:

```text
paper_cvpr/
  main.tex
  paper.tex
  main_template_original.tex
  preamble.tex
  main.bib
  cvpr.sty
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

Run static checks:

```bash
python skills/cvpr-paper-writing/scripts/check_submission_static.py --paper-dir paper_cvpr
```

## Writing Style

The skill uses flexible top-conference writing scaffolds, not rigid templates.

For abstracts, it checks that the paper covers:

```text
background significance -> existing progress -> unresolved problem -> core insight -> method -> evidence -> bounded implication
```

For introductions, it chooses the strongest narrative rather than forcing one structure. Supported patterns include:

- problem-driven;
- contradiction-driven;
- observation-driven;
- system/bottleneck-driven;
- benchmark/evaluation-driven;
- theory/analysis-driven.

For example, tokenizer-side controllability papers often work better as observation- or contradiction-driven stories than generic background-first stories.

Top-conference expression rule:

| Weak wording | Better wording |
|---|---|
| This problem is very important. | This setting exposes a bottleneck in [specific mechanism]. |
| Existing methods have achieved good results. | Existing methods improve [metric/capability] under [setting]. |
| We solve this problem. | We introduce [method], which [technical mechanism] to [measurable objective]. |
| Experiments show effectiveness. | On [dataset], [method] improves [metric] from [a] to [b] over [baseline], while [trade-off]. |

## Multi-Agent Roles

Research and execution roles:

| Role | Responsibility |
|---|---|
| `literature_agent` | Recent related work, baselines, and datasets. |
| `baseline_source_agent` | Official baseline repos, checkpoints, licenses, commits, and reproduction status. |
| `asset_ingestion_agent` | Existing code, configs, logs, metrics, checkpoints, plots, and result ledgers. |
| `compute_agent` | Local/server device profile and feasible run plan. |
| `implementation_agent` | Method, baseline, dataset, evaluation, and plotting code. |
| `experiment_runner_agent` | Launch, monitor, resume, and record training/evaluation jobs. |
| `result_analyst_agent` | Metric aggregation, statistics, LaTeX tables, figures, and failure cases. |

Paper roles:

| Role | Responsibility |
|---|---|
| `orchestrator` | Workflow state, checkpoints, synthesis. |
| `venue_template_agent` | Official rules and template setup. |
| `positioning_agent` | Problem, gap, contribution boundary. |
| `evidence_agent` | Related work and claim-source alignment. |
| `method_experiment_agent` | Method and experiment traceability. |
| `draft_editor_agent` | Manuscript prose in `paper.tex`. |
| `integrity_agent` | Claim/result/config verification. |
| `review_panel` | Independent reviewer reports. |
| `format_agent` | LaTeX, anonymity, and static checks. |

## Installation

### Codex

Install from GitHub:

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

## Repository Layout

```text
skills/cvpr-paper-writing/
  SKILL.md
  agents/openai.yaml
  references/
    research-experiment-pipeline.md
    baseline-source-and-existing-results.md
    compute-training-and-results.md
    top-conference-pipeline.md
    section-recipes.md
    experiment-and-results.md
    integrity-gates.md
    reviewer-gate.md
    multi-agent-orchestration.md
    multi-perspective-review.md
    latex-overleaf.md
    evidence-and-related-work.md
  scripts/
    setup_official_template.py
    check_submission_static.py
```

## License

See `LICENSE`.
