#!/usr/bin/env bash
# TODO: surely there's something better than having to make a script for this?
set -euo pipefail
IFS=$'\n\t'

cd "${0%/*}/../.."
echo "PWD: $(pwd)"

echo "Running remy_rs/models/train_model.py"
python ./remy_rs/models/train_model.py
