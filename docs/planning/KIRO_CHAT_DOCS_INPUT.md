# Kiro **Chat** — planning input for agora-code-kiro

**Not shipped user docs.** Condensed from user-provided Kiro Chat documentation (pages dated **2025-11-15** through **2026-03-19**). Add canonical URLs when available.

---

## 1. Chat basics

- Natural-language panel: questions, edits, features, debug, automation; **full project context** (plus explicit providers).
- **Vibe sessions** — Q&A, quick help, exploratory; less formal than Specs.
- **Spec sessions** — structured feature/bug workflow (see **`KIRO_SPECS_DOCS_INPUT.md`**). Picker when starting a session.
- **Multi-language** — model detects and mirrors language.
- **Export conversation** — right-click tab → Export Conversation → `.md`.

Access: **Cmd/Ctrl+L**, Command Palette “Kiro: Open Chat”, secondary side bar (**Cmd+Opt+B** / **Ctrl+Alt+B**).

---

## 2. Intent

**Smart intent** — informational (“how does this work?”) vs action (“create…”, “fix…”) without explicit mode switch.

---

## 3. Context providers (`#…`)

| Provider | Role (short) |
|----------|----------------|
| `#codebase` | Find relevant files project-wide |
| `#file` / `#folder` | Specific path |
| `#git diff` | Staged/unstaged |
| `#terminal` | **Active** terminal output/history — must select right terminal if many |
| `#problems` | Diagnostics in current file |
| `#url:…` | Web doc |
| `#code:…` | Snippet |
| `#repository` | Repo map |
| `#current` | Active editor file |
| `#steering:…` | Named steering file |
| `#docs:…` | Doc files |
| `#spec:…` | Spec folder (requirements/design/tasks) |
| `#mcp:…` | MCP tools/prompts/resources from connected servers |

Multiple providers can be combined in one message.

**agora planning note:** `#spec` loads **formal spec**; **`agora-code inject`** / **`get_session_context`** are **separate** memory streams — onboarding should not conflate them.

---

## 4. Autopilot vs Supervised

- **Autopilot (default)** — end-to-end changes without per-step approval; user can view all changes, revert all, interrupt.
- **Supervised** — yield after each turn that **edits files**; hunk/file accept/reject; inline chat on hunks.

Revert (per turn) vs **checkpoint** (see §9): revert = **files only** for latest turn; checkpoint = files **+** discard chat context after marker.

---

## 5. Slash commands (`/`)

- **Manual-trigger hooks** appear as commands (e.g. `/run-tests`).
- **Steering** with `inclusion: manual` in frontmatter appears as commands (pull that file into context on demand).

**agora planning note:** optional **manual** hook or steering for “refresh agora memory” / “dump session” patterns.

---

## 6. Terminal integration

- Natural language → suggested command → **Modify / Reject / Run / Run and Trust**.
- **Trusted commands** — prefix/wildcard rules (user + workspace); **danger:** broad patterns trust full string including pipes.
- **Denylist** — substring match; **evaluated before trust**; blocks e.g. `rm -rf`, `sudo`, `--force` in examples.
- **`#terminal`** — always **currently active** terminal window.

---

## 7. Dev servers

Long-running commands → dedicated named terminal, background, non-blocking; **reuse** same command+cwd; list/stop via chat.

---

## 8. Diagnostics tool

Uses **language extensions** / LSP: errors, types, lint. Works during agent execution; install language extensions first.

---

## 9. Agent notifications

OS notifications: action required, success, failure. Separate **usage/credit** notifications (proactive usage).

---

## 10. Checkpoints (Kiro native) — **not** agora `checkpoint`

- On each **user prompt**, Kiro creates a **checkpoint marker** in chat.
- **Restore** rewinds **codebase** (snapshots from **Kiro agent file tools**) **and** **discards chat context** after that point.
- **Does not track:** manual edits, formatters, **MCP tool file changes**, **bash** changes from agent execution.

**Revert** (after a turn): only **latest turn** file edits; checkpoints span **multiple** turns and also rewind **conversation**.

**agora planning note:** **Name collision** with **`agora-code checkpoint`** (SQLite/session structured memory). Kiro-native docs must distinguish **“Kiro checkpoint (rewind UI)”** vs **“agora checkpoint (persistent DB row)”**.

---

## 11. Chat summarization (Kiro)

Long threads → auto **summarize** when context ~**80%** of model window (meter in UI). **Conversation** compression, not the same as agora **`summarize_file`** on disk.

---

## 12. Subagents

- Parallel or delegated tasks; main agent waits for all subagents.
- Each subagent has **own context** (does not pollute main).
- **Steering + MCP** work in subagents **like main agent**.
- **Subagents do not have Specs**; **Hooks do not trigger in subagents.**

**agora planning note:** **`agora-session-inject`**, **pre/post tool hooks**, etc. **do not run** on subagent-only work — memory automation gaps unless main agent runs hooks or user uses MCP manually.

**Custom subagents** — `~/.kiro/agents` or `<workspace>/.kiro/agents` markdown + YAML (`name`, `description`, `tools`, `model`, `includeMcpJson`, `includePowers`, tool wildcards `@server/tool`). Can appear as `/slash` commands.

---

## 13. Web tools

`web_search`, `web_fetch`; limits (e.g. 10MB, 30s, html); governance for orgs (client-side enforcement caveat). Citations must be preserved if showing grounded output downstream.

---

## 14. Powers

Mentioned in subagent `includePowers`; bundled MCP packs — see Kiro Powers docs separately.

---

## 15. Sessions & execution history

Tabs for sessions; **History**; **Task list**; **execution history** (searches, edits, commands, …) — restore/delete sessions.

---

*Revision: user paste “whole chat part”, Mar 2026.*
