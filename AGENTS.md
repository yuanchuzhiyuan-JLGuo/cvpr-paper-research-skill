# AGENTS.md

This repository is a cross-platform Codex and Claude Code skill/plugin for top-conference paper writing. CVPR remains the built-in template path; other venues use official author-kit URLs.

## Purpose

The authoritative skill is:

```text
skills/cvpr-paper-writing/SKILL.md
```

It guides agents through:

- official LaTeX author-kit setup;
- Overleaf workflow with `main.tex` as root and `paper.tex` as the manuscript body;
- section-level writing from abstract through conclusion;
- claim/evidence/experiment/reviewer-risk traceability;
- integrity gates for claims, citations, results, and method/config consistency;
- multi-agent enhanced orchestration for complete-paper work, with read/write boundaries and final synthesis;
- multi-perspective top-conference review with independent reviewer reports;
- static checks for template misuse, anonymity leaks, unresolved TODOs, labels, and missing figures.

## Platform Entry Points

Codex:

```text
.codex-plugin/plugin.json
skills/cvpr-paper-writing/agents/openai.yaml
```

Claude Code:

```text
.claude-plugin/plugin.json
.claude-plugin/marketplace.json
CLAUDE.md
```

## Invariants

- Keep the skill generic. Do not add project-specific paper claims or method names.
- Preserve the official-template plus `paper.tex` workflow. If `main.tex` is adapted for compilation, keep `main_template_original.tex`.
- Preserve the multi-agent enhanced workflow for full papers while keeping a single-agent fallback for small tasks.
- Keep reviewer and integrity agents read-only with respect to manuscript source unless the orchestrator explicitly authorizes a bounded fix.
- Keep `SKILL.md` concise and move details into `references/`.
- Keep scripts deterministic and free of third-party Python dependencies.
- Update `VERSION`, `README.md`, `.codex-plugin/plugin.json`, `.claude-plugin/plugin.json`, and `.claude-plugin/marketplace.json` together on release.

## Validation

Run from repository root:

```powershell
python C:\Users\admin\.codex\skills\.system\skill-creator\scripts\quick_validate.py .\skills\cvpr-paper-writing
python -Werror -m py_compile .\skills\cvpr-paper-writing\scripts\setup_official_template.py .\skills\cvpr-paper-writing\scripts\check_submission_static.py
```

End-to-end smoke:

```powershell
$out = Join-Path $env:TEMP ("cvpr-skill-test-" + [guid]::NewGuid().ToString("N"))
python .\skills\cvpr-paper-writing\scripts\setup_official_template.py --output $out --venue CVPR
python .\skills\cvpr-paper-writing\scripts\check_submission_static.py --paper-dir $out
```
