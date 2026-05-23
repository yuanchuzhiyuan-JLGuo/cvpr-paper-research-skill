---
name: cvpr-paper-writing
description: Use when writing, revising, formatting, or preparing a top-tier conference paper, especially CVPR/ICCV/ECCV/NeurIPS/ICML/ICLR-style submissions, including official template setup, section writing, experiment planning, figure/table design, multi-agent orchestration, integrity gates, multi-perspective review, anonymity checks, and submission-readiness review.
---

# Top-Conference Paper Writing

This skill turns a research idea into a submission-ready top-conference paper. It is optimized for computer vision by default, but the workflow generalizes to ML/AI venues such as CVPR, ICCV, ECCV, NeurIPS, ICML, ICLR, ACL, EMNLP, SIGGRAPH, and related selective conferences.

CVPR-style official LaTeX setup is built in. For other venues, use the same workflow with the venue's official template or a user-provided official template zip URL.

## Core Principle

Every paper claim must pass this chain:

```text
Claim -> Evidence -> Experiment/Table/Figure -> Allowed Wording -> Reviewer Risk
```

If a link is missing, weaken the claim, add the missing evidence, or move it to limitations/future work.

## Multi-Agent Operating Model

For complete-paper drafting, major revision, final submission checks, or full simulated review, recommend the multi-agent enhanced workflow. Use delegated agents when the user asks for or approves multi-agent work and the platform supports it; otherwise preserve the same role separation as isolated passes. Use single-agent fallback only for small edits, quick explanations, or environments without agent support.

Core roles:

- `orchestrator`: owns the workflow state, user checkpoints, file ownership, and final synthesis.
- `venue_template_agent`: verifies venue rules, downloads the official template, and preserves the `main.tex` plus `paper.tex` project structure.
- `positioning_agent`: sharpens problem, gap, contribution boundary, and allowed claim strength.
- `evidence_agent`: audits citations, related work, and claim-source alignment.
- `method_experiment_agent`: checks method contract, experiment protocol, baselines, metrics, ablations, and traceability.
- `draft_editor_agent`: writes or revises `paper.tex` after upstream gates are clear.
- `integrity_agent`: verifies claims, numbers, configs, citations, and failure modes.
- `review_panel`: runs independent area-chair, closest-work, methodology, reproducibility, skeptical, and visual/qualitative reviews.
- `format_agent`: runs static checks, template checks, anonymity checks, and PDF/Overleaf readiness review.

Read `references/multi-agent-orchestration.md` before using delegated agents or a full review panel.

## Quick Start

1. Set up the official template. For CVPR/ICCV/3DV-style papers:

```powershell
python skills/cvpr-paper-writing/scripts/setup_official_template.py --output paper_cvpr --venue CVPR
```

For another venue with an official LaTeX zip, first verify the conference's official author-kit page, then pass its zip URL:

```powershell
python skills/cvpr-paper-writing/scripts/setup_official_template.py --output paper_topconf --venue NeurIPS --template-url <official-template-zip-url>
```

2. Inspect the generated template notes:

```text
paper_cvpr/TEMPLATE_AUDIT.md
paper_cvpr/main.tex
paper_cvpr/paper.tex
paper_cvpr/sec/
```

3. Keep Overleaf's root file as `main.tex`, and write the manuscript body in the generated `paper.tex`.

4. Before submission, run:

```powershell
python skills/cvpr-paper-writing/scripts/check_submission_static.py --paper-dir paper_cvpr
```

## Required Workflow

### 1. Venue and Template Gate

Use the latest official template unless the user specifies a target year or venue kit. Never recreate conference formatting by hand.

- For CVPR/ICCV/3DV, download from the official `cvpr-org/author-kit` GitHub release.
- For other venues, use the venue's official author kit or an official template URL supplied by the user.
- Preserve all original template files. For CVPR-style kits, that includes `cvpr.sty`, `main.tex`, `preamble.tex`, `ieeenat_fullname.bst`, `main.bib`, and `sec/`.
- Add `paper.tex` as the manuscript body file instead of replacing the official template project.
- Keep `main.tex` as the Overleaf root file. If the setup script edits it, it must save the original as `main_template_original.tex` and make only the minimal `\input{paper}` connection needed for compilation.
- Keep review mode for anonymous submissions, using the official venue switch.
- Do not manually recreate margins, columns, fonts, or page-number behavior.

Read `references/latex-overleaf.md` and `references/top-conference-pipeline.md`.

### 2. Positioning Gate

Before drafting:

- Define the target venue and track.
- Write the one-sentence problem statement.
- Write the precise gap against prior work.
- Define what is new: formulation, method, data, evaluation, analysis, or system.
- Define the maximum claim strength allowed by current evidence.

Output target:

- `plan/paper-positioning.md`

### 3. Evidence Gate

For Introduction and Related Work, create:

- `plan/evidence-map.md`
- `plan/section-blueprints/intro.md`
- `plan/section-blueprints/related_work.md`

Rules:

- One citation supports one concrete statement.
- Group prior work by technical family, not by chronological list.
- Do not cite papers only as name-dropping.
- Browse or verify sources when the claim depends on recent work, official specs, or exact numbers.

Read `references/evidence-and-related-work.md`.

### 4. Experiment Gate

Before writing Results:

- Define datasets, splits, baselines, metrics, ablations, seeds, and aggregation.
- Map each contribution to at least one result, figure, table, or limitation.
- Keep pilot/debug/smoke results clearly labeled.

Output targets:

- `plan/experiment-protocol.md`
- `plan/method-experiment-traceability.md`
- `tables/table-schema.md`
- `figures/data-manifest.md`

Read `references/experiment-and-results.md`.

### 5. Integrity Gate

Before treating a draft as submission-ready:

- Extract all numerical, factual, comparison, and causality claims.
- Trace each result number to a log, table, script, or user-provided data source.
- Check that Methods text matches actual configs, datasets, training runs, and evaluation scripts.
- Check for shortcut explanations, proxy-metric overreach, missing baselines, and hidden failure cases.
- Convert unsupported claims into limitations or remove them.

Output targets:

- `plan/review/claim-registry.md`
- `plan/review/result-ledger.md`
- `plan/review/integrity-audit.md`

Read `references/integrity-gates.md`.

### 6. Section Writing Gate

Write section text in `paper.tex`, which is included by the official root `main.tex`.

Use section recipes:

- Abstract: 5-7 sentences.
- Introduction: problem pressure, prior route, unresolved gap, method insight, contributions.
- Related Work: thematic synthesis with boundaries.
- Method: auditable definitions, architecture, training, inference.
- Experiments: setup first, then evidence.
- Limitations: specific, evidence-aware, not apologetic.

Read `references/section-recipes.md`.

### 7. Multi-Perspective Reviewer Gate

Before final polishing:

- Simulate reviewer objections from multiple non-overlapping perspectives, preferably as independent agents or isolated passes.
- Audit overclaims.
- Audit anonymity.
- Audit reproducibility.
- Audit tables, figures, and captions.
- Run static checks.

Output target:

- `plan/review/submission-risk-review.md`

Read `references/reviewer-gate.md`, `references/multi-perspective-review.md`, and `references/multi-agent-orchestration.md`.

### 8. Revision and Freeze Gate

After review:

- Create a revision roadmap that maps each issue to a manuscript edit, experiment, limitation, or rebuttal.
- Re-run integrity checks on changed sections.
- Freeze content before final formatting.
- Run static checks and inspect the compiled PDF.

## Top-Conference Writing Rules

- Lead with the technical problem, not a broad field essay.
- Use exact technical nouns and concrete verbs.
- Avoid inflated terms unless experiments support them.
- State limitations where they prevent overclaiming.
- Captions must say what is measured, under what setting, and what the reader should compare.
- Results prose should include both improvement and failure/constraint when relevant.
- Do not let process notes, TODOs, mock data labels, or prompt instructions leak into the manuscript.

## LaTeX Rules

- For CVPR/ICCV/3DV templates, keep `\documentclass[10pt,twocolumn,letterpaper]{article}` unless the official template changes.
- Use `\usepackage[review]{cvpr}` for review submissions.
- Use `\usepackage{cvpr}` only for camera-ready.
- Use `\usepackage[pagenumbers]{cvpr}` only for arXiv or explicitly requested variants.
- Keep `\input{paper}` in the working root file; do not make `paper.tex` a second standalone root unless explicitly creating a separate variant.
- Keep `hyperref` unless validation problems require disabling it.
- Use `\cref{}`/`\Cref{}` for cross-references if the template supports it.
- Put table captions above tables and figure captions below figures.
- Avoid custom margin, font, spacing, caption, or geometry packages unless the official kit permits them.
- Do not include supplementary pages in the main submission PDF unless the venue instructions allow it.
- For non-CVPR venues, follow the official template's equivalent review/camera-ready switches and bibliography rules.

## Bundled References

Load only the needed file:

- `references/latex-overleaf.md`: official template, Overleaf workflow, formatting constraints.
- `references/top-conference-pipeline.md`: general conference workflow, checkpoints, and artifacts.
- `references/multi-agent-orchestration.md`: agent roles, dispatch rules, file ownership, and synthesis protocol.
- `references/section-recipes.md`: paragraph and section-level writing recipes.
- `references/evidence-and-related-work.md`: citation discipline and related-work synthesis.
- `references/experiment-and-results.md`: experiment protocol, tables, figures, and result prose.
- `references/integrity-gates.md`: claim, result, config, and failure-mode audits.
- `references/multi-perspective-review.md`: top-conference simulated review perspectives and revision roadmap.
- `references/reviewer-gate.md`: pre-submission checklist and simulated review.

## Bundled Scripts

- `scripts/setup_official_template.py`: downloads the latest CVPR author kit or a user-provided official template zip, expands it, creates planning folders, and writes `TEMPLATE_AUDIT.md`.
- `scripts/check_submission_static.py`: performs static checks for template files, review mode, forbidden formatting packages, unresolved TODOs, anonymous submission leaks, and common LaTeX issues.
