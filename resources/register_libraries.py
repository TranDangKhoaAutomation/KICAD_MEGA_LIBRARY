#!/usr/bin/env python3
"""
Register Mega_* symbol and footprint libraries in KiCad's global tables.
Keeps existing entries, adds only new valid ones, writes atomically.
Copyright © Trần Đăng Khoa.
"""
import os, re, sys

ROOT = r"D:\KICAD_MEGA_LIBRARY"
CFG = r"C:\Users\trand\AppData\Roaming\kicad\10.0"
SYM_TABLE = os.path.join(CFG, "sym-lib-table")
FP_TABLE = os.path.join(CFG, "fp-lib-table")
SYM_DIR = os.path.join(ROOT, "symbols")
FP_DIR = os.path.join(ROOT, "footprints")

MEGA_VAR = "${MEGA_KICAD_LIB}"
EMPTY_SKIP = {"JLCPCB-Transformers.kicad_sym", "JLCPCB-Variable-Resistors.kicad_sym"}


def parse_entries(text):
    entries = []
    i = 0
    n = len(text)
    while i < n:
        if text.startswith("(lib", i):
            depth = 0
            j = i
            while j < n:
                c = text[j]
                if c == '"':
                    j += 1
                    while j < n and text[j] != '"':
                        if text[j] == '\\':
                            j += 1
                        j += 1
                elif c == '(':
                    depth += 1
                elif c == ')':
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            block = text[i:j + 1]
            def g(key):
                m = re.search(r'\(%s\s+"([^"]*)"' % key, block)
                return m.group(1) if m else ""
            entries.append({"name": g("name"), "type": g("type") or "KiCad",
                            "uri": g("uri"), "options": g("options"), "descr": g("descr")})
            i = j + 1
        else:
            i += 1
    return entries


def build(kind, entries):
    head = "(sym_lib_table\n" if kind == "sym" else "(fp_lib_table\n"
    lines = ["\t(version 7)"]
    for e in entries:
        lines.append('\t(lib (name "%s") (type "%s") (uri "%s") (options "%s") (descr "%s"))' % (
            e["name"], e["type"], e["uri"], e["options"], e["descr"]))
    return head + "\n".join(lines) + "\n)\n"


def validate(text):
    from sexpr import check_balance
    return check_balance(text) == 0


def register(kind, additions):
    table = SYM_TABLE if kind == "sym" else FP_TABLE
    with open(table, "r", encoding="utf-8") as fh:
        orig = fh.read()
    existing = parse_entries(orig)
    existing_names = {e["name"] for e in existing}
    existing_uris = {e["uri"] for e in existing}
    added = skipped = 0
    for name, uri, descr in additions:
        if name in existing_names:
            if uri in existing_uris:
                skipped += 1
                continue
            base = name
            i = 2
            while name in existing_names:
                name = "%s_%d" % (base, i)
                i += 1
        if uri in existing_uris:
            skipped += 1
            continue
        existing.append({"name": name, "type": "KiCad", "uri": uri, "options": "", "descr": descr})
        added += 1
    new_content = build(kind, existing)
    if not validate(new_content):
        print("ERROR: invalid %s table, aborting" % kind)
        sys.exit(1)
    tmp = table + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write(new_content)
    os.replace(tmp, table)
    print("[%s] added=%d skipped=%d" % (kind, added, skipped))


def main():
    sym_additions = []
    for fn in sorted(os.listdir(SYM_DIR)):
        if not fn.endswith(".kicad_sym") or fn in EMPTY_SKIP:
            continue
        full = os.path.join(SYM_DIR, fn)
        with open(full, "r", encoding="utf-8", errors="replace") as fh:
            content = fh.read()
        if not re.search(r'^\s*\(symbol\s+"', content, re.M):
            print("SKIP (no symbols): %s" % fn)
            continue
        base = fn[:-len(".kicad_sym")]
        if base.startswith("DigiKey_"):
            nick = "Mega_" + base
        elif base == "DigiKey":
            nick = "Mega_DigiKey"
        elif base == "Espressif":
            nick = "Mega_Espressif"
        elif base == "JLCPCB_Parts":
            nick = "Mega_JLCPCB_Parts"
        elif base.startswith("JLCPCB-"):
            nick = "Mega_" + base.replace("JLCPCB-", "JLCPCB_", 1)
        elif base.startswith("SparkFun-"):
            nick = "Mega_" + base
        else:
            nick = "Mega_" + base
        sym_additions.append((nick, "%s/symbols/%s" % (MEGA_VAR, fn), "Mega library: %s" % base))

    fp_additions = []
    for d in sorted(os.listdir(FP_DIR)):
        if not d.endswith(".pretty"):
            continue
        pretty_dir = os.path.join(FP_DIR, d)
        if not any(f.endswith(".kicad_mod") for f in os.listdir(pretty_dir)):
            continue
        base = d[:-len(".pretty")]
        if base == "JLCPCB":
            nick = "Mega_JLCPCB"
        elif base == "Espressif":
            nick = "Mega_Espressif"
        elif base == "digikey-footprints":
            nick = "Mega_DigiKey"
        elif base.startswith("SparkFun-"):
            nick = "Mega_" + base
        else:
            nick = "Mega_" + base
        fp_additions.append((nick, "%s/footprints/%s" % (MEGA_VAR, d), "Mega library: %s" % base))

    register("sym", sym_additions)
    register("fp", fp_additions)


if __name__ == "__main__":
    main()
