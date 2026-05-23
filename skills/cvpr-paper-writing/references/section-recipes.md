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

Use 5-7 sentences:

1. Problem setting.
2. Key limitation of existing approaches.
3. Main idea.
4. Method summary.
5. Evaluation protocol.
6. Main result with evidence boundary.
7. Broader implication or limitation, if space permits.

Checklist:

- Does it say what is new?
- Does it say how it is evaluated?
- Does it avoid claims not supported by experiments?
- Does it avoid citations unless the venue style permits them?

## Introduction

Recommended paragraph roles:

1. **Context pressure**: why the problem matters now.
2. **Prior routes**: what families of methods do.
3. **Gap cascade**: what remains unsolved and why it matters.
4. **Key insight**: the paper's technical move.
5. **Method and evaluation preview**: enough detail to make the contribution concrete.
6. **Contributions**: 3-4 bullets or a compact paragraph.

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
