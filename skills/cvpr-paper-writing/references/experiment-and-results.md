# Experiment and Results

Use this reference before writing any Results, Discussion, or claim-bearing caption.

## Experiment Protocol

Create `plan/experiment-protocol.md`:

```markdown
# Experiment Protocol

## Research Questions

## Datasets and Splits

## Baselines

## Metrics

## Training and Implementation Details

## Main Comparisons

## Ablations

## Robustness and Generalization

## Qualitative Analysis

## Failure Cases

## Reproducibility Notes
```

## Baseline Rules

A baseline is fair only if:

- it addresses the same task or property;
- it has comparable input information;
- it is trained/evaluated under comparable data and compute where possible;
- differences are disclosed;
- hyperparameters and checkpoints are described.

Include:

- standard published baselines;
- strong recent baselines;
- simple baselines;
- ablations of your own method;
- oracle or upper-bound variants if useful.

## Metric Rules

For every metric, state:

- what it measures;
- whether higher or lower is better;
- aggregation rule;
- unit or scale;
- confidence interval, standard deviation, or seed count when relevant;
- known failure modes.

Do not let proxy metrics become the only evidence for the main claim.

## Traceability Table

Create `plan/method-experiment-traceability.md`:

| Contribution | Required evidence | Experiment | Table/Figure | Current status | Allowed wording |
|---|---|---|---|---|---|

No contribution should remain in the Introduction unless this table gives it support or a limitation boundary.

## Table Schema

Create `tables/table-schema.md`:

| Table | Purpose | Rows | Metrics | Data source | Aggregation | Claim supported |
|---|---|---|---|---|---|---|

Main paper tables should be few and claim-bearing. Appendix tables can hold per-dataset, per-class, or per-seed detail.

## Figure Schema

Create `figures/data-manifest.md`:

| Figure | Purpose | Data source | Script/source | Output file | Claim supported |
|---|---|---|---|---|---|

Recommended figure types:

- method overview;
- dataset or task protocol;
- main quantitative plot;
- qualitative comparison;
- ablation visualization;
- failure cases.

## Captions

Caption formula:

```text
[What is shown.] [Experimental setting.] [What comparison to read.] [Important caveat if needed.]
```

Avoid:

- "Our method is best" as the caption's only message;
- unsupported causal interpretation;
- tiny text or unexplained symbols.

## Results Text

Strong evidence:

```text
Across [N] seeds on [dataset], our method improves [metric] by [value] over [baseline], while maintaining [secondary metric]. This supports [specific claim].
```

Preliminary evidence:

```text
In a pilot setting, the method shows [observed behavior]. We report this as a diagnostic result rather than a final performance claim.
```

Negative result:

```text
The method does not improve [metric] under [condition], indicating that [module/assumption] remains a bottleneck.
```

## Submission-Readiness Gates

| Gate | Required before strong claim |
|---|---|
| Dataset | clear splits and preprocessing |
| Baseline | strong and fair comparisons |
| Ablation | each claimed module tested |
| Seeds | repeated runs or reason why not |
| Metrics | primary and secondary metrics |
| Qualitative | representative and failure cases |
| Reproducibility | configs, hardware, training details |
| Statistics | mean/std or confidence where appropriate |
