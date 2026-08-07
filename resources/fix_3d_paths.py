#!/usr/bin/env python3
"""
Rewrite 3D model paths inside staged footprint .kicad_mod files so they
resolve on this KiCad install. Only modifies references whose model actually
exists in the target 3dmodels folder. Unfixable references are logged to
broken_3d_paths.txt and left untouched. offset/scale/rotate untouched.
Copyright © Trần Đăng Khoa.
"""
import os, re

ROOT = r"D:\KICAD_MEGA_LIBRARY"
FP = os.path.join(ROOT, "footprints")
MODELS = os.path.join(ROOT, "3dmodels")
CHANGES = os.path.join(ROOT, "logs", "3dmodel_changes.txt")
BROKEN = os.path.join(ROOT, "logs", "broken_3d_paths.txt")

MODEL_RE = re.compile(r'(\s*\(model\s+")([^"]+)(")')

RULES = [
    ("JLCPCB",
     os.path.join(MODELS, "JLCPCB"),
     [r'\$\{KICAD8_3RD_PARTY\}/3dmodels/com_github_CDFER_JLCPCB-Kicad-Library/JLCPCB\.3dshapes/',
      r'^/3dModels/']),
    ("Espressif",
     os.path.join(MODELS, "Espressif"),
     [r'\$\{KICAD8_3RD_PARTY\}/3dmodels/com_github_espressif_kicad-libraries/espressif\.3dshapes/',
      r'\$\{KICAD9_3RD_PARTY\}/3dmodels/com_github_espressif_kicad-libraries/espressif\.3dshapes/']),
]


def log(path, msg):
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(msg + "\n")


def fix_dir(pretty_dir, vendor, model_dir, prefixes):
    changed = broken = 0
    for fn in sorted(os.listdir(pretty_dir)):
        if not fn.endswith(".kicad_mod"):
            continue
        fp = os.path.join(pretty_dir, fn)
        with open(fp, "r", encoding="utf-8", errors="replace") as fh:
            content = fh.read()
        new_content = content
        modified = False
        for m in MODEL_RE.finditer(content):
            ref = m.group(2)
            base = os.path.basename(ref)
            if not any(re.search(p, ref) for p in prefixes):
                continue
            cand = os.path.join(model_dir, base)
            if not os.path.exists(cand):
                found = None
                if os.path.isdir(model_dir):
                    for f in os.listdir(model_dir):
                        if f.lower() == base.lower():
                            found = os.path.join(model_dir, f)
                            break
                if found is None:
                    log(BROKEN, "%s: ref '%s' model '%s' not in %s" % (fp, ref, base, model_dir))
                    broken += 1
                    continue
                cand = found
            new_ref = "${MEGA_KICAD_LIB}/3dmodels/%s/%s" % (vendor, os.path.basename(cand))
            new_content = new_content.replace('"%s"' % ref, '"%s"' % new_ref, 1)
            log(CHANGES, "[%s] %s: %s -> %s" % (vendor, fn, ref, new_ref))
            modified = True
        if modified:
            with open(fp, "w", encoding="utf-8") as fh:
                fh.write(new_content)
            changed += 1
    return changed, broken


def main():
    open(CHANGES, "a", encoding="utf-8").write("\n=== FIX 3D PATHS ===\n")
    open(BROKEN, "a", encoding="utf-8").write("\n=== BROKEN (unfixable) ===\n")
    total_c = total_b = 0
    for vendor, model_dir, prefixes in RULES:
        d = os.path.join(FP, "%s.pretty" % vendor)
        if not os.path.isdir(d):
            continue
        c, b = fix_dir(d, vendor, model_dir, prefixes)
        print("%s: changed=%d broken=%d" % (vendor, c, b))
        total_c += c
        total_b += b
    print("TOTAL changed=%d broken=%d" % (total_c, total_b))


if __name__ == "__main__":
    main()
