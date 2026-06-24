#!/bin/bash
set -euo pipefail

# End-of-session: consolidate state + git sync
# Usage: ./session_end.sh "summary text" [session_type]

SUMMARY="${1:-end of session}"
TYPE="${2:-session}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== SESSION END ==="
echo "Summary: $SUMMARY"
echo "Type: $TYPE"
echo ""

# 1. Update state files via Python script
python3 "$SCRIPT_DIR/update_ezra_state.py" --summary "$SUMMARY" --type "$TYPE"

# 2. Git sync
bash "$SCRIPT_DIR/git_sync.sh" "end-session"

echo ""
echo "=== SESSION END COMPLETE ==="
