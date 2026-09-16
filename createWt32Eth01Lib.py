#!/usr/bin/env python3
"""
createWt32Eth01Lib.py
=====================
Thêm board dev WT32-ETH01 (ESP32 + Ethernet LAN8720A, wireless-tag)
vào thư viện Mega.

Nguồn: https://github.com/egnor/wt32-eth01

Thư viện footprint : footprints/Espressif.pretty/
Thư viện symbol    : symbols/Espressif.kicad_sym
Model 3D           : 3dmodels/Espressif/

Copyright © Trần Đăng Khoa.
"""

import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE = os.path.dirname(os.path.abspath(__file__))
FP_DIR = os.path.join(BASE, "footprints", "Espressif.pretty")
SYM_FILE = os.path.join(BASE, "symbols", "Espressif.kicad_sym")
MODEL_DIR = os.path.join(BASE, "3dmodels", "Espressif")
LOGS_DIR = os.path.join(BASE, "logs")
SRC_DIR = os.path.join(BASE, "Sources", "wt32-eth01")

NAME = "WT32-ETH01"


def load_file(path):
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def extract_symbol_block(sym_file_text):
    """Trích block (symbol ...) đúng cân bằng ngoặc từ file symbol nguồn."""
    start = sym_file_text.find('(symbol "%s"' % NAME)
    if start < 0:
        return None
    depth = 0
    i = start
    while i < len(sym_file_text):
        if sym_file_text[i] == "(":
            depth += 1
        elif sym_file_text[i] == ")":
            depth -= 1
            if depth == 0:
                break
        i += 1
    return sym_file_text[start:i + 1]


def add_3d_models():
    """Copy model 3D từ repo nguồn (nếu chưa có), chuẩn hoá tên theo quy ước
    thư viện: .step -> .STEP, .wrl giữ nguyên."""
    added = 0
    pairs = [(".step", ".STEP"), (".wrl", ".wrl")]
    for src_ext, dst_ext in pairs:
        src = os.path.join(SRC_DIR, NAME + src_ext)
        if not os.path.exists(src):
            continue
        dst_name = NAME + dst_ext
        dst = os.path.join(MODEL_DIR, dst_name)
        if os.path.exists(dst):
            print(f"  [SKIP] model {dst_name} already exists")
            continue
        # có thể đã tồn tại dưới tên khác (vd .step thường) -> bỏ qua, đổi tên
        with open(src, "rb") as fh, open(dst, "wb") as fh2:
            fh2.write(fh.read())
        print(f"  [OK] model {dst_name}")
        added += 1
    return added


def add_footprint():
    """Copy footprint vào Espressif.pretty và đảm bảo model 3D được tham chiếu."""
    src = os.path.join(SRC_DIR, "WT32-ETH01.pretty", NAME + ".kicad_mod")
    txt = load_file(src)
    if not txt:
        print("  [SKIP] missing source footprint")
        return False
    txt = txt.strip()
    dst = os.path.join(FP_DIR, NAME + ".kicad_mod")
    if os.path.exists(dst):
        print(f"  [SKIP] footprint {NAME}.kicad_mod already exists")
        return False
    # thêm model 3D nếu footprint nguồn chưa có
    model_block = None
    step_path = os.path.join(MODEL_DIR, NAME + ".STEP")
    if os.path.exists(step_path):
        model_block = ('  (model "${MEGA_KICAD_LIB}/3dmodels/Espressif/%s.STEP"\n'
                       '    (offset (xyz 0 0 0))\n'
                       '    (scale (xyz 1 1 1))\n'
                       '    (rotate (xyz 0 0 0))\n'
                       '  )' % NAME)
    if model_block and "(model" not in txt:
        # chèn trước dấu đóng cuối cùng
        idx = txt.rfind(")")
        txt = txt[:idx] + model_block + "\n" + txt[idx:]
    with open(dst, "w", encoding="utf-8") as f:
        f.write(txt + "\n")
    print(f"  [OK] footprint {NAME}.kicad_mod")
    return True


def add_symbol():
    """Chèn symbol WT32-ETH01 vào Espressif.kicad_sym (idempotent)."""
    sym_file_text = load_file(SYM_FILE)
    if not sym_file_text:
        print(f"  [FAIL] cannot read {SYM_FILE}")
        return False
    if re.search(r'\(symbol "' + re.escape(NAME) + r'"\n', sym_file_text):
        print(f"  [SKIP] {NAME} already in Espressif.kicad_sym")
        return False
    src_sym = load_file(os.path.join(LOGS_DIR, "WT32-ETH01.sym.txt"))
    if not src_sym:
        # fallback: upgrade từ nguồn
        upgraded = os.path.join(SRC_DIR, "WT32-ETH01.upgraded.kicad_sym")
        src_sym = extract_symbol_block(load_file(upgraded) or "")
    if not src_sym:
        print(f"  [FAIL] cannot find symbol block for {NAME}")
        return False
    nl = "\r\n" if "\r\n" in sym_file_text else "\n"
    idx = sym_file_text.rfind(nl + ")" + nl)
    if idx < 0:
        print("  [FAIL] no insertion point in Espressif.kicad_sym")
        return False
    insert = nl.join(src_sym.splitlines()) + nl
    content = sym_file_text[:idx] + nl + insert + sym_file_text[idx:]
    with open(SYM_FILE, "w", encoding="utf-8", newline="") as f:
        f.write(content)
    print(f"  [OK] added {NAME} symbol to Espressif.kicad_sym")
    return True


def main():
    print(f"=== Build {NAME} (WT32-ETH01) into Mega library ===")
    print("[1] 3D models:")
    add_3d_models()
    print("[2] Footprint:")
    add_footprint()
    print("[3] Symbol:")
    add_symbol()
    print("=== Done ===")


if __name__ == "__main__":
    main()
