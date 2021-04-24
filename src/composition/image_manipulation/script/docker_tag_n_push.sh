#!/usr/bin/env bash

declare -r IMG='python3action'
declare -r IMG_VERSION='cmp-libs'
declare -r IMG_NAME="${IMG}:${IMG_VERSION}"
declare -r DK_FILE_ROOT="$(dirname "${BASH_SOURCE[0]}")/../docker"
declare -r DOCKER_REPO="alfredo94"

docker build -t "${IMG_NAME}" "${DK_FILE_ROOT}"
docker tag "${IMG_NAME}" "${DOCKER_REPO}/${IMG_NAME}"
docker push "${DOCKER_REPO}/${IMG_NAME}"
