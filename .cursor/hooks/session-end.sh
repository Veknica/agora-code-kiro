#!/bin/sh
# Cursor sessionEnd hook — checkpoint session state when conversation ends.
cat > /dev/null
agora-code checkpoint --quiet 2>/dev/null || true
exit 0
