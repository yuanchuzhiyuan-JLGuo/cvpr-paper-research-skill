# Baseline Source Discovery and Existing Result Ingestion

Use this reference before implementing baselines or writing comparison tables.

## Baseline Discovery Order

For each candidate baseline, search in this order:

1. Original paper.
2. Official project page.
3. Official/author GitHub repository.
4. Official checkpoints on HuggingFace, ModelScope, Google Drive, etc.
5. Maintained third-party reproduction.
6. Lightweight reimplementation only if no usable source exists.

Do not present a reimplementation as an official baseline.

## Baseline Classes

| Class | Meaning | Main-table eligibility |
|---|---|---|
| Official baseline | Official code/checkpoint used with documented settings | Strong |
| Reproduced baseline | Official code retrained or reevaluated by us | Strong if traceable |
| Adapted baseline | Official code modified for our task/data/metrics | Usable with adaptation notes |
| Reimplemented baseline | We implement the idea ourselves | Usable only if clearly labeled |
| Reported-only baseline | Number copied from paper/leaderboard | Separate table or context only |
| Excluded baseline | Too costly/incompatible/unavailable | Must record reason |

## Source Registry

Create `baselines/source-registry.md`:

| Baseline | Paper | Code | Official? | Checkpoint | License | Commit/version | Task fit | Compute fit | Status | Notes |
|---|---|---|---|---|---|---|---|---|---|---|

Create machine-readable `baselines/source-registry.yaml` when the project will run many baselines:

```yaml
baselines:
  - name:
    paper_url:
    code_url:
    official: true
    checkpoint_url:
    license:
    commit:
    supported_tasks: []
    compatible_with_our_task:
    required_gpu:
    install_status:
    smoke_test_status:
    reproduction_status:
    class: official|reproduced|adapted|reimplemented|reported_only|excluded
    notes:
```

## Third-Party Code Integration

Recommended layout:

```text
third_party/
  BaselineRepo/
baselines/
  wrappers/
    baseline_name_wrapper.py
  patches/
    baseline_name.patch
```

Rules:

- Record the source URL and commit hash.
- Record the license before using code or weights.
- Do not silently modify third-party code. Use wrappers or patches.
- Keep unified evaluation code in our repo when possible.
- If installation fails, record the error and mitigation.

## Existing Result Ingestion

Before launching new runs, scan:

```text
runs/
logs/
outputs/
checkpoints/
wandb/
tensorboard/
*.json
*.jsonl
*.csv
*.tsv
*.pt
*.pth
*.ckpt
```

Create `plan/existing-asset-index.md`:

| Asset | Path | Type | Dataset | Model | Seed | Status | Reusable for |
|---|---|---|---|---|---:|---|---|

Create or update `plan/review/result-ledger.md`:

| Result ID | Metric | Value | Source file | Config | Checkpoint | Command | Dataset/split | Aggregation | Seeds | Verified |
|---|---|---:|---|---|---|---|---|---|---:|---|

## Gap Analysis

Create `plan/experiment-gap-analysis.md`:

| Claim | Existing evidence | Missing evidence | Cheapest next run | Submission-grade run |
|---|---|---|---|---|

Use this to continue from existing experiments instead of rerunning everything.

## Hard Gates

- A baseline without a paper/source cannot enter the main comparison.
- A number without a raw result file cannot enter a paper table.
- A smoke result cannot be described as a main result.
- A reported-only number must not be mixed with unified-evaluation numbers.
- An adapted or reimplemented baseline must be labeled.
