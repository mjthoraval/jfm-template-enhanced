#!/usr/bin/env python3
"""
test_bibliography.py -- check that FLMguide's two bibliography configurations agree.

FLMguide's reference list is generated from jfm.bib with jfm_jabbrv.bst and shipped
inline (the .bbl pasted between the %%%BEGIN-INLINE-BBL%%% / %%%END-INLINE-BBL%%%
markers) so the guide can be submitted without running BibTeX. It is citation-driven:
only references actually \\cite'd in the text appear (the JFM rule -- every reference
must be cited, and vice versa). This test verifies:

  1. FLMguide compiles both inline and via \\bibliography{jfm};
  2. the inline .bbl is identical to a fresh BibTeX run on the citations (never stale);
  3. the rendered reference list is identical in both configurations;
  4. no jabbrv placeholder (@NBSP@/@SPACE@/...) leaks into the output;
  5. entries present in jfm.bib but NOT cited do not appear (rule enforced).

Run from the repo directory:   python test_bibliography.py
Requires pdflatex, bibtex and pdftotext on PATH (MiKTeX or TeX Live).
Exit code 0 = all checks passed, 1 = a check failed.
"""
import os, re, sys, subprocess

HERE = os.path.dirname(os.path.abspath(__file__)) or os.getcwd()
FAILS = []


def run(args):
    subprocess.run(args, cwd=HERE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def read(name):
    with open(os.path.join(HERE, name), encoding="utf-8", errors="replace") as fh:
        return fh.read()


def write(name, text):
    with open(os.path.join(HERE, name), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def norm(text):
    return "\n".join(l.rstrip() for l in text.replace("\r\n", "\n").split("\n")).strip()


def pdftotext(pdf):
    return subprocess.run(["pdftotext", "-layout", pdf, "-"], cwd=HERE,
                          capture_output=True, text=True, errors="replace").stdout


def references(pdf):
    txt = pdftotext(pdf)
    i = txt.lower().rfind("references")
    return norm(txt[i:]) if i >= 0 else ""


def latex(stem):
    run(["pdflatex", "-shell-escape", "-interaction=nonstopmode", stem + ".tex"])


def has_pdf(stem):
    return os.path.exists(os.path.join(HERE, stem + ".pdf"))


def cleanup(*stems):
    for stem in stems:
        for ext in (".tex", ".aux", ".bbl", ".blg", ".log", ".out", ".pdf", ".lnos"):
            try:
                os.remove(os.path.join(HERE, stem + ext))
            except OSError:
                pass


def check(cond, msg):
    print(("  PASS  " if cond else "  FAIL  ") + msg)
    if not cond:
        FAILS.append(msg)


flm = read("FLMguide.tex")

print("[1/4] building the BibTeX configuration (FLMguide's own citations) ...")
# drop the inline block, uncomment \bibliography{jfm}; NO \nocite{*} -> citation-driven
b = re.sub(r"%%%BEGIN-INLINE-BBL%%%.*?%%%END-INLINE-BBL%%%", "", flm, flags=re.S)
b = b.replace("%\\bibliographystyle{jfm_jabbrv}", "\\bibliographystyle{jfm_jabbrv}")
b = b.replace("%\\bibliography{jfm}", "\\bibliography{jfm}")
write("_B.tex", b)
latex("_B"); run(["bibtex", "_B"]); latex("_B"); latex("_B")
check(has_pdf("_B"), "FLMguide compiles in the BibTeX (\\bibliography{jfm}) configuration")
generated = read("_B.bbl") if os.path.exists(os.path.join(HERE, "_B.bbl")) else ""

print("[2/4] checking the inline .bbl is in sync with the citations ...")
m = re.search(r"%%%BEGIN-INLINE-BBL%%%\n(.*?)\n%%%END-INLINE-BBL%%%", flm, re.S)
check(m is not None, "FLMguide.tex contains the inline-bibliography markers")
inline = m.group(1) if m else ""
check(norm(inline) == norm(generated),
      "inline bibliography matches a fresh BibTeX run (else: regenerate and re-paste it)")

print("[3/4] building the inline configuration ...")
write("_A.tex", flm)
latex("_A"); latex("_A")
check(has_pdf("_A"), "FLMguide compiles in the INLINE configuration")

print("[4/4] comparing rendered output ...")
refsA, refsB = references("_A.pdf"), references("_B.pdf")
check(bool(refsA) and refsA == refsB, "rendered reference list is identical in both configurations")
leaks = sorted(set(re.findall(r"@[A-Z]+@", pdftotext("_A.pdf"))))
check(not leaks, "no jabbrv placeholder leaks in the output" + (" (found %s)" % leaks if leaks else ""))
check(("Abramowitz" not in refsA) and ("Barker" not in refsA),
      "uncited jfm.bib entries (Abramowitz, Barker) are absent -- JFM cite rule enforced")

cleanup("_A", "_B")
print()
if FAILS:
    print("RESULT: FAILED (%d)" % len(FAILS))
    sys.exit(1)
print("RESULT: all checks passed")
