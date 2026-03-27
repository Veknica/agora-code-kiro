# Kiro **Specs** — planning input for agora-code-kiro

**Not shipped user docs.** Condensed from user-provided Kiro documentation (pages dated **2025-11-17** through **2026-02-18**). Add canonical URLs when available.

---

## 1. What specs are

Structured artifacts for **features** and **bugfixes**: idea → **requirements / bug analysis** → **design** → **tasks** → implementation, with tracking and collaboration.

**Layout (per spec, under `.kiro/specs/<name>/`):**

| File | Role |
|------|------|
| **`requirements.md`** | Feature: user stories, acceptance criteria, **EARS** behaviors |
| **`bugfix.md`** | Bugfix: current / expected / **unchanged** behavior (regression guard) |
| **`design.md`** | Architecture, sequence diagrams, data flow, interfaces, error handling, testing |
| **`tasks.md`** | Discrete tasks, dependencies, optional vs required; **task execution UI** with status |

**Three phases (both feature and bugfix):** analysis (requirements or bugfix) → design → tasks → implementation.

---

## 2. Feature specs — workflow variants

Chosen **at spec creation**; **cannot switch** without starting a **new** spec (copy content over).

### Requirements-First

Flow: **requirements.md** → **design.md** → **tasks.md** → implement.

Use when: clear desired **behavior**, flexible architecture, product-led, greenfield.

### Design-First

Flow: **design.md** (high-level *or* low-level detail) → **requirements.md** (derived, “feasible”) → **tasks.md** → implement.

Use when: architecture/stack fixed, strict **non-functionals** (latency, compliance), porting existing designs, feasibility exploration.

### EARS (requirements)

Pattern: **`WHEN [condition/event] THE SYSTEM SHALL [expected behavior]`** — testable, traceable.

---

## 3. Bugfix specs

Same **three-phase shape**, but phase 1 is **`bugfix.md`**:

- **Current (defect):** `WHEN … THEN the system [incorrect behavior]`
- **Expected:** `WHEN … THE SYSTEM SHALL [correct behavior]`
- **Unchanged (regression prevention):** `WHEN … THE SYSTEM SHALL CONTINUE TO [existing behavior]`

Design phase: root cause, fix approach, **properties to test** (bug present, fix works, unchanged still works).

Tasks: may include **property-based tests (PBT)** for repro / fix / no regression.

---

## 4. Correctness — property-based testing (PBT)

Kiro maps **EARS-style** statements to **properties** (“for any … when … shall …”), generates many cases, **shrinking** on failure. Integrated in spec workflow: extract properties → tasks → run tests → fix loop. **PBT optional by default** so core implementation can come first.

*(Page dated 2025-11-17.)*

---

## 5. Specs vs “Vibe”

- **Specs:** complex features, costly regressions, team docs, iterative requirements/design.
- **Vibe:** quick exploration, unclear goals.

Can transition: **vibe → “Generate spec”** starts a spec session from chat context.

---

## 6. Chat and repo integration

- **`#spec`** — pick a spec; Kiro includes **requirements + design + tasks** in context (implementation, refine, validate).
- **Import:** paste/requirements in repo + `#foo-prfaq.md Generate a spec…`; or MCP from tools (JIRA, design tools) if available.
- **Iterate:** e.g. edit **requirements.md** → **Refine** on **design.md** to refresh design + tasks; **Update tasks** on **tasks.md**.
- **Many specs per repo** — e.g. `.kiro/specs/user-authentication/`, `product-catalog/`, …

**Run all tasks:** runs incomplete **required** tasks only.

**Already-done tasks:** **Update tasks** or ask in spec chat to scan codebase and mark complete.

---

## 7. Best-practice snippets (from paste)

- Workflow choice table (requirements-first vs design-first).
- Bugfix: include repro, current, expected, **constraints**.
- Sharing: version-controlled specs in repo; cross-team via submodules / central spec repo (Kiro asks for feedback on GitHub).

---

## 8. agora-code-kiro — implications (planning)

See **`AGORA_CODE_KIRO.md`** § Specs + memory. Short version:

- **Specs** = formal **what/how/tasks** for a feature or bug; **`#spec`** loads that bundle.
- **Agora** = **cross-session memory** + **token-efficient read/index** — orthogonal but **both** load context; product story should say how they **compose** (e.g. spec for this feature, agora for repo-wide learnings and checkpoints).
- Shipped hooks **`agora-inject-before-task`** / **`checkpoint-after-task`** already align with **per–spec-task** execution — agora-code-kiro can **name** that in steering (“spec task boundary = inject + checkpoint”).
- Optional future: tie **checkpoints** or **learnings** to **spec id** / path (schema or naming convention) — backlog only.

---

*Revision: initial ingest from user paste, Mar 2026.*
