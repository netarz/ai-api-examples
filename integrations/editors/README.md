# Cursor، Cline و Continue با کلید نِت اَرز

این ابزارها گزینهٔ «OpenAI-compatible» دارند و درگاه نِت اَرز همان رابط را پیاده می‌کند:
`/chat/completions` با استریم و فراخوانی ابزار (tools). پس کافی است نشانی پایه، کلید و شناسهٔ مدل را بدهید.
ما هر نسخهٔ این ابزارها را امتحان نکرده‌ایم؛ اگر تنظیمی در نسخهٔ شما جای دیگری است، در بخش Issues بنویسید.

| ابزار | کجا تنظیم کنید |
|---|---|
| **Continue** (VS Code و JetBrains) | فایل [`continue-config.yaml`](continue-config.yaml): `provider: openai` و `apiBase: https://netarz.ir/api/ai/v1` |
| **Cline** (VS Code) | Settings ← API Provider: **OpenAI Compatible**. Base URL را `https://netarz.ir/api/ai/v1`، API Key را کلید نِت اَرز و Model ID را شناسهٔ مدل بگذارید |
| **Cursor** | Settings ← Models: کلید را در OpenAI API Key و نشانی را در **Override OpenAI Base URL** بگذارید، بعد شناسهٔ مدل را به فهرست مدل‌ها اضافه کنید |

## پیش از شروع بدانید

- **مدلی با ابزار (tools) انتخاب کنید.** دستیارهای کدنویسی برای خواندن و نوشتن فایل از فراخوانی ابزار استفاده می‌کنند.
  در `GET https://netarz.ir/api/ai/v1/models?type=chat` مقدار `capabilities.tools` را ببینید.
  شناسهٔ Claude با `openrouter/anthropic/` شروع می‌شود.
- **برای این کلید سقف هزینه بگذارید.** این ابزارها در هر درخواست بخش بزرگی از کد پروژه را می‌فرستند و
  مصرف توکن بالا می‌رود. در پنل [/ai](https://netarz.ir/ai) برای کلید سقف هزینه تعیین کنید.
- **حجم هر درخواست سقف دارد** (در حال حاضر ۴ مگابایت). اگر خطای `request_too_large` گرفتید، فایل‌های کمتری را به گفت‌وگو اضافه کنید.
- **Cursor درخواست را از سرورهای خودش می‌فرستد**، نه از رایانهٔ شما؛ پس فهرست IP مجاز را برای این کلید خالی بگذارید.
  بعضی امکانات Cursor مثل تکمیل خودکار (Tab) همیشه با مدل‌های خودِ Cursor کار می‌کنند و از کلید شما استفاده نمی‌کنند.
- تکمیل خودکار خط‌به‌خط (FIM) را به این درگاه نسپارید؛ مسیر `/completions` متن را به یک پیام گفت‌وگو تبدیل می‌کند و برای FIM ساخته نشده.

خطاها و محدودیت‌ها: [netarz.ir/docs/ai/errors](https://netarz.ir/docs/ai/errors) و
[netarz.ir/docs/ai/rate-limits-and-security](https://netarz.ir/docs/ai/rate-limits-and-security)

---

**English.** Continue (`provider: openai`, `apiBase`), Cline (*OpenAI Compatible* provider) and Cursor (*Override OpenAI
Base URL*) can use `https://netarz.ir/api/ai/v1` with a NetArz key. Pick a model whose `capabilities.tools` is true,
set a spend limit on the key (coding agents send large contexts), keep requests under the current 4 MB body cap,
and leave the key's IP allow-list empty for Cursor, whose requests leave from Cursor's servers. Do not use the
gateway for FIM autocomplete. We have not tested every version of these tools; open an issue if a setting moved.
