# Kiro **MCP** — official documentation input for agora-code-kiro

**Not shipped user docs.** Condensed from user-provided **official Kiro MCP** documentation (pages dated **2025-11-20** through **2026-03-13**). Add canonical URLs when available.

**Next paste (user):** **Guides** — not captured here.

---

## 1. What MCP is

Protocol for **tools, prompts, resources** from external servers. Chat can use **`#`** for server prompts/resources; **elicitation** when a tool needs more input; extends Kiro with domain-specific capabilities.

**Setup:** enable **MCP** in Settings; prerequisites per server; **MCP servers** tab — status, tools, click tool → placeholder in chat. **Logs:** Output → **Kiro - MCP Logs**.

---

## 2. Configuration JSON

Top-level **`mcpServers`** map; each entry either **local** or **remote**.

### Local server

| Field | Required | Notes |
|--------|----------|--------|
| `command` | Yes | Executable |
| `args` | Yes | Argument array |
| `env` | No | `${VAR}` expansion (see **approved env vars** below) |
| `disabled` | No | default false |
| `autoApprove` | No | Tool names; **`"*"`** = all tools on that server |
| `disabledTools` | No | Omit tools from agent (panel or JSON) |

### Remote server

| Field | Required | Notes |
|--------|----------|--------|
| `url` | Yes | HTTPS (or HTTP for localhost) |
| `headers` | No | |
| `env` | No | |
| `disabled`, `autoApprove`, `disabledTools` | No | Same idea as local |

### Where config lives

| Location | Scope |
|----------|--------|
| **`.kiro/settings/mcp.json`** | Workspace |
| **`~/.kiro/settings/mcp.json`** | User (global) |

**Merge:** both can exist; **workspace overrides / takes precedence** on conflict.

**Open file:** Command Palette — **Kiro: Open workspace MCP config** / **Kiro: Open user MCP config**; or MCP panel **Open MCP Config**.

**Save:** reconnect on save (**Cmd+S**).

**Powers:** (from Powers doc) MCP from powers also registers under user config **Powers** section with namespacing — coordinate with this merge model.

---

## 3. Security (config & tools)

- Prefer **`${ENV_VAR}`** in JSON; **do not** commit secrets.  
- **`chmod 600`** on `~/.kiro/settings/mcp.json` and `.kiro/settings/mcp.json` (doc recommendation).  
- **Approved environment variables:** Kiro only expands env vars that are **allowlisted** in settings (**Mcp Approved Env Vars**); unapproved → security warning popup.  
- **autoApprove:** only for trusted, limited-scope tools; review parameters before approving ad hoc.  
- **disabledTools:** block dangerous ops (e.g. delete, force push) or reduce clutter.  
- **Workspace-level** MCP for project-specific tokens — isolates risk across projects.

---

## 4. Server directory & one-click install

Curated **Add to Kiro** list on Kiro’s site (AWS docs, Azure, GitHub, Postgres, Playwright, **Memory** (third-party graph memory), etc.) — **third-party** disclaimer.

**Install link schema:**

`https://kiro.dev/launch/mcp/add?name=<encoded>&config=<url-encoded-json>`

Doc provides **JS/TS**, **Python**, **bash** helpers and README **badge** snippet.

**agora planning:** same pattern could offer **one-click `agora-memory`** for Kiro users (`command` + `args` for `agora-code memory-server`).

---

## 5. Using tools

- Natural language → Kiro picks tool; or explicit **`#[server] tool_name …`** style (doc example: `#[aws-docs] search_documentation …`).  
- **Panel:** per-tool enable/disable; server context menu — Reconnect, Disable, Disable All Tools, Enable All Tools, MCP Logs.  
- **Approval** flow; **`autoApprove`** list per server.  
- **Chaining** and **specs** — doc says MCP can be used in implementation phases.

---

## 6. Prompts & resource templates

- Appear in **`#`** menu with MCP icon; **user-initiated** only.  
- Prompts may have **argument** forms; resource templates **URI params** → resolved content in context.

---

## 7. Elicitation

**Form-based** (text, number, yes/no, choice) or **URL-based** (e.g. OAuth). User can decline; server handles follow-up. Security: Kiro shows which server is asking.

---

## 8. Best practices (usage)

Specific requests; verify server connected; prefer **`disabledTools`** / careful **autoApprove**; combine MCP with local context.

---

## 9. agora-code-kiro — implications

1. **`agora-code memory-server`** fits **local** `command` + `args`; document **`PATH`** / full path; align with **approved env vars** if we use `${…}` for keys.  
2. **`disabledTools`** — optional **Kiro-only slim profile** without editing Python (complements server-side tool list ideas).  
3. **`autoApprove`** — matches shipped **`KIRO.md` / hooks** story for frictionless hook-driven MCP calls.  
4. **Install link + badge** — distribution path parallel to **Powers** marketplace story.  
5. **Workspace vs user** `mcp.json` — same as multi-root discussion: which file wins per root; **Memory** server name collisions across powers/workspace.  
6. Third-party **“Memory”** in directory is **not** agora — avoid naming confusion in marketing (`agora-memory` vs generic “Memory” MCP).

---

*Revision: MCP official user paste, Mar 2026. **Guides** section: pending.*
