#!/usr/bin/env python3
"""Check the fixed template and section/item structure without modifying files."""

import argparse
import re
from pathlib import Path


FORBIDDEN_COMMAND = re.compile(
    r"\\(?:subsection|subsubsection|paragraph|begin|end|section|item|input|include|"
    r"includegraphics|bibliography|bibliographystyle|cite\w*|ref|pageref|label|"
    r"footnote|url|href|def|newcommand|renewcommand|usepackage|title|author|date|"
    r"maketitle|newpage|clearpage|vspace|hspace|pagebreak)\b"
)


def validate_format(content, template):
    """Return format errors; semantic correctness requires separate review."""
    errors = []
    content = content.replace("\r\n", "\n").replace("\r", "\n")
    template = template.replace("\r\n", "\n").replace("\r", "\n")
    fixed_prefix, marker, _ = template.partition("\\maketitle\n")
    if not marker:
        return ["Template has no maketitle anchor."]
    fixed_prefix += marker
    if not content.startswith(fixed_prefix):
        return ["Preamble, fixed title, or document opening differs from template."]
    remainder = content[len(fixed_prefix):]
    closing = "\\end{document}"
    if not remainder.rstrip().endswith(closing):
        return ["Missing document closing or content follows document closing."]
    body = remainder.rstrip()[:-len(closing)]
    state = "section"
    section_count = 0
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
        if state == "section":
            section = re.fullmatch(r"\\section\{(.+)\}", line)
            if not section:
                errors.append(f"Body line {line_number}: expected section heading.")
                continue
            heading = section.group(1).strip()
            if heading.casefold() == "topic title":
                errors.append("Replace template topic placeholder.")
            if FORBIDDEN_COMMAND.search(heading):
                errors.append(f"Body line {line_number}: structural command in heading.")
            heading_key = " ".join(heading.split()).casefold()
            if heading_key in seen_sections:
                errors.append(f"Duplicate section heading: {heading}")
            seen_sections.add(heading_key)
            section_count += 1
            state = "list"
        elif state == "list":
            if line != "\\begin{itemize}":
                errors.append(f"Body line {line_number}: expected itemize opening.")
                continue
            current_items = 0
            state = "items"
        elif line == "\\end{itemize}":
            if not current_items:
                errors.append(f"Body line {line_number}: empty itemize.")
            state = "section"
        else:
            item = re.fullmatch(r"\\item\s+(.+)", line)
            if not item:
                errors.append(f"Body line {line_number}: expected one item per line or list closing.")
                continue
            name = item.group(1).strip()
            if name.casefold() == "concept name":
                errors.append("Replace template concept placeholder.")
            if FORBIDDEN_COMMAND.search(name) or "\\\\" in name:
                errors.append(f"Body line {line_number}: disallowed command in concept name.")
            name_key = " ".join(name.split()).casefold()
            if name_key in seen_names:
                errors.append(f"Duplicate concept name: {name}")
            seen_names.add(name_key)
            current_items += 1
            item_count += 1
    if state != "section":
        errors.append("Incomplete section or itemize structure.")
    if not section_count or not item_count:
        errors.append("At least one populated section is required.")
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
    print("Template format passed; mathematical content still requires index-based review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
