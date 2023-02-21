SHELL := /bin/bash

export README_TEMPLATE_FILE ?= $(BUILD_HARNESS_EXTENSIONS_PATH)/templates/README.md.gotmpl

export README_DEPS ?= docs/ansible.md docs/targets.md

-include $(shell curl -sSL -o .build-harness-ext "https://gitlab.com/sr2c/build-harness-extensions/-/raw/main/Makefile.bootstrap"; echo .build-harness-ext)
