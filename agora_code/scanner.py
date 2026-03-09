"""
scanner.py — 4-tier cascade orchestrator.

Usage:
    from agora_code import scan

    catalog = await scan("./my-api")           # auto-detect, auto-LLM if needed
    catalog = await scan("./my-api", use_llm=True)  # force LLM tier
    catalog = await scan("https://api.example.com") # remote OpenAPI

The cascade:
    Tier 1: OpenAPI spec  → universal, free, instant
    Tier 2: Python AST    → accurate, free, instant (Python only)
    Tier 3: LLM extract   → any language; auto if Tier 1+2 fail & key available
    Tier 4: Regex fallback → always works, ~70% accurate

Auto-escalation:
    If Tier 1 and 2 find nothing (or < AUTO_ESCALATE_THRESHOLD routes),
    Tier 3 is tried automatically IF any LLM key is configured.
    No --use-llm flag required.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from agora_code.models import RouteCatalog
from agora_code.extractors import openapi, python_ast, regex

# Below this many routes, we consider extraction suspect and try LLM
AUTO_ESCALATE_THRESHOLD = 2


async def scan(
    target: str,
    *,
    use_llm: bool = False,
    llm_provider: str = "auto",
    llm_model: Optional[str] = None,
    edition: str = "community",
) -> RouteCatalog:
    """
    Scan a codebase or API URL and return a RouteCatalog.

    Args:
        target:       local directory path or remote URL
        use_llm:      force Tier 3 LLM extraction (otherwise auto-escalates)
        llm_provider: "auto" | "claude" | "openai" | "gemini"
                      auto picks from ANTHROPIC/OPENAI/GEMINI_API_KEY
        llm_model:    override default LLM model
        edition:      "community" | "enterprise"

    Returns:
        RouteCatalog with all discovered routes
    """
    from agora_code.extractors import llm as llm_extractor

    # --- Tier 1: OpenAPI ---
    if openapi.can_handle(target):
        catalog = await openapi.extract(target)
        catalog.edition = edition
        _log(f"✅ Tier 1 (OpenAPI): {len(catalog)} routes from {target!r}")
        return catalog

    # --- Tier 2: Python AST ---
    tier2_catalog = None
    if python_ast.can_handle(target):
        tier2_catalog = await python_ast.extract(target)
        tier2_catalog.edition = edition
        if len(tier2_catalog) >= AUTO_ESCALATE_THRESHOLD:
            _log(f"✅ Tier 2 (Python AST): {len(tier2_catalog)} routes from {target!r}")
            return tier2_catalog
        else:
            _log(f"⚠️  Tier 2 (Python AST): only {len(tier2_catalog)} routes — escalating...")

    # --- Tier 3: LLM (auto-escalate or forced) ---
    should_try_llm = use_llm or llm_extractor.is_available()
    if should_try_llm:
        try:
            catalog = await llm_extractor.extract(
                target, provider=llm_provider, model=llm_model
            )
            catalog.edition = edition
            if len(catalog) > 0:
                _log(f"✅ Tier 3 (LLM/{catalog.extractor}): {len(catalog)} routes from {target!r}")
                return catalog
            _log("⚠️  Tier 3 (LLM): no routes found — falling back to Tier 4")
        except RuntimeError as e:
            # No LLM provider configured — logged but not fatal
            _log(f"ℹ️  Tier 3 skipped: {e}")
        except Exception as e:
            _log(f"⚠️  Tier 3 error: {e} — falling back")

    # Return Tier 2 result if we have one (even if sparse)
    if tier2_catalog is not None and len(tier2_catalog) > 0:
        _log(f"↩️  Using Tier 2 result ({len(tier2_catalog)} routes)")
        return tier2_catalog

    # --- Tier 4: Regex fallback ---
    catalog = await regex.extract(target)
    catalog.edition = edition
    _log(f"⚠️  Tier 4 (Regex): {len(catalog)} routes from {target!r} (70% accuracy)")
    return catalog


# --------------------------------------------------------------------------- #
#  Enterprise edition helper                                                   #
# --------------------------------------------------------------------------- #

async def scan_enterprise(
    target: str,
    *,
    supabase_url: str,
    supabase_key: str,
    project_id: str,
    use_llm: bool = False,
    llm_provider: str = "openai",
) -> RouteCatalog:
    """
    Enterprise edition: scan + persist catalog to Supabase.

    Routes are stored in a `route_catalogs` table for:
      - Multi-user shared access
      - Incremental recompile (skip unchanged files)
      - Future: org-level auth gating (Supabase Auth / WorkOS)

    Requires: pip install agora-code[enterprise]
    """
    try:
        from supabase import create_client
    except ImportError:
        raise ImportError("Install: pip install agora-code[enterprise]")

    catalog = await scan(
        target,
        use_llm=use_llm,
        llm_provider=llm_provider,
        edition="enterprise",
    )

    # Persist to Supabase
    client = create_client(supabase_url, supabase_key)
    rows = []
    for route in catalog.routes:
        rows.append({
            "project_id": project_id,
            "method": route.method,
            "path": route.path,
            "description": route.description,
            "params": [
                {"name": p.name, "type": p.type, "required": p.required,
                 "location": p.location}
                for p in route.params
            ],
            "tags": route.tags,
            "extractor": catalog.extractor,
            "source": catalog.source,
        })

    if rows:
        # Upsert on (project_id, method, path) — safe to re-run
        client.table("route_catalogs").upsert(
            rows,
            on_conflict="project_id,method,path",
        ).execute()

    _log(f"☁️  Enterprise: {len(catalog)} routes persisted to Supabase (project={project_id})")
    return catalog


def _log(msg: str) -> None:
    import sys
    print(msg, file=sys.stderr)
