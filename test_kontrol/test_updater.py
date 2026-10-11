"""Compatibility adapter routed to the single combined-app updater.

TEST KONTROL historically calls these function names from its standalone updater.
They remain here as a bridge, but no longer access the standalone TEST KONTROL
release or download stream.
"""
from __future__ import annotations

from unified_updater import latest_release, check_for_update as _check_ui, install_update


def check_for_update(current_exe=None) -> dict:
    """Return a shape compatible with the old TEST KONTROL updater API."""
    del current_exe
    info = latest_release()
    return {
        "available": bool(info.get("available")),
        "version": info.get("version", ""),
        "build": info.get("version", ""),
        "size": 0,
        "sha256": "",
        "file": "Mix_Test_PDFMatch_latest.exe",
        "chunks": [],
    }


def start_update(parent, update_button=None) -> None:
    """Use the unified updater instead of the old TEST KONTROL release."""
    install_update(parent, update_button=update_button)


def start_recovery_update(parent, status=None, update_button=None) -> None:
    """Recovery also uses the one unified Windows package."""
    install_update(parent, update_button=update_button, status_var=status)
