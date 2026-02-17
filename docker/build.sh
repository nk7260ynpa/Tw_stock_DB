#!/bin/bash
# 建立 DBmaker Docker image

set -euo pipefail

readonly IMAGE_NAME="nk7260ynpa/dbmaker"
readonly IMAGE_TAG="1.0.0"
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_DIR="$(dirname "${SCRIPT_DIR}")"

docker build \
  -f "${SCRIPT_DIR}/Dockerfile" \
  -t "${IMAGE_NAME}:${IMAGE_TAG}" \
  "${PROJECT_DIR}"
