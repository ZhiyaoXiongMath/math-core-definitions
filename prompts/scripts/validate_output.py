#!/usr/bin/env python3
"""Check template framing and ranking-list syntax; not mathematical semantics."""

import argparse
import re
from pathlib import Path


MAX_SECTIONS = 3
FIRST_LIST = r"\begin{enumerate}[series=definitions]"
NEXT_LIST = r"\begin{enumerate}[resume=definitions]"
LIST_END = r"\end{enumerate}"
FORBIDDEN_COMMAND = re.compile(
    r"\\(?:subsection|subsubsection|paragraph|subparagraph|chapter|part|"
    r"begin|end|section|item|input|include|includeonly|includegraphics|"
    r"InputIfFileExists|IfFileExists|endinput|verbatiminput|lstinputlisting|"
    r"bibliography|bibliographystyle|cite[A-Za-z]*|ref|pageref|eqref|label|"
    r"footnote|footnotemark|footnotetext|marginpar|url|href|"
    r"def|gdef|edef|xdef|let|futurelet|newcommand|renewcommand|providecommand|"
    r"DeclareRobustCommand|NewDocumentCommand|RenewDocumentCommand|"
    r"ProvideDocumentCommand|DeclareDocumentCommand|DeclareMathOperator|"
    r"newenvironment|renewenvironment|newtheorem|usepackage|RequirePackage|"
    r"documentclass|title|author|date|maketitle|tableofcontents|"
    r"newpage|clearpage|cleardoublepage|vspace|hspace|pagebreak|linebreak|"
    r"newline|par|setcounter|addtocounter|stepcounter|refstepcounter|"
    r"newcounter|setlist|restartlist|setlength|addtolength|newlength|"
    r"centering|raggedright|raggedleft|noindent|indent|smallskip|medskip|bigskip|"
    r"textbf|textit|textsl|textsc|textsf|texttt|emph|bfseries|itshape|"
    r"color|textcolor|colorbox|fcolorbox|rule|hrule|vrule|"
    r"tiny|scriptsize|footnotesize|small|normalsize|large|Large|LARGE|huge|Huge|"
    r"special|write|openout|closeout|read|openin|closein|immediate|"
    r"csname|endcsname|catcode|makeatletter|makeatother|ExplSyntaxOn|"
    r"ExplSyntaxOff|directlua|pdf[A-Za-z]*|every[A-Za-z]*|"
    r"expandafter|noexpand|scantokens|toks|loop|repeat|newif|"
    r"global|long|outer|protected|begingroup|endgroup|bgroup|egroup|"
    r"afterassignment|aftergroup|font|fontfamily|fontseries|fontshape|"
    r"fontsize|selectfont|usefont)(?![A-Za-z])"
)


def normalize_newlines(text):
    return text.replace("\r\n", "\n").replace("\r", "\n")


def without_trailing_blank_lines(text):
    """Ignore blank lines, never whitespace attached to a content line."""
    lines = text.split("\n")
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines)


def has_comment(text):
    """A percent is escaped only after an odd run of backslashes."""
    for match in re.finditer("%", text):
        start = match.start()
        preceding = start
        while preceding and text[preceding - 1] == "\\":
            preceding -= 1
        if (start - preceding) % 2 == 0:
            return True
    return False


def name_errors(name):
    """Mechanical checks only; English, concept identity and prose need review."""
    errors = []
    if FORBIDDEN_COMMAND.search(name) or "\\\\" in name:
        errors.append("disallowed command")
    if "\\[" in name or "\\]" in name or "$$" in name:
        errors.append("display math is not part of an inline concept name")
    if "^^" in name:
        errors.append("TeX character-code escapes are not ordinary notation")
    return errors


def validate_format(content, template):
    """Check structure, not mathematical importance or correctness of ranking."""
    errors = []
    content = normalize_newlines(content)
    template = normalize_newlines(template)
    document_start = r"\begin{document}"
    template_preamble, marker, template_remainder = template.partition(document_start)
    if not marker:
        return ["Template has no document opening."]
    preamble, marker, remainder = content.partition(document_start)
    if not marker or without_trailing_blank_lines(preamble) != without_trailing_blank_lines(template_preamble):
        return ["Pre-document block differs from template (only line endings and trailing blank lines may differ)."]
    if not preamble.endswith("\n"):
        return ["Document opening must start on its own line, as in the template."]
    opening, anchor, _ = template_remainder.partition("\\maketitle\n")
    if not anchor:
        return ["Template has no maketitle anchor."]
    opening += anchor
    if not remainder.startswith(opening):
        return ["Document opening or maketitle framing differs from template."]
    remainder = remainder[len(opening):]
    closing = r"\end{document}"
    remainder = without_trailing_blank_lines(remainder)
    if not remainder.endswith("\n" + closing):
        return ["Missing document closing or content follows document closing."]
    body = remainder[:-len(closing)]
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
        if has_comment(line):
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
                for issue in name_errors(heading):
                    errors.append(f"Body line {line_number}: {issue} in heading.")
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
        if name.startswith("["):
            errors.append(f"Body line {line_number}: manual item labels are not allowed.")
        if name.casefold() == "concept name":
            errors.append("Replace the example concept placeholder.")
        for issue in name_errors(name):
            errors.append(f"Body line {line_number}: {issue} in concept name.")
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
        default=Path(__file__).resolve().parent.parent / "template.tex",
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
    print("Structural format passed: fixed template, 0-3 sections, and continuous automatic rank syntax.")
    print("Still review English concept-only content, source support, provenance, synonyms and importance; compile and inspect the actual output.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
