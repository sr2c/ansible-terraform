SHELL := /bin/bash

export README_TEMPLATE_FILE ?= $(BUILD_HARNESS_EXTENSIONS_PATH)/templates/README.md.gotmpl
export README_DEPS ?= docs/ansible.md docs/targets.md

-include $(shell curl -sSL -o .build-harness "https://cloudposse.tools/build-harness"; echo .build-harness)

docs/ansible.md: $(wildcard defaults/*.yml handlers/*.yml tasks/*.yml vars/*.yml)
	@echo "<!-- markdownlint-disable -->" > $@
	@$(BUILD_HARNESS_EXTENSIONS_PATH)/bin/ansible_readme.py >> $@
	@echo "<!-- markdownlint-enable -->" >> $@

