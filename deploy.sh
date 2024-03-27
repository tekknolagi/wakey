#!/usr/bin/env bash
set -eux -o pipefail
rsync -avz index.html cgi-bin/ raspberrypi:www
