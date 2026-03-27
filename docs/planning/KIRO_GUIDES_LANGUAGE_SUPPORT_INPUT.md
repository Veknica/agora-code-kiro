# Kiro **Guides — Language support** — planning input

**Not shipped user docs.** Condensed from user-provided **IDE → Guides → Language support** pages: **TypeScript/JavaScript**, **Python**, **Java** (page dates **2025-11-16** in paste). Add URLs when available.

**Purpose:** Same narrative repeated per language — prerequisites, extensions, chat workflows, **steering**, **hooks**, **MCP**, **`#docs`**, debugging shortcuts. Useful for **positioning agora** next to Kiro’s “default” stack (steering + hooks + MCP + built-in docs).

---

## 1. Common pattern (all three languages)

| Layer | What the guide pushes |
|--------|------------------------|
| **Prereqs** | Runtime (Node / Python / JDK), package manager, venv or build tool, Git |
| **Extensions** | Open VSX — ESLint/Prettier or Python/Java packs (ties to **diagnostics** doc) |
| **Chat** | Init configs, structure, refactor, debug prompts |
| **Steering** | Foundation files (`product.md`, `tech.md`, `structure.md`) + **custom** `.kiro/steering/*.md` for conventions (e.g. `js-conventions.md`, `python-conventions.md`, `java-conventions.md`) |
| **Hooks** | NL-created hooks — tests on save, typecheck, lint, deps, docs (language-specific examples) |
| **MCP** | Pointer to main MCP docs + **one sample server** per guide where given |
| **`#docs`** | Built-in doc providers (`#TypeScript`, `#Python`, `#Spring`, …) + `#URL` |
| **Debug** | Cmd/Ctrl+I inline, Cmd/Ctrl+L add to chat, Quick fix → Ask Kiro |

---

## 2. TypeScript / JavaScript (extras)

- Sample **MCP:** AWS Labs **Frontend** server (`uvx` + `awslabs.frontend-mcp-server@latest`).  
- **`#docs`:** Node, TypeScript, React, Svelte, Express, Vue, Alpine.  
- Hook examples: Jest on save, `tsc`, npm outdated, ESLint autofix, React component docs.

---

## 3. Python (extras — **agora-code is Python**)

- Extensions: Python, PyLint, Jupyter, debugpy, Rainbow CSV.  
- Conventions: PEP 8, Black, type hints, `python-conventions.md`; Django + **data-science** steering templates.  
- Hooks: pytest on save, pip outdated, flake8/pylint flow, venv when `requirements.txt` / `pyproject.toml` changes.  
- **`#docs`:** Python, PyTorch, PySide6.

**Planning note:** Dogfooding **agora-code** in Kiro on this repo = align with Python guide patterns (steering for package layout, optional hooks for `pytest` / `ruff` — **separate** from **agora-memory** hooks).

---

## 4. Java (extras)

- JDK (Corretto suggested), Maven/Gradle; Extension Pack for Java, Spring, etc.  
- Steering: `java-conventions.md`, `spring-boot-patterns.md`.  
- Hooks: JUnit on save, Checkstyle/SpotBugs, deps, JavaDoc, Spring config validation, formatters.  
- Sample **MCP:** **Maven** server (`uvx` + `maven-mcp-server@latest`).  
- Pointers: AWS MCP Servers, Awesome MCP Servers.

---

## 5. agora-code-kiro — how this guide fits

- Kiro teaches **steering + hooks + MCP** as the **default** automation stack; **agora** is another **MCP** (and **CLI**) in that slot — onboarding should say where agora **replaces**, **augments**, or **coexists** with language-guide examples (e.g. “keep ESLint hook; add agora for session memory”).  
- **`#docs`** is **framework docs**; agora is **project memory** — don’t blur the two in copy.  
- **Python** guide is the closest **template** for documenting **agora-code** development **in** Kiro.

---

*Revision: language-support guides user paste; user indicated this rounds out their Kiro doc dump, Mar 2026.*
