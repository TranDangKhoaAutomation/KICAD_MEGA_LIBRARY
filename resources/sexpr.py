#!/usr/bin/env python3
"""
Minimal, correct S-expression helpers (strings respected).
Used by register_libraries / fix_3d_paths.
Copyright © Trần Đăng Khoa / TranDangKhoaAutomation.
"""


def check_balance(text):
    depth = 0
    i = 0
    n = len(text)
    while i < n:
        c = text[i]
        if c == '"':
            i += 1
            while i < n and text[i] != '"':
                if text[i] == '\\':
                    i += 1
                i += 1
        elif c == '(':
            depth += 1
        elif c == ')':
            depth -= 1
            if depth < 0:
                return depth
        i += 1
    return depth
