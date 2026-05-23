# CVPR Paper Writing Skill

A Codex skill for writing and preparing CVPR/ICCV/ECCV-style computer vision papers in the official LaTeX author-kit workflow.

The skill covers:

- official CVPR/ICCV/3DV LaTeX template setup from `cvpr-org/author-kit`;
- Overleaf workflow with `main.tex` as the root and `paper.tex` as the manuscript body;
- section-level writing recipes from abstract to conclusion;
- claim/evidence/experiment/reviewer-risk traceability;
- experiment, table, figure, baseline, and ablation planning;
- static checks for template misuse, anonymity leaks, unresolved TODOs, labels, and missing figures.

## Install

From Codex, install with:

```bash
python scripts/install-skill-from-github.py --repo 1961184386/cvpr-paper-writing-skill --path skills/cvpr-paper-writing
```

Then restart Codex to pick up the skill.

## Use

Invoke the skill when writing or formatting a vision conference paper:

```text
Use $cvpr-paper-writing to set up a CVPR paper project and draft the paper in the official template.
```

To create an Overleaf-ready paper folder:

```bash
python skills/cvpr-paper-writing/scripts/setup_official_template.py --output paper_cvpr --venue CVPR
```

To run static submission checks:

```bash
python skills/cvpr-paper-writing/scripts/check_submission_static.py --paper-dir paper_cvpr
```

## Repository Layout

```text
skills/
  cvpr-paper-writing/
    SKILL.md
    references/
    scripts/
```

## Version

Initial packaged release: `v0.1.0`.
