#!/bin/bash
# The first line tells the operating system to run this script with Bash.
set -e # Stop the script if a command fails.

# $0 is this script's path; dirname extracts its directory, and $(...) inserts that result.
# cd changes the working directory; /.. moves one level up to the project directory.
cd "$(dirname "$0")/.."

# $HOME is the current user's home directory; quotes keep paths with spaces together.
# Use uv's full path so cron can find it, then run main.py in the project's environment.
"$HOME/.local/bin/uv" run python main.py
