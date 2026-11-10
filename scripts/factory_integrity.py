#!/usr/bin/env python3
"""Explicit Factory alias integrity; no reliance on alias-versus-fallback bytes."""
from __future__ import annotations

from pathlib import Path


def verify_active_master_alias(core: Path, alias: Path) -> None:
    if not core.is_file() or not alias.is_file():
        raise ValueError("active master core or legacy alias missing")
    if core.read_bytes() != alias.read_bytes():
        raise ValueError("active v27 Master alias drift: master/MASTER_PROMPT_CURRENT.txt != master.path")
