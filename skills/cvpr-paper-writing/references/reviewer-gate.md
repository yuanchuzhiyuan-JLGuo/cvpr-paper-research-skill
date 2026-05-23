# Reviewer Gate

Use this before final polishing and before rebuttal planning. Pair it with `multi-perspective-review.md` when a full top-conference risk pass is needed.

## Simulated Reviewer Questions

1. What is the exact technical problem?
2. Why is this problem important for computer vision?
3. What is new beyond engineering combination?
4. What is the closest prior work, and is it fairly compared?
5. Are the baselines strong enough?
6. Are the metrics aligned with the main claim?
7. Do the ablations isolate the claimed modules?
8. Are results statistically reliable?
9. Are qualitative examples cherry-picked?
10. Are limitations and failure cases visible?
11. Is the method reproducible from the description?
12. Is the submission anonymous and template-compliant?
13. Do all numerical and factual claims pass the integrity audit?
14. Can a reviewer understand the paper's problem, gap, and evidence from the first two pages?
15. What is the strongest objection a skeptical reviewer would raise?

## Major Risk Triggers

Treat these as high-severity:

- unsupported state-of-the-art claim;
- missing closest baseline;
- no ablation for the central module;
- metric does not measure the claimed property;
- private data or labels without sufficient description;
- hand-wavy implementation details;
- introduction promises more than experiments show;
- related work misses a directly competing line;
- reported result is untraceable to logs, tables, scripts, or user-provided records;
- Methods text drifts from actual configs, datasets, or runs;
- the strongest likely reviewer objection is absent from the paper;
- figures unreadable at print size;
- tables omit variance when results are noisy;
- anonymous submission leaks author identity, institution, acknowledgments, repository names, or private paths;
- official template modified manually.

## Submission Risk Review

Create `plan/review/submission-risk-review.md`:

```markdown
# Submission Risk Review

## Summary Judgment
- Venue:
- Current readiness:
- Strongest claim:
- Weakest claim:
- Biggest reject risk:

## Major Risks
| Risk | Evidence | Severity | Fix | Manuscript action |
|---|---|---:|---|---|

## Claim Audit
| Claim | Supported by | Missing evidence | Allowed wording |
|---|---|---|---|

## Related Work Audit
| Closest area | Covered sources | Missing source risk | Action |
|---|---|---|---|

## Experiment Audit
| Contribution | Baseline | Metric | Ablation | Status |
|---|---|---|---|---|

## Integrity Audit
| Claim/result/config item | Evidence | Verdict | Required action |
|---|---|---|---|

## Format and Anonymity Audit
| Item | Status | Fix |
|---|---|---|

## Required Next Edits
1.
2.
3.
```

## Rebuttal Prep

For likely reviewer objections, prepare:

| Reviewer concern | Direct answer | Evidence | Manuscript change | Concession |
|---|---|---|---|---|

Do not answer a valid weakness with hype. Add evidence, clarify the scope, or concede and revise.
