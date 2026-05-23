# Top-Conference Pipeline

This workflow is a lightweight top-conference adaptation of rigorous academic research pipelines. It is intentionally simpler than a full multi-agent research system: it uses checkpoints and artifacts, not mandatory agent orchestration.

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
