#!/usr/bin/env python3
"""Validate fixed formatting, 0-3 sections, and continuous ranking-list syntax."""

import argparse
import re
from pathlib import Path


MAX_SECTIONS = 3
FIRST_LIST = r"\begin{enumerate}[series=definitions]"
NEXT_LIST = r"\begin{enumerate}[resume=definitions]"
LIST_END = r"\end{enumerate}"
FORBIDDEN_COMMAND = re.compile(
    r"\\(?:subsection|subsubsection|paragraph|begin|end|section|item|input|include|"
    r"includegraphics|bibliography|bibliographystyle|cite\w*|ref|pageref|label|"
    r"footnote|url|href|def|newcommand|renewcommand|usepackage|title|author|date|"
    r"maketitle|newpage|clearpage|vspace|hspace|pagebreak|setcounter|addtocounter|"
    r"setlist|restartlist)\b"
)


def validate_format(content, template):
    """Check structure, not mathematical importance or correctness of ranking."""
    errors = []
    content = content.replace("\r\n", "\n").replace("\r", "\n")
    template = template.replace("\r\n", "\n").replace("\r", "\n")
    prefix, marker, _ = template.partition("\\maketitle\n")
    if not marker:
        return ["Template has no maketitle anchor."]
    prefix += marker
    if not content.startswith(prefix):
        return ["Preamble, fixed title, or document opening differs from template."]
    remainder = content[len(prefix):]
    closing = r"\end{document}"
    if not remainder.rstrip().endswith(closing):
        return ["Missing document closing or content follows document closing."]
    body = remainder.rstrip()[:-len(closing)]
    state = "opening"
    mode = None
    section_count = 0
    list_count = 0
    item_count = 0
    current_items = 0
    seen_names = set()
    seen_sections = set()

    for line_number, raw_line in enumerate(body.splitlines(), 1):
        line = raw_line.strip()
        if not line:
            continue
        if re.search(r"(?<!\\)%", line):
            errors.append(f"Body line {line_number}: comments are not allowed.")
            continue
        if state == "finished":
            errors.append("An unsectioned document must contain exactly one ranking list.")
            continue
        if state == "opening":
            section = re.fullmatch(r"\\section\{(.+)\}", line)
            if section:
                mode = "sectioned"
                heading = section.group(1).strip()
                if not heading or heading.casefold() == "topic title":
                    errors.append("Replace the empty or example topic heading.")
                if FORBIDDEN_COMMAND.search(heading):
                    errors.append(f"Body line {line_number}: structural command in heading.")
                key = " ".join(heading.split()).casefold()
                if key in seen_sections:
                    errors.append(f"Duplicate section heading: {heading}")
                seen_sections.add(key)
                section_count += 1
                if section_count > MAX_SECTIONS:
                    errors.append(f"At most {MAX_SECTIONS} sections are allowed; prefer no sections.")
                state = "list"
            elif mode is None and line == FIRST_LIST:
                mode = "unsectioned"
                list_count += 1
                current_items = 0
                state = "items"
            else:
                errors.append(
                    f"Body line {line_number}: expected a section or the first ranking list."
                )
            continue
        if state == "list":
            expected = FIRST_LIST if list_count == 0 else NEXT_LIST
            if line != expected:
                errors.append(
                    f"Body line {line_number}: expected {expected}; rankings must not restart."
                )
                continue
            list_count += 1
            current_items = 0
            state = "items"
            continue
        if line == LIST_END:
            if not current_items:
                errors.append(f"Body line {line_number}: empty ranking list.")
            state = "finished" if mode == "unsectioned" else "opening"
            continue

        item = re.fullmatch(r"\\item\s+(.+)", line)
        if not item:
            errors.append(
                f"Body line {line_number}: expected one item per line or enumerate closing."
            )
            continue
        name = item.group(1).strip()
        if name.casefold() == "concept name":
            errors.append("Replace the example concept placeholder.")
        if FORBIDDEN_COMMAND.search(name) or "\\\\" in name:
            errors.append(f"Body line {line_number}: disallowed command in concept name.")
        if re.match(r"^\d+[.)]\s", name):
            errors.append(f"Body line {line_number}: use automatic ranking, not manual numbers.")
        key = " ".join(name.split()).casefold()
        if key in seen_names:
            errors.append(f"Duplicate concept name: {name}")
        seen_names.add(key)
        current_items += 1
        item_count += 1

    if state not in ("opening", "finished"):
        errors.append("Incomplete section or enumerate structure.")
    if not item_count or not list_count:
        errors.append("At least one populated ranking list is required.")
    if mode == "sectioned" and list_count != section_count:
        errors.append("Each section must have exactly one ranking list.")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tex", type=Path)
    parser.add_argument(
        "--template",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "assets" / "core_definitions.tex",
    )
    args = parser.parse_args()
    try:
        errors = validate_format(
            args.tex.read_text(encoding="utf-8-sig"),
            args.template.read_text(encoding="utf-8-sig"),
        )
    except (OSError, UnicodeError) as exc:
        parser.exit(2, f"Cannot read input: {exc}\n")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Format passed: 0-3 sections and continuous rank numbering. Review importance separately.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
