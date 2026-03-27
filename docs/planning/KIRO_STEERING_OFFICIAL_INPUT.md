# Kiro **Steering** — official documentation input for agora-code-kiro

**Not shipped user docs.** Condensed from user-provided **official Kiro Steering** documentation (page dated **2026-02-18**). Add canonical URLs when available.

**Related (official):** Steering doc links to **Skills** and **Hooks** as separate features — we have **`KIRO_HOOKS_OFFICIAL_INPUT.md`**; **Skills** has **no** planning `*_INPUT.md` file yet until you paste that section.

---

## 1. What steering is

Markdown files that give Kiro **persistent workspace knowledge** (patterns, libs, standards) so you do not repeat them every chat.

**Scopes:**

| Scope | Path | Applies to |
|--------|------|------------|
| **Workspace** | **`<workspace>/.kiro/steering/`** | That workspace only |
| **Global** | **`~/.kiro/steering/`** | All workspaces |

**Conflict:** **Workspace wins** over global — global defaults, workspace overrides.

**Team steering:** Push global files via MDM/GPO or shared repo → users copy to `~/.kiro/steering/`.

---

## 2. Foundational steering (generated)

From Kiro panel: **Generate Steering Docs** or **+** → **Foundation steering files** → creates:

- **`product.md`** — product purpose, users, features, business goals  
- **`tech.md`** — stack, tools, constraints  
- **`structure.md`** — layout, naming, imports, architecture  

Included **by default** in every interaction as baseline context.

---

## 3. Custom steering

**+** → workspace or global → filename (e.g. `api-standards.md`) → markdown. Workspace files can use **Refine**. Effective immediately across interactions.

---

## 4. AGENTS.md

- Markdown like steering but **no inclusion modes** — **always** picked up.  
- Locations: **`~/.kiro/steering/AGENTS.md`** or **workspace root `AGENTS.md`**.

---

## 5. Inclusion modes (YAML front matter)

Must be **first** in file — `---` … `---`, **no** blank lines before.

### Always included (default)

```yaml
---
inclusion: always
---
```

Every interaction. Core standards, stack, security, universal conventions.

### Conditional — `fileMatch`

```yaml
---
inclusion: fileMatch
fileMatchPattern: "components/**/*.tsx"
# or array: ["**/*.ts", "**/*.tsx"]
---
```

Loaded when active file matches pattern.

### Manual

```yaml
---
inclusion: manual
---
```

On demand: **`#steering-file-name`** in chat, or **slash command** `/…` from file name.

### Auto

```yaml
---
inclusion: auto
name: api-design
description: REST API design patterns. Use when creating or modifying API endpoints.
---
```

Kiro matches **`description`** to the user request (similar to **skills**). Also available as **slash** command.

---

## 6. File references in steering body

Embed live workspace files:

```markdown
#[[file:relative/path/to/file]]
```

e.g. `#[[file:api/openapi.yaml]]` — keeps steering synced with repo files.

---

## 7. Best practices (doc summary)

One domain per file; clear filenames; explain **why**; examples; no secrets; review when architecture changes; test `#[[file:…]]` after moves.

---

## 8. agora-code-kiro — implications

- Shipped **`.kiro/steering/agora-memory.md`** uses **`inclusion: always`** — matches **Always included**; essential because MCP alone does not force tool use.
- Optional **second file** with **`inclusion: manual`** or **`auto`** for heavy agora workflows could reduce always-on token load (if descriptions/keywords are good).
- **Workspace > global:** team can override global steering per repo for agora conventions.
- **AGENTS.md** at repo root is another channel — could duplicate or complement `agora-memory.md`; product should say **one source of truth** or intentional split.
- Compare **auto steering** vs **Agent Skills** — see **`KIRO_SKILLS_OFFICIAL_INPUT.md`** (progressive disclosure vs `inclusion: auto`).

---

*Revision: Steering official user paste, Mar 2026.*
