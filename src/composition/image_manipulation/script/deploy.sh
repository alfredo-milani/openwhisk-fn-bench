#!/usr/bin/env bash


# enable alias exapansion
shopt -s expand_aliases

# source shortcut.sh for launcher.sh script
source "$(dirname "${BASH_SOURCE[0]}")/../../../../script/shortcut.sh"

concurrency=1
[[ -n "${1}" ]] && concurrency="${1}"

# deploy img_man composition and relative actions
launcher deploy cmp nodejs:10 composition/image_manipulation/img_man "${concurrency}" n \
    deploy fn python:img_cmp composition/image_manipulation/resize "${concurrency}" n \
    deploy fn python:img_cmp composition/image_manipulation/mirror "${concurrency}" n \
    deploy fn python:img_cmp composition/image_manipulation/greyscale "${concurrency}" n
