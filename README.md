# سواقين المخبز

صفحة تثبيت تطبيق الدوام للسواقين، منشورة على GitHub Pages من مجلد `docs/`:
https://mosaadzomara1-tech.github.io/bakery-drivers/

| الملف | الغرض |
|---|---|
| `docs/index.html` | صفحة التثبيت (أندرويد + آيفون): خطوات مصوّرة، مشاكل شائعة، مشاركة على واتساب، وتدعم الوضع الليلي |
| `docs/config.json` | عنوان السيرفر ورقم آخر نسخة ورابط الـ APK — الصفحة وتطبيق الأندرويد بيقروه |
| `docs/icon.png` | الأيقونة (وبتظهر في معاينة اللينك على واتساب) |

## النظام كله ماشي إزاي

```
drivers-app (خاص: كود Flutter)
   │  أي push على main
   ▼
GitHub Actions ─► يبني APK موقّع ─► Release هنا (bakery-drivers.apk)
                                   └► يكتب version + apk في docs/config.json

docs/config.json ─► تطبيق الأندرويد: بيجيب عنوان السيرفر كل ما يفتح أو الدوام يبدأ،
                    ولو version أكبر من نسخته يظهر للسوّاق «في نسخة جديدة»
                 ─► الصفحة: زرار التحميل + ضبط Traccar على الآيفون
```

## `config.json`

```json
{
 "server": "https://<عنوان سيرفر Traccar>",
 "version": 2,
 "apk": "https://github.com/mosaadzomara1-tech/bakery-drivers/releases/latest/download/bakery-drivers.apk"
}
```

- **server**: عنوان سيرفر Traccar اللي بيستقبل المواقع. **ده الحقل الوحيد اللي بتعدّله بإيدك.**
- **version** و **apk**: بيتكتبوا لوحدهم بعد كل بناء. ماتغيّرهمش بإيدك — لو version زاد من غير نسخة
  جديدة، كل السواقين هيشوفوا «في نسخة جديدة» على الفاضي.

كل تعديل على `config.json` بيتفحص تلقائياً (`.github/workflows/check-config.yml`). لو فيه غلطة
(فاصلة ناقصة، عنوان مش `https`) هيظهر ❌ على الـ commit، صلّحه على طول عشان التطبيق والصفحة يفضلوا شغّالين.

## تغيير عنوان السيرفر

عدّل `server` في `docs/config.json` وارفع التعديل.
- **أندرويد:** مش محتاج أي حاجة — التطبيق بياخد العنوان الجديد لوحده.
- **آيفون:** Traccar بيحفظ العنوان جوّاه، فالسوّاق لازم يفتح الصفحة ويدوس «اضبط التطبيق» تاني.
  الصفحة بتقوله إن السيرفر اتغيّر.

## ⚠ ثبّت عنوان السيرفر (مُستحسن)

الروابط اللي بتخلص بـ `trycloudflare.com` مؤقتة وبتتغيّر مع كل تشغيل، وكل مرة سواقين الآيفون
بيقفوا لحد ما يضبطوا من الأول. الحل إنك تعمل **Named Tunnel** بدومين ثابت:

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
