"""
tldr.py — Backwards-compatibility shim.

This module re-exports everything from the split modules:
  - agora_code.compress  (route catalog + session state compression)
  - agora_code.summarizer (file content summarization + token estimation)

New code should import from compress or summarizer directly.
"""

# ruff: noqa: F401

from agora_code.compress import (
    DEFAULT_TOKEN_BUDGET,
    LEVELS,
    SESSION_DEFAULT_BUDGET,
    auto_compress_session,
    auto_level,
    compress_catalog,
    compress_catalog_auto,
    compress_session,
    measure_compression,
    session_restored_banner,
    summarize_routes,
    _session_age_str,
)

from agora_code.summarizer import (
    FILE_SIZE_THRESHOLD,
    FILE_SUMMARY_TOKEN_BUDGET,
    estimate_tokens,
    summarize_file,
)
