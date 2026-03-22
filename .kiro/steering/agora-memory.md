---
inclusion: always
---

# Persistent Memory via agora-memory MCP

You have access to the `agora-memory` MCP server. Most memory work is automatic via hooks — you only call MCP tools for deeper work.

## What happens automatically

| Event | Hook | Cost |
|---|---|---|
| Every prompt | `agora-code inject` runs — LEARNINGS + last session context injected | 0 credits |
| Every agent stop | `agora-a-summarize-interaction` fires first → you call `store_learning` with one sentence. Then `agora-z-checkpoint` runs the shell checkpoint. Always in this order. | small + free |
| Before `readCode` / `readFile` / `readMultipleFiles` | You call `summarize_file` then `read_file_range` | small |
| After `fsWrite` / `fsAppend` / `strReplace` / `editCode` | You call `index_file` | small |
| After `grepSearch` | You call `log_search` + `index_file` for matched files | small |
| Spec task start/end | inject and checkpoint fire | 0 credits |

## When to call MCP tools manually

| Situation | Tool |
|---|---|
| Need full structured session detail | `get_session_context` |
| Completed a meaningful step | `save_checkpoint` |
| Found something non-obvious | `store_learning` |
| Starting a task — check if solved before | `recall_learnings` |
| Session done | `complete_session` |
| Read a specific line range from a file | `read_file_range` (start_line, end_line) |
| Save a finding for the whole team | `store_team_learning` |
| Search team knowledge | `recall_team` |

## Rules

1. **Don't call `get_session_context` on every prompt** — inject already loaded it. Only call it when you need full detail (hypothesis, next steps, files changed).

2. **Before reading any file**, call `summarize_file` first. Then `read_file_range` for just the section you need. Saves 90%+ tokens on large files.

3. **After every agent stop**, `agora-a-summarize-interaction` fires first (alphabetically before `agora-z-checkpoint`). Write one sentence summarizing what was done, call `store_learning` with it, then stop. The checkpoint shell command runs automatically after. Do not call any other tools in response to the summarize hook.

4. **Call `store_learning`** any time you discover something non-obvious mid-task. Don't wait for the hook.

5. **Call `recall_learnings`** before starting a task to check if it's been done before.

## Example flow

```
Session start:
  inject runs automatically → LEARNINGS from past sessions injected

User asks something → you answer
  Agent stops → checkpoint saves (shell, free)
             → you write: "Explained SQLite overflow: fillInCell() chains
               pages via 4-byte pointers when payload > maxLocal" → store_learning

Next question same session → same cycle

New session next day:
  inject runs → that summary appears in LEARNINGS
  Feels like continuation — no full chat replay, ~200 tokens not 10k
```
