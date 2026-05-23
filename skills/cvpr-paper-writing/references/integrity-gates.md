# Integrity Gates

Use this before submitting, before rebuttal, and after any major revision. The goal is to catch research-writing failures that look polished but are not supported.

## Required Artifacts

Create:

- `plan/review/claim-registry.md`
- `plan/review/result-ledger.md`
- `plan/review/config-method-audit.md`
- `plan/review/integrity-audit.md`

## Claim Registry

| Claim ID | Claim text | Type | Section | Support | Evidence file/source | Verdict | Manuscript action |
|---|---|---|---|---|---|---|---|

Claim types:

- numerical;
- factual;
- comparative;
- causal/mechanistic;
- novelty;
- limitation;
- methodological.

Verdicts:

- `VERIFIED`: support is direct and sufficient.
- `BOUNDED`: support exists but wording must be scoped.
- `WEAK`: support is indirect or incomplete.
- `UNSUPPORTED`: remove, rewrite, or move to future work.
- `UNVERIFIABLE`: needs source/log/config access before submission.

## Result Ledger

| Result ID | Paper location | Reported value | Source file/log | Command/config | Aggregation | Seeds | Verified? |
|---|---|---:|---|---|---|---:|---|

Rules:

- Every table value must trace to a file, log, notebook, or user-provided record.
- Every percentage improvement must trace to the raw numerator and denominator.
- Every "N seeds" claim must match actual run directories or records.
- Pilot/debug/smoke values must be labeled as such in captions and prose.

## Config-Method Audit

| Method statement | Code/config/log support | Risk | Fix |
|---|---|---|---|

Check:

- dataset names and splits;
- training epochs, learning rate, batch size, optimizer;
- model modules and losses;
- inference procedure;
- evaluation metrics;
- baseline settings;
- hardware/software where relevant.

The Methods section must describe what was actually run. If a method is conceptual or planned, label it clearly.

## Seven Top-Conference Failure Modes

Use these as an audit checklist:

1. **Implementation mismatch**: code or config does not implement the method described.
2. **Unsupported citation**: a cited source exists but does not support the claim.
3. **Untraceable result**: a table number or improvement cannot be traced to raw evidence.
4. **Shortcut explanation**: the result may be caused by a shortcut, leakage, or confound rather than the claimed mechanism.
5. **Bug-as-insight**: an unexpected result is narrated as a discovery without ruling out implementation error.
6. **Methodology drift**: the paper describes a cleaner experiment than the one actually run.
7. **Frame lock**: early positioning forces the paper to overclaim despite weaker evidence.

For each mode, record `CLEAR`, `RISK`, or `INSUFFICIENT EVIDENCE`.

## Integrity Audit Template

```markdown
# Integrity Audit

## Summary
- Overall status:
- Strongest verified claim:
- Claims weakened:
- Blocking issues:

## Failure Mode Checklist
| Mode | Status | Evidence | Action |
|---|---|---|---|

## Claim Registry Summary
| Verdict | Count |
|---|---:|

## Result Ledger Summary
| Result family | Verified count | Open issues |
|---|---:|---|

## Required Manuscript Edits
1.
2.
3.
```

## Pass Criteria

A top-conference submission can proceed only if:

- no main contribution claim is `UNSUPPORTED`;
- no main result is untraceable;
- every major baseline omission is either fixed or explicitly scoped;
- Methods text matches actual implementation;
- known negative or weak results are not hidden when they affect the claim.
