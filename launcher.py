from __future__ import annotations

import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from mix_meta import BUILD_VERSION
from unified_updater import check_for_update, install_update


def _base_dir() -> Path:
    return Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))


def _check(parent, manual=True):
    check_for_update(
        parent,
        manual=manual,
        update_button=getattr(parent, "_mix_update_button", None),
        version_label=getattr(parent, "_mix_version_label", None),
        status_var=getattr(parent, "_mix_status_var", None),
    )


def _install(parent):
    install_update(
        parent,
        update_button=getattr(parent, "_mix_update_button", None),
        status_var=getattr(parent, "_mix_status_var", None),
    )


def _run_pdf_match():
    pdf_dir = str(_base_dir() / "pdf_match")
    if pdf_dir not in sys.path:
        sys.path.insert(0, pdf_dir)
    try:
        import desktop_app
        from unified_updater import check_for_update as common_check, install_update as common_install

        # Disable the legacy PDF Match updater; all checks and installs use
        # the unified MIX TEST PDFMATCH release.
        desktop_app.App._schedule_update_check = lambda self: None
        desktop_app.App._manual_update_check = lambda self: common_check(
            self,
            manual=True,
            update_button=getattr(self, "_update_button", None),
            version_label=getattr(self, "_update_build_label", None),
            status_var=getattr(self, "_mix_status_var", None),
        )
        desktop_app.App.download_available_update = lambda self: common_install(
            self,
            update_button=getattr(self, "_update_button", None),
            status_var=getattr(self, "_mix_status_var", None),
        )

        from desktop_grouped_app import GroupedApp
        GroupedApp().mainloop()
    except Exception as exc:
        messagebox.showerror("PDF MATCH başlatılamadı", str(exc))


def _run_test_kontrol():
    test_dir = str(_base_dir() / "test_kontrol")
    if test_dir not in sys.path:
        sys.path.insert(0, test_dir)
    try:
        from unified_updater import check_for_update as common_check, install_update as common_install
        from test_kontrol.app import TestControlApp

        # Disable standalone update polling and route update entry points to
        # the same combined release used by PDF Match.
        TestControlApp._schedule_update_check = lambda self: None
        TestControlApp._manual_update_check = lambda self: common_check(
            self,
            manual=True,
            update_button=getattr(self, "_update_button", None),
            version_label=getattr(self, "_update_build_label", None),
            status_var=getattr(self, "_mix_status_var", None),
        )
        TestControlApp._start_update = lambda self: common_install(
            self,
            update_button=getattr(self, "_update_button", None),
            status_var=getattr(self, "_mix_status_var", None),
        )
        TestControlApp._open_update_page = lambda self: common_install(
            self,
            update_button=getattr(self, "_update_button", None),
            status_var=getattr(self, "_mix_status_var", None),
        )
        TestControlApp().mainloop()
    except Exception as exc:
        messagebox.showerror("TEST KONTROL başlatılamadı", str(exc))


def _show_home():
    root = tk.Tk()
    root.title("MIX TEST PDFMATCH")
    root.geometry("680x430")
    root.minsize(580, 360)
    root.configure(bg="#f0f4f9")

    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass
    style.configure("TFrame", background="#f0f4f9")
    style.configure("Card.TFrame", background="#ffffff")
    style.configure("Title.TLabel", background="#ffffff", foreground="#0f172a", font=("Segoe UI", 12, "bold"))
    style.configure("Body.TLabel", background="#ffffff", foreground="#475569", font=("Segoe UI", 9))
    style.configure("Launch.TButton", font=("Segoe UI", 9), padding=(14, 9))
    style.configure("Secondary.TButton", font=("Segoe UI", 8), padding=(8, 3))

    selected = {"app": None}

    wrapper = ttk.Frame(root, padding=18)
    wrapper.pack(fill="both", expand=True)
    header = ttk.Frame(wrapper, style="Card.TFrame", padding=16)
    header.pack(fill="x", pady=(0, 12))
    ttk.Label(header, text="MIX TEST PDFMATCH", style="Title.TLabel").pack(anchor="w")
    ttk.Label(
        header,
        text="PDF/AHU/motor karşılaştırması ve AHU test/devreye alma",
        style="Body.TLabel",
    ).pack(anchor="w", pady=(4, 0))

    card = ttk.Frame(wrapper, style="Card.TFrame", padding=16)
    card.pack(fill="both", expand=True)
    ttk.Label(card, text="Açmak istediğiniz programı seçin", style="Title.TLabel").pack(anchor="w", pady=(0, 12))

    def choose(name):
        selected["app"] = name
        root.destroy()

    ttk.Button(
        card,
        text="PDF MATCH — PDF / AHU / Motor karşılaştırma",
        style="Launch.TButton",
        command=lambda: choose("pdf"),
    ).pack(fill="x", pady=(0, 8))
    ttk.Button(
        card,
        text="TEST KONTROL — C600 / Fan / Damper / Sensör",
        style="Launch.TButton",
        command=lambda: choose("test"),
    ).pack(fill="x")

    footer = ttk.Frame(wrapper, style="Card.TFrame", padding=10)
    footer.pack(fill="x", pady=(10, 0))
    status_var = tk.StringVar(value=f"Sürüm {BUILD_VERSION}")
    ttk.Label(footer, textvariable=status_var, style="Body.TLabel").pack(side="left", fill="x", expand=True)
    ttk.Button(
        footer,
        text="Güncellemeleri kontrol et",
        style="Secondary.TButton",
        command=lambda: _check(root, True),
    ).pack(side="left", padx=(6, 4))
    version_label = ttk.Label(footer, text="", style="Body.TLabel")
    version_label.pack(side="left", padx=(4, 0))
    update_button = ttk.Button(
        footer,
        text="Güncelle",
        style="Secondary.TButton",
        command=lambda: _install(root),
        state="disabled",
    )
    update_button.pack(side="left", padx=(4, 0))
    root._mix_status_var = status_var
    root._mix_version_label = version_label
    root._mix_update_button = update_button
    root.after(
        800,
        lambda: check_for_update(
            root,
            manual=False,
            update_button=update_button,
            version_label=version_label,
            status_var=status_var,
        ),
    )
    root.mainloop()
    return selected["app"]


def main():
    # When either child application is closed, return to the choice screen.
    # The loop avoids growing the Python call stack across repeated switches.
    while True:
        selected = _show_home()
        if selected == "pdf":
            _run_pdf_match()
        elif selected == "test":
            _run_test_kontrol()
        else:
            return


if __name__ == "__main__":
    main()
