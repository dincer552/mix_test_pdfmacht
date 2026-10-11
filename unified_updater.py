"""One checksum-verified updater shared by PDF Match and TEST KONTROL."""
from __future__ import annotations
import hashlib, json, os, shutil, subprocess, sys, tempfile, threading, urllib.request
from pathlib import Path
from tkinter import messagebox
from mix_meta import BUILD_SHA, BUILD_VERSION

REPO = "dincer552/mix_test_pdfmacht"
RELEASE_API = f"https://api.github.com/repos/{REPO}/releases/tags/latest"
EXE_ASSET = "Mix_Test_PDFMatch_latest.exe"
HASH_ASSET = "Mix_Test_PDFMatch_latest.sha256"
USER_AGENT = "Mix-Test-PDFMatch-Updater/1.0"

def _request_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=12) as response:
        return json.loads(response.read().decode("utf-8"))

def latest_release():
    payload = _request_json(RELEASE_API)
    assets = {item.get("name"): item.get("browser_download_url") for item in payload.get("assets", [])}
    metadata = {}
    for line in (payload.get("body") or "").splitlines():
        key, sep, value = line.partition(":")
        if sep:
            metadata[key.strip().lower()] = value.strip()
    version = metadata.get("version") or payload.get("name") or "latest"
    sha = metadata.get("build") or ""
    return {
        "version": version, "build_sha": sha, "download_url": assets.get(EXE_ASSET),
        "hash_url": assets.get(HASH_ASSET),
        "available": bool(assets.get(EXE_ASSET) and sha and sha.lower() != BUILD_SHA.lower()),
    }

def check_for_update(parent, manual=False, update_button=None, version_label=None, status_var=None):
    if update_button is not None:
        try: update_button.configure(state="disabled", text="Kontrol ediliyor…")
        except Exception: pass
    def worker():
        try: info, error = latest_release(), None
        except Exception as exc: info, error = None, str(exc)
        def apply_result():
            if update_button is not None:
                try: update_button.configure(text="Güncelle", state="normal" if info and info.get("available") else "disabled")
                except Exception: pass
            if version_label is not None:
                try: version_label.configure(text=info.get("version", "") if info and info.get("available") else "")
                except Exception: pass
            if status_var is not None:
                if error: status_var.set("Güncelleme kontrol edilemedi")
                elif info and info.get("available"): status_var.set(f"Yeni sürüm bulundu: {info['version']}")
                else: status_var.set(f"Güncel — {BUILD_VERSION}")
            if manual:
                if error: messagebox.showwarning("Güncelleme", "Güncelleme bilgisi alınamadı.\n\n" + error, parent=parent)
                elif info and info.get("available"): messagebox.showinfo("Güncelleme", f"Yeni ortak sürüm: {info['version']}\nKurmak için Güncelle düğmesine basın.", parent=parent)
                else: messagebox.showinfo("Güncelleme", f"Programınız güncel.\nSürüm: {BUILD_VERSION}", parent=parent)
        try: parent.after(0, apply_result)
        except Exception: pass
    threading.Thread(target=worker, name="mix-update-check", daemon=True).start()

def install_update(parent, update_button=None, status_var=None):
    if not getattr(sys, "frozen", False):
        messagebox.showinfo("Güncelleme", "Güncelleme yalnızca paketlenmiş Windows EXE üzerinden uygulanabilir.", parent=parent)
        return
    try: info = latest_release()
    except Exception as exc:
        messagebox.showerror("Güncelleme", "Sürüm bilgisi alınamadı.\n\n" + str(exc), parent=parent)
        return
    if not info.get("available"):
        messagebox.showinfo("Güncelleme", f"Yeni sürüm bulunamadı.\nSürüm: {BUILD_VERSION}", parent=parent)
        return
    if not info.get("hash_url"):
        messagebox.showerror("Güncelleme", "SHA-256 dosyası bulunamadı.", parent=parent)
        return
    if not messagebox.askyesno("Güncelleme", f"{info['version']} indirilsin ve program yeniden başlatılsın mı?", parent=parent):
        return
    if update_button is not None:
        try: update_button.configure(state="disabled", text="İndiriliyor…")
        except Exception: pass
    if status_var is not None:
        try: status_var.set("Yeni sürüm indiriliyor…")
        except Exception: pass
    def worker():
        temp = Path(tempfile.gettempdir())
        pid = os.getpid()
        exe = temp / f"Mix_Test_PDFMatch_update_{pid}.exe"
        hash_file = temp / f"Mix_Test_PDFMatch_update_{pid}.sha256"
        try:
            for url, destination in ((info["download_url"], exe), (info["hash_url"], hash_file)):
                req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
                with urllib.request.urlopen(req, timeout=120) as source, open(destination, "wb") as output:
                    shutil.copyfileobj(source, output)
            expected = hash_file.read_text(encoding="utf-8").strip().split()[0].lower()
            actual = hashlib.sha256(exe.read_bytes()).hexdigest().lower()
            if actual != expected: raise ValueError("İndirilen EXE'nin SHA-256 doğrulaması başarısız.")
            target = Path(sys.executable).resolve()
            ps1 = temp / f"mix_update_{pid}.ps1"
            quote = lambda value: "'" + str(value).replace("'", "''") + "'"
            script = f"$ErrorActionPreference='Stop'\n$processId={pid}\nwhile (Get-Process -Id $processId -ErrorAction SilentlyContinue) {{ Start-Sleep -Milliseconds 500 }}\nCopy-Item -LiteralPath {quote(exe)} -Destination {quote(target)} -Force\nStart-Process -FilePath {quote(target)}\nRemove-Item -LiteralPath $PSCommandPath -Force\n"
            ps1.write_text("\ufeff" + script, encoding="utf-8")
            flags = getattr(subprocess, "CREATE_NO_WINDOW", 0) | getattr(subprocess, "DETACHED_PROCESS", 0)
            subprocess.Popen(["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-WindowStyle", "Hidden", "-File", str(ps1)], creationflags=flags, close_fds=True)
            try: parent.after(0, parent.destroy)
            except Exception: pass
        except Exception as exc:
            try:
                parent.after(0, lambda err=str(exc): messagebox.showerror("Güncelleme", "Güncelleme tamamlanamadı.\n\n" + err, parent=parent))
                if update_button is not None: parent.after(0, lambda: update_button.configure(text="Güncelle", state="normal"))
            except Exception: pass
    threading.Thread(target=worker, name="mix-update-download", daemon=True).start()
