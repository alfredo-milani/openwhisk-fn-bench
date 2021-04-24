#!/usr/bin/env bash

# enable alias exapansion
shopt -s expand_aliases

# source shortcut.sh for launcher.sh script
source "$(dirname "${BASH_SOURCE}")/../../../../script/shortcut.sh"

concurrency=1
[[ -n "${1}" ]] && concurrency="${1}"

# deploy cmp composition and relative actions
launcher deploy fn python:3 cpu_bound/factorization "${concurrency}" n
