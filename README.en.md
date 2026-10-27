# math-core-definitions

English | [中文](README.md)

A Codex skill for readers and researchers who need concise, source-supported lists of mathematical concepts. Supply subject folders, clearly labelled attachments, book PDFs, Index excerpts or existing Index caches. The skill checks the available material, reads all usable indexes, and selects, deduplicates and globally ranks core and important English concept names within each user-designated subject.

Each subject produces one standalone `CLASS_core_definitions.tex`, where `CLASS` is the full subject-folder name, preserving spaces and capitalization. The document contains a fixed title, automatic rank numbers, concept names and optional broad English section headings. `main.tex` and original PDFs are optional when usable Index material is supplied.

Current version: **0.3.0**, from `metadata.version` in [SKILL.md](SKILL.md).

## Features

- Identifies books using a bibliography, manifest or inventory of the actual inputs; preserves the user's subject grouping.
- Reuses readable Index caches, resolves transferred cache paths against supplied files, and repairs only affected Index portions when source PDFs are available.
- Reads all usable subject indexes and concept-bearing notation indexes. PDF access is limited to Index pages and the small amount of cover matter, contents or bookmarks needed for identification and location; no body reading or whole-book extraction/OCR.
- Applies a consistent admission threshold, recovers full names from Index context, and merges genuine synonyms without changing mathematical meaning. There are no book, topic or length quotas.
- Ranks all core concepts before all important concepts, then orders each tier by structural importance to the user's subject. Alphabetical order breaks ties only when no reliable importance distinction remains.
- Requires a concise internal provenance record linking every final rank, name and tier to an identifiable Index entry: book identifier, cache file, usable location and necessary parent context. Known synonym-source links are retained.
- Uses a fixed LaTeX template with no sections by default and at most three; sectioning preserves the global order and continuous automatic numbering.
- Checks a candidate before replacement and preserves any existing output in a unique, byte-verified backup in the working cache.
- Includes a Python structural checker and a standalone prompt package usable without installing the skill.

This is a workflow executed by Codex, not an automated PDF extraction application. The model performs the mathematical selection. The user's subject determines importance; the supplied Index entries determine which candidates have evidence. Frequency, repeated editions, fame, difficulty and teaching order are not ranking weights. Ranks are ordinal positions within one subject, not numerical importance scores, cross-subject measurements or theorem-quality scores.

## Requirements

- A Codex environment with local file access and command execution.
- Python 3 for the read-only checker; it uses only the standard library.
- PDF page-reading and text-extraction tools when PDFs are supplied. Scanned or damaged Index pages also need rendering/OCR tools. Cache-only inputs do not require absent original PDFs.
- A standard LaTeX compiler such as **pdfLaTeX**, plus a PDF viewer or renderer for inspecting the compiled result. The template uses `article`, `cmap`, `fontenc`, `inputenc`, `geometry`, `amsmath`, `amssymb` and `enumitem`.
- Your own source material. This repository does not include books, extracted book indexes or generated subject lists.

## Installation

Clone the repository into the Codex skills directory under the name `math-core-definitions`. If that directory already exists, inspect its contents before changing it; do not overwrite it blindly.

PowerShell:

~~~powershell
$skillsRoot = if ($env:CODEX_HOME) {
    Join-Path $env:CODEX_HOME 'skills'
} else {
    Join-Path $env:USERPROFILE '.codex\skills'
}
New-Item -ItemType Directory -Force -Path $skillsRoot | Out-Null
git clone https://github.com/ZhiyaoXiongMath/math-core-definitions.git (Join-Path $skillsRoot 'math-core-definitions')
~~~

macOS / Linux:

~~~sh
if [ -n "$CODEX_HOME" ]; then
    skills_root="$CODEX_HOME/skills"
else
    skills_root="$HOME/.codex/skills"
fi
mkdir -p "$skills_root"
git clone https://github.com/ZhiyaoXiongMath/math-core-definitions.git "$skills_root/math-core-definitions"
~~~

Invoke `$math-core-definitions` in Codex and supply the input paths or clearly labelled attachments. No fixed subject, book count or model is required. New chats are created only when explicitly requested.

## Usage and input/output example

Example input layout, combining a PDF-based subject and a cache-only subject:

~~~text
library/
├── Differential Geometry/
│   ├── main.tex
│   └── differential-geometry.pdf
└── Topology/
    └── .core-definitions-work/
        ├── index-manifest.json
        └── indexes/
            └── topology-index.txt
~~~

In a Codex chat that can access these paths:

~~~text
$math-core-definitions
Please process these subject folders:
./library/Differential Geometry
./library/Topology
~~~

Expected reader-facing outputs:

~~~text
library/Differential Geometry/Differential Geometry_core_definitions.tex
library/Topology/Topology_core_definitions.tex
~~~

The filename retains the complete folder name, including the space and capital letters in `Differential Geometry`. For attachments labelled `Differential Geometry`, use a working folder with that same label. Working Index material, input-status records, final provenance and any verified backups remain in `.core-definitions-work` or an adequate existing cache layout. Source books, bibliographies and supplied Index material remain unchanged.

The generated list uses entries such as:

~~~latex
\begin{enumerate}[series=definitions]
\item Smooth manifold
\item Tangent bundle
\end{enumerate}
~~~

These filenames and entries illustrate the expected interface and structure; they are not supplied books or a verified ranking. Actual names and positions must follow the available Index evidence and subject-specific review. Different subjects are processed independently, and the same concept may occur in more than one list.

## Standalone prompt package

Use [prompts/README.md](prompts/README.md) without installing the skill. The complete package is independent of the skill installation directory and contains the mandatory quartet: `core-definitions-rules.txt`, `prompt.txt`, `preamble.tex` and `template.tex`.

~~~text
Execute ./prompts/workflow.md.
INPUT_DIRS:
- ./library/Differential Geometry
- ./library/Topology
~~~

[Stage one](prompts/01-extract-indexes.md) handles input accounting and Index material; [stage two](prompts/02-index-to-core-definitions.md) handles selection, ranking and delivery after that material has been checked and read. These Markdown files are concise entrypoints, not replacements for the quartet. Supply all four companion files even when invoking only one stage.

## Rules, template and validation

Read the complete authoritative quartet before processing: [rules](references/core-definitions-rules.txt), [prompt](references/prompt.txt), [preamble](assets/preamble.tex) and [template](assets/template.tex). The stage references provide operational guidance without overriding those rules. Preserve all four files during generation.

Copy `assets/template.tex` and replace its concept-list body. It already embeds the preamble; do not load `preamble.tex` again. The result is standalone and has no dependency on the skill or prompt package. Keep the class, packages, margins, fixed title, author/date fields, list settings and document framing. Pre-document comparison normalizes line endings and ignores trailing blank lines only.

Check a generated candidate from the repository root, for example:

~~~sh
python scripts/validate_output.py "library/Differential Geometry/Differential Geometry_core_definitions.tex"
~~~

The checker verifies structural formatting, including the fixed preamble, zero to three sections, continuous rank syntax and forbidden structural commands. It cannot establish concept-only English content, source support, synonym equivalence, mathematical importance or completeness. Review those separately and match the provenance record to the actual final list.

Compile the actual complete candidate with a compatible compiler such as pdfLaTeX, explicitly selecting its filename. Inspect the rendered pages for clipped text, missing glyphs and numbering defects. A temporary directory may use the target basename before the checked file is copied unchanged into place. Do not substitute `main.tex`, the preamble fragment or an old output for this check. Record successful, unperformed and failed checks separately; an unavailable compiler is different from a failed build.

Before replacing an existing accepted output, create a non-colliding backup in the working cache and verify byte equality. Do not accept a failed candidate. Deliver one TeX file per subject; deliver a PDF only when requested. Disclose actual source gaps, unresolved material, edition differences and incomplete checks briefly outside the TeX.

Validation for this version included 14 checker test methods and a synthetic cache-only workflow that produced a 17-item list, compiled it with pdfLaTeX and inspected the rendered result. This does not establish real-book extraction coverage or mathematical ranking quality. When the user requests a rules update, keep the skill, standalone quartet, guides and checker synchronized.

## Scope and limitations

- An Index is a book's subject index, not its table of contents. All usable relevant Index material must be read; snippets, arbitrary samples and old generated lists are not candidate evidence.
- Readable caches remain usable when original PDFs are absent. A matching hash proves supplied bytes, not OCR correctness or completeness against an absent original. Material may be complete as supplied, partial, unavailable or unresolved.
- Partial sources can support a qualified result, but cannot justify a claim of complete subject coverage. If no usable Index exists for a subject, report the gap and continue with the others; do not add concepts from general knowledge.
- No automatic book downloads or body reading. Final TeX contains no definitions, explanations, citations, source pages, tier labels, scores or reports, including in comments. Provenance is retained internally, not added to the reader-facing list.
