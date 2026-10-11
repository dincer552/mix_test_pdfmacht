"""Legacy webbrowser compatibility shim for the combined app.

Any old TEST KONTROL route to open the updater now delegates to the shared
MIX TEST PDFMATCH updater. No stand-alone TEST KONTROL release is consulted.
"""
from __future__ import annotations


def open(url: str, new: int = 0, autoraise: bool = True) -> bool:
    del url, new, autoraise
    try:
        import tkinter as tk
        from unified_updater import install_update
        parent = tk._default_root
        if parent is None:
            return False
        install_update(parent)
        return True
    except Exception:
        return False
