# Planning — **agora-code-kiro** (and related)

**This folder is not part of the shipped “how to use agora-code in Kiro” path.** It holds **inputs and product notes** for designing **agora-code-kiro**: a Kiro-first experience that should be *extremely* good in that editor—without folding Kiro IDE internals into core `KIRO.md` / hooks reference unless we deliberately promote something to user docs later.

| File | Role |
|------|------|
| **`AGORA_CODE_KIRO.md`** | Product direction, principles, backlog themes for the Kiro-specific line. |
| **`KIRO_EDITOR_DOCS_INPUT.md`** | Condensed **Kiro IDE documentation** excerpts (indexing, multi-root, ignore, …). |
| **`KIRO_SPECS_DOCS_INPUT.md`** | Kiro **Specs** system (requirements/design/tasks, EARS, bugfix specs, PBT, `#spec`, workflows). |
| **`KIRO_CHAT_DOCS_INPUT.md`** | Kiro **Chat** (vibe/spec, `#` providers, autopilot, terminal, dev servers, **Kiro checkpoints**, subagents, slash commands). |
| **`KIRO_POWERS_DOCS_INPUT.md`** | Kiro **Powers** (POWER.md, keywords, dynamic MCP, install, create, mcp.json namespacing). |
| **`KIRO_HOOKS_OFFICIAL_INPUT.md`** | Kiro **Agent Hooks** — official triggers, actions, `USER_PROMPT`, tool categories, blocking, timeouts. |
| **`KIRO_STEERING_OFFICIAL_INPUT.md`** | Kiro **Steering** — scopes, inclusion modes, `AGENTS.md`, `#[[file:]]`, foundation files. |
| **`KIRO_SKILLS_OFFICIAL_INPUT.md`** | Kiro **Agent Skills** — `SKILL.md`, progressive disclosure, import, vs steering/powers. |
| **`KIRO_MCP_OFFICIAL_INPUT.md`** | Kiro **MCP** — config JSON, local/remote, merge, tools, prompts, elicitation, security, install links. |
| **`KIRO_GUIDES_LANGUAGE_SUPPORT_INPUT.md`** | **Guides** — TS/JS, Python, Java (steering/hooks/MCP/`#docs` patterns). |

**How to add material:** drop new files here or append to an `*_INPUT.md`. Long pastes are **planning / spec fuel** for agora-code-kiro — **do not** auto-promote to `KIRO.md` or `docs/KIRO_*.md` unless someone explicitly asks. Promote in a **separate** change when ready for all agora users.
