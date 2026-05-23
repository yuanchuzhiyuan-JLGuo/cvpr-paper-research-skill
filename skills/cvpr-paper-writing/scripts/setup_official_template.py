#!/usr/bin/env python3
"""Download and prepare an official top-conference LaTeX author kit.

By default this fetches the latest official CVPR/ICCV/3DV author kit from
cvpr-org/author-kit. For other venues, pass --template-url with an official
LaTeX zip URL.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import textwrap
import urllib.request
import zipfile
from pathlib import Path


REPO_API = "https://api.github.com/repos/cvpr-org/author-kit/releases/latest"
REPO_URL = "https://github.com/cvpr-org/author-kit"


def fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "cvpr-paper-writing-skill"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def download(url: str, dst: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": "cvpr-paper-writing-skill"})
    with urllib.request.urlopen(req, timeout=120) as resp, dst.open("wb") as f:
        shutil.copyfileobj(resp, f)


def copy_tree_contents(src: Path, dst: Path, overwrite: bool) -> None:
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        if item.name == ".git":
            continue
        target = dst / item.name
        if target.exists():
            if not overwrite:
                continue
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()
        if item.is_dir():
            shutil.copytree(item, target)
        else:
            shutil.copy2(item, target)


def find_extracted_root(extract_dir: Path) -> Path:
    children = [p for p in extract_dir.iterdir() if p.is_dir()]
    if len(children) == 1:
        return children[0]
    return extract_dir


def ensure_plan_dirs(output: Path) -> None:
    for rel in [
        "plan/section-blueprints",
        "plan/review",
        "tables",
        "figures",
    ]:
        (output / rel).mkdir(parents=True, exist_ok=True)


def write_if_missing(path: Path, text: str) -> None:
    if not path.exists():
        path.write_text(text, encoding="utf-8")


def make_paper_tex(output: Path, overwrite: bool) -> None:
    paper = output / "paper.tex"
    if paper.exists() and not overwrite:
        return
    paper.write_text(
        textwrap.dedent(
            r"""
            \begin{abstract}
            % Write a 5--7 sentence abstract: problem, gap, idea, method, evaluation, result, implication.
            \end{abstract}

            \section{Introduction}
            \label{sec:introduction}

            % Context pressure, prior routes, unresolved gap, key insight, method preview, contributions.

            \section{Related Work}
            \label{sec:related-work}

            % Organize by technical theme. Each paragraph should synthesize prior work and state a boundary.

            \section{Method}
            \label{sec:method}

            % Define the problem, notation, model, objective, and inference procedure.

            \section{Experiments}
            \label{sec:experiments}

            % Datasets, baselines, metrics, implementation details, main results, ablations, qualitative analysis.

            \section{Limitations}
            \label{sec:limitations}

            % State concrete technical boundaries and what evidence would address them.

            \section{Conclusion}
            \label{sec:conclusion}

            % Restate the contribution and the best-supported implication. Do not introduce new claims.
            """
        ).lstrip(),
        encoding="utf-8",
    )


def fallback_main_tex(output: Path, venue: str, year: str, overwrite: bool) -> str:
    main = output / "main.tex"
    if main.exists() and not overwrite:
        return "main.tex exists; fallback root was not written"
    main.write_text(
        textwrap.dedent(
            rf"""
            % {venue} Paper Template; official style files are from https://github.com/cvpr-org/author-kit

            \documentclass[10pt,twocolumn,letterpaper]{{article}}

            %%%%%%%%% PAPER TYPE - update only when preparing a different version.
            % \usepackage{{cvpr}}              % CAMERA-READY
            \usepackage[review]{{cvpr}}      % REVIEW
            % \usepackage[pagenumbers]{{cvpr}} % arXiv/preprint with page numbers

            % Import additional packages before hyperref.
            \input{{preamble}}

            \definecolor{{cvprblue}}{{rgb}}{{0.21,0.49,0.74}}
            \usepackage[pagebackref,breaklinks,colorlinks,allcolors=cvprblue]{{hyperref}}

            %%%%%%%%% PAPER ID - update after assignment.
            \def\paperID{{*****}}
            \def\confName{{{venue}}}
            \def\confYear{{{year}}}

            %%%%%%%%% TITLE - update.
            \title{{Paper Title}}

            %%%%%%%%% AUTHORS - review mode will display anonymous submission info.
            \author{{Anonymous Authors}}

            \begin{{document}}
            \maketitle
            \input{{paper}}

            {{
                \small
                \bibliographystyle{{ieeenat_fullname}}
                \bibliography{{main}}
            }}

            % WARNING: do not include supplementary pages in the main submission PDF unless allowed.
            % \input{{sec/X_suppl}}

            \end{{document}}
            """
        ).lstrip(),
        encoding="utf-8",
    )
    return "wrote fallback CVPR-style main.tex because no official root file was detected"


def infer_year(tag: str, explicit_year: str | None) -> str:
    if explicit_year:
        return explicit_year
    match = re.search(r"(20\d{2})", tag or "")
    return match.group(1) if match else "2026"


def uncommented(line: str) -> str:
    escaped = False
    for idx, ch in enumerate(line):
        if ch == "\\" and not escaped:
            escaped = True
            continue
        if ch == "%" and not escaped:
            return line[:idx]
        escaped = False
    return line


def likely_root_tex_files(output: Path) -> list[Path]:
    ignored = {"paper.tex", "preamble.tex"}
    candidates: list[Path] = []
    for path in sorted(output.rglob("*.tex")):
        if ".template_download" in path.parts:
            continue
        if path.name in ignored or path.parts[-2:] == ("sec", "X_suppl.tex"):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if "\\documentclass" in text and "\\begin{document}" in text:
            candidates.append(path)
    return candidates


def find_body_region(lines: list[str]) -> tuple[int, int] | None:
    maketitle = None
    begin_doc = None
    for idx, line in enumerate(lines):
        code = uncommented(line)
        if "\\begin{document}" in code and begin_doc is None:
            begin_doc = idx
        if "\\maketitle" in code:
            maketitle = idx
            break

    start = (maketitle + 1) if maketitle is not None else ((begin_doc + 1) if begin_doc is not None else None)
    if start is None:
        return None

    for idx in range(start, len(lines)):
        code = uncommented(lines[idx])
        if "\\bibliographystyle" in code or "\\bibliography" in code or "\\printbibliography" in code:
            end = idx
            while end > start and not uncommented(lines[end - 1]).strip():
                end -= 1
            if end > start and uncommented(lines[end - 1]).strip() == "{":
                end -= 1
            return start, end
        if code.strip() == "{":
            lookahead = "".join(uncommented(line) for line in lines[idx : min(idx + 5, len(lines))])
            if "\\bibliographystyle" in lookahead or "\\bibliography" in lookahead or "\\printbibliography" in lookahead:
                return start, idx
        if "\\end{document}" in code:
            return start, idx
    return start, len(lines)


def inject_paper_input(main: Path, overwrite: bool) -> str:
    text = main.read_text(encoding="utf-8", errors="replace")
    if "\\input{paper}" in text or "\\include{paper}" in text:
        return "official root already includes paper.tex"

    backup = main.with_name("main_template_original.tex")
    if not backup.exists() or overwrite:
        backup.write_text(text, encoding="utf-8")

    lines = text.splitlines(keepends=True)
    region = find_body_region(lines)
    if region is None:
        with main.open("a", encoding="utf-8") as f:
            f.write("\n% Manuscript body added by setup_official_template.py\n\\input{paper}\n")
        return "saved original root as main_template_original.tex; could not identify body region, so appended paper.tex include"

    start, end = region
    replacement = [
        "% Manuscript body lives in paper.tex; official formatting remains in this root file.\n",
        "\\input{paper}\n",
        "\n",
    ]
    main.write_text("".join(lines[:start] + replacement + lines[end:]), encoding="utf-8")
    return "saved original root as main_template_original.tex; preserved official preamble/bibliography and replaced sample body with \\input{paper}"


def prepare_main_tex(output: Path, venue: str, year: str, overwrite: bool, keep_official_main: bool) -> list[str]:
    notes: list[str] = []
    main = output / "main.tex"

    if not main.exists():
        candidates = likely_root_tex_files(output)
        if candidates:
            source = candidates[0]
            shutil.copy2(source, main)
            notes.append(f"copied likely official root `{source.relative_to(output)}` to `main.tex` for Overleaf")
        else:
            notes.append(fallback_main_tex(output, venue, year, overwrite=True))

    if keep_official_main:
        notes.append("kept official main.tex unchanged; add \\input{paper} manually if the audit says it is missing")
        return notes

    if main.exists():
        notes.append(inject_paper_input(main, overwrite=overwrite))
    return notes


def bootstrap_plan_files(output: Path, venue: str, tag: str, release_url: str) -> None:
    write_if_missing(
        output / "plan" / "venue-profile.md",
        textwrap.dedent(
            f"""\
            # Venue Profile

            - Venue: {venue}
            - Track:
            - Year:
            - Review format:
            - Page limit:
            - Supplement policy:
            - Anonymity policy:
            - AI usage / disclosure policy:
            - Official template source: {release_url}
            - Template release: {tag}
            - Bibliography style:
            - Artifact / code policy:
            - Rebuttal policy:
            """
        ),
    )
    write_if_missing(
        output / "plan" / "paper-positioning.md",
        textwrap.dedent(
            f"""\
            # Paper Positioning

            - Venue: {venue}
            - Template release: {tag}
            - Template source: {release_url}

            ## One-Sentence Problem

            ## Gap Against Prior Work

            ## Main Technical Idea

            ## Contributions

            ## Maximum Allowed Claim Strength
            """
        ),
    )
    write_if_missing(
        output / "plan" / "evidence-map.md",
        "| Source ID | Citation | Source type | What it shows | Supported claim | Citation slot | Risk |\n"
        "|---|---|---|---|---|---|---|\n",
    )
    write_if_missing(
        output / "plan" / "method-contract.md",
        "| Method claim | Implemented in | Inputs | Outputs | Assumptions | Unsupported wording |\n"
        "|---|---|---|---|---|---|\n",
    )
    write_if_missing(
        output / "plan" / "experiment-protocol.md",
        textwrap.dedent(
            """\
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
            """
        ),
    )
    write_if_missing(
        output / "plan" / "method-experiment-traceability.md",
        "| Contribution | Required evidence | Experiment | Table/Figure | Current status | Allowed wording |\n"
        "|---|---|---|---|---|---|\n",
    )
    write_if_missing(
        output / "tables" / "table-schema.md",
        "| Table | Purpose | Rows | Metrics | Data source | Aggregation | Claim supported |\n"
        "|---|---|---|---|---|---|---|\n",
    )
    write_if_missing(
        output / "figures" / "data-manifest.md",
        "| Figure | Purpose | Data source | Script/source | Output file | Claim supported |\n"
        "|---|---|---|---|---|---|\n",
    )
    write_if_missing(
        output / "plan" / "section-blueprints" / "intro.md",
        textwrap.dedent(
            """\
            # Introduction Blueprint

            ## Problem Pressure
            ## Prior Route
            ## Unresolved Gap
            ## Method Insight
            ## Contributions
            ## Evidence Boundaries
            """
        ),
    )
    write_if_missing(
        output / "plan" / "section-blueprints" / "related_work.md",
        textwrap.dedent(
            """\
            # Related Work Blueprint

            | Paragraph | Theme | Representative sources | Shared capability | Shared limitation | Link to this paper |
            |---|---|---|---|---|---|
            """
        ),
    )
    write_if_missing(
        output / "plan" / "review" / "claim-registry.md",
        "| Claim ID | Claim text | Type | Section | Support | Evidence file/source | Verdict | Manuscript action |\n"
        "|---|---|---|---|---|---|---|---|\n",
    )
    write_if_missing(
        output / "plan" / "review" / "result-ledger.md",
        "| Result ID | Paper location | Reported value | Source file/log | Command/config | Aggregation | Seeds | Verified? |\n"
        "|---|---:|---|---|---|---|---:|---|\n",
    )
    write_if_missing(
        output / "plan" / "review" / "config-method-audit.md",
        "| Method statement | Code/config/log support | Risk | Fix |\n"
        "|---|---|---|---|\n",
    )
    write_if_missing(
        output / "plan" / "review" / "integrity-audit.md",
        textwrap.dedent(
            """\
            # Integrity Audit

            ## Summary
            - Overall status:
            - Strongest verified claim:
            - Claims weakened:
            - Blocking issues:

            ## Failure Mode Checklist
            | Mode | Status | Evidence | Action |
            |---|---|---|---|

            ## Required Manuscript Edits
            1.
            2.
            3.
            """
        ),
    )
    write_if_missing(
        output / "plan" / "review" / "submission-risk-review.md",
        textwrap.dedent(
            """\
            # Submission Risk Review

            ## Summary Judgment
            - Venue:
            - Current readiness:
            - Biggest reject risk:

            ## Major Risks
            | Risk | Evidence | Severity | Fix | Manuscript action |
            |---|---|---:|---|---|
            """
        ),
    )
    write_if_missing(
        output / "plan" / "review" / "revision-roadmap.md",
        textwrap.dedent(
            """\
            # Revision Roadmap

            ## Priority 0: Blocking
            ## Priority 1: Major
            ## Priority 2: Minor
            ## Claims To Weaken
            ## Experiments To Add
            ## Figures/Tables To Change
            ## Rebuttal Notes
            """
        ),
    )


def inspect_template(output: Path) -> dict:
    main = output / "main.tex"
    sty = output / "cvpr.sty"
    preamble = output / "preamble.tex"
    sec = output / "sec"
    main_text = main.read_text(encoding="utf-8", errors="replace") if main.exists() else ""
    sty_text = sty.read_text(encoding="utf-8", errors="replace") if sty.exists() else ""
    return {
        "has_main_tex": main.exists(),
        "has_paper_tex": (output / "paper.tex").exists(),
        "has_cvpr_sty": sty.exists(),
        "has_preamble": preamble.exists(),
        "has_sec_dir": sec.exists(),
        "main_inputs_paper": "\\input{paper}" in main_text,
        "uses_review_mode": "\\usepackage[review]{cvpr}" in main_text,
        "uses_camera_ready_mode": "\\usepackage{cvpr}" in main_text and "\\usepackage[review]{cvpr}" not in main_text,
        "has_hyperref": "hyperref" in main_text or "hyperref" in sty_text,
        "has_bibliography_style": "ieeenat_fullname" in main_text,
        "has_supplement_input_enabled": "\\input{sec/X_suppl}" in main_text and "% \\input{sec/X_suppl}" not in main_text,
    }


def write_audit(output: Path, venue: str, release: dict, inspection: dict, source_url: str, root_notes: list[str]) -> None:
    checks = "\n".join(f"- {k}: `{v}`" for k, v in inspection.items())
    notes = "\n".join(f"- {note}" for note in root_notes) or "- n/a"
    audit = f"""# Template Audit

## Source

- Venue: {venue}
- Template source: {source_url}
- Default CVPR repository: {REPO_URL}
- Release: {release.get("tag_name", "unknown")}
- Release URL: {release.get("html_url", "unknown")}
- Release note: {release.get("body", "").strip() or "n/a"}

## Detected Template Properties

{checks}

## Root File Preparation

{notes}

## Required Author Actions

1. Keep review mode for anonymous review submissions.
2. Replace `\\paperID{{*****}}` only after a paper ID is assigned.
3. Replace the title and anonymous author block according to venue rules.
4. Keep `main.tex` as the Overleaf root file.
5. Write the manuscript body in `paper.tex`.
6. Put BibTeX entries in `main.bib`.
7. Do not alter margins, fonts, spacing, or `cvpr.sty`.
8. Keep supplementary input disabled in the main submission unless the venue permits it.
9. Compile from a clean state before submission and check unresolved references/citations.

## Body File

Write the manuscript in:

- `paper.tex`

Optional: split `paper.tex` into `sec/*.tex` only if the manuscript becomes large. Keep `main.tex` as the root and keep `\\input{{paper}}` unless you intentionally change the include structure.
"""
    (output / "TEMPLATE_AUDIT.md").write_text(audit, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, help="Output directory for the paper project.")
    parser.add_argument("--venue", default="CVPR", help="Venue label to record in plan files.")
    parser.add_argument("--year", default=None, help="Conference year. Defaults to the year inferred from the official release tag.")
    parser.add_argument("--template-url", default=None, help="Official LaTeX zip URL for non-CVPR venues.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing template files.")
    parser.add_argument("--keep-archive", action="store_true", help="Keep downloaded zip archive.")
    parser.add_argument("--keep-official-main", action="store_true", help="Do not edit main.tex to input paper.tex.")
    args = parser.parse_args()

    output = Path(args.output).resolve()
    output.mkdir(parents=True, exist_ok=True)

    if args.template_url:
        release = {
            "tag_name": f"{args.venue}-custom-template",
            "html_url": args.template_url,
            "body": "User-provided official template URL.",
        }
        zip_url = args.template_url
    else:
        release = fetch_json(REPO_API)
        zip_url = release.get("zipball_url")
        if not zip_url:
            raise RuntimeError("Latest release did not include zipball_url.")
    year = infer_year(release.get("tag_name", ""), args.year)

    tmp_dir = output / ".template_download"
    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)
    tmp_dir.mkdir(parents=True)
    archive = tmp_dir / "author-kit.zip"

    download(zip_url, archive)
    with zipfile.ZipFile(archive) as zf:
        zf.extractall(tmp_dir / "extract")

    root = find_extracted_root(tmp_dir / "extract")
    copy_tree_contents(root, output, overwrite=args.overwrite)
    make_paper_tex(output, overwrite=args.overwrite)
    root_notes = prepare_main_tex(output, args.venue, year=year, overwrite=args.overwrite, keep_official_main=args.keep_official_main)
    ensure_plan_dirs(output)
    bootstrap_plan_files(output, args.venue, release.get("tag_name", "unknown"), release.get("html_url", REPO_URL))
    inspection = inspect_template(output)
    write_audit(output, args.venue, release, inspection, source_url=zip_url, root_notes=root_notes)

    if args.keep_archive:
        shutil.copy2(archive, output / "author-kit.zip")
    shutil.rmtree(tmp_dir)

    print(f"[DONE] Official template prepared at: {output}")
    print(f"[INFO] Release: {release.get('tag_name', 'unknown')}")
    print(f"[INFO] Audit: {output / 'TEMPLATE_AUDIT.md'}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        raise SystemExit(1)
