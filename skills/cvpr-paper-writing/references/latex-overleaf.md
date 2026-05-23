# LaTeX and Overleaf

Use the official template as the source of truth. For CVPR/ICCV/3DV, the current official author kit is maintained at:

```text
https://github.com/cvpr-org/author-kit
```

The setup script downloads the latest CVPR GitHub release by default. If another target venue/year provides a separate author kit page, verify that official page and pass its LaTeX zip URL with `--template-url`.

## Official Template Workflow

1. Run:

```powershell
python skills/cvpr-paper-writing/scripts/setup_official_template.py --output paper_cvpr --venue CVPR
```

For a non-CVPR venue with an official zip:

```powershell
python skills/cvpr-paper-writing/scripts/setup_official_template.py --output paper_topconf --venue NeurIPS --template-url <official-template-zip-url>
```

The script should produce a complete paper project that still contains the original template files. It adds `paper.tex` for the manuscript body and saves the untouched original root as `main_template_original.tex` when it needs to connect `main.tex` to `paper.tex`.

2. Edit the generated files:

```text
paper_cvpr/main.tex
paper_cvpr/preamble.tex
paper_cvpr/paper.tex
paper_cvpr/main.bib
```

3. Upload the whole `paper_cvpr/` folder to Overleaf, or zip the folder contents and import the zip.

4. Set Overleaf's main document to `main.tex`.

5. Use pdfLaTeX unless the venue template says otherwise.

## Root File and Body File

For CVPR-style projects, use this structure:

```text
main.tex   = official root file, package mode, title/authors, \maketitle, \input{paper}, bibliography
paper.tex  = abstract and all manuscript sections
main.bib   = BibTeX entries
preamble.tex = allowed packages/macros before hyperref
```

Do not set `paper.tex` as the Overleaf root. `paper.tex` is intentionally not standalone; it is included by `main.tex` so the official template controls formatting.

For non-CVPR templates, keep the same root/body separation when possible. If the official template requires a different root file, preserve the official root, copy or expose it as `main.tex` for Overleaf when needed, and include `paper.tex` from it. Keep the original root backup in the project so the author can inspect venue-specific formatting requirements.

## Review vs Camera-Ready

CVPR-style review submission:

```latex
\usepackage[review]{cvpr}
```

CVPR-style camera-ready:

```latex
\usepackage{cvpr}
```

CVPR-style arXiv/preprint with page numbers:

```latex
\usepackage[pagenumbers]{cvpr}
```

Do not submit camera-ready mode to anonymous review unless the venue explicitly requests it. For other venues, follow their official review/camera-ready switches.

## Template Files To Preserve

Keep every file from the official kit unless the venue instructions say otherwise. For CVPR-style kits, this includes:

- `cvpr.sty`
- `main.tex`
- `paper.tex`
- `preamble.tex`
- `main.bib`
- `ieeenat_fullname.bst`
- `sec/`
- `main_template_original.tex` when the setup script needed to adapt the root file

Do not replace `cvpr.sty` with an older local copy.

## Formatting Requirements To Respect

The official template controls:

- two-column layout;
- 10pt body text;
- Times-like font stack;
- title and heading style;
- margins and print area;
- review line/page numbering behavior;
- bibliography style;
- figure/table caption size and placement.

Avoid manual overrides:

- `geometry`
- `fullpage`
- `setspace`
- `titlesec`
- custom `\textwidth`, `\oddsidemargin`, `\evensidemargin`, `\topmargin`
- custom caption spacing that changes official style

## Figures and Tables

- Use `figure` for one-column figures and `figure*` for two-column figures.
- Use `table` and `table*` analogously.
- Prefer vector PDF/SVG-derived PDF for diagrams and high-resolution PNG for raster images.
- Ensure text in figures is readable when printed.
- Avoid color-only distinctions; combine color with line style, markers, or labels.
- Table captions go above tables.
- Figure captions go below figures.
- Captions should be self-contained enough for skimming.

## Cross-References

Prefer:

```latex
\Cref{fig:overview} shows ...
... as shown in \cref{tab:main}.
```

Use stable labels:

```latex
\label{fig:method-overview}
\label{tab:main-results}
\label{sec:experiments}
\label{eq:objective}
```

Do not use vague labels like `fig1` or `table2` in new work.

## Bibliography

Use the template's bibliography style:

```latex
{\small
\bibliographystyle{ieeenat_fullname}
\bibliography{main}
}
```

Rules:

- Put BibTeX entries in `main.bib`.
- Do not hand-format references inside the paper body.
- Verify titles, authors, venue, and year for every cited work.
- Cite recent claims from primary sources.

## Supplementary Material

The author kit may include `sec/X_suppl.tex`.

- Keep supplementary content out of the main submission PDF unless the instructions allow it.
- If supplementary is allowed, compile and check it separately when required.
- Never leave the template warning comment unresolved at submission time.

## Overleaf Practical Checks

Before final export:

- Recompile from scratch.
- Confirm `main.tex` is the selected root file.
- Confirm `main.tex` contains `\input{paper}`.
- Check for undefined references and citations.
- Download the PDF and inspect first page, figures, tables, references, and page count.
- Search the source for `TODO`, `FIXME`, `anonymous`, placeholder names, and private paths.
- Verify the PDF metadata if anonymity rules are strict.
