# Evidence and Related Work

Use this reference for Introduction, Related Work, and any claim that depends on prior work. Pair it with `integrity-gates.md` when checking whether cited sources truly support the manuscript's claims.

## Evidence Map

Create `plan/evidence-map.md`:

| Source ID | Citation | Source type | What it shows | Supported claim | Citation slot | Risk |
|---|---|---|---|---|---|---|

Rules:

- Use primary sources when possible.
- For recent models, datasets, benchmarks, or rules, verify current information.
- Do not cite a paper for a claim that is only implied by the title.
- Mark weak support as `Risk: indirect`.
- Separate factual background from comparative claims.

## Claim Types

| Claim type | Required evidence |
|---|---|
| A method exists | original paper or official project |
| A benchmark measures X | benchmark paper or official docs |
| A model achieves SOTA | current leaderboard or paper table; verify recency |
| Prior work lacks Y | careful comparison across representative works |
| The proposed method improves X | own experiment with fair baseline |
| A trend is emerging | multiple recent primary sources |

## Related Work Blueprint

For each paragraph:

```markdown
### Paragraph N
- Theme:
- Representative sources:
- Shared capability:
- Shared limitation:
- Link to our paper:
- Forbidden overclaim:
```

## Synthesis Patterns

Contrast:

```text
While [family A] improves [capability], it typically assumes [condition]. [Family B] relaxes [condition] but still depends on [limitation]. Our work targets [gap].
```

Boundary:

```text
These methods are complementary to ours: they address [level/module], whereas this paper studies [different level/module].
```

Progression:

```text
Early approaches [did X], recent methods [do Y], but the evaluation of [property Z] remains underdeveloped.
```

## Citation Hygiene

- Use `\cite{...}` or `\citep{...}` consistently with the template.
- Do not cite unavailable private documents.
- Do not invent BibTeX entries.
- Verify author names, year, title, venue, and arXiv identifiers.
- If using a project page for an unreleased system, cite it as a web/source note only if allowed.

## Common Related-Work Failures

- Chronological paper dump.
- Too many citations in one sentence with no synthesis.
- Missing the strongest closest work.
- Attacking prior work unfairly.
- Claiming novelty because "no one has combined A and B" without explaining why the combination matters.
- Treating related work as detached from the paper's experiments.
