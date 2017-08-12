SPHINXOPTS  =
SPHINXBUILD = python -msphinx
SPHINXPROJ  = YouShouldRead
SOURCEDIR   = source
BUILDDIR    = build


.PHONY: help Makefile
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
