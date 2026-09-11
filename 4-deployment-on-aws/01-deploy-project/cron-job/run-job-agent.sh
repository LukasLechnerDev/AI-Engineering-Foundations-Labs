#!/bin/bash
set -e

# Run from the project directory, one level above this script.
cd "$(dirname "$0")/.."

"$HOME/.local/bin/uv" run python main.py
