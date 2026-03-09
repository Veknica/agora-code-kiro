# agora-code

**Turn any codebase into a memory-aware API agent.**

agora-code is a two-part tool:

1. **Route Discovery** — scans Python, JavaScript, OpenAPI specs, or any codebase and extracts every API endpoint automatically.
2. **Session Memory** — remembers everything about your API testing sessions (what you tried, what you learned, what broke) and restores that context automatically when you come back.

This is not just a route scanner. It's a context manager that happens to know about your APIs. The AI assistant you're working with gets rich, compressed context about your session instead of starting fresh every time.

---

## Installation

```bash
pip install agora-code
```

For semantic search (enables recall by meaning, not just keyword):
```bash
pip install agora-code[memory]      # sqlite-vec + OpenAI embeddings
```

For LLM-based route extraction (non-Python/non-OpenAPI projects):
```bash
pip install agora-code[llm]         # OpenAI extract support
```

---

## Quick Start

### 1. Scan your API

```bash
agora-code scan ./my-fastapi-app
agora-code scan https://api.example.com          # remote OpenAPI URL
agora-code scan ./my-node-app --use-llm          # LLM extraction for non-Python
```

### 2. Serve as an MCP tool (Claude / Cline)

```bash
agora-code serve ./my-api --url http://localhost:8000
```

Add to Claude Desktop or Cline config:

```json
{
  "mcpServers": {
    "my-api": {
      "command": "agora-code",
      "args": ["serve", "./my-api", "--url", "http://localhost:8000"]
    }
  }
}
```

Claude can now call your API directly as tools.

### 3. Save your session

```bash
agora-code checkpoint --goal "Debug POST /users email failures"
```

Next time you start the server, Claude instantly sees where you left off.

---

## How Route Discovery Works

agora-code uses a 4-tier extraction pipeline, trying each in order:

| Tier | Method | When it runs |
|---|---|---|
| 1 | OpenAPI / Swagger spec parsing | Always (if spec file or URL found) |
| 2 | Python AST analysis | FastAPI, Flask, Django |
| 3 | LLM extraction (opt-in) | `--use-llm` flag — any language |
| 4 | Regex fallback | Catches JS/TS `app.get`, `router.post`, etc. |

**Output** is a `RouteCatalog` — a structured list of routes with method, path, params (name, type, location, required), and description.

---

## How Session Memory Works

The memory system has two storage layers:

### Active Session (`.agora-code/session.json`)

The current session is a **JSON file** in your project directory. Human-readable, gitignored, editable by hand. No database, no YAML.

```json
{
  "session_id": "2026-03-08-debug-post-users",
  "goal": "Fix 422 errors on POST /users",
  "hypothesis": "Email validation middleware too strict",
  "current_action": "Testing + symbol in email addresses",
  "endpoints_tested": [
    {
      "method": "POST", "path": "/users",
      "attempts": 8, "successes": 3, "failures": 5,
      "last_error": "422 Unprocessable Entity",
      "working_parameters": {"email": "user@example.com"},
      "failing_parameters": [{"email": "user+tag@example.com"}]
    }
  ],
  "discoveries": [
    {
      "finding": "API rejects + symbol in emails",
      "confidence": "confirmed",
      "evidence": "422 on user+tag@example.com, 200 on user@example.com"
    }
  ],
  "next_steps": ["Check email validation middleware", "Try URL-encoding the +"],
  "blockers": []
}
```

### Learnings Database (`~/.agora-code/memory.db`)

Completed sessions and stored learnings live in a local SQLite database. Searchable by keyword or meaning.

- **FTS5 / BM25** keyword search — always works, zero extra dependencies
- **Cosine similarity** semantic search — add `pip install sqlite-vec` + an API key

---

## Embeddings & Search

Embeddings determine how well `agora-code recall` matches by meaning rather than exact words.

**Provider priority (auto-detected):**

```
OPENAI_API_KEY set?   →  text-embedding-3-small  (1536 dims, ~$0.00002/call)
GEMINI_API_KEY set?   →  gemini-embedding-001    (768 dims, free tier)
Neither set?          →  FTS5/BM25 keyword search only  (still useful)
```

No API key needed to use agora-code. You just won't get semantic recall — keyword search works fine.

---

## Context Compression

This is the core of the context manager. Instead of dumping thousands of tokens of JSON into Claude's context on every session start, agora-code compresses the session to the highest-detail level that fits your **token budget**.

| Level | What's included | Approximate tokens |
|---|---|---|
| **index** | Goal + endpoint list | ~50 |
| **summary** | + hypothesis + discoveries + next steps | ~200 |
| **detail** | + all attempts, decisions, blockers per endpoint | ~500 |
| **full** | Raw JSON (no compression) | 3,000+ |

The auto-picker tries `detail` → `summary` → `index` until it fits the budget (default: 2,000 tokens). The restoration banner Claude sees on startup is typically **~120 tokens** instead of 3,000+.

---

## Session Commands

### `agora-code checkpoint`
Save the current session state.

```bash
agora-code checkpoint --goal "Debug POST /users"
agora-code checkpoint --hypothesis "Email validation too strict"
agora-code checkpoint --action "Testing + in email"
agora-code checkpoint --next "Try URL encoding" --next "Check middleware"
agora-code checkpoint --blocker "No access to middleware source"
```

All flags are optional — run with no flags to just update `last_active` timestamp.

---

### `agora-code status`
Show the current session in detail.

```bash
agora-code status
```

```
════════════════════════════════════════════════════════════
🗂  SESSION: 2026-03-08-debug-post-users
════════════════════════════════════════════════════════════
GOAL: Debug POST /users email validation failures
HYPOTHESIS: Email validation middleware too strict
WHAT YOU DISCOVERED:
  ✓ API rejects + symbol in emails
  ~ Rate limit may be 100 req/min
NEXT STEPS:
  → Try URL encoding +
  → Check middleware config
ENDPOINTS:
  • POST /users  (3/8 ok)

🧠 Memory: 4 sessions, 12 learnings, 47 API calls logged  [vector search: off]
```

---

### `agora-code complete`
Archive the current session and store it in the learnings DB.

```bash
agora-code complete --summary "Found that POST /users rejects RFC-valid emails with + symbol"
agora-code complete --outcome partial
agora-code complete --outcome abandoned
```

Outcomes: `success` (default) | `partial` | `abandoned`

---

### `agora-code restore`
Load a past session as the active session.

```bash
agora-code restore                                    # list recent sessions
agora-code restore 2026-03-08-debug-post-users        # restore specific session
```

---

### `agora-code learn`
Store a permanent finding about an API. Persists in `~/.agora-code/memory.db` forever.

```bash
agora-code learn "POST /users rejects + in email addresses"
agora-code learn "Rate limit is 100 req/min on /data endpoints" \
    --endpoint "GET /data" \
    --api "https://api.example.com" \
    --tags "rate-limit,data" \
    --confidence confirmed
agora-code learn "Auth token expires after 15 minutes (not 1 hour as documented)" \
    --confidence confirmed \
    --evidence "Got 401 after 15m despite docs saying 1h"
```

Confidence levels: `confirmed` | `likely` | `hypothesis`

---

### `agora-code recall`
Search your learnings knowledge base.

```bash
agora-code recall "email validation"       # finds email-related learnings
agora-code recall "rate limit" --limit 10
agora-code recall "auth expires"           # semantic: finds "token expiry" even without exact words
```

If `OPENAI_API_KEY` is set, search is semantic (finds conceptually related results).
Otherwise, FTS5 keyword search is used.

---

## Auto-Context Injection (MCP Server)

When Claude starts the MCP server via `agora-code serve`, it:

1. Checks `.agora-code/session.json` — is it < 24 hours old?
2. If yes, compresses the session to fit the token budget
3. Emits it as a `notifications/message` over the MCP protocol **before the main loop**

Claude sees the restoration banner **immediately** without any user prompt.

Every API call made through a tool:
- Gets logged to `~/.agora-code/memory.db` with method, path, params, status, latency
- If the same parameter combo fails 3+ times, a `💡 PATTERN` hint appears in the tool response

---

## Python API

```python
import asyncio
from agora_code import scan, MCPServer
from agora_code.session import new_session, save_session, load_session_if_recent
from agora_code.tldr import compress_session, auto_compress_session
from agora_code.vector_store import get_store
from agora_code.embeddings import get_embedding

# Scan
catalog = asyncio.run(scan("./my-api"))

# Serve as MCP
server = MCPServer(catalog, base_url="http://localhost:8000")
asyncio.run(server.serve())

# Session
session = new_session(goal="Debug POST /users")
save_session(session)

# Compress for Claude context
summary = compress_session(session, level="summary")        # ~200 tokens
banner = auto_compress_session(session, token_budget=500)   # fits budget

# Learnings
store = get_store()
embedding = get_embedding("POST /users rejects + in emails")
store.store_learning("POST /users rejects + in emails", embedding=embedding, tags=["email"])

# Recall
results = store.search_learnings_keyword("email validation")
```

---

## Project Structure

```
agora-code/
├── agora_code/
│   ├── __init__.py           # Public API: scan, MCPServer, APICallNode
│   ├── scanner.py            # 4-tier extraction pipeline orchestrator
│   ├── models.py             # Route, Param, RouteCatalog dataclasses
│   ├── agent.py              # MCPServer (JSON-RPC 2.0 stdio), APICallNode
│   ├── cli.py                # All CLI commands (click)
│   ├── tldr.py               # Context compression: routes + sessions
│   ├── session.py            # JSON session lifecycle manager
│   ├── vector_store.py       # SQLite + sqlite-vec + FTS5 storage
│   ├── embeddings.py         # OpenAI / Gemini / keyword auto-select
│   ├── memory_layer.py       # agora-mem integration (optional)
│   └── extractors/
│       ├── openapi.py        # Tier 1: OpenAPI/Swagger spec parser
│       ├── ast_parser.py     # Tier 2: Python AST (FastAPI, Flask, Django)
│       ├── llm.py            # Tier 3: LLM-based extraction (opt-in)
│       └── regex.py          # Tier 4: Regex fallback (JS/TS/any)
├── tests/
│   ├── test_extractors_ast.py
│   ├── test_extractors_openapi.py
│   ├── test_integration.py
│   ├── test_mcp_server.py
│   └── test_memory.py
├── .agora-code/              # Project-local (gitignored)
│   └── session.json          # Active session state
│  ~/.agora-code/             # Global (persists across projects)
│   └── memory.db             # Learnings + API call history
└── pyproject.toml
```

---

## Environment Variables

| Variable | Purpose |
|---|---|
| `OPENAI_API_KEY` | Enables OpenAI embeddings + LLM extraction |
| `GEMINI_API_KEY` | Enables Gemini embeddings + LLM extraction |
| `AGORA_AUTH_TOKEN` | Default bearer token for API calls |
| `AGORA_CODE_DB` | Override memory DB path (default: `~/.agora-code/memory.db`) |

---

## Authentication

```bash
agora-code auth ./my-api                              # interactive prompt
agora-code auth ./my-api --type bearer --token mytoken
agora-code auth ./my-api --type api-key --token mykey
agora-code auth ./my-api --type none                  # disable
```

Or pass inline:
```bash
agora-code serve ./my-api --url http://localhost:8000 --auth-token mytoken
AGORA_AUTH_TOKEN=mytoken agora-code serve ./my-api --url http://localhost:8000
```

Auth config is saved to `.agora-code/auth.json` (gitignored).

---

## Context Compression Levels Explained

Use `--level` in the `chat` command to control how much of the API catalog is sent to the LLM:

```bash
agora-code chat ./my-api --url http://localhost:8000 --level index    # smallest
agora-code chat ./my-api --url http://localhost:8000 --level summary  # default
agora-code chat ./my-api --url http://localhost:8000 --level detail   # more context
agora-code chat ./my-api --url http://localhost:8000 --level full     # entire catalog
```

- **index** — `METHOD /path` only. Use when you have many endpoints and need to minimize tokens.
- **summary** — `METHOD /path — description`. Best default for most sessions.
- **detail** — Adds all parameters with types and required/optional status. Use when debugging specific endpoint contracts.
- **full** — Raw JSON. Use for inspection or when building tools on top.

The same levels apply to `agora-code inject` and the session compression system.

---

## Running Tests

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

60 tests covering: AST extraction, OpenAPI parsing, regex fallback, MCP server protocol, memory stats, and end-to-end scan→serve pipeline.

---

## What agora-code is NOT

- Not an API proxy or gateway
- Not a hosted service — everything runs locally
- Not a replacement for Postman (it's for AI-assisted API development sessions)
- Not dependent on any cloud service (works fully offline with keyword search)
