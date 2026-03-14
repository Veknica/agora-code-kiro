#!/bin/sh
# Gemini CLI BeforeTool:read_file hook — intercept large file reads.
#
# Gemini sends JSON via stdin with tool_name + tool_input.
# Output JSON to stdout: {"decision":"allow"} or {"decision":"deny","reason":"<summary>"}.
# Exit 0 = success (stdout parsed). Exit 2 = block (stderr as reason).

INPUT=$(cat)

FILE_PATH=$(printf '%s' "$INPUT" | python3 -c "
import sys, json
try:
    d = json.loads(sys.stdin.read())
    ti = d.get('tool_input', {})
    if isinstance(ti, str):
        import json as j2
        ti = j2.loads(ti)
    print(ti.get('file_path') or ti.get('path') or ti.get('target_file') or '')
except Exception:
    print('')
" 2>/dev/null)

if [ -z "$FILE_PATH" ]; then
    printf '{"decision":"allow"}\n'
    exit 0
fi

RESULT=$(agora-code summarize "$FILE_PATH" --json-output 2>/dev/null)

if [ -z "$RESULT" ]; then
    printf '{"decision":"allow"}\n'
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
    REASON=$(printf '%s' "$RESULT" | python3 -c "
import sys, json
d = json.loads(sys.stdin.read())
s = d.get('summary', '')
orig = d.get('original_lines', 0)
toks = d.get('summary_tokens', 0)
msg = s + '\n\n[File has ' + str(orig) + ' lines. Summary is ~' + str(toks) + ' tokens. To read specific sections, request line ranges.]'
print(json.dumps(msg))
" 2>/dev/null)
    printf '{"decision":"deny","reason":%s}\n' "$REASON"
else
    printf '{"decision":"allow"}\n'
fi
