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

## Credits and licensing

- The JFM class and BibTeX style are © Cambridge University Press and may only
  be used to prepare papers for Cambridge journals. They are included here
  unmodified for convenience.
- `jabbrv` and its LTWA abbreviation lists are by Marco Cuoghi / contributors,
  from <https://github.com/compholio/jabbrv>.
- `natbib` is by Patrick W. Daly.
- The enhancements in `jfm_jabbrv.bst` and `patches.sty` are by
  Marie-Jean Thoraval. Originally derived in 2018 from the then-current JFM
  template and re-derived in 2025 against the official `JFM-FLM_Au.cls` template.
