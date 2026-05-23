# Multi-Agent Orchestration

Use this when the task involves complete-paper drafting, major revision, final submission readiness, or full simulated review. The goal is higher quality through independent expertise, not more agents for its own sake.

## Execution Modes

| Mode | Use when | Behavior |
|---|---|---|
| `multi-agent-enhanced` | full paper, major revision, final checks, complete review | dispatch specialized roles, synthesize outputs, then edit |
| `isolated-pass` | no agent tooling but enough time for depth | run the same roles as separate read-only passes in one agent |
| `single-agent-compact` | small section edit, quick explanation, minor formatting | use the normal workflow without delegation |

Prefer `multi-agent-enhanced` for high-stakes conference submissions when the user asks for or approves multi-agent work and agent tooling is available.

## Agent Roster

| Agent | Owns | Writes |
|---|---|---|
| `orchestrator` | task state, workplan, checkpoints, synthesis | `plan/agent-workplan.md`, final integration notes |
| `venue_template_agent` | official rules, template source, Overleaf structure | `TEMPLATE_AUDIT.md`, `plan/venue-profile.md` |
| `positioning_agent` | problem, gap, contribution boundary | `plan/paper-positioning.md` |
| `evidence_agent` | related work and citation support | `plan/evidence-map.md`, related-work blueprint |
| `method_experiment_agent` | method contract, results plan, ablations | `plan/method-contract.md`, `plan/experiment-protocol.md` |
| `draft_editor_agent` | prose, section flow, final manuscript edits | `paper.tex` |
| `integrity_agent` | claim/result/config verification | `plan/review/*integrity*`, claim registry, result ledger |
| `review_panel` | independent reviewer reports | `plan/review/reviewer-*.md` |
| `format_agent` | LaTeX, anonymity, static checks, PDF readiness | checker output, `plan/review/format-audit.md` |

Only `draft_editor_agent` should directly edit `paper.tex` after the drafting phase begins. Reviewer and integrity agents are read-only with respect to manuscript source unless the orchestrator explicitly authorizes a bounded fix.

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
