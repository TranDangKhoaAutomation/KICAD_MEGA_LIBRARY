#!/usr/bin/env python3
"""
Stage vendor libraries from Sources/ into the managed footprints/ and symbols/
directories. Sources/ repos stay clean for git updates. Idempotent: files that
already exist at the destination are kept (never overwritten, never duplicated).
New files are copied.
Copyright © Trần Đăng Khoa / TranDangKhoaAutomation.
"""
import os, shutil, time

ROOT = r"D:\KICAD_MEGA_LIBRARY"
FP_DEST = os.path.join(ROOT, "footprints")
SYM_DEST = os.path.join(ROOT, "symbols")
LOG = os.path.join(ROOT, "logs", "stage_libraries.txt")

PLAN = [
    ("Espressif",
     [os.path.join(ROOT, "Sources", "Espressif", "footprints", "Espressif.pretty")],
     [os.path.join(ROOT, "Sources", "Espressif", "symbols", "Espressif.kicad_sym")]),
    ("SparkFun",
     [os.path.join(ROOT, "Sources", "SparkFun", "footprints", p)
      for p in sorted(os.listdir(os.path.join(ROOT, "Sources", "SparkFun", "footprints")))
      if p.endswith(".pretty")],
     [os.path.join(ROOT, "Sources", "SparkFun", "symbols", p)
      for p in sorted(os.listdir(os.path.join(ROOT, "Sources", "SparkFun", "symbols")))
      if p.endswith(".kicad_sym")]),
    ("DigiKey",
     [os.path.join(ROOT, "Sources", "DigiKey", "digikey-footprints.pretty")],
     []),
]


def log(msg):
    with open(LOG, "a", encoding="utf-8") as fh:
        fh.write(msg + "\n")


def copy_dir(src_dir, dst_dir):
    copied = skipped = 0
    os.makedirs(dst_dir, exist_ok=True)
    for fn in os.listdir(src_dir):
        sp = os.path.join(src_dir, fn)
        if not os.path.isfile(sp):
            continue
        dp = os.path.join(dst_dir, fn)
        if os.path.exists(dp):
            skipped += 1
            continue
        shutil.copy2(sp, dp)
        copied += 1
    return copied, skipped


def main():
    open(LOG, "a", encoding="utf-8").write("\n=== STAGE LIBRARIES %s ===\n" % time.strftime("%Y-%m-%d %H:%M:%S"))
    for vendor, fp_srcs, sym_srcs in PLAN:
        for s in fp_srcs:
            if not os.path.isdir(s):
                log("[missing] fp source %s" % s)
                continue
            name = os.path.basename(s)
            dst = os.path.join(FP_DEST, name)
            c, sk = copy_dir(s, dst)
            log("[fp] %s: copied=%d skipped=%d" % (name, c, sk))
            print("[fp] %s: copied=%d skipped=%d" % (name, c, sk))
        for s in sym_srcs:
            if not os.path.isfile(s):
                log("[missing] sym source %s" % s)
                continue
            name = os.path.basename(s)
            dst = os.path.join(SYM_DEST, name)
            if os.path.exists(dst):
                log("[sym] %s skipped (exists)" % name)
                continue
            shutil.copy2(s, dst)
            log("[sym] %s copied" % name)
            print("[sym] %s copied" % name)
    print("Done.")


if __name__ == "__main__":
    main()
