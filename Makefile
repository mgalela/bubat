PYTHON ?= python3
DOCX_TOOLS := tools/docx-generator
DOC_EXPORT := $(DOCX_TOOLS)/export-doc.py
DOC_SELECT := $(DOCX_TOOLS)/select-output.py
DOC_OUT ?= output/documents
DOC_SLUG ?=
DOC_ROOT ?= .

.PHONY: help architecture-docx fsd-docx docs-docx architecture-template-docx fsd-template-docx doc-templates-docx

help:
	@echo "Targets:"
	@echo "  make architecture-docx          Export architecture DOCX from final markdown (fails if missing)"
	@echo "  make fsd-docx                   Export FSD DOCX from final markdown (fails if missing)"
	@echo "  make docs-docx                  Generate architecture + FSD DOCX"
	@echo "  make architecture-template-docx Generate architecture template DOCX"
	@echo "  make fsd-template-docx          Generate FSD template DOCX"
	@echo "Variables: DOC_ROOT=. DOC_OUT=output/documents DOC_SLUG=<slug>"

architecture-docx:
	$(PYTHON) $(DOC_SELECT) --root $(DOC_ROOT) --mode architecture --format docx --output-dir $(DOC_OUT) --require-source $(if $(DOC_SLUG),--slug $(DOC_SLUG),)

fsd-docx:
	$(PYTHON) $(DOC_SELECT) --root $(DOC_ROOT) --mode fsd --format docx --output-dir $(DOC_OUT) --require-source $(if $(DOC_SLUG),--slug $(DOC_SLUG),)

docs-docx: architecture-docx fsd-docx

architecture-template-docx:
	$(PYTHON) $(DOC_EXPORT) --template architecture --format docx --output $(DOC_OUT)/architecture-template.docx

fsd-template-docx:
	$(PYTHON) $(DOC_EXPORT) --template fsd --format docx --output $(DOC_OUT)/fsd-template.docx

doc-templates-docx: architecture-template-docx fsd-template-docx
