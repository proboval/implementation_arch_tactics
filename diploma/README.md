# Thesis Document

LaTeX source for the thesis: "Automated Implementation of Architectural Tactics for Software Quality Improvement".

## Building

```bash
cd latex_diploma
pdflatex thesis.tex
biber thesis
pdflatex thesis.tex
pdflatex thesis.tex
```

## Structure

```
latex_diploma/
├── thesis.tex     # Main document
├── ref.bib        # Bibliography (biber format)
└── chapters/      # Chapter files
```
