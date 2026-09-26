# -*- coding: utf-8 -*-
"""بيتأكد إن docs/config.json سليم، عشان غلطة صغيرة فيه بتوقف التطبيق والصفحة عند كل السواقين."""
import json
import sys
from urllib.parse import urlparse

PATH = sys.argv[1] if len(sys.argv) > 1 else "docs/config.json"
errors = []

try:
    with open(PATH, encoding="utf-8") as f:
        cfg = json.load(f)
except json.JSONDecodeError as e:
    sys.exit(f"❌ {PATH}: الملف مش JSON سليم (سطر {e.lineno}، عمود {e.colno}): {e.msg}")

if not isinstance(cfg, dict):
    sys.exit(f"❌ {PATH}: لازم يكون كائن {{...}}")


def https_url(key):
    v = cfg.get(key)
    if not isinstance(v, str) or not v.strip():
        errors.append(f"«{key}» فاضي أو مش موجود")
        return
    u = urlparse(v.strip())
    if u.scheme != "https" or not u.netloc:
        errors.append(f"«{key}» لازم يكون رابط كامل يبدأ بـ https://  (القيمة الحالية: {v})")
    elif v != v.strip():
        errors.append(f"«{key}» فيه مسافات في الأول أو الآخر")


https_url("server")
https_url("apk")
if "admin" in cfg:  # اختياري: عنوان لوحة Traccar لو مختلف عن server
    https_url("admin")
v = cfg.get("version")
if not isinstance(v, int) or isinstance(v, bool) or v < 1:
    errors.append(f"«version» لازم يكون رقم صحيح موجب (القيمة الحالية: {v!r})")

if errors:
    print(f"❌ {PATH}:")
    for e in errors:
        print("  -", e)
    sys.exit(1)
print(f"✅ {PATH} سليم — السيرفر: {cfg['server']} — النسخة: {cfg['version']}")
