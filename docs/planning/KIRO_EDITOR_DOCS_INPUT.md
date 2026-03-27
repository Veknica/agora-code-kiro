# Kiro IDE docs — **planning input** for agora-code-kiro

**Not user-facing agora documentation.** This file exists so **agora-code-kiro** can be designed against **how Kiro the editor actually behaves**. See **`README.md`** in this folder.

**Provenance:** User-provided paste from Kiro docs; on-page dates in originals ranged **2025-11-16** through **2026-02-03**. Replace or augment with **canonical URLs** when available.

---

## 1. Codebase indexing (Kiro’s index)

Kiro maintains its **own** codebase index for the IDE (completion, navigation, cross-file context, docs lookup). It:

- Runs on **project import**, **new/added files**, **external changes** (e.g. git), and can be **forced** or **rebuilt** from the Command Palette (`Kiro: Codebase Force Re-Index`, `Kiro: Rebuild codebase index`, docs indexing commands).
- Indexes **source**, **documentation** (Markdown, MDX, etc.), **configuration**, **dependencies**.
- Progress appears in **Output → Kiro Logs**.

### Planning note (agora-code-kiro)

**Kiro’s index ≠ agora memory.** MCP **`index_file` / `summarize_file`** target **`memory.db`**. Product copy and onboarding for **agora-code-kiro** should state both systems so users are not surprised.

---

## 2. Multi-root workspaces

- Each workspace root can have its own **`.kiro`** tree (specs, steering, hooks, MCP definitions).
- **Specs / steering / hooks** from all roots appear as **unified lists** in the Kiro panel; the **root name** is shown next to each item.
- **Hooks** tied to **File Create / Save / Delete** run only when the agent changes files under the **same root** where that hook is defined.
- **Codebase indexing** and **repository maps** span **all** roots.
- **`#file` context:** if multiple files share a name, Kiro prompts to pick the path.

### MCP servers (from Kiro multi-root docs)

1. **All** MCP server definitions from **all** roots are initialized at startup.
2. If two roots define a server with the **same name**, the definition in the **last** defining root wins.
3. Servers are launched with the **first root folder** as their **current working directory**, **regardless of which root** defined the server.

### Planning note (agora-code-kiro)

If **`agora-code`** resolves project via **process cwd** / git, multi-root workspaces can bind **`memory.db`** to the **wrong** repo unless the user orders roots carefully or we add an explicit **project root** override. **agora-code-kiro** should treat this as a first-class scenario.

---

## 3. Kiroignore (`.kiroignore`)

- **Gitignore-style** patterns to keep files out of **agent** context (secrets, noise).
- Workspace setting **`kiroAgent.agentIgnoreFiles`** can list files such as `.kiroignore` (can combine with `.gitignore`).
- Subdirectory `.kiroignore` files apply with usual gitignore precedence.
- Global: `~/.kiro/settings/kiroignore` and optionally git’s global excludes file.

### Planning note (agora-code-kiro)

Kiroignore controls **Kiro’s agent** reads; agora does **not** automatically honor it unless we implement that. Decide whether **agora-code-kiro** should **read** `.kiroignore` (or a dedicated allowlist) for MCP/index operations.

---

## 4. Source control (brief)

- AI **commit message** generation (Conventional Commits style).
- **`#Git Diff`** in chat includes staged/unstaged context.

Low direct impact on memory MCP; useful for **steering examples** in templates.

---

## 5. Extension registry

Kiro can point **`product.json` → `extensionsGallery`** at a private Open VSX–compatible registry (org deployments).

Relevant for **enterprise Kiro rollout**, not core MCP behavior.

---

## 6. Open questions for more Kiro docs

| Topic | Why |
|--------|-----|
| `.kiro.hook` JSON schema, `when.type`, `toolTypes` | Reliable hooks + shell migration. |
| Hook **order** when multiple hooks match one event | Checkpoint vs `store_learning` ordering. |
| **`runCommand` stdin/env** on Pre/Post Tool Use | Shell-first summarize/index. |
| Single-root MCP **cwd** (if different from multi-root) | Confirm in official docs. |

---

*Append revisions and URLs here as you collect them.*
