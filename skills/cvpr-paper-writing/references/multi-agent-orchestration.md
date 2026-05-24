# Multi-Agent Orchestration

Use this when the task involves complete-paper drafting, major revision, final submission readiness, or full simulated review. The goal is higher quality through independent expertise, not more agents for its own sake.

## Execution Modes

| Mode | Use when | Behavior |
|---|---|---|
| `research-experiment-paper` | full research loop: survey, baseline source discovery, existing result ingestion, code/training/eval, result analysis, then paper | dispatch research, code, compute, runner, analysis, writing, integrity, and review roles |
| `multi-agent-enhanced` | full paper, major revision, final checks, complete review | dispatch specialized roles, synthesize outputs, then edit |
| `isolated-pass` | no agent tooling but enough time for depth | run the same roles as separate read-only passes in one agent |
| `single-agent-compact` | small section edit, quick explanation, minor formatting | use the normal workflow without delegation |

Prefer `research-experiment-paper` when the user expects the agent to conduct or continue experiments, not just write from provided results. Prefer `multi-agent-enhanced` for high-stakes paper drafting/review when experiment assets already exist.

## Agent Roster

| Agent | Owns | Writes |
|---|---|---|
| `orchestrator` | task state, workplan, checkpoints, synthesis | `plan/agent-workplan.md`, final integration notes |
| `literature_agent` | recent related work, baselines, datasets | `plan/baseline-dataset-survey.md` |
| `baseline_source_agent` | official baseline repos, checkpoints, licenses, reproduction status | `baselines/source-registry.md`, `baselines/reproduction-log.md` |
| `asset_ingestion_agent` | existing code, configs, logs, metrics, checkpoints, plots | `plan/existing-asset-index.md`, updates to `plan/review/result-ledger.md` |
| `compute_agent` | local/server device profile and feasible run plan | `plan/compute-profile.md` |
| `implementation_agent` | method/baseline/dataset/eval/plot code changes | changed code files, `plan/method-code-contract.md` |
| `experiment_runner_agent` | launch/monitor/resume training and eval jobs | logs, run directories, `plan/experiment-runbook.md` |
| `result_analyst_agent` | metric aggregation, statistics, tables, figures, failure cases | `analysis/result-summary.md`, `tables/*.tex`, `figures/*` |
| `venue_template_agent` | official rules, template source, Overleaf structure | `TEMPLATE_AUDIT.md`, `plan/venue-profile.md` |
| `positioning_agent` | problem, gap, contribution boundary | `plan/paper-positioning.md` |
| `evidence_agent` | related work and citation support | `plan/evidence-map.md`, related-work blueprint |
| `method_experiment_agent` | method contract, results plan, ablations | `plan/method-contract.md`, `plan/experiment-protocol.md`, `plan/experiment-matrix.yaml` |
| `draft_editor_agent` | prose, section flow, final manuscript edits | `paper.tex` |
| `integrity_agent` | claim/result/config verification | `plan/review/*integrity*`, claim registry, result ledger |
| `review_panel` | independent reviewer reports | `plan/review/reviewer-*.md` |
| `format_agent` | LaTeX, anonymity, static checks, PDF readiness | checker output, `plan/review/format-audit.md` |

Only `draft_editor_agent` should directly edit `paper.tex` after the drafting phase begins. Reviewer and integrity agents are read-only with respect to manuscript source unless the orchestrator explicitly authorizes a bounded fix.

For code-running workflows, implementation and experiment-runner agents may edit code or create run artifacts, but they must not edit `paper.tex`. Keep third-party baseline code isolated under `third_party/` plus wrappers/patches.

## Workplan Template

Create `plan/agent-workplan.md`:

```markdown
# Agent Workplan

## Mode
- multi-agent-enhanced / isolated-pass / single-agent-compact

## File Ownership
| File or artifact | Owner | Other agents read/write? |
|---|---|---|

## Dispatch Plan
| Agent | Task | Inputs | Output | Blocking? |
|---|---|---|---|---|

## Synthesis Decisions
| Issue | Raised by | Decision | Manuscript action |
|---|---|---|---|
```

## Dispatch Rules

- Give each agent a concrete, bounded task and output path.
- Tell code-editing agents they are not alone in the repository and must not revert edits made by others.
- Split write scopes so two agents never own the same manuscript file at the same time.
- Run evidence, method/experiment, and reviewer passes independently when possible.
- Keep reviewer passes read-only; they should produce reports, not manuscript edits.
- The orchestrator integrates conflicts and chooses final edits after reviewing agent outputs.

## Recommended Parallel Pattern

For `research-experiment-paper`:

1. Dispatch `asset_ingestion_agent` to index existing code/results.
2. Dispatch `literature_agent` and `baseline_source_agent` in parallel for recent datasets/baselines and official source discovery.
3. Dispatch `compute_agent` to profile local/server resources.
4. Orchestrator synthesizes an experiment matrix and gap analysis.
5. Dispatch `implementation_agent` only for missing code with disjoint file ownership.
6. Dispatch `experiment_runner_agent` for bounded runs; do not wait idly if analysis can proceed.
7. Dispatch `result_analyst_agent` to build tables/figures/result summaries from raw files.
8. Then proceed to positioning, evidence, drafting, integrity, and reviewer gates.

After template setup and positioning:

1. Dispatch `evidence_agent` to build/verify the evidence map.
2. Dispatch `method_experiment_agent` to audit method and experiment contracts.
3. Dispatch `positioning_agent` to pressure-test novelty and claim strength.
4. Let `draft_editor_agent` write only after the orchestrator has synthesized these outputs.
5. Dispatch `integrity_agent` and `review_panel` after a coherent draft exists.
6. Let `format_agent` run last, after content is frozen.

## Review Panel Pattern

Use independent review roles:

- area chair / meta-reviewer;
- closest-work reviewer;
- methodology reviewer;
- reproducibility reviewer;
- skeptical reviewer;
- visual/qualitative reviewer for vision, video, graphics, or demo-heavy papers;
- cross-area reviewer when the paper spans communities.

Each reviewer should answer from its own lens. The orchestrator then creates one revision roadmap and decides which edits are manuscript changes, which are experiments, which are limitations, and which are rebuttal notes.

## Failure Recovery

| Problem | Recovery |
|---|---|
| agents disagree on novelty | ask `closest-work reviewer` and `positioning_agent` for evidence-linked comparison, then weaken or sharpen claims |
| result cannot be traced | block strong claims until `result-ledger.md` is filled |
| reviewer edits manuscript directly | discard direct edits and convert them into a review report |
| two agents edit same file | stop, diff both edits, and let orchestrator merge intentionally |
| context gets stale | reload `SKILL.md`, `agent-workplan.md`, and the latest artifact before continuing |

## Compatibility

Codex can use delegated subagents when the user asks for or approves multi-agent work and the tool is available. Claude Code can use its task/subagent mechanisms when available. If no agent tooling is available, preserve the same role separation as isolated passes with separate output artifacts.
