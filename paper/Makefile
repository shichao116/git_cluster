
USE_BIBTEX=yes

all: ms.pdf
pdf: ms.pdf
# General rules on how to make postscript or PDF versions of a document

%.pdf: %.tex
	pdflatex $*.tex $@
ifeq ($(USE_BIBTEX),yes)
	-bibtex $*
endif
	pdflatex $*.tex $@
	pdflatex $*.tex $@

response: response.tex
	pdflatex response.tex || true
	pdflatex response.tex

.PHONY : clean

clean:
	rm -f *.log *.aux *.out *.dvi *.blg *.toc *.lof *.lot *.tbx \
	 *.fgx *~ ms.pdf ms.ps ms.fdb_latexmk ms.fls *.bbl

tar:
	tar cvzf submit.tar.gz fesc-table.tex fesc-table2.tex lf-table.tex \
	macros.tex ms.tex stats-table.tex ms.bbl Figs/*.pdf
