from __future__ import annotations

import tkinter as tk
from tkinter import ttk


def main() -> None:
    root = tk.Tk()
    root.title("AHU Match + Test Kontrol")
    root.geometry("760x500")
    root.minsize(620, 420)
    root.configure(bg="#f0f4f9")

    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass
    style.configure("TFrame", background="#f0f4f9")
    style.configure("Card.TFrame", background="#ffffff")
    style.configure("Title.TLabel", background="#ffffff", foreground="#0f172a", font=("Segoe UI", 14, "bold"))
    style.configure("Body.TLabel", background="#ffffff", foreground="#475569", font=("Segoe UI", 9))
    style.configure("Launch.TButton", font=("Segoe UI", 10), padding=(18, 12))

    wrapper = ttk.Frame(root, padding=24)
    wrapper.pack(fill="both", expand=True)
    header = ttk.Frame(wrapper, style="Card.TFrame", padding=20)
    header.pack(fill="x", pady=(0, 16))
    ttk.Label(header, text="AHU MATCH + TEST KONTROL", style="Title.TLabel").pack(anchor="w")
    ttk.Label(header, text="PDF motor karşılaştırması ve AHU test/devreye alma araçları", style="Body.TLabel").pack(anchor="w", pady=(6, 0))

    card = ttk.Frame(wrapper, style="Card.TFrame", padding=20)
    card.pack(fill="both", expand=True)
    ttk.Label(card, text="Bir modül seçin", style="Title.TLabel").pack(anchor="w", pady=(0, 14))

    def open_pdf_match() -> None:
        root.destroy()
        from desktop_grouped_app import GroupedApp
        GroupedApp().mainloop()

    def open_test_control() -> None:
        root.destroy()
        from test_kontrol.app import TestControlApp
        TestControlApp().mainloop()

    ttk.Button(card, text="PDF MATCH — PDF / AHU / Motor karşılaştırma", style="Launch.TButton", command=open_pdf_match).pack(fill="x", pady=(0, 10))
    ttk.Button(card, text="TEST KONTROL — C600 / Fan / Damper / Sensör", style="Launch.TButton", command=open_test_control).pack(fill="x")
    ttk.Label(wrapper, text="Her modül kendi işlevlerini korur; tek kurulum ve tek başlangıç ekranı kullanılır.", style="Body.TLabel").pack(anchor="w", pady=(12, 0))
    root.mainloop()


if __name__ == "__main__":
    main()
