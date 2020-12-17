#!/usr/bin/env bash
# TODO: surely there's something better than having to make a script for this?
set -euo pipefail
IFS=$'\n\t'

cd "${0%/*}"
echo "PWD: $(pwd)"

echo "Running make_dataset.py"
python3 ./make_dataset.py
