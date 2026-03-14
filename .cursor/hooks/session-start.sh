#!/bin/sh
# Cursor sessionStart hook — inject session context into the agent.
# Cursor sends JSON via stdin (may include transcript_path). We use it, then run inject.
# Output MUST be JSON: {"additional_context": "..."} — plain text causes a parse error.
payload=$(cat)
context=$(agora-code inject --quiet 2>/dev/null)

# If Cursor sent a transcript path, append last ~8K of that transcript to context
transcript_path=$(printf '%s' "$payload" | python3 -c "
import sys, json
try:
    d = json.loads(sys.stdin.read())
    print(d.get('transcript_path') or d.get('transcriptPath') or '')
except Exception:
    print('')
" 2>/dev/null)
if [ -n "$transcript_path" ] && [ -r "$transcript_path" ]; then
    transcript_tail=$(tail -c 8192 "$transcript_path" 2>/dev/null)
    if [ -n "$transcript_tail" ]; then
        context="${context:+$context

}[Current conversation transcript (tail)]
$transcript_tail"
    fi
fi

if [ -n "$context" ]; then
    escaped=$(printf '%s' "$context" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))")
    printf '{"additional_context":%s}\n' "$escaped"
else
    printf '{}\n'
fi
