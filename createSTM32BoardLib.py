#!/usr/bin/env python3
"""
createSTM32BoardLib.py
======================
Tạo thư viện footprint + symbol cho các board dev STM32 trong hệ thống Mega Library.

Thư viện footprint : footprints/STM32_Board.pretty/
Thư viện symbol    : symbols/STM32_Board.kicad_sym

Cấu trúc:
- Board "pill" (Blue/Black Pill): footprint + symbol có pinout header thực tế.
- Board Nucleo/Discovery/Core: footprint chuẩn + symbol MCU STM32 chính thức
  (trong symbols/MCU_ST_STM32*.kicad_sym).

Copyright © Trần Đăng Khoa.
"""

import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
FP_DIR = os.path.join(BASE, "footprints", "STM32_Board.pretty")
SYM_FILE = os.path.join(BASE, "symbols", "STM32_Board.kicad_sym")
SYM_DIR = os.path.join(BASE, "symbols")
LOGS_DIR = os.path.join(BASE, "logs")

os.makedirs(FP_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# 1. FOOTPRINTS
# ---------------------------------------------------------------------------

# (nguồn log, tên file trong thư viện, danh sách board dùng chung)
FP_SOURCES = [
    ("bluepill_mod.txt", "BluePill_STM32F103.kicad_mod",
     ["STM32F103C8T6 Blue Pill", "STM32F103CBT6 Blue Pill"]),
    ("blackpill_mod.txt", "BlackPill_STM32F4.kicad_mod",
     ["STM32F401CCU6 Black Pill", "STM32F411CEU6 Black Pill",
      "WeAct STM32F401 Black Pill", "WeAct STM32F411 Black Pill"]),
    ("nucleo64_mod.txt", "Nucleo_64.kicad_mod",
     ["NUCLEO-F030R8", "NUCLEO-F103RB", "NUCLEO-F401RE", "NUCLEO-F411RE",
      "NUCLEO-F446RE", "NUCLEO-G431RB", "NUCLEO-G474RE", "NUCLEO-L476RG"]),
    ("nucleo144_mod.txt", "Nucleo_144.kicad_mod",
     ["NUCLEO-F446ZE", "NUCLEO-F767ZI", "NUCLEO-H743ZI", "NUCLEO-H753ZI"]),
    ("nucleo32_mod.txt", "Nucleo_32.kicad_mod",
     ["NUCLEO-32", "NUCLEO-L432KC"]),
    ("f4disco_mod.txt", "STM32F4DISCOVERY.kicad_mod",
     ["STM32F4DISCOVERY", "STM32F407G-DISC1"]),
]

# Core board footprint: (footprint nguồn log, tên trong thư viện, board)
FP_CORE = [
    ("lqfp144.txt", "LQFP-144_20x20mm_P0.5mm.kicad_mod",
     ["STM32F407ZGT6 Core Board"]),
]

# Copy base footprint từ digikey (format chuẩn) cho core boards
FP_BASE_COPY = [
    ("digikey-footprints.pretty/LQFP-100_14x14mm.kicad_mod", "LQFP-100_14x14mm.kicad_mod",
     ["STM32F407VET6 Core Board", "STM32F407VGT6 Core Board",
      "STM32H743VIT6 Core Board", "STM32H750VBT6 Core Board"]),
    ("digikey-footprints.pretty/LQFP-64_10x10mm.kicad_mod", "LQFP-64_10x10mm.kicad_mod",
     ["STM32F405RGT6 Core Board"]),
]


def normalize_footprint(txt, name):
    """Chuẩn hoá footprint sang format KiCad 10, đổi tên bên trong khớp file."""
    txt = txt.strip()
    if txt.startswith("(module "):
        m = re.match(r"\(module\s+[^\s(]+", txt)
        if m:
            txt = txt[m.end():]
        # bỏ (layer F.Cu) (tedit ...) cũ nếu có
        txt = re.sub(r"^\s*\(layer\s+F\.Cu\)\s*(\(tedit\s+[0-9A-F]+\))?\s*", "", txt)
        txt = ('(footprint "%s"\n\t(version 20240108)\n\t(generator pcbnew)\n'
               '\t(layer "F.Cu")' % name) + txt
    else:
        # format mới: đổi tên bên trong cho khớp
        txt = re.sub(r'^\(footprint "[^"]*"', '(footprint "%s"' % name, txt)
    return txt


def clean_3d_models(txt):
    """Xóa model 3D trỏ đường dẫn broken (không dùng biến chuẩn).
    Giữ model dùng ${...} biến chuẩn (KISYS/KICAD6/KICAD7/KICAD8)."""
    out = []
    lines = txt.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith("(model"):
            # kiểm tra có biến chuẩn không
            keep = ("${KISYS" in line or "${KICAD" in line or "${KICAD6" in line
                    or "${KICAD7" in line or "${KICAD8" in line
                    or "${KISYS3DMOD}" in line)
            # đóng khối model: tìm dòng đóng ngoặc cân bằng
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


def build_footprints():
    created = {}
    for logfile, fname, boards in FP_SOURCES:
        src = os.path.join(LOGS_DIR, logfile)
        if not os.path.exists(src):
            print(f"  [SKIP] thiếu nguồn {logfile}")
            continue
        with open(src, "r", encoding="utf-8", errors="replace") as f:
            txt = f.read()
        libname = fname.replace(".kicad_mod", "")
        txt = normalize_footprint(txt, libname)
        txt = clean_3d_models(txt)
        dst = os.path.join(FP_DIR, fname)
        with open(dst, "w", encoding="utf-8") as f:
            f.write(txt + "\n")
        created[libname] = fname
        for b in boards:
            created[b] = fname
        print(f"  [OK] {fname} <- {logfile}")
    # Core board footprints từ log LQFP
    for logfile, fname, boards in FP_CORE:
        src = os.path.join(LOGS_DIR, logfile)
        if not os.path.exists(src):
            print(f"  [SKIP] thiếu nguồn {logfile}")
            continue
        with open(src, "r", encoding="utf-8", errors="replace") as f:
            txt = f.read()
        libname = fname.replace(".kicad_mod", "")
        txt = normalize_footprint(txt, libname)
        txt = clean_3d_models(txt)
        dst = os.path.join(FP_DIR, fname)
        with open(dst, "w", encoding="utf-8") as f:
            f.write(txt + "\n")
        created[libname] = fname
        for b in boards:
            created[b] = fname
        print(f"  [OK] {fname} <- {logfile}")
    # Copy base footprint từ digikey
    for src_rel, fname, boards in FP_BASE_COPY:
        src = os.path.join(BASE, "footprints", src_rel)
        if not os.path.exists(src):
            print(f"  [SKIP] thiếu nguồn {src_rel}")
            continue
        with open(src, "r", encoding="utf-8", errors="replace") as f:
            txt = f.read()
        libname = fname.replace(".kicad_mod", "")
        txt = normalize_footprint(txt, libname)
        txt = clean_3d_models(txt)
        dst = os.path.join(FP_DIR, fname)
        with open(dst, "w", encoding="utf-8") as f:
            f.write(txt + "\n")
        created[libname] = fname
        for b in boards:
            created[b] = fname
        print(f"  [OK] {fname} <- {src_rel}")
    return created


# ---------------------------------------------------------------------------
# 2. SYMBOLS
# ---------------------------------------------------------------------------

def load_symbol_pins(path):
    """Trích pin (name, number, type, x, y) từ symbol board dev có sẵn."""
    pins = []
    if not os.path.exists(path):
        return pins
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
    pat = re.compile(
        r'\(pin\s+(\w+)\s+\w+.*?\(at\s+([-\d.]+)\s+([-\d.]+)\s+(\d+)\).*?'
        r'\(name\s+"([^"]+)".*?\(number\s+"([^"]+)"', re.DOTALL)
    for m in pat.finditer(content):
        etype, x, y, rot, name, num = m.groups()
        pins.append((name, num, etype, float(x), float(y)))
    return pins


def gen_symbol(name, value, footprint, pins, desc=""):
    """Sinh symbol KiCad 10 cho board dev với pinout cho trước."""
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
    L.append(f'\t\t(property "Footprint" "{footprint}"')
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
    # Pins - sắp xếp theo vị trí trái/phải từ dữ liệu nguồn
    L.append(f'\t\t(symbol "{name}_1_1"')
    left_pins = [p for p in pins if p[3] < 0]
    right_pins = [p for p in pins if p[3] >= 0]
    # sắp xếp theo y giảm dần
    left_pins.sort(key=lambda p: -p[4])
    right_pins.sort(key=lambda p: -p[4])
    for side, side_pins, orient in (("L", left_pins, 0), ("R", right_pins, 180)):
        y = 30.0
        for (nm, num, etype, _, _) in side_pins:
            px = -30.48 if side == "L" else 30.48
            etype_kicad = {"B": "bidirectional", "I": "input", "O": "output",
                           "W": "power_in", "w": "power_out", "P": "passive"}.get(etype, "bidirectional")
            L.append(f'\t\t\t(pin {etype_kicad} line (at {px:.2f} {y:.2f} {orient}) (length 5.08)')
            L.append(f'\t\t\t\t(name "{nm}" (effects (font (size 1.27 1.27))))')
            L.append(f'\t\t\t\t(number "{num}" (effects (font (size 1.27 1.27))))')
            L.append('\t\t\t)')
            y -= 2.54
    L.append('\t\t)')
    L.append('\t)')
    return "\n".join(L)


def load_mcu_pins(lib, defname):
    """Trích pinout từ symbol MCU trong lib kicad_sym (KiCad 10 format)."""
    pins = []
    path = os.path.join(SYM_DIR, lib)
    if not os.path.exists(path):
        return pins
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
    # Theo dõi alias (extends ...) — lấy pinout từ symbol gốc
    seen = set()
    cur = defname
    while cur not in seen:
        seen.add(cur)
        start = content.find('(symbol "' + cur + '"')
        if start < 0:
            return pins
        # tìm điểm kết thúc: dòng ")" cấp 0 sau khối
        depth = 0
        end = len(content)
        i = start
        while i < len(content):
            c = content[i]
            if c == '(':
                depth += 1
            elif c == ')':
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
            i += 1
        seg = content[start:end]
        # nếu là alias, đổi sang symbol gốc
        ext = re.search(r'\(extends "([^"]+)"', seg)
        if ext:
            cur = ext.group(1)
            continue
        break
    else:
        return pins
    # Trích từng khối (pin ... (name ...) (number ...)) bằng stack balance
    for m in re.finditer(r'\(pin\s+', seg):
        start_pin = m.start()
        # tìm đóng ngoặc cân bằng
        d = 0
        j = start_pin
        while j < len(seg):
            if seg[j] == '(':
                d += 1
            elif seg[j] == ')':
                d -= 1
                if d == 0:
                    break
            j += 1
        pin_seg = seg[start_pin:j + 1]
        nm = re.search(r'\(name\s+"([^"]+)"', pin_seg)
        num = re.search(r'\(number\s+"([^"]+)"', pin_seg)
        et = re.search(r'\(pin\s+(\w+)', pin_seg)
        at = re.search(r'\(at\s+([-\d.]+)\s+([-\d.]+)', pin_seg)
        if nm and num and at:
            pins.append((nm.group(1), num.group(1),
                         et.group(1) if et else "B",
                         float(at.group(1)), float(at.group(2))))
    return pins


# Board map: tên board -> (symbol MCU def, lib file)
# (G431/G474/H747/U5 không có trong KiCad official, dùng MCU tương đương gần nhất)
BOARD_MCU = {
    "STM32F103C8T6 Mini": ("STM32F103C8Tx", "MCU_ST_STM32F1.kicad_sym"),
    "STM32F407VET6 Core Board": ("STM32F407VETx", "MCU_ST_STM32F4.kicad_sym"),
    "STM32F407ZGT6 Core Board": ("STM32F407ZGTx", "MCU_ST_STM32F4.kicad_sym"),
    "STM32F407VGT6 Core Board": ("STM32F407VGTx", "MCU_ST_STM32F4.kicad_sym"),
    "STM32F405RGT6 Core Board": ("STM32F405RGTx", "MCU_ST_STM32F4.kicad_sym"),
    "STM32H743VIT6 Core Board": ("STM32H743VITx", "MCU_ST_STM32H7.kicad_sym"),
    "STM32H750VBT6 Core Board": ("STM32H750VBTx", "MCU_ST_STM32H7.kicad_sym"),
    "Maple Mini STM32F103": ("STM32F103CBUx", "MCU_ST_STM32F1.kicad_sym"),
    "STM32F0DISCOVERY": ("STM32F051R8Tx", "MCU_ST_STM32F0.kicad_sym"),
    "STM32F3DISCOVERY": ("STM32F303VCTx", "MCU_ST_STM32F3.kicad_sym"),
    "STM32F4DISCOVERY": ("STM32F407VGTx", "MCU_ST_STM32F4.kicad_sym"),
    "STM32F407G-DISC1": ("STM32F407VGTx", "MCU_ST_STM32F4.kicad_sym"),
    "STM32F401C-DISCO": ("STM32F401CCUx", "MCU_ST_STM32F4.kicad_sym"),
    "STM32F411E-DISCO": ("STM32F411CEUx", "MCU_ST_STM32F4.kicad_sym"),
    "STM32F429I-DISCO": ("STM32F429ZITx", "MCU_ST_STM32F4.kicad_sym"),
    "STM32F469I-DISCO": ("STM32F469NIHx", "MCU_ST_STM32F4.kicad_sym"),
    "STM32F746G-DISCO": ("STM32F746NGHx", "MCU_ST_STM32F7.kicad_sym"),
    "STM32F769I-DISCO": ("STM32F769NIHx", "MCU_ST_STM32F7.kicad_sym"),
    "STM32H747I-DISCO": ("STM32H743VITx", "MCU_ST_STM32H7.kicad_sym"),
    "STM32L476G-DISCO": ("STM32L476VGTx", "MCU_ST_STM32L4.kicad_sym"),
    "STM32U5G9J-DK": ("STM32L4R5AGIx", "MCU_ST_STM32L4+.kicad_sym"),
    "NUCLEO-F030R8": ("STM32F030R8Tx", "MCU_ST_STM32F0.kicad_sym"),
    "NUCLEO-F103RB": ("STM32F103R8Tx", "MCU_ST_STM32F1.kicad_sym"),
    "NUCLEO-F401RE": ("STM32F401RETx", "MCU_ST_STM32F4.kicad_sym"),
    "NUCLEO-F411RE": ("STM32F411RETx", "MCU_ST_STM32F4.kicad_sym"),
    "NUCLEO-F446RE": ("STM32F446RETx", "MCU_ST_STM32F4.kicad_sym"),
    "NUCLEO-F446ZE": ("STM32F446ZETx", "MCU_ST_STM32F4.kicad_sym"),
    "NUCLEO-F767ZI": ("STM32F767ZITx", "MCU_ST_STM32F7.kicad_sym"),
    "NUCLEO-G431RB": ("STM32L432KCUx", "MCU_ST_STM32L4.kicad_sym"),
    "NUCLEO-G474RE": ("STM32L476RGTx", "MCU_ST_STM32L4.kicad_sym"),
    "NUCLEO-H743ZI": ("STM32H743ZITx", "MCU_ST_STM32H7.kicad_sym"),
    "NUCLEO-H753ZI": ("STM32H753ZITx", "MCU_ST_STM32H7.kicad_sym"),
    "NUCLEO-L432KC": ("STM32L432KCUx", "MCU_ST_STM32L4.kicad_sym"),
    "NUCLEO-L476RG": ("STM32L476RGTx", "MCU_ST_STM32L4.kicad_sym"),
}

# Footprint tương ứng cho từng board (dùng chung)
BOARD_FP = {
    "STM32F103C8T6 Mini": "Mega_STM32_Board:BluePill_STM32F103",
    "STM32F407VET6 Core Board": "Mega_STM32_Board:LQFP-100_14x14mm",
    "STM32F407ZGT6 Core Board": "Mega_STM32_Board:LQFP-144_20x20mm_P0.5mm",
    "STM32F407VGT6 Core Board": "Mega_STM32_Board:LQFP-100_14x14mm",
    "STM32F405RGT6 Core Board": "Mega_STM32_Board:LQFP-64_10x10mm",
    "STM32H743VIT6 Core Board": "Mega_STM32_Board:LQFP-100_14x14mm",
    "STM32H750VBT6 Core Board": "Mega_STM32_Board:LQFP-100_14x14mm",
    "Maple Mini STM32F103": "Mega_STM32_Board:BluePill_STM32F103",
    "STM32F0DISCOVERY": "Mega_STM32_Board:STM32F4DISCOVERY",
    "STM32F3DISCOVERY": "Mega_STM32_Board:STM32F4DISCOVERY",
    "STM32F4DISCOVERY": "Mega_STM32_Board:STM32F4DISCOVERY",
    "STM32F407G-DISC1": "Mega_STM32_Board:STM32F4DISCOVERY",
    "STM32F401C-DISCO": "Mega_STM32_Board:STM32F4DISCOVERY",
    "STM32F411E-DISCO": "Mega_STM32_Board:STM32F4DISCOVERY",
    "STM32F429I-DISCO": "Mega_STM32_Board:STM32F4DISCOVERY",
    "STM32F469I-DISCO": "Mega_STM32_Board:STM32F4DISCOVERY",
    "STM32F746G-DISCO": "Mega_STM32_Board:STM32F4DISCOVERY",
    "STM32F769I-DISCO": "Mega_STM32_Board:STM32F4DISCOVERY",
    "STM32H747I-DISCO": "Mega_STM32_Board:STM32F4DISCOVERY",
    "STM32L476G-DISCO": "Mega_STM32_Board:STM32F4DISCOVERY",
    "STM32U5G9J-DK": "Mega_STM32_Board:STM32F4DISCOVERY",
    "NUCLEO-F030R8": "Mega_STM32_Board:Nucleo_64",
    "NUCLEO-F103RB": "Mega_STM32_Board:Nucleo_64",
    "NUCLEO-F401RE": "Mega_STM32_Board:Nucleo_64",
    "NUCLEO-F411RE": "Mega_STM32_Board:Nucleo_64",
    "NUCLEO-F446RE": "Mega_STM32_Board:Nucleo_64",
    "NUCLEO-F446ZE": "Mega_STM32_Board:Nucleo_144",
    "NUCLEO-F767ZI": "Mega_STM32_Board:Nucleo_144",
    "NUCLEO-G431RB": "Mega_STM32_Board:Nucleo_64",
    "NUCLEO-G474RE": "Mega_STM32_Board:Nucleo_64",
    "NUCLEO-H743ZI": "Mega_STM32_Board:Nucleo_144",
    "NUCLEO-H753ZI": "Mega_STM32_Board:Nucleo_144",
    "NUCLEO-L432KC": "Mega_STM32_Board:Nucleo_32",
    "NUCLEO-L476RG": "Mega_STM32_Board:Nucleo_64",
}


def build_symbols():
    bluepins = load_symbol_pins(os.path.join(LOGS_DIR, "bluepill_sym.txt"))
    blackpins = load_symbol_pins(os.path.join(LOGS_DIR, "blackpill_sym.txt"))
    print(f"  Pinout: BluePill={len(bluepins)}, BlackPill={len(blackpins)}")

    symbols = []
    # Blue Pill (pinout header 2x20 = 40 pin)
    symbols.append(gen_symbol(
        "STM32F103C8T6_BluePill", "STM32F103C8T6 Blue Pill",
        "Mega_STM32_Board:BluePill_STM32F103", bluepins,
        "STM32 Blue Pill development board (STM32F103C8T6)"))
    symbols.append(gen_symbol(
        "STM32F103CBT6_BluePill", "STM32F103CBT6 Blue Pill",
        "Mega_STM32_Board:BluePill_STM32F103", bluepins,
        "STM32 Blue Pill development board (STM32F103CBT6)"))
    # Black Pill (pinout 2x20 = 40 pin)
    symbols.append(gen_symbol(
        "STM32F401CCU6_BlackPill", "STM32F401CCU6 Black Pill",
        "Mega_STM32_Board:BlackPill_STM32F4", blackpins,
        "WeAct Black Pill development board (STM32F401CCU6)"))
    symbols.append(gen_symbol(
        "STM32F411CEU6_BlackPill", "STM32F411CEU6 Black Pill",
        "Mega_STM32_Board:BlackPill_STM32F4", blackpins,
        "WeAct Black Pill development board (STM32F411CEU6)"))
    symbols.append(gen_symbol(
        "WeAct_STM32F401_BlackPill", "WeAct STM32F401 Black Pill",
        "Mega_STM32_Board:BlackPill_STM32F4", blackpins,
        "WeAct STM32F401 Black Pill development board"))
    symbols.append(gen_symbol(
        "WeAct_STM32F411_BlackPill", "WeAct STM32F411 Black Pill",
        "Mega_STM32_Board:BlackPill_STM32F4", blackpins,
        "WeAct STM32F411 Black Pill development board"))

    # Board còn lại: trích pinout từ symbol MCU chính thức
    for board, (defname, lib) in BOARD_MCU.items():
        pins = load_mcu_pins(lib, defname)
        fp = BOARD_FP.get(board, "Mega_STM32_Board:Nucleo_64")
        symname = board.replace(" ", "_").replace("-", "_")
        if pins:
            symbols.append(gen_symbol(symname, board, fp, pins,
                f"{board} development board"))
            print(f"    {board}: {len(pins)} pins (MCU {defname})")
        else:
            print(f"    {board}: KHÔNG có pinout MCU {defname}")

    with open(SYM_FILE, "w", encoding="utf-8") as f:
        f.write('(kicad_symbol_lib\n\t(version 20251024)\n\t(generator "kicad_symbol_editor")\n\t(generator_version "10.0")\n')
        f.write("\n".join(symbols))
        f.write("\n)\n")
    print(f"  [OK] symbols/STM32_Board.kicad_sym ({len(symbols)} symbols)")


def main():
    print("=== Build STM32 Board Library ===")
    print("[1/2] Footprints:")
    build_footprints()
    print("[2/2] Symbols:")
    build_symbols()
    print("=== Done ===")


if __name__ == "__main__":
    main()
