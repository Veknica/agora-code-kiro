"""
session.py — Session lifecycle manager for agora-code.

Session state is stored as JSON (not YAML, not SQLite) so it's:
  - Human-readable and debuggable
  - Easy to grep/cat from the terminal
  - Editable by hand if needed

File locations:
  - .agora-code/session.json   (project-local — take priority)
  - ~/.agora-code/session.json (global fallback)

The VectorStore (SQLite) is used separately only for:
  - Learnings (searchable knowledge base)
  - API call logs (pattern detection)

Session JSON shape:
{
  "session_id": "2026-03-08-debug-user-api",
  "started_at": "2026-03-08T09:30:00Z",
  "last_active": "2026-03-08T14:45:00Z",
  "status": "in_progress",
  "goal": "Fix 500 errors on POST /users",
  "hypothesis": "Email validation middleware too strict",
  "current_action": "Testing email formats",
  "api_base_url": "https://api.example.com",
  "endpoints_tested": [...],
  "discoveries": [...],
  "decisions_made": [...],
  "next_steps": [...],
  "blockers": [...],
  "tags": []
}
"""
from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


# --------------------------------------------------------------------------- #
#  File resolution                                                              #
# --------------------------------------------------------------------------- #

_AGORA_DIR  = ".agora-code"
_SESSION_FILE = "session.json"
_GLOBAL_DIR = Path.home() / ".agora-code"


def _find_project_root(start: Optional[Path] = None) -> Path:
    """
    Walk up from start until we find .agora-code/, .git/, or pyproject.toml.
    Returns start if nothing found.
    """
    current = (start or Path.cwd()).resolve()
    while True:
        if (current / _AGORA_DIR).is_dir():
            return current
        if (current / ".git").is_dir():
            return current
        if (current / "pyproject.toml").is_file():
            return current
        parent = current.parent
        if parent == current:
            return (start or Path.cwd()).resolve()
        current = parent


def get_session_path(project_root: Optional[Path] = None) -> Path:
    """Return path to the session.json for this project."""
    root = project_root or _find_project_root()
    return root / _AGORA_DIR / _SESSION_FILE


def get_global_session_path() -> Path:
    return _GLOBAL_DIR / _SESSION_FILE


def _resolve_session_path() -> Path:
    """Project-local wins over global."""
    local = get_session_path()
    if local.exists():
        return local
    return get_global_session_path()


# --------------------------------------------------------------------------- #
#  Session creation                                                             #
# --------------------------------------------------------------------------- #

def new_session(
    goal: Optional[str] = None,
    api_base_url: Optional[str] = None,
    tags: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Create a fresh session dict.
    Does NOT save to disk — call save_session() to persist.
    """
    now = _now()
    return {
        "session_id":      _slug(goal),
        "started_at":      now,
        "last_active":     now,
        "status":          "in_progress",
        "goal":            goal or "",
        "hypothesis":      None,
        "current_action":  None,
        "api_base_url":    api_base_url or "",
        "endpoints_tested":  [],
        "discoveries":       [],
        "decisions_made":    [],
        "next_steps":        [],
        "blockers":          [],
        "tags":              tags or [],
    }


# --------------------------------------------------------------------------- #
#  Save / load                                                                 #
# --------------------------------------------------------------------------- #

def save_session(
    session: Dict[str, Any],
    project_root: Optional[Path] = None,
) -> Path:
    """
    Write session to .agora-code/session.json.
    Always updates last_active to now.
    Writes atomically (temp file + rename).
    """
    session = {**session, "last_active": _now()}

    path = get_session_path(project_root)
    path.parent.mkdir(parents=True, exist_ok=True)

    # Write a gitignore so session.json isn't accidentally committed
    _ensure_gitignore(path.parent)

    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(session, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(path)
    return path


def load_session(project_root: Optional[Path] = None) -> Optional[Dict[str, Any]]:
    """
    Load the current session JSON.
    Returns None if no session file exists.
    """
    path = get_session_path(project_root)
    if not path.exists():
        # Try global path
        path = get_global_session_path()
        if not path.exists():
            return None

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else None
    except Exception:
        return None


def load_session_if_recent(
    max_age_hours: float = 24.0,
    project_root: Optional[Path] = None,
) -> Optional[Dict[str, Any]]:
    """
    Load session only if last_active is within max_age_hours.
    Returns None if session is stale or missing.

    This is what MCPServer calls on startup to auto-restore context.
    """
    session = load_session(project_root)
    if not session:
        return None

    try:
        last = datetime.fromisoformat(session["last_active"])
        # Make timezone-aware if naive
        if last.tzinfo is None:
            last = last.replace(tzinfo=timezone.utc)
        age_hours = (datetime.now(timezone.utc) - last).total_seconds() / 3600
        if age_hours > max_age_hours:
            return None
    except Exception:
        return None

    return session


def update_session(
    updates: Dict[str, Any],
    project_root: Optional[Path] = None,
) -> Dict[str, Any]:
    """
    Merge updates into the current session and save.
    Creates a new minimal session if none exists.
    """
    existing = load_session(project_root) or new_session()
    merged = {**existing, **updates}
    save_session(merged, project_root)
    return merged


def archive_session(
    summary: Optional[str] = None,
    outcome: str = "success",
    project_root: Optional[Path] = None,
) -> Dict[str, Any]:
    """
    Mark session as complete and persist to VectorStore for long-term memory.
    Also saves a summary embedding if embeddings are available.
    Returns the final session dict.
    """
    session = load_session(project_root) or {}
    session["status"] = "complete"
    session["outcome"] = outcome
    if summary:
        session["summary"] = summary
    save_session(session, project_root)

    # Persist to vector store for future recall
    try:
        from agora_code.vector_store import get_store
        from agora_code.embeddings import get_embedding

        text = _session_embedding_text(session)
        embedding = get_embedding(text)

        store = get_store()
        store.save_session(session, embedding=embedding)
    except Exception:
        pass  # Non-fatal: session is still saved to JSON

    return session


# --------------------------------------------------------------------------- #
#  Endpoint tracking helpers                                                   #
# --------------------------------------------------------------------------- #

def record_endpoint_attempt(
    session: Dict[str, Any],
    *,
    method: str,
    path: str,
    success: bool,
    params: Optional[dict] = None,
    error: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Update endpoints_tested in-place for a single API call result.
    Returns the modified session (not saved — caller must call save_session).
    """
    tested = session.setdefault("endpoints_tested", [])

    # Find existing entry for this endpoint
    key = f"{method.upper()} {path}"
    entry = next((e for e in tested if f"{e['method']} {e['path']}" == key), None)

    if entry is None:
        entry = {
            "method": method.upper(),
            "path": path,
            "attempts": 0,
            "successes": 0,
            "failures": 0,
            "last_attempt": None,
            "last_error": None,
            "working_parameters": None,
            "failing_parameters": [],
        }
        tested.append(entry)

    entry["attempts"]    += 1
    entry["last_attempt"] = _now()

    if success:
        entry["successes"] += 1
        if params:
            entry["working_parameters"] = params
    else:
        entry["failures"] += 1
        entry["last_error"] = error
        if params and params not in entry["failing_parameters"]:
            entry["failing_parameters"].append(params)

    return session


def add_discovery(
    session: Dict[str, Any],
    finding: str,
    *,
    evidence: Optional[str] = None,
    confidence: str = "confirmed",
    tags: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Append a discovery to the session. Returns modified session (not saved)."""
    session.setdefault("discoveries", []).append({
        "timestamp": _now(),
        "finding":   finding,
        "evidence":  evidence,
        "confidence": confidence,
        "tags":      tags or [],
    })
    return session


# --------------------------------------------------------------------------- #
#  Helpers                                                                     #
# --------------------------------------------------------------------------- #

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _slug(goal: Optional[str]) -> str:
    """Create a readable session ID like '2026-03-08-fix-post-users'."""
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if not goal:
        return f"{date}-{uuid.uuid4().hex[:6]}"
    words = "".join(c if c.isalnum() else "-" for c in goal.lower()).strip("-")
    words = "-".join(w for w in words.split("-") if w)[:40]
    return f"{date}-{words}"


def _session_embedding_text(session: Dict) -> str:
    """Build a text snippet to embed for semantic session search."""
    parts = [
        session.get("goal", ""),
        session.get("hypothesis", "") or "",
        session.get("summary", "") or "",
    ]
    for d in session.get("discoveries", [])[:5]:
        parts.append(d.get("finding", ""))
    return " ".join(p for p in parts if p).strip()


def _ensure_gitignore(agora_dir: Path) -> None:
    gi = agora_dir / ".gitignore"
    if not gi.exists():
        try:
            gi.write_text("# agora-code local state — do not commit\n*\n", encoding="utf-8")
        except Exception:
            pass
