# CLAUDE.md

This file guides Claude Code when working in this repository.

## Repository Type

This is a Claude Code and Codex plugin repository, not an application service. The main deliverable is a reusable top-conference writing skill:

```text
skills/cvpr-paper-writing/SKILL.md
```

Claude Code plugin metadata lives in:

```text
.claude-plugin/plugin.json
.claude-plugin/marketplace.json
```

## Claude Code Usage

For local development:

```bash
claude --plugin-dir .
```

For marketplace-style installation after publishing:

```text
/plugin marketplace add yuanchuzhiyuan-JLGuo/cvpr-paper-research-skill
/plugin install cvpr-paper-research-skill@cvpr-paper-writing
/reload-plugins
```

The skill is exposed under the plugin namespace:

```text
/cvpr-paper-research-skill:cvpr-paper-writing
```

## Architecture

- `skills/cvpr-paper-writing/SKILL.md`: compact routing and workflow instructions.
- `skills/cvpr-paper-writing/references/`: progressively loaded writing, LaTeX, experiment, and review guides.
- `skills/cvpr-paper-writing/scripts/`: deterministic setup and static-check scripts.
- `.claude-plugin/`: Claude Code plugin and marketplace metadata.
- `.codex-plugin/`: Codex plugin metadata.
- `AGENTS.md`: cross-agent repository maintenance instructions.

## Rules To Preserve

- Keep this skill generic to top-conference papers, with computer vision as the default example domain.
- Do not introduce paper-specific research claims.
- Keep `main.tex` as the Overleaf root and `paper.tex` as the manuscript body. If the root is adapted, preserve the original as `main_template_original.tex`.
- Preserve official template integrity; do not encourage manual margin, font, spacing, or `cvpr.sty` edits.
- Preserve the multi-agent enhanced workflow for full papers and major reviews, with single-agent fallback for small tasks.
- Keep reviewer and integrity roles read-only until the orchestrator authorizes a bounded manuscript edit.
- Do not add hooks or MCP servers unless the user explicitly requests them.

## Validation Commands

```bash
python skills/cvpr-paper-writing/scripts/setup_official_template.py --output /tmp/cvpr-paper-test --venue CVPR
python skills/cvpr-paper-writing/scripts/check_submission_static.py --paper-dir /tmp/cvpr-paper-test
```

On Windows PowerShell:

```powershell
python -Werror -m py_compile .\skills\cvpr-paper-writing\scripts\setup_official_template.py .\skills\cvpr-paper-writing\scripts\check_submission_static.py
```
