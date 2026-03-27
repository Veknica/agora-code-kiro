#!/bin/sh
cat > /dev/null
printf '[agora-code] REMINDER: Before launching an Explore subagent on any file over ~100 lines, run:\n'
printf '  agora-code summarize <file>\n'
printf 'Then use offset+limit to read only the sections you need. Skipping this wastes the entire point of the tool.\n'
exit 0
