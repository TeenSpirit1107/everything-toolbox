#!/usr/bin/env bash
set -euo pipefail

echo "==== Script Logger for Ubuntu ===="
echo "==== Author: Yimeng (Rosalind) ===="
echo "==== Github Profile: https://github.com/TeenSpirit1107 ===="
echo "==== Email: yimengteng@link.cuhk.edu.cn ===="

# 1) Prepare directory
LOG_DIR="$HOME/logging"
mkdir -p "$LOG_DIR"

# 2) Prompt user to enter a comment (input on next line)
echo "Please enter a comment (press Enter to skip):"
IFS= read -r COMMENT || true  # Prevent Ctrl+D from terminating the script

# 3) Handle timestamp and filename
#    MMdd_HHmm = month-day_hour-minute
STAMP="$(date +%m%d_%H%M)"

# 4) Sanitize comment (keep only alphanumeric, underscore, hyphen, and dot; convert spaces to underscores)
if [[ -n "${COMMENT// }" ]]; then
  SAFE_COMMENT="$(printf '%s' "$COMMENT" | tr ' ' '_' | tr -cd '[:alnum:]_.-')"
else
  SAFE_COMMENT=""
fi

if [[ -n "$SAFE_COMMENT" ]]; then
  FILENAME="${STAMP}_${SAFE_COMMENT}.log"
else
  FILENAME="${STAMP}.log"
fi

LOG_PATH="$LOG_DIR/$FILENAME"

# 5) Check if script command is available
if ! command -v script >/dev/null 2>&1; then
  echo "Error: 'script' command not found. Please install it first (e.g., sudo apt-get install bsdutils or script from util-linux)."
  exit 1
fi

# 6) Start recording. You can execute commands in this session; type exit or press Ctrl-D to end.
echo "Starting recording to:"
echo "$LOG_PATH"
script -f "$LOG_PATH"

# 7) Echo absolute path after recording ends
echo "Saved to:"
echo "$LOG_PATH"

