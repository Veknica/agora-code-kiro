# Kiro **Agent Skills** — official documentation input for agora-code-kiro

**Not shipped user docs.** Condensed from user-provided **official Kiro Agent Skills** documentation (page dated **2026-02-18**). Add canonical URLs when available.

**Next paste (user):** **MCP** official section — not captured here.

---

## 1. What skills are

**Portable instruction packages** following the **open Agent Skills** standard: instructions + optional scripts/templates. Import from community / other compatible tools; export yours the same way.

**Problem skills solve:** agents lack team/process context; loading everything upfront **overloads** context.

**Progressive disclosure:**

1. **Discovery** — at startup, only **name + description** of each skill  
2. **Activation** — when the user request **matches** the description, full instructions load  
3. **Execution** — follow instructions; **scripts** / **reference** files loaded **as needed**

---

## 2. Using skills

- **Automatic** activation when description matches the task.  
- **Manual:** **`/`** in chat → skill as **slash command** → full skill loads.  
- **UI:** Kiro panel → **Agent Steering & Skills** (view/manage).

---

## 3. Scope

| Scope | Path | Notes |
|--------|------|--------|
| **Workspace** | **`.kiro/skills/`** | Project-specific workflows |
| **Global** | **`~/.kiro/skills/`** | Personal workflows across repos |

**Name collision:** **workspace** skill wins over global (override pattern, same as steering).

---

## 4. Import

Panel **+** → **Import a skill** → **GitHub** (URL to **skill folder** or **`SKILL.md`** — must be **subdir**, not repo root) or **Local folder**. Copied into skills dir; works immediately.

---

## 5. Layout & `SKILL.md`

```
my-skill/
├── SKILL.md        # required
├── scripts/        # optional
├── references/     # optional
└── assets/         # optional
```

**Frontmatter (required):**

- **`name`** — must match folder name; lowercase, digits, hyphens; max **64** chars  
- **`description`** — when to use; used for matching; max **1024** chars  

**Optional:** `license`, `compatibility`, `metadata` — see Agent Skills spec.

Body: focused instructions; heavy docs in **`references/`**. Use **scripts** for deterministic steps (validation, codegen, API calls).

---

## 6. Skills vs steering vs powers (official)

| Mechanism | Role |
|-----------|------|
| **Skills** | Open standard, portable, on-demand, can include **scripts**. Reusable workflows to **share/import**. |
| **Steering** | Kiro-specific; **always / auto / fileMatch / manual**; project standards. |
| **Powers** | **MCP +** bundled guidance; keyword activation; doc says **Powers usually better fit for MCP integrations**. |

---

## 7. Best practices (doc)

Precise **descriptions** (keywords); lean **`SKILL.md`**; **scripts** for deterministic work; pick **global** vs **workspace** scope deliberately.

---

## 8. agora-code-kiro — implications

- **Optional product:** ship an **`agora-code` skill** (`.kiro/skills/agora-code/` or importable repo) for **on-demand** “how to use memory / MCP / hooks” without bloating **always-on** steering — complements **`agora-memory.md`**.
- **Do not conflate** with **Cursor/Codex** `SKILL.md` in `.cursor`/`.codex` — same *idea*, different paths and hosts; Kiro reads **`.kiro/skills/`**.
- **Powers vs skill for agora:** if the deliverable is **MCP-heavy**, official guidance favors **Power**; a **Skill** can still document workflows that combine CLI + chat + `#mcp`.
- **Auto steering** (`inclusion: auto` + description) vs **Skills** — both match on natural language; avoid duplicate “when to load” messaging for the same workflow.

---

*Revision: Agent Skills official user paste, Mar 2026.*
