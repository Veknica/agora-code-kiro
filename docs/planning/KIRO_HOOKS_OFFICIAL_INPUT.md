# Kiro **Hooks** — official documentation input for agora-code-kiro

**Not shipped user docs.** Condensed from user-provided **official Kiro Agent Hooks** documentation (pages dated **2025-11-16** through **2026-02-18**). Add canonical URLs when available.

**Cross-ref:** Create-power example used **`userTriggered`** — official name here is **Manual Trigger** (`KIRO_POWERS_DOCS_INPUT.md` §5).

---

## 1. What hooks are

Automated triggers on IDE events → **either** an **agent prompt (Ask Kiro)** **or** a **shell command (Run Command)**. Goals: consistency, less manual repetition, quality/security hooks.

**Flow:** event detected → action runs.

**Authoring:** Kiro panel **+** → **Ask Kiro** (natural language) **or** **Manual** form (title, description, event, tool names, file pattern, action, instructions/command). Command Palette: **Kiro: Open Kiro Hook UI**.

---

## 2. Trigger types (official names)

| Trigger | When |
|---------|------|
| **Prompt Submit** | User submits a prompt. |
| **Agent Stop** | Agent finished its turn. |
| **Pre Tool Use** | Before a tool runs. |
| **Post Tool Use** | After a tool runs. |
| **File Create** | New files match pattern. |
| **File Save** | Files match pattern on save. |
| **File Delete** | Deleted files match pattern. |
| **Pre Task Execution** | Spec task → **in_progress**. |
| **Post Task Execution** | Spec task → **completed**. |
| **Manual Trigger** | On demand (panel play / Start Hook); aligns with slash commands for manual hooks in Chat docs. |

### Prompt Submit + shell

**`USER_PROMPT`** environment variable exposes the user’s prompt to the shell command.

*Use cases (doc):* extra context, block prompts by content, log prompts.

### Pre / Post Tool Use — tool matching

**Tool name** field: multiple entries allowed.

**Built-in categories:**

`read` · `write` · `shell` · `web` · `spec` · `*` (all built-in **and** MCP)

**Prefix filters (regex on `@…`):**

- `@mcp` — all MCP tools  
- `@powers` — all Powers tools  
- `@builtin` — all built-in tools  
- Patterns like `@mcp.*sql.*` for subsets.

Doc: you can ask Kiro for available tool names; **concrete tool names** also work (as in shipped agora hooks).

### Blocking semantics (shell action)

- Exit code **0** → **stdout** appended to **agent context**.
- **Non-zero** → **stderr** to agent + error notification; additionally:
  - **Pre Tool Use** → **tool invocation is blocked**
  - **Prompt Submit** → **user prompt submission is blocked**

**Timeout:** default **60s**; set **0** to disable.

---

## 3. Actions

| Action | Behavior | Credits / speed |
|--------|-----------|-----------------|
| **Agent prompt (Ask Kiro)** | New agent loop; same as chat for that step. **Prompt Submit** variant is **“Add to prompt”** — hook text is **appended** to the user prompt, then sent. | **Uses credits** (new agent loop). |
| **Shell command (Run Command)** | Deterministic; **no LLM** for the hook itself. | **No** hook credits; faster, local. |

**Guidance (doc):** Ask Kiro when you need natural-language, context-dependent behavior; Run Command for fixed commands/scripts.

---

## 4. Examples (doc titles only)

Security review on **Agent Stop**; **Prompt Submit** shell logging to Loki with **`${USER_PROMPT}`**; **File Save** i18n + test coverage; **Manual** documentation agent; **File Save** + Figma MCP validation.

**MCP + hooks:** configure servers, reference tools in hook text, **auto-approval** for frequent tools.

---

## 5. Management & ops

Panel: enable/disable (eye), edit (immediate apply), delete (irreversible), run manual hooks (▷ / Start Hook).

**Best practices (summary):** one clear task per hook; narrow file patterns; test edge cases; watch frequency/performance; document for team; VCS shared `.kiro/hooks`.

**Troubleshooting:** pattern match, enabled flag, event type; conflicting hooks; simplify agent prompts; shorten shell commands.

---

## 6. agora-code-kiro — implications

1. **`USER_PROMPT`** — official contract for **Prompt Submit + shell**. Useful if **`agora-code inject`** should react to prompt text without Ask Kiro (still need any extra stdin Kiro provides beyond env).
2. **Categories vs concrete tools** — shipped agora hooks use names like `readCode`, `fsWrite`. Official **also** supports **`read` / `write` / `@mcp`** etc. **Rewire option:** broader matchers = fewer breakages when Kiro renames built-in tools.
3. **`@powers`** — distinct from `@mcp`; Powers tools are addressable in Pre/Post hooks.
4. **Blocking** — a failing **pre-tool** shell hook **blocks the tool**; use carefully for `agora-code summarize` if it must not block reads on transient errors.
5. **Spec tasks** — **Pre Task Execution** / **Post Task Execution** match **`agora-inject-before-task`** / **`checkpoint-after-task`** semantics (status transitions).
6. **Reconcile** internal **`docs/KIRO_HOOKS.md`** (inventory of **this repo’s** JSON) with this **product** doc when you **promote** to user-facing docs (UI labels like “File Save” vs JSON `when.type` values such as `fileSaved` if they differ).

---

*Revision: official Hooks section user paste, Mar 2026. Next paste mentioned: **Steering**.*
