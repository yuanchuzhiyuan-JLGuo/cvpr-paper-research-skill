# Section Recipes

These recipes are optimized for CVPR/ICCV/ECCV-style papers: compact, technical, evidence-driven, and reviewer-aware.

## Title

Good titles are specific and technical:

```text
[Method/Concept]: [Specific Technical Contribution] for [Task/Setting]
```

Avoid:

- vague adjectives like "Powerful", "Robust", "Universal" without evidence;
- overbroad task claims;
- acronyms that hide the contribution.

## Abstract

Use templates as diagnostic scaffolds, not rigid prose. If a stronger paper-specific narrative exists, prefer that narrative while preserving the underlying logical roles: background significance, existing progress, unresolved problem, core insight, method, evidence, and bounded implication.

Default abstract logic: background significance -> existing progress -> unresolved problem -> our solution -> method -> empirical effect -> bounded implication. Use 5-7 sentences when this order fits the paper. Write in a top-conference style: concrete technical nouns, active verbs, bounded claims, and no generic "important problem" filler.

1. Background and significance: why this research problem matters now.
2. Existing research progress: what current methods or systems have achieved.
3. Remaining problem: the specific gap, limitation, or contradiction that still blocks progress.
4. Our solution idea: the core insight or design principle.
5. Method summary: the proposed model/framework/training/evaluation mechanism.
6. Empirical effect: what result is achieved, under what setting, and against what baseline.
7. Bounded implication: what the result suggests, plus any scope limitation if needed.

Top-conference abstract scaffold:

```text
[Technical setting] increasingly depends on [core mechanism/resource], making [specific capability] a key bottleneck for [task/use case]. Recent methods improve [existing capability], but they typically [specific limitation] and therefore fail to measure/handle [unresolved property]. We address this gap by [core solution idea]. We introduce [method name], a [technical object] that [main mechanism] and [secondary mechanism]. Under [datasets/settings], [method name] achieves [primary result] compared with [baseline] while [secondary result or trade-off]. These results support [bounded implication] and identify [remaining limitation/failure mode] for future work.
```

Prefer:

- "Recent latent video generators rely on compact spatiotemporal codes" over "video generation is important".
- "Existing tokenizers optimize reconstruction but are rarely evaluated under factor-level token replacement" over "existing methods have problems".
- "We formulate/evaluate/introduce/show" over "we try to solve".
- "single-seed pilot", "three-seed mean", "controlled setting" when evidence is bounded.

Avoid:

- broad openings such as "With the rapid development of deep learning";
- unsupported words such as "significant", "robust", "universal", "complete", "solve";
- claims about causality, understanding, or generality unless directly tested.

Checklist:

- Does it say what is new?
- Does it say how it is evaluated?
- Does it avoid claims not supported by experiments?
- Does it avoid citations unless the venue style permits them?

## Introduction

Use templates as diagnostic scaffolds, not rigid section blueprints. The introduction should choose the strongest paper-specific narrative while ensuring the reader understands: why the problem matters, what prior work achieved, what gap remains, what insight unlocks the method, what the method does, and what evidence supports it.

Default introduction logic: first paragraph background, second paragraph existing methods and problems, third paragraph theoretical/empirical observation, fourth paragraph solution and contributions. Use this four-part structure when it fits; otherwise choose one of the narrative patterns below. Each paragraph should narrow the reader toward the paper's claim; avoid survey-like lists.

Recommended 4-paragraph structure:

1. **Background and significance**: define the research area, explain why it matters now, and establish the practical/scientific pressure.
2. **Existing methods and unresolved problems**: synthesize the dominant method families, state what they have achieved, and identify the concrete limitation that motivates the paper.
3. **Key observation or theoretical basis**: explain what the authors discovered, hypothesized, or formalized that makes the proposed direction plausible. This can be a theoretical insight, an empirical diagnosis, a failure-mode analysis, or a reformulation.
4. **Our solution and contributions**: describe how the paper solves the problem, name the method, preview evaluation, and list contributions.

Expanded paragraph roles when more space is available:

1. **Context pressure**: why the problem matters now.
2. **Prior routes**: what families of methods do.
3. **Gap cascade**: what remains unsolved and why it matters.
4. **Key insight**: the paper's technical move.
5. **Method and evaluation preview**: enough detail to make the contribution concrete.
6. **Contributions**: 3-4 bullets or a compact paragraph.

Top-conference four-paragraph introduction scaffold:

```text
Paragraph 1: [Technical systems/tasks] increasingly rely on [core mechanism], because [specific pressure such as scale, controllability, annotation, compute, or deployment]. This makes [precise capability] a central requirement for [target setting].

Paragraph 2: Existing methods mainly address this through [family A] or [family B]. These approaches improve [measured capability], but they are usually optimized/evaluated for [property X] rather than [property Y]. As a result, [specific failure mode] remains difficult to diagnose.

Paragraph 3: We observe/formalize that [key empirical or theoretical basis]. In particular, [diagnostic fact/reformulation] implies that [design principle] is necessary or useful for [target property]. This turns [vague challenge] into [measurable objective].

Paragraph 4: Based on this insight, we propose [method], which [main mechanism] and [implementation detail that matters]. We evaluate it with [datasets/protocol/metrics], comparing against [baseline families] and testing [ablations]. Our contributions are: [formulation], [method], [evaluation/analysis], and [result or diagnostic].
```

## Alternative Introduction Narratives

Pick the narrative that best matches the paper. Do not force every paper into the same four paragraphs.

### Problem-Driven
Use when the task pain point is obvious and practical.

1. Background and practical pressure.
2. Why current method families fail under the target setting.
3. Proposed method and why it addresses the failure.
4. Evidence and contributions.

### Contradiction-Driven
Use when existing methods appear strong under standard metrics but fail under a new diagnostic.

1. Standard progress and apparent success.
2. Contradiction: a key property remains poor or unmeasured.
3. Reframing/diagnostic that exposes the contradiction.
4. Method, evaluation, and results.

### Observation-Driven
Use when the paper starts from an empirical or theoretical finding.

1. Present the surprising observation or failure mode.
2. Explain why existing methods or metrics miss it.
3. Derive the design principle or formulation.
4. Introduce method and evidence.

### System/Bottleneck-Driven
Use for foundation-model systems, toolchains, or infrastructure-heavy work.

1. System-level demand and bottleneck.
2. Existing system designs and where the bottleneck appears.
3. Design principles.
4. System implementation, evaluation, and contributions.

### Benchmark/Evaluation-Driven
Use for datasets, benchmarks, protocols, or diagnostic papers.

1. Evaluation gap and why current metrics are insufficient.
2. Requirements for a better benchmark/protocol.
3. Proposed benchmark/protocol and what it measures.
4. Findings, baselines, and implications.

### Theory/Analysis-Driven
Use when the central contribution is a formal explanation or scaling/optimization law.

1. Empirical phenomenon or unresolved behavior.
2. Limitations of existing explanations.
3. Theory/formulation/analysis.
4. Algorithmic consequence and validation.

For tokenizer-side controllability or intervention papers, an observation- or contradiction-driven narrative is often stronger than a generic background-first narrative.

## Top-Conference Expression Rules

Use this style when rewriting abstracts, introductions, captions, and result paragraphs:

| Weak / thesis-like wording | Top-conference wording |
|---|---|
| This problem is very important. | This setting exposes a bottleneck in [specific mechanism]. |
| Existing methods have achieved good results. | Existing methods improve [metric/capability] under [setting]. |
| However, there are still many problems. | However, they do not directly evaluate/control [specific property]. |
| We propose a new method to solve this problem. | We introduce [method], which [technical mechanism] to [measurable objective]. |
| Experiments show our method is effective. | On [dataset], [method] improves [metric] from [a] to [b] over [baseline], while [trade-off]. |
| This proves the superiority of our method. | This supports [bounded claim] under [setting]. |

Result wording must match evidence:

- Full multi-seed evidence: "Across [N] seeds, ... improves ..."
- Single run: "In a single-run controlled setting, ..."
- Smoke/pilot: "A pilot result suggests ..." or "Smoke tests verify the pipeline ..."
- Negative result: "The gap in [metric] indicates that [module/assumption] remains a bottleneck."

Contribution template:

```text
We [formulate/propose/introduce/show] [technical object], enabling/measuring [specific property] under [setting].
```

Avoid:

- "To the best of our knowledge" unless carefully verified.
- a survey-style introduction with no clear gap.
- contribution bullets that repeat the abstract.
- claims that require experiments not yet run.

## Related Work

Organize by technical theme:

```text
Theme -> representative methods -> shared limitation -> relation to this paper
```

Each paragraph should synthesize, not list.

Good paragraph structure:

1. Name the family.
2. Summarize 2-4 representative works.
3. State the boundary of that family.
4. Bridge to the proposed method.

Bad pattern:

```text
Paper A does X. Paper B does Y. Paper C does Z.
```

## Method

Make the method auditable:

- Define notation before using it.
- State inputs, outputs, and assumptions.
- Separate architecture, training objective, inference procedure, and implementation details.
- Explain design choices only where they affect behavior or claims.
- Use equations for core operations, losses, or guarantees, not for decorative formality.

Useful order:

1. Problem formulation.
2. Method overview.
3. Main modules.
4. Objective/losses.
5. Inference or deployment.
6. Implementation details.

## Experiments

Start with setup before results:

1. Datasets and splits.
2. Baselines.
3. Metrics.
4. Implementation details.
5. Main comparison.
6. Ablations.
7. Robustness/generalization.
8. Qualitative analysis and failure cases.

Every subsection should answer a reviewer question.

## Results Prose

Pattern:

```text
Under [setting], [method] achieves [metric/result] compared with [baseline]. This supports [bounded claim]. The remaining gap in [metric/failure] suggests [limitation or next experiment].
```

Avoid:

- "significantly" without statistical support;
- "clearly demonstrates" for small or preliminary effects;
- only discussing the best metric.

## Limitations

Write limitations as technical boundaries:

- dataset scope;
- metric reliability;
- computational cost;
- missing baselines;
- failure cases;
- assumptions;
- scalability;
- annotation or supervision dependency.

Good limitation:

```text
The evaluation is limited to short clips with known camera metadata; validating longer videos with estimated camera trajectories remains future work.
```

Bad limitation:

```text
More experiments are needed.
```

## Conclusion

Keep it short:

1. Restate the technical contribution.
2. State the best-supported result.
3. State the cleanest implication.

Do not introduce new claims, new citations, or new limitations.
