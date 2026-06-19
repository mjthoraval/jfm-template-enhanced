# jfm-template-enhanced

Enhanced [Journal of Fluid Mechanics](https://www.cambridge.org/core/journals/journal-of-fluid-mechanics)
(JFM) LaTeX template: the **official 2025 template** plus a drop-in enhanced
BibTeX style that adds clickable DOI/URL reference hyperlinks, automatic
journal-name abbreviation, and a few citation/reference fixes.

The class and style files (`JFM-FLM_Au.cls`, `jfm.bst`, `lineno-FLM.sty`) are
the ones distributed by Cambridge University Press in March 2025 (downloaded
from the JFM ["Preparing your materials"](https://www.cambridge.org/core/journals/journal-of-fluid-mechanics/information/author-instructions/preparing-your-materials)
page) and are **unmodified**. The bibliography enhancements live in separate
files (`jfm_jabbrv.bst`, `patches.sty`) so the official template can be updated
without losing them. `jfm.bib` has DOIs added to its entries, and
`FLMguide.tex`'s reference list is now generated from `jfm.bib` via
`jfm_jabbrv.bst` (pasted inline so the guide compiles without a BibTeX run),
which brings in the DOI links, journal abbreviation and published-style
formatting automatically.

## Usage

```latex
\documentclass[lineno]{JFM-FLM_Au}
\usepackage{patches}          % journal abbreviation + DOI/year hyperlinks
% ... your preamble ...
\begin{document}
% ... your paper ...
\bibliographystyle{jfm_jabbrv} % enhanced style (use {jfm} for the plain official one)
\bibliography{your-references}
\end{document}
```

Compile with the usual `pdflatex → bibtex → pdflatex → pdflatex` cycle.
[`FLMguide.tex`](FLMguide.tex) is the worked example: its reference list is
generated from [`jfm.bib`](jfm.bib) with `jfm_jabbrv.bst` and shipped two
equivalent ways — **inline** (the `.bbl` pasted in, so it compiles without a
BibTeX run — this is what you submit) or via **`\bibliography{jfm}`**. Run
[`test_bibliography.py`](test_bibliography.py) to check that both configurations
compile and produce an identical reference list (and that the inline copy is not
stale).

## Enhancements

All of these are in `jfm_jabbrv.bst` (a copy of the official `jfm.bst` with the
changes below) and `patches.sty`:

- **Clickable reference hyperlinks** — each reference links to its **DOI**
  (`https://doi.org/...`) if a `doi` field is present, otherwise to its `url`.
- **Automatic journal-title abbreviation** — journal names are wrapped in
  `\JournalTitle{...}` and abbreviated to ISO-4 form (e.g. *Journal of Fluid
  Mechanics* → *J. Fluid Mech.*) via the [jabbrv](https://github.com/compholio/jabbrv)
  package.
- **Author first names → initials** in the reference list.
- **"et al." for more than 10 authors**, per the JFM guidelines.
- **Fixed the `others` case** in author lists.
- **arXiv eprint hidden once published** — an `eprint` is only printed when the
  entry has no `volume`.
- **No empty `, ,`** when a book/series entry has no series.
- **Published page style** — no `pp.`/`p.` before page numbers, and hyphen page
  ranges become en-dashes, matching the printed JFM reference format.
- **Year-only citation hyperlinks** — `\citep`/`\citet` link only the year (as
  in the published articles), via a small `natbib` patch in `patches.sty`.

## Files

| File | Origin | Role |
|------|--------|------|
| `JFM-FLM_Au.cls` | Cambridge, 2025 (unmodified) | the JFM document class |
| `jfm.bst` | Cambridge, 2025 (unmodified) | the plain official BibTeX style |
| `lineno-FLM.sty` | Cambridge, 2025 (unmodified) | line numbers (`lineno` option) |
| `jfm_jabbrv.bst` | **enhanced** | `jfm.bst` + the bibliography enhancements above |
| `patches.sty` | **enhanced** | loads jabbrv, sets hyperlink options, year-only citation patch |
| `jabbrv.sty`, `jabbrv-ltwa-*.ldf` | [compholio/jabbrv](https://github.com/compholio/jabbrv) | journal-abbreviation engine + ISO-4 word lists |
| `jabbrv-jfm.ldf` | this repo | custom/extra journal abbreviations |
| `natbib.sty` | bundled (v8.31b) | the natbib version the year-only patch targets |
| `jfm.bib` | Cambridge example + DOIs added | example bibliography database |
| `FLMguide.tex`, `FLMguide.pdf` | Cambridge guide, adapted | worked example; reference list generated from `jfm.bib` (inline `.bbl` + `\bibliography{jfm}` toggle) |
| `Fig1.eps`, `Fig2.eps` | Cambridge, 2025 | figures used by `FLMguide.tex` |
| `test_bibliography.py` | this repo | checks the inline and `\bibliography{jfm}` configs compile and produce an identical reference list |

## Provenance, modifications & licensing

Every file records its own origin and changes in its header; this is the summary.

**Unmodified Cambridge files** — © Cambridge University Press, for use only in
preparing papers for Cambridge journals; included verbatim from the 2025 JFM
author-materials page: `JFM-FLM_Au.cls`, `jfm.bst`, `lineno-FLM.sty` (Cambridge's
wrapper around the `lineno` package), `Fig1.eps`, `Fig2.eps`.

**Cambridge files adapted here** (each carries a header listing its changes):
- `jfm.bib` — Cambridge's example database (`jfm2esam.bib`); DOIs/URLs added and a
  few example references corrected (Batchelor, Brownell, Ursell, Briukhanov, …).
- `FLMguide.tex` / `FLMguide.pdf` — Cambridge's author guide, with
  `\usepackage{patches}`, the bibliography switched to the generated inline `.bbl`,
  and one added citation/note so the guide obeys the JFM "every reference must be
  cited" rule.

**Third-party packages, bundled unmodified:**
- `jabbrv.sty`, `jabbrv-ltwa-*.ldf` — © **Erich Hoover**, latest from
  <https://github.com/compholio/jabbrv> (journal-abbreviation engine + ISO-4 lists).
- `natbib.sty` — © **Patrick W. Daly** (v8.31b, the version the year-only patch targets).

**Enhancements by Marie-Jean Thoraval** (first derived 2018, re-derived 2025 against
`JFM-FLM_Au.cls`):
- `jfm_jabbrv.bst` — a modified copy of `jfm.bst` (which keeps its original
  jfm.bst / merlin.mbs header, P.W. Daly): author initials, "et al." for >10 authors,
  journal abbreviation via jabbrv, DOI/URL links anchored on text, no "pp.", and more.
- `patches.sty` — loads jabbrv, sets the hyperlink options, and patches natbib for
  year-only citation links.
- `jabbrv-jfm.ldf` — custom JFM journal abbreviations, under the LaTeX Project Public
  License (LPPL 1.3c).
