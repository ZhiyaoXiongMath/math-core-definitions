# math-core-definitions

English | [中文](README.md)

A Codex skill for readers and researchers who need concise lists of mathematical concepts. Provide one or more local folders containing a main.tex bibliography and mathematical book PDFs. The skill first extracts and caches each book's back-of-book index, then selects, deduplicates and globally ranks concepts by importance into core_definitions.tex inside each input folder.

The output contains continuous rank numbers, English names of core and important mathematical concepts, and optional broad English topic headings, without explaining the definitions. Each folder represents a category chosen by the user and is processed and ranked independently.

Current version: 0.2.0, sourced from metadata.version in SKILL.md.

## Features

- Matches book PDFs using citation keys, MR numbers, titles and authors in main.tex.
- Reads index pages and limited locating material, without reading the full body, extracting full-book text or running full-book OCR.
- Preserves index page references, subentries and cross-references; caches provenance and processing status, and reuses valid caches.
- Selects core and important concepts from the indexes, normalizes English terminology, and merges synonyms and duplicates within each category.
- Places core definitions before important definitions, with descending importance within each tier; continuous numbering starts at 1, the highest rank.
- Uses a fixed article template with enumerate entries. No sections by default, at most 3; sectioning must not change the global order or restart numbering.
- Includes a read-only Python format checker for the template, section limit, continuous-numbering syntax, duplicate entries and unfilled example content.
- Bundles standalone two-stage Markdown prompts, a template and a checker that can be used without installing the skill.
- Produces one independent list per input folder. New chats are created only when explicitly requested.

This is a skill workflow executed by Codex, not a standalone automated PDF extraction program. The script checks output formatting; the model performs the mathematical selection.

The ranking provides concept-importance context for later theorem evaluation. It prioritizes structural roles in the category's central problems, main theories, major theorems and key methods, rather than mechanically using frequency, difficulty or teaching order. Ranks are not numerical scores or direct measures of theorem quality, and ranks across categories do not share a calibrated scale.

## Requirements

- A Codex environment with local file access and command execution.
- Python 3 for the format checker, which uses only the standard library.
- PDF page-reading and text-extraction tools. Scanned indexes also require page rendering and OCR capabilities.
- A LaTeX compiler for final validation, such as Codex's compile_latex_document tool or a local LaTeX installation. The template uses article, fontenc, inputenc, geometry, amsmath, amssymb and enumitem.
- Your own main.tex and corresponding book PDFs. This repository contains no books, extracted index data or generated results.

## Installation

Clone the repository into the Codex skills directory under the name math-core-definitions. If that directory already exists, inspect its contents before changing it; do not overwrite it blindly.

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

Then invoke $math-core-definitions in Codex and supply the source folder paths. The default workflow has no fixed subject, book count, model or machine-specific path.

## Usage and input/output example

Prepare your materials, for example:

~~~text
library/
├── topology/
│   ├── main.tex
│   └── algebraic-topology.pdf
└── geometry/
    ├── main.tex
    └── differential-geometry.pdf
~~~

These filenames illustrate the layout; you provide the actual books. In a Codex chat that can access those relative paths, enter:

~~~text
$math-core-definitions
Please process these folders:
./library/topology
./library/geometry
~~~

Expected additions inside each input directory:

~~~text
core_definitions.tex
.core-definitions-work/
├── index-manifest.json
└── indexes/
    └── Per-book index text and any necessary index-page images
~~~

The final deliverables are two core_definitions.tex files. Each list combines available indexes from its own directory without reclassifying material across folders. The same concept may appear in different categories. The original main.tex and PDFs are preserved.

Example entry structure in the generated document:

~~~latex
\begin{enumerate}[series=definitions]
\item Smooth manifold
\item Tangent bundle
\end{enumerate}
~~~

This illustrates the expected structure. It does not mean the repository includes those books, extraction has been run against the example PDFs, or the example concepts' actual ranks have been verified. Actual ranking must follow each folder's index evidence and selection rules.

## Standalone prompts without skill installation

After obtaining the repository, use the standalone prompt pack described in [prompts/README.md](prompts/README.md). You still need an execution environment with local file access and PDF/TeX capabilities. The complete pack can be copied and reused independently of the skill installation directory.

~~~text
Execute ./prompts/workflow.md.
INPUT_DIRS:
- ./library/topology
- ./library/geometry
MODE: direct execution
~~~

Each folder still runs index caching before ranking and produces one core_definitions.tex. You can also invoke [stage one](prompts/01-extract-indexes.md) alone to cache indexes, or [stage two](prompts/02-index-to-core-definitions.md) on existing caches to repeat selection and ranking. The stage-two Markdown includes the complete template and can be supplied on its own.

## Template, validation and future changes

- assets/core_definitions.tex is the fixed template. Its preamble, title and page settings stay unchanged; only ranked concept names and optional topic headings are filled.
- references/extract-indexes.md defines index extraction and caching.
- references/select-definitions.md defines selection, integration, global importance ranking and output requirements.
- scripts/validate_output.py checks the resulting TeX without modifying it. Example:

~~~sh
python scripts/validate_output.py path/to/core_definitions.tex
~~~

After the format check, the skill validates compilation with an available LaTeX tool. Select core_definitions.tex explicitly so the compiler does not use the adjacent main.tex instead. Internal compilation previews are not delivered as PDFs.

If sections are needed, form the global ranking first, then split it into at most 3 natural, contiguous blocks. Each section has exactly one enumerate list: the first uses [series=definitions], and subsequent lists use [resume=definitions]. If natural sections cannot preserve the ranking, use the default unsectioned list.

This version has validated skill structure, compilation of the template and zero-/three-section examples, and the format checker's acceptance/rejection behavior. End-to-end extraction from real mathematical books and mathematical ranking quality are not automated tests.

When refining the output format, update the template, second-stage instructions and checker in both the skill and standalone prompt pack together.

## Scope and limitations

- Index means the mathematical subject index at the back of a book, not the table of contents.
- The list covers candidates represented in the extracted indexes; it cannot guarantee coverage of definitions omitted from those indexes.
- Missing PDFs, indexes that cannot be located and unreadable pages are recorded accurately while available material is processed. If no index is available, the skill does not fabricate a list from general knowledge.
- Books are not downloaded automatically. Results contain no definition bodies, page references, citations, tier labels, numerical scores or importance explanations; no PDF or audit report is delivered.
- The format checker cannot determine mathematical importance, ranking correctness, synonym equivalence or completeness. The model must review those against the index evidence.
