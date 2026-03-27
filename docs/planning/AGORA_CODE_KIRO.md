# agora-code-kiro — product planning

**Working name:** **agora-code-kiro** — the line of work where agora is tuned so the **Kiro** experience is first-class: hooks, MCP, steering, credits, multi-root, and clarity vs Kiro’s **own** codebase index.

**This doc is planning only.** Implementation may live in this repo, a fork, or a separate package; decide when you scope the project.

---

## Principles

1. **Do not confuse** Kiro’s built-in **codebase indexing** (IDE completion/navigation) with agora’s **`memory.db`** / MCP **`index_file`** — messaging for agora-code-kiro should make the split obvious.
2. **Respect Kiro’s rules** for **multi-root** (MCP **cwd**, duplicate server names, per-root hooks) — see **`KIRO_EDITOR_DOCS_INPUT.md`**.
3. **Prefer shell-first** where Kiro exposes enough **stdin/env** on tool boundaries, so we are not paying **Ask Kiro** credits for work the CLI already does well.
4. **Minimal surface** for the “default Kiro user” — extra MCP tools are power features, not the onboarding story.
5. **Specs vs agora** — Kiro **specs** formalize *this feature/bug* (`#spec` loads requirements/design/tasks). **Agora** holds *cross-session* memory and efficient reads. agora-code-kiro should **explain the pairing** in steering/onboarding, not collapse them into one story.
6. **Kiro checkpoint ≠ agora checkpoint** — Kiro **Restore** rewinds **agent file-tool edits** + **chat**; it **does not** snapshot **MCP** or **shell** file changes. **`agora-code checkpoint`** writes **structured session state** to **`memory.db`**. Same English word, different products — **naming and docs must separate them** (see **`KIRO_CHAT_DOCS_INPUT.md` §10**).
7. **Powers vs raw MCP** — Powers **activate by keywords** and load a **subset** of tools/context; raw workspace MCP loads **everything** registered. agora-code-kiro can ship **agora as a Power** so memory tools are not always in baseline context — see **`KIRO_POWERS_DOCS_INPUT.md`**.

---

## Powers + agora (Kiro)

- Official flow: **`POWER.md`** + optional **`mcp.json`** → MCP entries under **`mcp.json` Powers** with **namespaced** server names.
- Risk: Power onboarding that adds **hooks** while the repo already ships **`.kiro/hooks`** for agora — avoid **double** automation; document **either** power-first **or** copy-from-repo.
- Distribution: **kiro.dev/powers** one-click vs current **pip + KIRO.md** — decide for Kiro-native packaging.

---

## Chat + agora (Kiro)

- **`#mcp`** — users can pull MCP (including **`agora-memory`**) into a message explicitly; complements automatic tool use from steering.
- **Subagents:** **hooks do not run** in subagents — no automatic **`inject`** / pre-read / post-write from `.kiro/hooks` on subagent-only paths; only main-agent turns get those. Plan for **gaps** or document limitation.
- **Kiro chat auto-summarize (~80% context)** is **conversation** compaction; agora **`summarize_file`** is **file** outlines — different layer, both help “context” in different senses.

---

## Specs + memory (Kiro)

- **Per-spec-task hooks** in this repo (`agora-inject-before-task`, `checkpoint-after-task`) already match Kiro’s **task execution** model — good to **call out in Kiro-native copy** so users see “spec task ↔ inject/checkpoint.”
- **Optional later:** link checkpoints/learnings to a **spec path or id** (convention or DB field) for traceability — only if product needs it.

---

## Inputs

- **`KIRO_EDITOR_DOCS_INPUT.md`** — pasted / linked Kiro IDE docs (indexing, multi-root, kiroignore, etc.).
- **`KIRO_SPECS_DOCS_INPUT.md`** — Kiro **Specs** (`.kiro/specs/…`, EARS, feature vs bugfix, PBT, `#spec`).
- **`KIRO_CHAT_DOCS_INPUT.md`** — Kiro **Chat** (providers, checkpoints, subagents, terminal, slash commands).
- **`KIRO_POWERS_DOCS_INPUT.md`** — Kiro **Powers** (keyword activation, POWER.md, bundled MCP, create/share).
- **`KIRO_HOOKS_OFFICIAL_INPUT.md`** — Kiro **Hooks** (official triggers/actions, `USER_PROMPT`, `read`/`write`/`@mcp`, blocking).
- **`KIRO_STEERING_OFFICIAL_INPUT.md`** — Kiro **Steering** (always/fileMatch/manual/auto, global vs workspace).
- **`KIRO_SKILLS_OFFICIAL_INPUT.md`** — Kiro **Agent Skills** (`.kiro/skills/`, `SKILL.md`, progressive disclosure).
- **`KIRO_MCP_OFFICIAL_INPUT.md`** — Kiro **MCP** (mcp.json, autoApprove, disabledTools, install URLs, elicitation).
- **`KIRO_GUIDES_LANGUAGE_SUPPORT_INPUT.md`** — **Guides** language support (TS/JS, Python, Java).
- **`../REFACTOR_REWIRE_PLAN.md`** — tweak / rewire / rewrite template for *this* repo (optional; not required reading for end users).
- **`../KIRO_HOOKS.md`**, **`../KIRO_AGORA_INSIGHTS_AND_PLAN.md`** — current shipped integration inventory and insights.

---

## Backlog themes (fill as you plan)

**Kiro official / IDE doc corpus (planning):** editor, specs, chat, powers, hooks, steering, skills, MCP, language guides — all under `docs/planning/*_INPUT.md` unless promoted.

- [ ] Multi-root: explicit **project root** for `memory.db` (env or Kiro-provided) vs “first workspace folder.”
- [ ] Optional alignment with **`.kiroignore`** for MCP/index paths (if product requires parity with agent visibility).
- [ ] Shell pre-read / post-write if **`runCommand` contract** is documented or stable.
- [ ] Slim **`agora-memory`** tool set or install profile for Kiro-only users.
- [ ] Single hook bundle or debounce strategy to avoid redundant **`index_file`** on the same save path.
- [ ] **Onboarding copy:** when to use **Specs** vs **vibe** vs **agora-only** memory; when to use **`#spec`** together with **`inject`**.
- [ ] Optional: **spec-scoped** checkpoint or learning tags (`.kiro/specs/foo`).
- [ ] **Glossary / onboarding:** “Kiro checkpoint” vs “agora checkpoint”; “chat summarize” vs “agora summarize_file.”
- [ ] Document **subagent** limitation: **hooks off** — when to rely on **`#mcp`** or main-agent turns for agora.
- [ ] **Agora as a Kiro Power** — POWER.md keywords, `mcp.json`, onboarding vs duplicate project hooks; marketplace path.
- [ ] Reconcile **Power MCP namespacing** (`power-*`) with docs that reference `agora-memory` today.
- [ ] Align **`docs/KIRO_HOOKS.md`** (shipped JSON inventory) with **`KIRO_HOOKS_OFFICIAL_INPUT.md`** when promoting user docs; consider **category** tool matchers (`read`, `write`, `@mcp`) vs concrete names.
- [ ] **K4 satisfied (partial):** `USER_PROMPT` for **Prompt Submit + shell** — design shell-first inject/summarize around env + any extra stdin.
- [ ] **Steering strategy:** `agora-memory.md` **always** vs optional **manual/auto** steering for advanced MCP workflows; vs **AGENTS.md** duplication.
- [x] **Guides (language support)** captured in **`KIRO_GUIDES_LANGUAGE_SUPPORT_INPUT.md`** (user: completes primary Kiro doc paste set).
- [ ] Optional: **importable Agent Skill** for agora (on-demand) vs **Power** vs **always-on steering** only.
- [ ] **One-click MCP:** `https://kiro.dev/launch/mcp/add?...` for **`agora-memory`** (see **`KIRO_MCP_OFFICIAL_INPUT.md` §4**).

---

*Add dates and owners when this becomes a staffed effort.*
