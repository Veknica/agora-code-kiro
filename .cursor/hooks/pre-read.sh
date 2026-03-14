#!/bin/sh
# Cursor preToolUse:Read hook — intercept large file reads and return summaries.
# Fires before every Read tool call. Small files pass through; large files get
# an AST/regex summary injected via agent_message instead.
#
# Input JSON from Cursor: {"tool_name":"Read","tool_input":{"file_path":"..."},...}
# Output: {"permission":"allow"} or {"permission":"deny","agent_message":"<summary>"}

INPUT=$(cat)

FILE_PATH=$(printf '%s' "$INPUT" | python3 -c "
import sys, json
try:
    d = json.loads(sys.stdin.read())
    ti = d.get('tool_input', {})
    if isinstance(ti, str):
        import json as j2
        ti = j2.loads(ti)
    print(ti.get('file_path') or ti.get('path') or '')
except Exception:
    print('')
" 2>/dev/null)

if [ -z "$FILE_PATH" ]; then
    printf '{"permission":"allow"}\n'
    exit 0
fi

RESULT=$(agora-code summarize "$FILE_PATH" --json-output 2>/dev/null)

if [ -z "$RESULT" ]; then
    printf '{"permission":"allow"}\n'
    exit 0
fi

ACTION=$(printf '%s' "$RESULT" | python3 -c "
import sys, json
try:
    d = json.loads(sys.stdin.read())
    print(d.get('action', 'allow'))
except Exception:
    print('allow')
" 2>/dev/null)

if [ "$ACTION" = "summarize" ]; then
    SUMMARY=$(printf '%s' "$RESULT" | python3 -c "
import sys, json
d = json.loads(sys.stdin.read())
s = d.get('summary', '')
orig = d.get('original_lines', 0)
toks = d.get('summary_tokens', 0)
msg = s + '\n\n[File has ' + str(orig) + ' lines. Summary is ~' + str(toks) + ' tokens. To read specific sections, request line ranges.]'
print(json.dumps(msg))
" 2>/dev/null)
    printf '{"permission":"deny","agent_message":%s}\n' "$SUMMARY"
else
    printf '{"permission":"allow"}\n'
fi
