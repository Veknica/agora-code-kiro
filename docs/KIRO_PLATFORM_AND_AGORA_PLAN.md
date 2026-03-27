# Kiro platform notes & agora-code context plan

How Kiro fits together, where durable state tends to live on macOS, and how **agora-code** adds project-scoped memory on top. Local folder / GitHub repo name can stay **`agora-code`**; no rename required for this work.

---

## Sources (where each part comes from)

| Topic | Source |
|--------|--------|
| MCP, steering, hooks, Powers (concepts) | Official Kiro documentation and changelog, e.g. [kiro.dev](https://kiro.dev), [Steering](https://kiro.dev/docs/steering), [Powers](https://kiro.dev/powers), [changelog](https://kiro.dev/changelog/remote-mcp-and-global-steering/). |
| Product positioning (“AI IDE”, interfaces) | **`Kiro` repo** (e.g. clone at `~/Desktop/Kiro`) — upstream README and docs in that repository. |
| How Amazon structures Power packs (MCP + steering + hooks) | **`kiro-powers` repo** (e.g. `~/Desktop/kiro-powers`) — per-pack `.kiro` layouts under each vertical. |
| Demo app patterns (steering, prompting, layout) | **`spirit-of-kiro` repo** (e.g. `~/Desktop/spirit-of-kiro`) — README and `.kiro/steering/` in that demo project. |
| agora-code ↔ Kiro wiring (CLI, MCP, hooks, steering) | **This repo**: `KIRO.md`, `.kiro/settings/mcp.json`, `.kiro/steering/agora-memory.md`, `.kiro/hooks/*.kiro.hook`, `power-agora-memory/POWER.md`. |
| macOS app data layout (paths below) | **Conventional layout** for Electron/VS Code–family apps on macOS (`~/Library/Application Support/<AppName>/`); subdirectory names such as `User/globalStorage/<extension-id>/` follow VS Code’s model. Specific paths listed are **as documented for troubleshooting**, not a guarantee of every future Kiro version. |
| Setup gotchas (PATH, steering empty, testing) | **Prior agora-code / Cursor working sessions** in this project (informal; verify against current Kiro UI and docs). |

---

## 1. What Kiro is (high level)

- **Kiro** is an **AI-first IDE** in the VS Code lineage, with first-class **agent**, **MCP**, **steering**, and **hooks**.
- Extension points (see Sources: official docs):
  - **MCP** — project `.kiro/settings/mcp.json` or global `~/.kiro/settings/mcp.json`.
  - **Steering** — Markdown in project `.kiro/steering/` or global `~/.kiro/steering/`.
  - **Hooks** — lifecycle automation (prompt, agent stop, pre/post tool use, spec tasks, save, etc.); tool names and events should be confirmed in-product if something does not fire.
  - **Powers** — bundled MCP + steering + hooks for specific workflows.

**Why it can feel different from stock VS Code:** shared storage patterns (Chromium/Electron, `User/` state, SQLite) with **agent-specific** global storage under the Kiro agent extension id.

---

## 2. Related repositories (local examples)

These paths are typical clone locations; adjust if your machine differs.

| Path | Repository role | Usefulness |
|------|-----------------|------------|
| `~/Desktop/Kiro` | Kiro product / upstream materials | How Kiro describes itself; not application code for agora-code. |
| `~/Desktop/kiro-powers` | Official Powers monorepo | **Reference** for MCP + steering + hooks packaging. |
| `~/Desktop/spirit-of-kiro` | Spirit of Kiro demo (game) | **Workflow / steering / prompting** examples; README notes heavy Kiro-assisted development. |
| `~/Desktop/powers`, `~/Desktop/elixir/.kiro` | Other local projects | Optional; only when relevant. |
| This repo (`agora-code`) | Persistent memory CLI + MCP | **Canonical** Kiro integration we ship (`KIRO.md`, `.kiro/*`). |

---

## 3. Kiro data on macOS (reference paths)

Base directory (same *class* of layout as VS Code–family apps):

`~/Library/Application Support/Kiro/`

| Location | Role |
|----------|------|
| `User/workspaceStorage/<id>/` | Per-workspace state; `workspace.json` typically maps a workspace id to a `file:///...` folder URI. |
| `User/globalStorage/kiro.kiroagent/` | Global data for the **Kiro agent** extension. |
| `User/globalStorage/kiro.kiroagent/**/*.chat` | Per-conversation chat payloads (opaque to agora-code). **Private; do not commit.** |
| `User/globalStorage/kiro.kiroagent/workspace-sessions` | Session-related metadata (internal format). |
| `User/globalStorage/kiro.kiroagent/state.vscdb` (+ `.backup`) | SQLite-style extension state (VS Code pattern). |
| `User/globalStorage/kiro.kiroagent/config.json`, `profile.json`, `index` | Local agent configuration / indexing hints. |
| `blob_storage`, `Cache`, `CachedData`, `WebStorage`, … | Caches — not a substitute for **project memory**. |

**Implication for agora-code:** Kiro persists chats locally, but that layer is **product-owned** and not **git-aware, searchable, project-keyed memory**. agora-code provides that second layer via `~/.agora-code/memory.db` (or `AGORA_CODE_DB`), MCP, and CLI.

---

## 4. Setup lessons (informal — verify in your build)

From earlier agora-code work sessions (not official Kiro spec):

- **MCP** (`agora-code memory-server`) is portable; **hooks** differ by IDE and must be mapped per product.
- **Steering** must actually **instruct** the model (a configured MCP plus an **empty** global steering file is a common miss).
- Prefer a **full path** to `agora-code` in `mcp.json` if the IDE spawns MCP with a minimal `PATH`.
- **Smoke test:** MCP shows `agora-memory` connected; ask for current session and confirm `get_session_context` runs.
- **Hook tool names** (e.g. `readCode`, `writeFile`) must match what Kiro exposes; confirm in UI/docs if a hook never runs.

Do not commit secrets; rotate any credential that was ever exposed in chat or embedded in a remote URL.

---

## 5. How agora-code manages context next to Kiro

| Need | Kiro alone | agora-code |
|------|------------|------------|
| Raw chat history | Extension-owned `.chat` / internal state | Optional summaries via `store_learning`, checkpoints, sessions |
| “What was I doing?” across days | Mostly chat scroll | `inject`, `get_session_context`, DB sessions |
| Durable repo facts | Steering if you write them | `store_learning` / `recall_learnings` (+ team tools) |
| Large-file discipline | Hooks + steering | `summarize_file`, `read_file_range`, snapshot cache |
| Cross-session symbols | Editor features | `index_file`, `get_file_symbols`, `search_symbols` |

**Doc / product checklist:**

1. Keep **`KIRO.md`** as the primary Kiro install guide; link from README if desired.
2. Optional: short pointer in `KIRO.md` to this file for “where Kiro stores chats vs where agora-code stores memory.”
3. Align **`DATABASE.md`** vs **`DATABASE_AND_STRUCTURED_LAYER.md`** roles (schema vs inject/cache behavior).
4. After Kiro upgrades, re-check hook tool names and events against a real project.
5. Optional: a Power-style bundle modeled on **`kiro-powers`** packs.

---

## 6. Spirit of Kiro (demo repo)

Useful for **methodology** (steering, project layout, documentation style). For **MCP/hook manifest patterns**, prefer **`kiro-powers`** and official Kiro docs.

---

## 7. References inside agora-code

- `KIRO.md` — setup, hook table, verification.
- `.kiro/settings/mcp.json`, `.kiro/steering/agora-memory.md`, `.kiro/hooks/*.kiro.hook`
- `power-agora-memory/POWER.md`

---

*Kiro’s on-disk layout can change between releases; re-check paths after major upgrades.*
