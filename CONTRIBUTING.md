# راهنمای مشارکت

خوشحالیم که می‌خواهید نمونه‌کدهای وب‌سرویس هوش مصنوعی نِت اَرز را بهتر کنید. این راهنما کوتاه است و کمک می‌کند Pull Request شما زودتر بررسی و ادغام شود.

## چه کمکی به کار می‌آید

- اصلاح کدی که با [مستندات فعلی](https://netarz.ir/docs/ai?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=contributing) جور نیست یا اجرا نمی‌شود
- نمونهٔ تازه برای زبان، فریم‌ورک یا ابزاری که این‌جا نیست
- توضیح روشن‌تر در README یا در توضیح بالای فایل‌ها

## چه چیزی جای این مخزن نیست

- **حساب، اعتبار، پرداخت و کلید:** از پنل نِت اَرز [تیکت بزنید](https://netarz.ir/tickets?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=contributing) یا به `info@netarz.ir` ایمیل بفرستید.
- **مشکل امنیتی:** در Issue یا Pull Request عمومی ننویسید. طبق [سیاست امنیتی](SECURITY.md) به `dev@netarz.ir` بفرستید.

## پیش از فرستادن Pull Request

1. برای تغییر بزرگ، اول یک Issue باز کنید تا پیش از نوشتن کد دربارهٔ راه‌حل هم‌نظر شویم.
2. کلید واقعی (`sk-ntz-v1-…`)، توکن ربات یا نشانی سرور خصوصی در کد، README یا تاریخچهٔ گیت نگذارید. اگر اشتباهی کلیدی را کامیت کردید، پیش از هر کاری آن را از پنل نِت اَرز باطل کنید؛ پاک کردن کامیت کافی نیست.
3. کلید را فقط از متغیر محیطی `NETARZ_API_KEY` بخوانید و نشانی پایه را از `NETARZ_BASE_URL` با مقدار پیش‌فرض `https://netarz.ir/api/ai/v1`.
4. در هر درخواست گفت‌وگو `max_tokens` بفرستید؛ نمونه‌ای که آن را ندارد به کاربر یاد می‌دهد اعتبارش را بی‌دلیل رزرو کند.
5. شناسهٔ مدل را از [فهرست زندهٔ مدل‌ها](https://netarz.ir/api/ai/v1/models?type=chat) بردارید. Claude فقط با پیشوند `openrouter/anthropic/` کار می‌کند.
6. کد، نام متغیرها و توضیح‌های داخل کد انگلیسی باشد. README فارسی است و یک بخش English کوتاه دارد.
7. فایل تازه را در جدول «فهرست نمونه‌ها» در README اضافه کنید، با لینک صفحهٔ مستندات مربوط.
8. کد را یک بار واقعاً اجرا کنید. بررسی سریع نحو: `python -m py_compile <file>.py` · `node --check <file>.mjs` · `php -l <file>.php` · `bash -n <file>.sh`

## سبک نوشتن متن فارسی

- خواننده را «شما» خطاب کنید و جمله‌ها را کوتاه بنویسید.
- اصطلاح فنی را بار اول با توضیح بیاورید، مثل «کلید دسترسی (API Key)». نام endpoint، پارامتر و کد لاتین می‌ماند.
- ایموجی و علامت تعجب نگذارید. نام برند همیشه «نِت اَرز» (یا NetArz) است.

## مجوز

با فرستادن Pull Request می‌پذیرید که کد شما با مجوز همین مخزن (MIT) منتشر شود.
همه در این مخزن از [آیین رفتار](CODE_OF_CONDUCT.md) پیروی می‌کنند.

---

## Contributing (English)

Thanks for improving the NetArz AI API examples. Open an issue before a large change. Never commit a real key (`sk-ntz-v1-…`) or token;
if you did, revoke it in the NetArz panel first. Read the key from `NETARZ_API_KEY`, always send `max_tokens`, take model ids from the live `/models` list. Run the code once for real before opening a pull request.
Account, credit and billing questions go to `info@netarz.ir`, security issues to `dev@netarz.ir` (see [SECURITY.md](SECURITY.md)).
By contributing you agree your work is released under MIT.
