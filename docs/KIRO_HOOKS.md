# Kiro hooks — internal reference for agora-code

**What this is:** A concise map from **Kiro’s hook capabilities** (events, actions, how tools are matched) to **what we ship** in `.kiro/hooks/*.kiro.hook` and why. For **planning, risks, backlog, and which other docs to write**, use **`docs/KIRO_AGORA_INSIGHTS_AND_PLAN.md`**. For **Python module roles vs Kiro, official-doc gaps, and known drift**, use **`docs/KIRO_CODEBASE_AUDIT_AND_GAPS.md`**. For **agora-code-kiro product planning** (Kiro IDE inputs, not shipped user docs), use **`docs/planning/`**.

**What this is not:** A substitute for trying hooks in Kiro — behavior can change between app versions.

---

## 1. Hook execution model (facts we rely on)

1. **Event** fires (prompt submitted, tool about to run, file saved, spec task started, etc.).
2. **Action** runs:
   - **Ask Kiro** — agent prompt; **uses credits**; model may call MCP tools.
   - **Run Command** — shell; **no credits**; exit `0` → stdout into context; non‑zero → stderr, and **Pre Tool Use** / **Prompt Submit** can **block** the underlying action.

Hooks can be created in the Kiro Hook UI or edited as JSON under `.kiro/hooks/`. Checking hooks into the repo keeps the team aligned.

---

## 2. Trigger types → how we use them for agora-code

| Trigger | Our typical use | Rationale |
|---------|-----------------|-----------|
| **Prompt Submit** | `agora-code inject` (shell) | Session + learnings in context before the model answers. |
| **Agent Stop** | `store_learning` (Ask Kiro) + `agora-code checkpoint` (shell) | Persist what happened + structured checkpoint. |
| **Pre Tool Use** | Summarize then targeted read (Ask Kiro + MCP) | Token reduction on large files. |
| **Post Tool Use** | `index_file`, `log_search` (Ask Kiro + MCP) | DB stays aligned with edits and search. |
| **File Save** | `index_file` (Ask Kiro) | Catches saves that are not agent write tools. |
| **Pre / Post Task Execution** | inject / checkpoint (shell) | Spec workflow boundaries. |
| **File Create / Delete** | — | Not shipped; add if a workflow needs it. |
| **Manual Trigger** | — | Optional for ops / debugging. |

Shell hooks can use **`USER_PROMPT`** on Prompt Submit where Kiro provides it — we do not depend on that in the default set yet.

---

## 3. Pre / Post Tool Use — matching tools

Kiro can match by **category** or **name**:

| Pattern | Meaning |
|---------|---------|
| `read` / `write` / `shell` / `web` / `spec` | Built-in families |
| `*` | All tools |
| `@mcp` / `@powers` / `@builtin` | By origin; regex allowed on `@…` prefixes |

**Our choice:** we mostly list **concrete** `toolTypes` (`readCode`, `fsWrite`, `fsAppend`, …) so each hook is explicit. **Tradeoff:** more **brittle** if Kiro renames tools — see insights doc for upgrade practice.

---

## 4. Actions — when shell vs Ask Kiro

| Action | Use when | Examples here |
|--------|----------|----------------|
| **Run Command** | Deterministic, no MCP needed | `agora-code inject --quiet`, `agora-code checkpoint --quiet` |
| **Ask Kiro** | Needs MCP or judgment | Instructions to call `summarize_file`, `read_file_range`, `index_file`, `store_learning`, `log_search` |

**Future:** if Kiro exposes stable **paths in env** for pre/post tool hooks, some Ask Kiro **index** steps could become **`agora-code index`** shell actions (credits ↓).

---

## 5. Shipped hooks (inventory)

JSON `when.type` values are as in-repo (UI labels may differ, e.g. File Save vs `fileSaved`).

| File | `when.type` | Tool / scope | `then.type` | Role |
|------|-------------|--------------|-------------|------|
| `agora-session-inject.kiro.hook` | `promptSubmit` | — | `runCommand` | Inject before each prompt |
| `agora-summarize-interaction.kiro.hook` | `agentStop` | — | `askAgent` | One-sentence `store_learning` |
| `agora-auto-checkpoint.kiro.hook` | `agentStop` | — | `runCommand` | Checkpoint after stop |
| `agora-inject-before-task.kiro.hook` | `preTaskExecution` | — | `runCommand` | Inject before spec task |
| `checkpoint-after-task.kiro.hook` | `postTaskExecution` | — | `runCommand` | Checkpoint after spec task |
| `agora-summarize-before-read.kiro.hook` | `preToolUse` | `readCode` | `askAgent` | Summarize before read |
| `agora-summarize-before-readfile.kiro.hook` | `preToolUse` | `readFile` | `askAgent` | Same |
| `agora-summarize-before-readmulti.kiro.hook` | `preToolUse` | `readMultipleFiles` | `askAgent` | Same |
| `agora-index-after-write.kiro.hook` | `postToolUse` | `fsWrite`, `fsAppend` | `askAgent` | Index after write |
| `agora-index-after-strreplace.kiro.hook` | `postToolUse` | `strReplace` | `askAgent` | Index after replace |
| `agora-index-after-editcode.kiro.hook` | `postToolUse` | `editCode` | `askAgent` | Index after edit |
| `agora-log-grep-results.kiro.hook` | `postToolUse` | `grepSearch` | `askAgent` | Log + index matches |
| `agora-index-on-save.kiro.hook` | `fileSaved` | — | `askAgent` | Index on save |

**Agent Stop:** `agora-summarize-interaction` is named to sort **before** `agora-auto-checkpoint` so learning is stored before checkpoint (depends on Kiro’s ordering — noted in insights doc).

**MCP:** Ask Kiro hooks expect **`agora-memory`** configured (`.kiro/settings/mcp.json`) and steering aligned (e.g. stop after `store_learning`).

---

## 6. MCP + autoApprove

Frequent tools are listed under `autoApprove` so hooks are not blocked on approval. If you add other MCP servers, consider narrowing some hooks to **`@mcp`** patterns so only relevant tool calls get follow-up behavior.

---

## 7. Maintenance checklist

| Item | Note |
|------|------|
| Tool renames | Reconcile `toolTypes` after Kiro upgrades; consider category matchers if stable. |
| Credits | Prefer shell for inject/checkpoint; tighten Ask Kiro prompts if needed. |
| Blocking pre-read | Shell + non-zero exit can block tool — only use with a clear contract. |
| File patterns | Narrow globs on file events if hooks run too often. |
| Steering | Keep `.kiro/steering/agora-memory.md` in sync with hook prompts. |

---

## 8. Other docs in this tree

| Doc | Use |
|-----|-----|
| **`docs/KIRO_AGORA_INSIGHTS_AND_PLAN.md`** | Insights, what works, fragilities, backlog, **doc map** |
| **`docs/KIRO_USER_PATH_AND_CONTEXT.md`** | Kiro user path through CLI/MCP + context/token investigation table |
| **`docs/KIRO_PLATFORM_AND_AGORA_PLAN.md`** | Kiro vs `memory.db` storage, local reference repos |
| **`KIRO.md`** | Install and copy-paste setup |
| **`docs/DATABASE.md`**, **`DATABASE_AND_STRUCTURED_LAYER.md`** | What `index_file` / inject read from |
| **`power-agora-memory/POWER.md`** | Power-style packaging |

---

## 9. Quick troubleshooting

| Symptom | Check |
|---------|--------|
| Hook never runs | Tool name / category mismatch; hook enabled; restart after adding files |
| MCP errors | Full path to `agora-code`; `autoApprove` includes tool |
| Double work on agent stop | Hook order + steering (“one tool then stop”) |
| Unexpected block | Shell hook exited non-zero on Pre Tool Use or Prompt Submit |
