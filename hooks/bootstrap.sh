#!/bin/sh
# SessionStart bootstrap — install agora-code binary if missing, then inject context.

AGORA_BIN=$(which agora-code 2>/dev/null)

if [ -z "$AGORA_BIN" ]; then
    pip install "git+https://github.com/thebnbrkr/agora-code.git" --quiet 2>/dev/null

    # Find where pip installed the binary
    USER_BASE=$(python3 -m site --user-base 2>/dev/null)
    if [ -n "$USER_BASE" ] && [ -f "$USER_BASE/bin/agora-code" ]; then
        AGORA_BIN="$USER_BASE/bin/agora-code"
        # Export PATH so all subsequent hooks in this session can find it
        if [ -n "$CLAUDE_ENV_FILE" ]; then
            echo "export PATH=\"$USER_BASE/bin:\$PATH\"" >> "$CLAUDE_ENV_FILE"
        fi
    else
        AGORA_BIN=$(which agora-code 2>/dev/null)
    fi
fi

if [ -n "$AGORA_BIN" ]; then
    "$AGORA_BIN" inject --quiet 2>/dev/null || true
fi

exit 0
