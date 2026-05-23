#!/usr/bin/env python3
"""Static checks for a top-conference LaTeX paper directory."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


FORBIDDEN_PACKAGES = {
    "geometry": "official template controls margins",
    "fullpage": "official template controls margins",
    "setspace": "official template controls spacing",
    "titlesec": "official template controls heading style",
}

TODO_PATTERNS = [
    r"\bTODO\b",
    r"\bFIXME\b",
    r"\bTBD\b",
    r"\?\?\?",
    r"replace before submission",
    r"PLANNING DATA",
]

ANON_PATTERNS = [
    r"acknowledg(e)?ments?",
    r"grant\s+\w+",
    r"funded by",
    r"supported by",
    r"github\.com/[A-Za-z0-9_.-]+/",
    r"C:\\Users\\",
    r"/home/[A-Za-z0-9_.-]+/",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def tex_files(root: Path) -> list[Path]:
    return sorted(root.rglob("*.tex"))


def strip_latex_comment(line: str) -> str:
    escaped = False
    for i, ch in enumerate(line):
        if ch == "\\" and not escaped:
            escaped = True
            continue
        if ch == "%" and not escaped:
            return line[:i]
        escaped = False
    return line


def resolve_input(root: Path, base: Path, name: str) -> Path:
    raw = Path(name)
    if raw.suffix == "":
        raw = raw.with_suffix(".tex")
    if raw.is_absolute():
        return raw
    candidates = [base.parent / raw, root / raw]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def included_tex_files(root: Path) -> list[Path]:
    main = root / "main.tex"
    seen: set[Path] = set()
    ordered: list[Path] = []
    input_re = re.compile(r"\\(?:input|include)\{([^}]+)\}")

    def visit(path: Path) -> None:
        path = path.resolve()
        if path in seen or not path.exists():
            return
        seen.add(path)
        ordered.append(path)
        for line in read(path).splitlines():
            code = strip_latex_comment(line)
            for match in input_re.finditer(code):
                visit(resolve_input(root, path, match.group(1)))

    visit(main)
    return ordered


def add_issue(issues: list[tuple[str, str, str]], severity: str, path: str, msg: str) -> None:
    issues.append((severity, path, msg))


def is_cvpr_style(root: Path, main_text: str) -> bool:
    return (root / "cvpr.sty").exists() or "usepackage[review]{cvpr}" in main_text or "usepackage{cvpr}" in main_text


def check_required_files(root: Path, issues: list[tuple[str, str, str]], cvpr_style: bool) -> None:
    for rel in ["main.tex", "paper.tex"]:
        if not (root / rel).exists():
            add_issue(issues, "ERROR", rel, "required paper project file is missing")

    if not cvpr_style:
        return

    for rel in ["cvpr.sty", "preamble.tex", "main.bib", "ieeenat_fullname.bst"]:
        if not (root / rel).exists():
            add_issue(issues, "ERROR", rel, "required CVPR-style official template file is missing")
    if not (root / "sec").exists():
        add_issue(issues, "WARN", "sec/", "CVPR author-kit section directory is missing")


def check_main(root: Path, issues: list[tuple[str, str, str]], cvpr_style: bool) -> None:
    main = root / "main.tex"
    text = read(main)
    if not text:
        return

    if cvpr_style and "\\usepackage[review]{cvpr}" not in text:
        add_issue(issues, "WARN", "main.tex", "review mode not detected; check whether this is intended")
    if cvpr_style and "\\usepackage{cvpr}" in text and "\\usepackage[review]{cvpr}" not in text:
        add_issue(issues, "WARN", "main.tex", "camera-ready mode detected; do not use for anonymous review")
    if cvpr_style and "ieeenat_fullname" not in text:
        add_issue(issues, "WARN", "main.tex", "template bibliography style not detected")
    if "\\input{sec/X_suppl}" in text and "% \\input{sec/X_suppl}" not in text:
        add_issue(issues, "WARN", "main.tex", "supplement input appears enabled in main PDF")
    if cvpr_style and "\\def\\paperID{*****}" in text:
        add_issue(issues, "WARN", "main.tex", "paper ID placeholder is still present")
    if "\\input{paper}" not in text:
        add_issue(issues, "WARN", "main.tex", "`\\input{paper}` not detected; expected body file workflow")
    if not (root / "paper.tex").exists():
        add_issue(issues, "ERROR", "paper.tex", "body file is missing")


def check_forbidden_packages(root: Path, issues: list[tuple[str, str, str]]) -> None:
    pattern = re.compile(r"\\usepackage(?:\[[^\]]*\])?\{([^}]+)\}")
    for path in included_tex_files(root):
        text = read(path)
        for match in pattern.finditer(text):
            packages = [p.strip() for p in match.group(1).split(",")]
            for pkg in packages:
                if pkg in FORBIDDEN_PACKAGES:
                    add_issue(issues, "ERROR", str(path.relative_to(root)), f"uses `{pkg}`; {FORBIDDEN_PACKAGES[pkg]}")


def check_todos(root: Path, issues: list[tuple[str, str, str]]) -> None:
    compiled = [re.compile(p, re.IGNORECASE) for p in TODO_PATTERNS]
    for path in included_tex_files(root) + sorted(root.rglob("*.bib")):
        text = read(path)
        for lineno, line in enumerate(text.splitlines(), start=1):
            code = strip_latex_comment(line)
            if re.search(r"\\(?:newcommand|renewcommand)\{\\(?:todo|TODO)\}", code):
                continue
            if any(p.search(code) for p in compiled):
                add_issue(issues, "WARN", f"{path.relative_to(root)}:{lineno}", "unresolved TODO/planning marker")


def check_anonymity(root: Path, issues: list[tuple[str, str, str]]) -> None:
    compiled = [re.compile(p, re.IGNORECASE) for p in ANON_PATTERNS]
    for path in included_tex_files(root) + sorted(root.rglob("*.bib")):
        text = read(path)
        for lineno, line in enumerate(text.splitlines(), start=1):
            code = strip_latex_comment(line)
            stripped = code.strip()
            if stripped.startswith("%") and "github.com/cvpr-org/author-kit" in stripped:
                continue
            if any(p.search(code) for p in compiled):
                add_issue(issues, "WARN", f"{path.relative_to(root)}:{lineno}", "possible anonymity or private-path leak")


def check_labels_and_refs(root: Path, issues: list[tuple[str, str, str]]) -> None:
    all_text = "\n".join("\n".join(strip_latex_comment(line) for line in read(p).splitlines()) for p in included_tex_files(root))
    labels = set(re.findall(r"\\label\{([^}]+)\}", all_text))
    refs = re.findall(r"\\(?:C?ref|autoref|eqref)\{([^}]+)\}", all_text)
    for ref_group in refs:
        for ref in [r.strip() for r in ref_group.split(",")]:
            if ref and ref not in labels:
                add_issue(issues, "WARN", "refs", f"reference `{ref}` has no matching label in source")

    duplicate_labels = []
    seen = set()
    for label in re.findall(r"\\label\{([^}]+)\}", all_text):
        if label in seen:
            duplicate_labels.append(label)
        seen.add(label)
    for label in sorted(set(duplicate_labels)):
        add_issue(issues, "WARN", "labels", f"duplicate label `{label}`")


def check_figures(root: Path, issues: list[tuple[str, str, str]]) -> None:
    all_text = "\n".join("\n".join(strip_latex_comment(line) for line in read(p).splitlines()) for p in included_tex_files(root))
    graphics = re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", all_text)
    for g in graphics:
        candidates = [root / g]
        if not Path(g).suffix:
            candidates.extend(root / f"{g}{ext}" for ext in [".pdf", ".png", ".jpg", ".jpeg"])
        if not any(c.exists() for c in candidates):
            add_issue(issues, "WARN", "figures", f"graphic `{g}` was not found")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper-dir", required=True, help="Paper directory containing main.tex.")
    parser.add_argument("--fail-on-warn", action="store_true", help="Return nonzero if warnings are present.")
    args = parser.parse_args()

    root = Path(args.paper_dir).resolve()
    issues: list[tuple[str, str, str]] = []
    main_text = read(root / "main.tex")
    cvpr_style = is_cvpr_style(root, main_text)

    check_required_files(root, issues, cvpr_style)
    check_main(root, issues, cvpr_style)
    check_forbidden_packages(root, issues)
    check_todos(root, issues)
    check_anonymity(root, issues)
    check_labels_and_refs(root, issues)
    check_figures(root, issues)

    if issues:
        for severity, path, msg in issues:
            print(f"[{severity}] {path}: {msg}")
    else:
        print("[OK] static submission checks passed")

    has_error = any(sev == "ERROR" for sev, _, _ in issues)
    has_warn = any(sev == "WARN" for sev, _, _ in issues)
    if has_error or (args.fail_on_warn and has_warn):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
