#!/usr/bin/env python3
"""
createEsp32BoardLib.py
======================
Thêm các board dev ESP32 phổ biến (DevKit) vào thư viện Espressif.

Thư viện footprint : footprints/Espressif.pretty/
Thư viện symbol    : symbols/Espressif.kicad_sym

Copyright © Trần Đăng Khoa / TranDangKhoaAutomation.
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
LOGS_DIR = os.path.join(BASE, "logs")

# ---------------------------------------------------------------------------
# Board dev ESP32 phổ biến
# (tên symbol, value, nguồn footprint log, nguồn symbol log, mô tả)
# ---------------------------------------------------------------------------
BOARDS = [
    {
        "name": "ESP32-DevKit-V1-DOIT",
        "value": "ESP32 DevKit V1 (DOIT)",
        "mod_src": "esp32_38pin_mod.txt",
        "sym_src": "esp32_38pin_sym.txt",
        "desc": "ESP32 DevKit V1 (DOIT) - 38-pin development board with CP2102 USB-UART",
    },
    {
        "name": "NodeMCU-32S",
        "value": "NodeMCU-32S (AI-Thinker)",
        "mod_src": "nodemcu32s_mod.txt",
        "sym_src": "nodemcu32s_sym.txt",
        "desc": "NodeMCU-32S development board (AI-Thinker) - ESP32 WROOM-32, 38-pin",
    },
    {
        "name": "ESP32-S3-DevKitC-1",
        "value": "ESP32-S3-DevKitC-1",
        "mod_src": "s3devkitc_mod.txt",
        "sym_src": "s3devkitc_sym.txt",
        "desc": "Espressif ESP32-S3-DevKitC-1 development board (N8R2/N8R8)",
    },
    {
        "name": "NodeMCU-ESP8266",
        "value": "NodeMCU ESP8266 (Lolin V3)",
        "mod_src": "nodemcu8266_mod.txt",
        "sym_src": None,  # symbol tạo thủ công từ pinout chuẩn
        "manual_pins": [
            ("GPIO16", "1"), ("GPIO5", "2"), ("GPIO4", "3"), ("GPIO0", "4"),
            ("GPIO2", "5"), ("GPIO14", "6"), ("GPIO12", "7"), ("GPIO13", "8"),
            ("GPIO15", "9"), ("GPIO3/RX0", "10"), ("GPIO1/TX0", "11"),
            ("GND", "12"), ("GND", "13"), ("GPIO9", "14"), ("GPIO10", "15"),
            ("GPIO11", "16"), ("GPIO6", "17"), ("GPIO7", "18"), ("GPIO8", "19"),
            ("GPIO20", "20"), ("RST", "21"), ("3V3", "22"), ("GND", "23"),
            ("GND", "24"), ("ADC0", "25"), ("EN", "26"), ("3V3", "27"),
            ("GND", "28"), ("VIN", "29"), ("3V3", "30"),
        ],
        "desc": "NodeMCU ESP8266 (Lolin V3) development board - ESP-12E module, 30-pin",
    },
]


def load_file(path):
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def extract_pin_map(sym_text):
    """Trích (name, number) từ symbol nguồn."""
    pins = []
    pat = re.compile(r'\(name\s+"([^"]+)".*?\(number\s+"([^"]+)"', re.DOTALL)
    for m in pat.finditer(sym_text):
        name, num = m.groups()
        pins.append((name, num))
    return pins


def gen_board_symbol(name, value, footprint_ref, pins, desc):
    """Sinh symbol board dev ESP32 (KiCad 10 format)."""
    L = []
    L.append(f'\t(symbol "{name}"')
    L.append('\t\t(exclude_from_sim no)')
    L.append('\t\t(in_bom yes)')
    L.append('\t\t(on_board yes)')
    L.append('\t\t(in_pos_files yes)')
    L.append('\t\t(duplicate_pin_numbers_are_jumpers no)')
    # Reference
    L.append('\t\t(property "Reference" "U"')
    L.append('\t\t\t(at -30.48 40.64 0)')
    L.append('\t\t\t(show_name no)')
    L.append('\t\t\t(do_not_autoplace no)')
    L.append('\t\t\t(effects')
    L.append('\t\t\t\t(font')
    L.append('\t\t\t\t\t(size 1.27 1.27)')
    L.append('\t\t\t\t)')
    L.append('\t\t\t\t(justify left)')
    L.append('\t\t\t)')
    L.append('\t\t)')
    # Value
    L.append(f'\t\t(property "Value" "{value}"')
    L.append('\t\t\t(at -30.48 38.1 0)')
    L.append('\t\t\t(show_name no)')
    L.append('\t\t\t(do_not_autoplace no)')
    L.append('\t\t\t(effects')
    L.append('\t\t\t\t(font')
    L.append('\t\t\t\t\t(size 1.27 1.27)')
    L.append('\t\t\t\t)')
    L.append('\t\t\t\t(justify left)')
    L.append('\t\t\t)')
    L.append('\t\t)')
    # Footprint
    L.append(f'\t\t(property "Footprint" "{footprint_ref}"')
    L.append('\t\t\t(at 0 -50.8 0)')
    L.append('\t\t\t(show_name no)')
    L.append('\t\t\t(do_not_autoplace no)')
    L.append('\t\t\t(hide yes)')
    L.append('\t\t\t(effects')
    L.append('\t\t\t\t(font')
    L.append('\t\t\t\t\t(size 1.27 1.27)')
    L.append('\t\t\t\t)')
    L.append('\t\t\t)')
    L.append('\t\t)')
    # Datasheet
    L.append('\t\t(property "Datasheet" ""')
    L.append('\t\t\t(at 0 0 0)')
    L.append('\t\t\t(show_name no)')
    L.append('\t\t\t(do_not_autoplace no)')
    L.append('\t\t\t(hide yes)')
    L.append('\t\t\t(effects')
    L.append('\t\t\t\t(font')
    L.append('\t\t\t\t\t(size 1.27 1.27)')
    L.append('\t\t\t\t)')
    L.append('\t\t\t)')
    L.append('\t\t)')
    # Description
    L.append(f'\t\t(property "Description" "{desc}"')
    L.append('\t\t\t(at 0 0 0)')
    L.append('\t\t\t(show_name no)')
    L.append('\t\t\t(do_not_autoplace no)')
    L.append('\t\t\t(hide yes)')
    L.append('\t\t\t(effects')
    L.append('\t\t\t\t(font')
    L.append('\t\t\t\t\t(size 1.27 1.27)')
    L.append('\t\t\t\t)')
    L.append('\t\t\t)')
    L.append('\t\t)')
    # Graphic body
    L.append(f'\t\t(symbol "{name}_0_1"')
    L.append('\t\t\t(rectangle')
    L.append('\t\t\t\t(start -25.4 33.02)')
    L.append('\t\t\t\t(end 25.4 -33.02)')
    L.append('\t\t\t\t(stroke')
    L.append('\t\t\t\t\t(width 0)')
    L.append('\t\t\t\t\t(type default)')
    L.append('\t\t\t\t\t(color 0 0 0 0)')
    L.append('\t\t\t\t)')
    L.append('\t\t\t\t(fill (type background))')
    L.append('\t\t\t)')
    L.append('\t\t)')
    # Pins
    L.append(f'\t\t(symbol "{name}_1_1"')
    # sắp xếp: số lẻ bên trái, số chẵn bên phải (theo layout board dev)
    n_pins = len(pins)
    # vị trí: trái = số từ 1..n, phải = số từ n+1..2n (cho board 2 hàng)
    left_pins = []
    right_pins = []
    for idx, (pname, pnum) in enumerate(pins):
        try:
            n = int(pnum)
        except ValueError:
            n = idx + 1
        if n <= n_pins / 2:
            left_pins.append((pname, pnum))
        else:
            right_pins.append((pname, pnum))
    y_left = 30.0
    y_right = 30.0
    for pname, pnum in left_pins:
        L.append(f'\t\t\t(pin bidirectional line (at -30.48 {y_left:.2f} 0) (length 5.08)')
        L.append(f'\t\t\t\t(name "{pname}" (effects (font (size 1.27 1.27))))')
        L.append(f'\t\t\t\t(number "{pnum}" (effects (font (size 1.27 1.27))))')
        L.append('\t\t\t)')
        y_left -= 2.54
    for pname, pnum in right_pins:
        L.append(f'\t\t\t(pin bidirectional line (at 30.48 {y_right:.2f} 180) (length 5.08)')
        L.append(f'\t\t\t\t(name "{pname}" (effects (font (size 1.27 1.27))))')
        L.append(f'\t\t\t\t(number "{pnum}" (effects (font (size 1.27 1.27))))')
        L.append('\t\t\t)')
        y_right -= 2.54
    L.append('\t\t)')
    L.append('\t)')
    return "\n".join(L)


def clean_3d_models(txt):
    """Xóa model 3D trỏ đường dẫn broken (không dùng biến chuẩn)."""
    out = []
    lines = txt.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith("(model"):
            keep = ("${KISYS" in line or "${KICAD" in line
                    or "${KISYS3DMOD}" in line or "${KICAD6" in line)
            depth = 0
            j = i
            block_end = i
            while j < len(lines):
                depth += lines[j].count("(") - lines[j].count(")")
                block_end = j
                if depth <= 0 and j > i:
                    break
                j += 1
            if keep:
                out.extend(lines[i:block_end + 1])
            i = block_end + 1
        else:
            out.append(line)
            i += 1
    return "\n".join(out)


def add_footprint(mod_src, target_name):
    """Thêm footprint board dev vào Espressif.pretty."""
    txt = load_file(os.path.join(LOGS_DIR, mod_src))
    if not txt:
        print(f"  [SKIP] missing source {mod_src}")
        return False
    txt = txt.strip()
    # đổi tên bên trong nếu format cũ (module)
    if txt.startswith("(module "):
        m = re.match(r"\(module\s+[^\s(]+", txt)
        if m:
            txt = txt[m.end():]
        txt = re.sub(r"^\s*\(layer\s+F\.Cu\)\s*(\(tedit\s+[0-9A-F]+\))?\s*", "", txt)
        txt = ('(footprint "%s"\n\t(version 20240108)\n\t(generator pcbnew)\n'
               '\t(layer "F.Cu")' % target_name) + txt
    else:
        txt = re.sub(r'^\(footprint "[^"]*"', '(footprint "%s"' % target_name, txt)
    txt = clean_3d_models(txt)
    dst = os.path.join(FP_DIR, target_name + ".kicad_mod")
    with open(dst, "w", encoding="utf-8") as f:
        f.write(txt + "\n")
    print(f"  [OK] footprint {target_name}.kicad_mod")
    return True


def add_symbol(name, value, footprint_ref, sym_src, desc, manual_pins=None):
    """Tạo symbol board dev và trả về text."""
    pins = None
    if sym_src:
        sym_txt = load_file(os.path.join(LOGS_DIR, sym_src))
        if sym_txt:
            pins = extract_pin_map(sym_txt)
    if not pins and manual_pins:
        pins = manual_pins
    if not pins:
        print(f"  [SKIP] could not extract pinout for {name}")
        return None
    print(f"  {name}: {len(pins)} pins")
    return gen_board_symbol(name, value, footprint_ref, pins, desc)


def main():
    print("=== Build ESP32 Board Dev Library ===")
    # 1) Footprint DOIT DevKit V1
    print("[1] Footprints:")
    for b in BOARDS:
        if b["mod_src"]:
            add_footprint(b["mod_src"], b["name"])

    # 2) Symbol - chèn vào cuối Espressif.kicad_sym (trước dấu đóng)
    print("[2] Symbols:")
    with open(SYM_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    new_syms = []
    for b in BOARDS:
        if not (b.get("sym_src") or b.get("manual_pins")):
            print(f"  [SKIP] {b['name']} uses existing footprint (no new symbol)")
            continue
        # bỏ qua nếu symbol đã tồn tại
        if re.search(r'\(symbol "' + re.escape(b["name"]) + r'"\n', content):
            print(f"  [SKIP] {b['name']} already exists")
            continue
        sym = add_symbol(b["name"], b["value"],
                         f"Mega_Espressif:{b['name']}",
                         b.get("sym_src"), b["desc"],
                         b.get("manual_pins"))
        if sym:
            new_syms.append(sym)

    if new_syms:
        # xác định newline style
        nl = "\r\n" if "\r\n" in content else "\n"
        # chèn trước dấu đóng cuối cùng (tìm trên bản gốc, không rstrip)
        idx = content.rfind(nl + ")" + nl)
        if idx >= 0:
            insert = nl.join(new_syms) + nl
            content = content[:idx] + nl + insert + content[idx:]
            with open(SYM_FILE, "w", encoding="utf-8", newline="") as f:
                f.write(content)
            print(f"  [OK] added {len(new_syms)} symbols to Espressif.kicad_sym")
        else:
            print("  [FAIL] no insertion point found in Espressif.kicad_sym")
    print("=== Done ===")


if __name__ == "__main__":
    main()
