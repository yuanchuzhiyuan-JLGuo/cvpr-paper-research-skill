# Research-to-Paper Experiment Pipeline

Use this reference when the user wants the skill to behave like a research collaborator: survey recent baselines/datasets, reuse existing assets, implement missing code, run experiments, analyze results, and then write the paper.

## Stage Map

| Stage | Purpose | Required artifact | Gate |
|---|---|---|---|
| 0. Research question | Pin down the task, claim boundary, and evaluation target | `plan/research-question.md` | No overbroad claim |
| 1. Baseline/dataset survey | Identify recent comparable work and data | `plan/baseline-dataset-survey.md` | Recent work verified |
| 2. Source discovery | Find official baseline code/checkpoints/licenses | `baselines/source-registry.md` | Baselines classified |
| 3. Existing asset ingestion | Index current repo code, runs, logs, metrics, checkpoints | `plan/existing-asset-index.md` | No duplicate work |
| 4. Compute profile | Decide local/server strategy from actual resources | `plan/compute-profile.md` | Feasible plan |
| 5. Experiment matrix | Define smoke, pilot, main, and submission runs | `plan/experiment-matrix.yaml` | Claims mapped to runs |
| 6. Implementation | Add missing method/baseline/data/eval/plot code | `plan/method-code-contract.md` | Code matches method |
| 7. Execution | Launch, monitor, resume, and log training/eval | `plan/experiment-runbook.md` | Every run traceable |
| 8. Analysis | Aggregate metrics, statistics, plots, and qualitative panels | `analysis/result-summary.md` | Real results only |
| 9. Paper | Draft, audit, review, and format | `paper.tex`, `plan/review/*` | Integrity gate passed |

## Core Rule

Do not treat the repository as empty. Before writing code or designing runs, discover:

- existing training/evaluation scripts;
- configs and resolved configs;
- checkpoints and output folders;
- metrics JSON/CSV files;
- TensorBoard/W&B exports;
- previous result ledgers and experiment logs;
- third-party baseline folders;
- dataset manifests and preprocessing scripts.

## Research Question Artifact

Create `plan/research-question.md`:

| Item | Content |
|---|---|
| Target venue/task |  |
| One-sentence problem |  |
| Main claim |  |
| What is not claimed |  |
| Required evidence |  |
| Fastest falsification experiment |  |
| Submission-grade evidence |  |

## Baseline and Dataset Survey

For fast-moving ML/CV topics, browse and verify recent work, normally the last three years plus older canonical baselines. Prioritize primary sources: papers, official project pages, official repositories, OpenReview pages, and benchmark docs.

Create `plan/baseline-dataset-survey.md` with:

- technical families;
- closest baselines;
- dataset candidates;
- compatibility with the paper task;
- expected compute cost;
- what can be reused versus must be adapted.

## Experiment Stages

| Stage | Goal | Typical evidence strength |
|---|---|---|
| Smoke | Verify code/data/metrics execute | Plumbing only |
| Pilot | Test whether the idea has signal | Feasibility claim |
| Main | Compare against fair baselines and ablations | Bounded empirical claim |
| Submission | Multi-seed, statistics, qualitative/failure cases, external validation | Stronger paper claim |

## Code Implementation Rule

Prefer adapting existing code paths and official baseline repositories. If implementing from scratch:

- explain why official code cannot be used;
- keep the implementation minimal and auditable;
- mark it as `reimplemented baseline` if it is a baseline;
- add config, command, and metric traceability before reporting results.

## Paper Transition Rule

Only move from experiments to manuscript claims after:

- `result-ledger.md` traces every number;
- `method-code-contract.md` confirms paper method matches code;
- `experiment-gap-analysis.md` lists missing baselines/ablations;
- all pilot/smoke results are visibly labeled.
