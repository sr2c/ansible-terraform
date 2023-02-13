SHELL := /bin/bash

export README_TEMPLATE_FILE ?= $(BUILD_HARNESS_EXTENSIONS_PATH)/templates/README.md.gotmpl
export README_DEPS ?= docs/ansible.md docs/targets.md

-include $(shell curl -sSL -o .build-harness "https://cloudposse.tools/build-harness"; echo .build-harness)


