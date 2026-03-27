# Kiro **Powers** — official doc input for agora-code-kiro

**Not shipped user docs.** Condensed from user-provided **official Kiro Powers** documentation (pages dated **2025-12-03** through **2026-01-15**). Add canonical URLs when available.

---

## 1. Concept

**Problem — context overload:** Many MCP servers registered at once → **100+ tools**, **tens of thousands of tokens** before the first user line — slow, noisy, lower quality.

**Powers:** **Keyword-driven** activation — Kiro evaluates **installed powers** against the task and loads **only relevant** power context + MCP tools. When the topic shifts (e.g. payments → database), another power can activate and prior ones **drop** from that framing.

---

## 2. What’s in a power

| Piece | Role |
|--------|------|
| **`POWER.md`** | Required. **Frontmatter** (when to activate: `name`, `displayName`, `description`, **`keywords`**). Body: **onboarding** steps (deps, CLI, **optional hook snippets**), **steering** / best practices (inline or pointers to `steering/`). |
| **`mcp.json`** | Optional. MCP server defs; **server names in POWER.md must match** `mcpServers` keys. |
| **`steering/`** | Optional. Per-workflow markdown; POWER.md can map situations → which steering file to load. |
| **Hooks** | Optional. Onboarding in POWER.md can instruct adding files under **`.kiro/hooks/`** (example in official doc uses **`userTriggered`** + **`askAgent`**). |

---

## 3. Install & discovery

- **Curated:** kiro.dev/powers, launch partners (Datadog, Figma, Neon, Netlify, Postman, Supabase, Stripe, etc.); **IDE** Powers panel (👻⚡) → Install → Try.
- **Custom:** GitHub URL or **local path**; repo root must have **`POWER.md`**.
- **MCP from powers:** Registered in **`~/.kiro/settings/mcp.json`** under **Powers** section; Kiro **namespaces** server names to avoid clashes (e.g. `supabase-local` → `power-supabase-supabase-local`).
- **Third-party warning** — trust, terms, licensing; Kiro disclaims responsibility.

**Updates:** Powers panel → power → **Check for updates** → Update.

---

## 4. Create / author (summary)

- **Keywords:** Match how devs talk (`database`, `supabase`, …) so activation is predictable.
- **Onboarding:** Validate deps, install steps, **paste hook JSON** for workspace (official Supabase example uses `userTriggered` + MCP `get_advisors`).
- **Steering:** Simple = all in POWER.md; complex = split `steering/*.md` and document **when to load which** in POWER.md.
- **mcp.json:** Use **env vars** for secrets; names align with POWER.md tool references.
- **Share:** Public GitHub; others install via **Add power from GitHub**.

**Example layouts** (from docs): simple (`POWER.md` + `mcp.json`); prisma-style with one steering file; full-stack multi-steering; docs-only power (no MCP).

---

## 5. Hook snippet in official “Create power” doc (for cross-ref to Hooks)

Official POWER.md onboarding example includes a **`.kiro/hooks/*.kiro.hook`** with:

- `"when": { "type": "userTriggered" }`
- `"then": { "type": "askAgent", "prompt": "… MCP …" }`

The create-power example used **`userTriggered`** in JSON; official **Hooks** doc names this **Manual Trigger** — see **`KIRO_HOOKS_OFFICIAL_INPUT.md` §2**.

---

## 6. agora-code-kiro — implications (planning)

- **Powers vs project MCP:** Today agora is often wired as **workspace** `.kiro/settings/mcp.json` + **`.kiro/hooks/`** in-repo. A **first-class Kiro-native** path could be an **agora Power** (`POWER.md` + keywords like `memory`, `session`, `checkpoint`, `context`) so **`agora-memory`** loads **only when relevant** — aligns with official “dynamic MCP” story and your **slim baseline context** goal.
- **Namespace:** Expect **`power-*`** prefixed MCP server names if agora ships inside a power — document for users who also add raw `agora-memory`.
- **Hooks duplication:** Power onboarding might add hooks; **project** already ships **13 hooks** — product must say **use one path** or **merge** to avoid double inject/index.
- **Marketplace:** “One-click” install from kiro.dev vs pip + copy `.kiro` — distribution decision for agora-code-kiro.

---

*Revision: Powers official user paste, Mar 2026. **Hooks** full official doc: pending separate paste.*
