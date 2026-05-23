# Multi-Perspective Review

Use this to simulate top-conference review with a true multi-agent panel when possible. If agent tooling is unavailable, run each perspective as an isolated pass and keep outputs separate until synthesis.

## Review Panel

Configure 4-7 perspectives depending on the paper:

| Perspective | Primary questions |
|---|---|
| Area chair / meta-reviewer | Is the contribution clear, significant, and venue-appropriate? |
| Closest-work reviewer | Is novelty real relative to the strongest prior work? |
| Methodology reviewer | Are experiments, metrics, baselines, and ablations sufficient? |
| Reproducibility reviewer | Can the method and results be reproduced from the paper? |
| Skeptical reviewer | What shortcut, leakage, confound, or overclaim could invalidate the paper? |
| Cross-area reviewer | Does the paper connect to adjacent communities or miss obvious framing? |

For CVPR-style papers, include a visual/qualitative reviewer when the paper depends on images, videos, figures, or demos.

## Multi-Agent Dispatch

When using delegated agents, assign each reviewer one perspective only:

| Reviewer file | Perspective |
|---|---|
| `plan/review/reviewer-area-chair.md` | Area chair / meta-reviewer |
| `plan/review/reviewer-closest-work.md` | Closest-work reviewer |
| `plan/review/reviewer-methodology.md` | Methodology reviewer |
| `plan/review/reviewer-reproducibility.md` | Reproducibility reviewer |
| `plan/review/reviewer-skeptical.md` | Skeptical reviewer |
| `plan/review/reviewer-visual.md` | Visual/qualitative reviewer |
| `plan/review/reviewer-cross-area.md` | Cross-area reviewer |

Do not let reviewers coordinate before writing their reports. The value comes from independent failure finding.

## Read-Only Rule

Review passes must not edit the manuscript directly. They produce reports and a revision roadmap. Edits happen only after the author selects which issues to address.

## Review Report Template

```markdown
# Review Perspective: [Name]

## Summary

## Strengths

## Major Weaknesses
| Issue | Evidence | Severity | Required fix |
|---|---|---:|---|

## Minor Weaknesses

## Questions For Authors

## Score
- Technical quality:
- Novelty:
- Evidence:
- Clarity:
- Confidence:

## Decision
Accept / Weak Accept / Borderline / Weak Reject / Reject
```

## Editorial Synthesis

After perspective reports, synthesize:

| Issue | Raised by | Consensus? | Severity | Action |
|---|---|---|---:|---|

Actions:

- `experiment`: run or add evidence;
- `rewrite`: clarify or weaken wording;
- `related-work`: add source or contrast;
- `limitation`: state boundary explicitly;
- `rebuttal`: prepare answer if no manuscript change is appropriate;
- `defer`: acknowledge but out of scope.

## Revision Roadmap

Create `plan/review/revision-roadmap.md`:

```markdown
# Revision Roadmap

## Priority 0: Blocking

## Priority 1: Major

## Priority 2: Minor

## Claims To Weaken

## Experiments To Add

## Figures/Tables To Change

## Rebuttal Notes
```

## Top-Conference Scoring Heuristic

Use scores as diagnostic, not truth:

| Dimension | Typical reject trigger |
|---|---|
| Novelty | closest-work gap is unclear |
| Rigor | missing baseline or ablation for central claim |
| Evidence | main result is pilot-only or proxy-only |
| Clarity | reader cannot state contribution after Introduction |
| Reproducibility | method/config/dataset details insufficient |
| Fit | contribution does not match venue expectations |

If any single dimension has a reject-level issue, the paper is not ready even if other dimensions are strong.
