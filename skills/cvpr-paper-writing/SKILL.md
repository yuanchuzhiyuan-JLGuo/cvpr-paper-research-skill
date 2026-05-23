---
name: cvpr-paper-writing
description: Use when writing, revising, formatting, or preparing a CVPR/ICCV/ECCV-style computer vision conference paper in LaTeX or Overleaf, including official template setup, section writing, experiment planning, figure/table design, anonymity checks, and submission-readiness review.
---

# CVPR Paper Writing

This skill turns a computer vision research idea into a submission-ready conference paper using the official LaTeX template. It combines writing structure, evidence discipline, experiment design, reviewer-risk checks, and Overleaf-ready formatting.

## Core Principle

Every paper claim must pass this chain:

```text
Claim -> Evidence -> Experiment/Table/Figure -> Allowed Wording -> Reviewer Risk
```

If a link is missing, weaken the claim, add the missing evidence, or move it to limitations/future work.

## Quick Start

1. Set up the official template:

```powershell
python skills/cvpr-paper-writing/scripts/setup_official_template.py --output paper_cvpr --venue CVPR
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

### 1. Template Gate

Use the latest official template unless the user specifies a target year or venue kit.

- Download from the official `cvpr-org/author-kit` GitHub release.
- Preserve `cvpr.sty`, `main.tex`, `preamble.tex`, `ieeenat_fullname.bst`, `main.bib`, and `sec/`.
- Add `paper.tex` as the manuscript body file.
- Keep `main.tex` as the Overleaf root file; it should load the official style, title/authors, `\maketitle`, `\input{paper}`, and bibliography.
- Keep review mode for anonymous submissions.
- Do not manually recreate margins, columns, fonts, or page-number behavior.

Read `references/latex-overleaf.md` for template and Overleaf rules.

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

### 5. Section Writing Gate

Write section text in `paper.tex`, which is included by the official root `main.tex`.

Use section recipes:

- Abstract: 5-7 sentences.
- Introduction: problem pressure, prior route, unresolved gap, method insight, contributions.
- Related Work: thematic synthesis with boundaries.
- Method: auditable definitions, architecture, training, inference.
- Experiments: setup first, then evidence.
- Limitations: specific, evidence-aware, not apologetic.

Read `references/section-recipes.md`.

### 6. Reviewer Gate

Before final polishing:

- Simulate reviewer objections.
- Audit overclaims.
- Audit anonymity.
- Audit reproducibility.
- Audit tables, figures, and captions.
- Run static checks.

Output target:

- `plan/review/submission-risk-review.md`

Read `references/reviewer-gate.md`.

## CVPR-Style Writing Rules

- Lead with the technical problem, not a broad field essay.
- Use exact technical nouns and concrete verbs.
- Avoid inflated terms unless experiments support them.
- State limitations where they prevent overclaiming.
- Captions must say what is measured, under what setting, and what the reader should compare.
- Results prose should include both improvement and failure/constraint when relevant.
- Do not let process notes, TODOs, mock data labels, or prompt instructions leak into the manuscript.

## LaTeX Rules

- Keep `\documentclass[10pt,twocolumn,letterpaper]{article}` unless the official template changes.
- Use `\usepackage[review]{cvpr}` for review submissions.
- Use `\usepackage{cvpr}` only for camera-ready.
- Use `\usepackage[pagenumbers]{cvpr}` only for arXiv or explicitly requested variants.
- Keep `\input{paper}` in `main.tex`; do not make `paper.tex` a second standalone root unless explicitly creating a separate variant.
- Keep `hyperref` unless validation problems require disabling it.
- Use `\cref{}`/`\Cref{}` for cross-references if the template supports it.
- Put table captions above tables and figure captions below figures.
- Avoid custom margin, font, spacing, caption, or geometry packages unless the official kit permits them.
- Do not include supplementary pages in the main submission PDF unless the venue instructions allow it.

## Bundled References

Load only the needed file:

- `references/latex-overleaf.md`: official template, Overleaf workflow, formatting constraints.
- `references/section-recipes.md`: paragraph and section-level writing recipes.
- `references/evidence-and-related-work.md`: citation discipline and related-work synthesis.
- `references/experiment-and-results.md`: experiment protocol, tables, figures, and result prose.
- `references/reviewer-gate.md`: pre-submission checklist and simulated review.

## Bundled Scripts

- `scripts/setup_official_template.py`: downloads the latest official author kit, expands it, creates planning folders, and writes `TEMPLATE_AUDIT.md`.
- `scripts/check_submission_static.py`: performs static checks for template files, review mode, forbidden formatting packages, unresolved TODOs, anonymous submission leaks, and common LaTeX issues.
