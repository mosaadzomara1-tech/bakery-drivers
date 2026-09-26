# سواقين المخبز

صفحة تثبيت تطبيق الدوام للسواقين، منشورة على GitHub Pages من مجلد `docs/`:
https://mosaadzomara1-tech.github.io/bakery-drivers/

| الملف | الغرض |
|---|---|
| `docs/index.html` | صفحة التثبيت (أندرويد + آيفون) |
| `docs/config.json` | عنوان السيرفر ورابط الـ APK — الصفحة بتقراه كل مرة بتفتح |
| `docs/icon.png` | الأيقونة (وبتظهر في معاينة اللينك على واتساب) |

## `config.json`

```json
{
  "server": "https://<عنوان سيرفر Traccar>",
  "version": 2,
  "apk": "https://github.com/mosaadzomara1-tech/bakery-drivers/releases/latest/download/bakery-drivers.apk"
}
```

- **server**: عنوان سيرفر Traccar اللي بيستقبل المواقع.
- **version**: رقم إصدار الـ APK، وبيظهر تحت زرار التحميل. زوّده لما ترفع APK جديد.
- **apk**: رابط التحميل. ارفع الملف باسم `bakery-drivers.apk` على **Release** جديد، والرابط هيجيب آخر نسخة لوحده.

## تغيير عنوان السيرفر

عدّل `server` في `docs/config.json` وارفع التعديل. الصفحة بتاخد العنوان الجديد على طول.
على الآيفون الصفحة هتقول للسوّاق إن السيرفر اتغيّر وتطلب منه يدوس «اضبط التطبيق» تاني.

## ⚠ ثبّت عنوان السيرفر (مُستحسن)

الروابط اللي بتخلص بـ `trycloudflare.com` مؤقتة وبتتغيّر مع كل تشغيل. عشان كده كان لازم تعدّل
الملف كل شوية، وكل سوّاق آيفون يضبط التطبيق من الأول. الحل إنك تعمل **Named Tunnel** بدومين ثابت:

```bash
cloudflared tunnel login                     # مرة واحدة (محتاج دومين على Cloudflare)
cloudflared tunnel create bakery
cloudflared tunnel route dns bakery track.<الدومين-بتاعك>
cloudflared tunnel run --url http://localhost:5055 bakery
```

وحط في `config.json` العنوان `https://track.<الدومين-بتاعك>`، ومش هتحتاج تغيّره تاني.
(`5055` هو منفذ استقبال المواقع الافتراضي في Traccar. غيّره لو إنت مشغّل على منفذ تاني.)

## الخصوصية

الصفحة مش بتتفهرس في محركات البحث (`noindex`). والتطبيق بيبعت الموقع وقت الدوام بس.
