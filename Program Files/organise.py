#!/usr/bin/env python3
"""
SmartAutoSort – auto-installer edition
• Installs its own Python dependencies (python-docx, PyPDF2) the first time it is run
• Then runs the normal SmartAutoSort logic
"""

# ───────────────────────────── 1.  BOOTSTRAP ─────────────────────────────
import subprocess, sys, importlib.util, os, time

def _is_installed(pkg: str) -> bool:
    return importlib.util.find_spec(pkg) is not None

def _install(pkg: str):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
    except subprocess.CalledProcessError:
        print(f"❌  Could not install {pkg}. Please install it manually.")
        sys.exit(1)

_required = ["python-docx", "PyPDF2"]
for _pkg in _required:
    if not _is_installed(_pkg.split("-")[0]):          # "python-docx" → "python"
        print(f"📦  Installing {_pkg} …")
        _install(_pkg)

# ───────────────────────────── 2.  MAIN PROGRAM ──────────────────────────
import logging, shutil
from pathlib import Path
from typing import List, Tuple
from datetime import datetime

try:
    from docx import Document        # noqa: E402  (import after install)
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

try:
    import PyPDF2                    # noqa: E402
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

logging.basicConfig(level=logging.WARNING,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class SmartAutoSort:
    def __init__(self):
        self.script_dir  = Path(__file__).parent.resolve()
        self.script_name = Path(__file__).name
        self.categories  = {
            "Images"      : { "extensions": [".jpg",".jpeg",".png",".gif",".bmp",
                                              ".tiff",".tif",".svg",".webp",".ico",
                                              ".raw",".cr2",".nef",".arw"],
                              "folder"    : "Images" },
            "Videos"      : { "extensions": [".mp4",".avi",".mkv",".mov",".wmv",
                                              ".flv",".webm",".m4v",".mpg",".mpeg",
                                              ".3gp",".f4v"],
                              "folder"    : "Videos" },
            "Audio"       : { "extensions": [".mp3",".wav",".flac",".aac",".ogg",
                                              ".wma",".m4a",".opus",".aiff",".au"],
                              "folder"    : "Audio" },
            "Documents"   : { "extensions": [".pdf",".doc",".docx",".txt",".rtf",
                                              ".odt",".pages",".tex",".wpd"],
                              "folder"    : "Documents" },
            "Archives"    : { "extensions": [".zip",".rar",".7z",".tar",".gz",".bz2",
                                              ".xz",".tar.gz",".tar.bz2"],
                              "folder"    : "Archives" },
            "Applications": { "extensions": [".exe",".msi",".deb",".dmg",".pkg",
                                              ".app",".apk"],
                              "folder"    : "Applications" },
        }

    # ------------- helper methods -------------
    def categorize_by_extension(self, f: Path) -> str:
        ext = f.suffix.lower()
        for cat, info in self.categories.items():
            if ext in info["extensions"]:
                return cat
        return "Unsorted"

    @staticmethod
    def file_date(f: Path) -> datetime:
        try:
            return datetime.fromtimestamp(os.path.getmtime(f))
        except Exception:
            return datetime.now()

    @staticmethod
    def monthly_folder(dt: datetime) -> str:
        return dt.strftime("%Y-%m")

    @staticmethod
    def uniq_name(target_dir: Path, name: str) -> str:
        base, ext = Path(name).stem, Path(name).suffix
        i = 1
        while (target_dir / name).exists():
            name = f"{base}_{i}{ext}"
            i += 1
        return name

    # ------------- core work -------------
    def move(self, src: Path, cat: str, dt: datetime) -> bool:
        folder = self.categories.get(cat, {}).get("folder", "Unsorted")
        dest_dir = self.script_dir / folder / self.monthly_folder(dt)
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / self.uniq_name(dest_dir, src.name)
        try:
            shutil.move(str(src), dest)
            print(f"✓ {src.name} → {folder}/{dest.parent.name}/")
            return True
        except Exception as e:
            print(f"✗ {src.name}: {e}")
            return False

    # ------------- public API -------------
    def run(self):
        print(f"🚀  SmartAutoSort – {self.script_dir}")
        files = [f for f in self.script_dir.iterdir()
                 if f.is_file() and f.name != self.script_name and not f.name.startswith('.')]
        if not files:
            print("✅  No files to organize."); return

        plans: List[Tuple[Path,str,datetime]] = []
        for f in files:
            cat = self.categorize_by_extension(f)
            plans.append((f, cat, self.file_date(f)))

        print(f"📊  Found {len(plans)} files.")
        moved = sum(self.move(f, c, d) for f,c,d in plans)
        print(f"\n✅  Done. Moved {moved}/{len(plans)} files.")
        time.sleep(2)                      # brief pause before exit

# ------------- script entry point -------------
if __name__ == "__main__":
    SmartAutoSort().run()
