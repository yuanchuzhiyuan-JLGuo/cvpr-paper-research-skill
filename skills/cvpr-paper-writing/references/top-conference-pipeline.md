# Top-Conference Pipeline

This workflow is a top-conference adaptation of rigorous academic research pipelines. It supports a multi-agent enhanced path for complete-paper work and a compact single-agent path for small edits.

## Stage Map

| Stage | Purpose | Required artifact | Gate |
|---|---|---|---|
| 0. Venue profile | Identify venue rules, track, anonymity, template, page limits | `plan/venue-profile.md` | Template/source verified |
| 1. Positioning | Define problem, gap, contribution boundary | `plan/paper-positioning.md` | Claims are scoped |
| 2. Evidence map | Tie background and related work to sources | `plan/evidence-map.md` | Each citation has a role |
| 3. Method contract | Define what the method actually does | `plan/method-contract.md` | Method text matches implementation |
| 4. Experiment contract | Define datasets, baselines, metrics, ablations, seeds | `plan/experiment-protocol.md` | Each contribution has evidence |
| 5. Draft | Write `paper.tex` in the official template | `paper.tex` | No process notes in manuscript |
| 6. Integrity audit | Verify claims, numbers, configs, citations, and limitations | `plan/review/integrity-audit.md` | No unsupported major claim |
| 7. Multi-perspective review | Simulate top-conference reviewer objections | `plan/review/submission-risk-review.md` | Major risks triaged |
| 8. Revision | Map issues to edits, experiments, limitations, or rebuttal | `plan/review/revision-roadmap.md` | All major issues addressed or scoped |
| 9. Freeze and format | Final static checks and PDF inspection | `TEMPLATE_AUDIT.md` + checker output | Template and anonymity pass |

## Agent Map

| Stage | Recommended agent |
|---|---|
| 0. Venue profile | `venue_template_agent` |
| 1. Positioning | `positioning_agent` |
| 2. Evidence map | `evidence_agent` |
| 3. Method contract | `method_experiment_agent` |
| 4. Experiment contract | `method_experiment_agent` |
| 5. Draft | `draft_editor_agent` |
| 6. Integrity audit | `integrity_agent` |
| 7. Multi-perspective review | `review_panel` |
| 8. Revision | `orchestrator` + `draft_editor_agent` |
| 9. Freeze and format | `format_agent` |

For full submissions, create `plan/agent-workplan.md` and follow `multi-agent-enhanced` mode in `multi-agent-orchestration.md`.

## Checkpoint Rule

Do not move from a stage to a stronger manuscript claim unless the stage artifact exists. A missing artifact does not always stop writing, but it limits wording strength.

Examples:

- No baseline table -> do not claim "outperforms".
- No full source support -> do not claim a prior method "cannot" do something.
- No run log -> do not report a numerical result as real.
- No official template -> do not call the PDF submission-ready.

## Venue Profile

Create `plan/venue-profile.md`:

```markdown
# Venue Profile

- Venue:
- Track:
- Year:
- Review format:
- Page limit:
- Supplement policy:
- Anonymity policy:
- AI usage / disclosure policy:
- Official template source:
- Bibliography style:
- Artifact / code policy:
- Rebuttal policy:
```

For any rule that may change annually, verify the current official venue page.

## Method Contract

Create `plan/method-contract.md`:

| Method claim | Implemented in | Inputs | Outputs | Assumptions | Unsupported wording |
|---|---|---|---|---|---|

The Method section must not describe experiments, modules, objectives, or deployment behavior that are not implemented or explicitly framed as proposed/future.

## Claim Strength Levels

| Evidence state | Allowed wording |
|---|---|
| full multi-seed, fair baselines, ablations | strong result claim |
| one dataset with fair baselines | bounded empirical claim |
| pilot/debug/smoke run | feasibility or diagnostic claim |
| planned experiment | future work or experiment plan only |
| qualitative observation only | hypothesis or failure analysis |
| no evidence | remove or move to motivation |

## Human Oversight

At each gate, ask:

- What did we learn?
- What claim became stronger?
- What claim must be weakened?
- What would the toughest reviewer attack next?

This preserves human judgment while still making the workflow systematic.
