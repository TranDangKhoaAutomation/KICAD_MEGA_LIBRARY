#!/usr/bin/env python3
"""
Consolidate 3D models from all sources into D:\\KICAD_MEGA_LIBRARY\\3dmodels\\<Vendor>\\.
Copies unique files; keeps existing files. Idempotent.
Copyright © Trần Đăng Khoa / TranDangKhoaAutomation.
"""
import os, shutil, hashlib, time

ROOT = r"D:\KICAD_MEGA_LIBRARY"
DEST = os.path.join(ROOT, "3dmodels")
LOG = os.path.join(ROOT, "logs", "3dmodel_changes.txt")

SOURCES = {
    "JLCPCB": [
        os.path.join(ROOT, "3dmodels", "JLCPCB.3dshapes"),
        os.path.join(ROOT, "Archived-Symbols-Footprints", "JLCPCB-Kicad-Footprints", "3dModels"),
        os.path.join(ROOT, "Sources", "JLCPCB-CDFER", "3dmodels", "JLCPCB.3dshapes"),
    ],
    "Espressif": [
        os.path.join(ROOT, "Sources", "Espressif", "3dmodels", "espressif.3dshapes"),
    ],
}

MODEL_EXTS = (".step", ".stp", ".wrl", ".stl")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    lines = ["=== 3D CONSOLIDATION %s ===" % time.strftime("%Y-%m-%d %H:%M:%S")]
    copied = skipped = 0
    for vendor, dirs in SOURCES.items():
        vendor_dir = os.path.join(DEST, vendor)
        os.makedirs(vendor_dir, exist_ok=True)
        for src_dir in dirs:
            if not os.path.isdir(src_dir):
                continue
            for fn in sorted(os.listdir(src_dir)):
                if not fn.lower().endswith(MODEL_EXTS):
                    continue
                src = os.path.join(src_dir, fn)
                if not os.path.isfile(src):
                    continue
                dst = os.path.join(vendor_dir, fn)
                if os.path.exists(dst):
                    skipped += 1
                    continue
                shutil.copy2(src, dst)
                copied += 1
                lines.append("[copy] %s" % os.path.relpath(dst, ROOT))
    lines.append("SUMMARY: copied=%d skipped=%d" % (copied, skipped))
    with open(LOG, "a", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
