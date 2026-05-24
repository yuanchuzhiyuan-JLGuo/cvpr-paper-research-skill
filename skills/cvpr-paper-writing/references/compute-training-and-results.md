# Compute-Aware Training, Result Analysis, and Figures

Use this reference when experiments must actually run or when existing runs need to be summarized into top-conference tables and figures.

## Compute Profile

Ask or infer whether experiments run locally or on a server. If unclear, ask the user for the target device. Then inspect:

- OS and shell;
- GPU model/count/memory;
- CUDA, driver, PyTorch/JAX/TensorFlow versions;
- CPU/RAM;
- disk space;
- Python/conda/venv;
- network/data access;
- job runner: local foreground, `tmux`, `nohup`, Slurm, PowerShell background process, etc.

Create `plan/compute-profile.md`:

| Item | Value | Risk | Action |
|---|---|---|---|

## Experiment Matrix

Create `plan/experiment-matrix.yaml`:

```yaml
experiments:
  - name:
    stage: smoke|pilot|main|submission
    model:
    baseline_class: official|reproduced|adapted|reimplemented|ours
    dataset:
    config:
    seeds: []
    command:
    expected_time:
    expected_gpu_memory:
    output_dir:
    blocking_claims: []
    status: planned|running|completed|failed|skipped
```

## Runbook

Create `plan/experiment-runbook.md`:

| Run | Command | Workdir | Env | Output | Log | Resume command | Success criterion |
|---|---|---|---|---|---|---|---|

When running jobs:

- save stdout/stderr logs;
- save resolved config;
- save git commit or source snapshot when possible;
- record seed;
- record checkpoint path;
- detect NaN/crash/OOM;
- resume rather than restart when possible.

## Training Strategy by Compute

| Compute | Strategy |
|---|---|
| CPU / no GPU | unit tests, data preprocessing, tiny smoke only |
| Single small GPU | small model, low resolution, smoke and pilot |
| Single strong GPU | main single-seed runs, selected ablations |
| Multi-GPU server | multi-seed, baseline sweeps, richer data |
| Cluster | full submission matrix, robustness and statistics |

## Result Aggregation

Generate `analysis/result-summary.md`:

- completed runs;
- failed/skipped runs;
- primary metric table;
- ablation interpretation;
- variance/statistics;
- qualitative observations;
- failure cases;
- claim wording updates.

For each metric:

- state direction;
- state unit/scale;
- state aggregation;
- include seed count or confidence/standard deviation;
- identify proxy-metric failure modes.

## Top-Conference Table Rules

- Main table: answer the main claim.
- Ablation table: isolate each module.
- Dataset/generalization table: show external validity.
- Efficiency table: parameters, FLOPs/steps, GPU memory, training/inference time when relevant.
- Separate pilot/smoke from final main results.
- Keep official reported numbers separate from unified evaluation.

Output LaTeX tables in `tables/*.tex`.

## Top-Conference Figure Rules

Produce figures from scripts and traceable data:

- method overview;
- protocol/dataset diagram;
- main metric plot with error bars where possible;
- qualitative comparison panel;
- ablation trend plot;
- failure-case panel;
- leakage/probe heatmap.

Output publication figures as vector PDF when possible, or high-resolution PNG for raster/video frames. Create `figures/data-manifest.md`:

| Figure | Data source | Script | Output | Claim supported | Caveat |
|---|---|---|---|---|---|

## Claim Update After Results

After aggregation, update:

- `plan/review/result-ledger.md`;
- `plan/review/claim-registry.md`;
- `plan/review/integrity-audit.md`;
- manuscript tables/captions.

If results are weak or negative, write them honestly as limitations, diagnostics, or failure cases. Do not hide negative results that affect the main claim.
