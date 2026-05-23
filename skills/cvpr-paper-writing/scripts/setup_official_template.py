#!/usr/bin/env python3
"""Download and prepare the official CVPR/ICCV/3DV LaTeX author kit."""

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


def infer_year(tag: str, explicit_year: str | None) -> str:
    if explicit_year:
        return explicit_year
    match = re.search(r"(20\d{2})", tag or "")
    return match.group(1) if match else "2026"


def make_main_tex(output: Path, venue: str, year: str, overwrite: bool) -> None:
    main = output / "main.tex"
    if main.exists() and not overwrite:
        original = main.read_text(encoding="utf-8", errors="replace")
        if "\\input{paper}" in original:
            return
        backup = output / "main_template_original.tex"
        if not backup.exists():
            backup.write_text(original, encoding="utf-8")
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


def bootstrap_plan_files(output: Path, venue: str, tag: str, release_url: str) -> None:
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


def write_audit(output: Path, venue: str, release: dict, inspection: dict) -> None:
    checks = "\n".join(f"- {k}: `{v}`" for k, v in inspection.items())
    audit = f"""# Template Audit

## Source

- Venue: {venue}
- Official repository: {REPO_URL}
- Release: {release.get("tag_name", "unknown")}
- Release URL: {release.get("html_url", "unknown")}
- Release note: {release.get("body", "").strip() or "n/a"}

## Detected Template Properties

{checks}

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
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing template files.")
    parser.add_argument("--keep-archive", action="store_true", help="Keep downloaded zip archive.")
    parser.add_argument("--keep-official-main", action="store_true", help="Do not rewrite main.tex to input paper.tex.")
    args = parser.parse_args()

    output = Path(args.output).resolve()
    output.mkdir(parents=True, exist_ok=True)

    release = fetch_json(REPO_API)
    year = infer_year(release.get("tag_name", ""), args.year)
    zip_url = release.get("zipball_url")
    if not zip_url:
        raise RuntimeError("Latest release did not include zipball_url.")

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
    if not args.keep_official_main:
        make_main_tex(output, args.venue, year=year, overwrite=True)
    ensure_plan_dirs(output)
    bootstrap_plan_files(output, args.venue, release.get("tag_name", "unknown"), release.get("html_url", REPO_URL))
    inspection = inspect_template(output)
    write_audit(output, args.venue, release, inspection)

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
