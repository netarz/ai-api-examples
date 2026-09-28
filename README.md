<div align="center">

# نمونه‌کد وب‌سرویس هوش مصنوعی (API) نِت اَرز

**GPT، Claude، Gemini و DeepSeek با یک کلید و یک نشانی سازگار با OpenAI. اعتبار را به تومان می‌خرید.**

OpenAI-compatible AI API examples for developers in Iran: one key for GPT, Claude, Gemini and DeepSeek, prepaid in Toman.

[![CI](https://github.com/netarz/ai-api-examples/actions/workflows/ci.yml/badge.svg)](https://github.com/netarz/ai-api-examples/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-ffc700?style=flat-square&labelColor=14161f)](LICENSE)
[![OpenAI compatible](https://img.shields.io/badge/OpenAI-compatible-ffc700?style=flat-square&labelColor=14161f)](https://netarz.ir/docs/ai/migrating-from-openai?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=header)
[![Python](https://img.shields.io/badge/Python-3.9%2B-ffc700?style=flat-square&labelColor=14161f&logo=python&logoColor=white)](python/)
[![Node.js](https://img.shields.io/badge/Node.js-18%2B-ffc700?style=flat-square&labelColor=14161f&logo=nodedotjs&logoColor=white)](node/)
[![PHP](https://img.shields.io/badge/PHP-8.1%2B-ffc700?style=flat-square&labelColor=14161f&logo=php&logoColor=white)](php/)
[![Go](https://img.shields.io/badge/Go-1.21%2B-ffc700?style=flat-square&labelColor=14161f&logo=go&logoColor=white)](go/)
[![.NET](https://img.shields.io/badge/.NET-8-ffc700?style=flat-square&labelColor=14161f&logo=dotnet&logoColor=white)](dotnet/)
[![Ruby](https://img.shields.io/badge/Ruby-3.0%2B-ffc700?style=flat-square&labelColor=14161f&logo=ruby&logoColor=white)](ruby/)
[![Docs](https://img.shields.io/badge/docs-netarz.ir%2Fdocs%2Fai-ffc700?style=flat-square&labelColor=14161f)](https://netarz.ir/docs/ai?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=header)

[معرفی سرویس](https://netarz.ir/ai-api?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=header) · [مستندات](https://netarz.ir/docs/ai?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=header) · [مدل‌ها و قیمت‌ها](https://netarz.ir/ai-api/models?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=header) · [ساخت کلید](https://netarz.ir/ai?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=header) · [English](#english)

</div>

<a id="intro"></a>

این مخزن نمونه‌کدهای آماده برای وصل شدن به **API هوش مصنوعی نِت اَرز** (وب سرویس هوش مصنوعی) را دارد: Python، Node.js،
PHP، Laravel، Go، C# (.NET)، Ruby، cURL، LangChain، n8n، ربات تلگرام و ویرایشگرهای کد مثل Cursor و Cline.

اگر با کتابخانهٔ رسمی OpenAI کار کرده‌اید، کد شما تقریباً همان است. فقط دو مقدار عوض می‌شود:

| مقدار | در OpenAI | در نِت اَرز |
|---|---|---|
| نشانی پایه (base URL) | `https://api.openai.com/v1` | `https://netarz.ir/api/ai/v1` |
| کلید دسترسی (API Key) | `sk-proj-…` | `sk-ntz-v1-…` |

هزینهٔ هر درخواست به دلار از اعتبار تومانی شما کم می‌شود و کارت ارزی لازم نیست.

## فهرست

- [شروع در دو دقیقه](#quickstart)
- [پیش از اجرای نمونه‌ها](#before-you-run)
- [فهرست نمونه‌ها](#examples)
- [Go، C# و Ruby](#more-languages)
- [یک کلید، چهار سازنده](#providers)
- [هزینه را کنترل کنید](#cost)
- [کلید را کجا نگه دارید](#key-safety)
- [خطاهای رایج](#errors)
- [پرسش‌های رایج](#faq)
- [بررسی خودکار کد و فهرست تغییرات](#ci)
- [مخزن‌های دیگر نِت اَرز](#related)
- [مشارکت و پشتیبانی](#support)
- [English](#english)

<a id="quickstart"></a>

## شروع در دو دقیقه

**۱. فهرست مدل‌ها را ببینید.** این درخواست کلید نمی‌خواهد:

```bash
curl "https://netarz.ir/api/ai/v1/models?type=chat"
```

**۲. کلید بسازید.** در [نِت اَرز](https://netarz.ir/ai?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=quickstart) ثبت‌نام کنید، اعتبار بخرید و در پنل یک کلید بسازید.

**۳. اولین درخواست را بفرستید:**

```bash
git clone https://github.com/netarz/ai-api-examples.git
cd ai-api-examples/python
pip install -r requirements.txt
export NETARZ_API_KEY="sk-ntz-v1-..."
python chat.py
```

همین کار با Node.js:

```bash
cd ai-api-examples/node && npm install
NETARZ_API_KEY="sk-ntz-v1-..." npm run chat
```

یا در کد خودتان:

```python
from openai import OpenAI

client = OpenAI(base_url="https://netarz.ir/api/ai/v1", api_key="sk-ntz-v1-...")
r = client.chat.completions.create(
    model="gpt-4o-mini",  # یا openrouter/anthropic/claude-sonnet-4.5، gemini-3.5-flash، deepseek-flash
    messages=[{"role": "user", "content": "سلام"}],
    max_tokens=200,
)
print(r.choices[0].message.content)
```

راهنمای قدم‌به‌قدم: [شروع سریع در مستندات](https://netarz.ir/docs/ai/quickstart?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=quickstart)

<a id="before-you-run"></a>

## پیش از اجرای نمونه‌ها

1. در [نِت اَرز](https://netarz.ir/?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=before-you-run) ثبت‌نام کنید و از پنل [/ai](https://netarz.ir/ai?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=before-you-run) اعتبار بخرید.
   حداقل مبلغ شارژ و مالیات بر ارزش افزوده را پیش از پرداخت می‌بینید.
2. در همان پنل یک پروژه و برای آن یک کلید بسازید. کلید کامل را فقط همان یک بار می‌بینید.
3. کلید را در متغیر محیطی بگذارید (فایل `.env.example` را ببینید):

```bash
export NETARZ_API_KEY="sk-ntz-v1-..."
```

در هیچ فایلی از این مخزن کلید واقعی نیست. کلید خودتان را هم در گیت کامیت نکنید.

<a id="examples"></a>

## فهرست نمونه‌ها

| پوشه / فایل | چه کاری می‌کند | راهنمای مربوط |
|---|---|---|
| [`python/chat.py`](python/chat.py) | گفت‌وگوی ساده با کتابخانهٔ `openai` | [Chat Completions](https://netarz.ir/docs/ai/chat-completions?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=examples) |
| [`python/stream.py`](python/stream.py) · [`node/stream.mjs`](node/stream.mjs) · [`curl/stream.sh`](curl/stream.sh) | پاسخ تکه‌به‌تکه (استریم، SSE) | [استریم](https://netarz.ir/docs/ai/streaming?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=examples) |
| [`python/structured_output.py`](python/structured_output.py) · [`node/structured-output.mjs`](node/structured-output.mjs) | خروجی JSON و JSON Schema | [Chat Completions](https://netarz.ir/docs/ai/chat-completions?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=examples) |
| [`python/tool_calling.py`](python/tool_calling.py) · [`node/tools.mjs`](node/tools.mjs) | فراخوانی تابع (tools) با چرخهٔ کامل | [Chat Completions](https://netarz.ir/docs/ai/chat-completions?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=examples) |
| [`python/embeddings.py`](python/embeddings.py) · [`node/embeddings.mjs`](node/embeddings.mjs) | امبدینگ و جست‌وجوی معنایی ساده | [امبدینگ](https://netarz.ir/docs/ai/embeddings?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=examples) |
| [`python/images.py`](python/images.py) | ساخت تصویر با مدل‌های GPT Image | [تصویر](https://netarz.ir/docs/ai/images?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=examples) |
| [`python/audio.py`](python/audio.py) | متن به گفتار و گفتار به متن | [صوت](https://netarz.ir/docs/ai/audio?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=examples) |
| [`python/responses_api.py`](python/responses_api.py) | Responses API (فقط مدل‌های OpenAI) | [Responses API](https://netarz.ir/docs/ai/responses-api?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=examples) |
| [`python/account_and_models.py`](python/account_and_models.py) · [`curl/models-and-account.sh`](curl/models-and-account.sh) | فهرست مدل‌ها (بدون کلید) و موجودی حساب | [احراز هویت](https://netarz.ir/docs/ai/authentication?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=examples) |
| [`python/vision.py`](python/vision.py) · [`node/vision.mjs`](node/vision.mjs) | فرستادن تصویر به مدل (vision)، با نشانی اینترنتی یا فایلی روی سیستم خودتان | [Chat Completions](https://netarz.ir/docs/ai/chat-completions?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=examples) |
| [`python/rag_persian.py`](python/rag_persian.py) | RAG فارسی کوچک: امبدینگ، شباهت کسینوسی (cosine similarity) و جوابی که فقط از متن‌های پیداشده می‌آید | [امبدینگ](https://netarz.ir/docs/ai/embeddings?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=examples) |
| [`python/usage_and_cost.py`](python/usage_and_cost.py) | خواندن مصرف توکن از فیلد `usage`، برآورد هزینه و مبلغ کسرشده با `GET /requests/{id}` و `GET /usage` | [حساب و مصرف](https://netarz.ir/docs/ai/account-and-usage?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=examples) |
| [`python/retry_and_errors.py`](python/retry_and_errors.py) | مدیریت خطا و تلاش دوباره | [خطاها](https://netarz.ir/docs/ai/errors?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=examples) |
| [`node/`](node/) | همین نمونه‌ها با Node.js، به‌علاوهٔ [`server-proxy.mjs`](node/server-proxy.mjs) که کلید را روی سرور نگه می‌دارد | [SDKها](https://netarz.ir/docs/ai/sdks?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=examples) |
| [`php/`](php/) | `openai-php/client`، و cURL خالص برای هاست اشتراکی (معمولی و استریم) | [SDKها](https://netarz.ir/docs/ai/sdks?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=examples) |
| [`laravel/`](laravel/) | سرویس `NetArzAi` با Http لاراول و یک route نمونه | [SDKها](https://netarz.ir/docs/ai/sdks?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=examples) |
| [`go/`](go/) | Go با `net/http` و بدون کتابخانهٔ جانبی: گفت‌وگو و استریم | [SDKها](https://netarz.ir/docs/ai/sdks?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=examples) |
| [`dotnet/`](dotnet/) | C# (.NET 8) با `HttpClient` و بدون بستهٔ NuGet: گفت‌وگو و استریم | [SDKها](https://netarz.ir/docs/ai/sdks?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=examples) |
| [`ruby/`](ruby/) | Ruby با `net/http` و بدون gem: گفت‌وگو و استریم | [SDKها](https://netarz.ir/docs/ai/sdks?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=examples) |
| [`curl/`](curl/) | همهٔ endpointهای اصلی با cURL | [مرجع تعاملی](https://netarz.ir/docs/ai/reference?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=examples) |
| [`langchain/`](langchain/) | LangChain پایتون: گفت‌وگو، عوض کردن مدل، RAG کوچک | [SDKها](https://netarz.ir/docs/ai/sdks?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=examples) |
| [`telegram-bot/`](telegram-bot/) | ربات تلگرام که با مدل جواب می‌دهد | [راهنمای ربات تلگرام](https://netarz.ir/wiki/ai-telegram-bot-webservice?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=examples) |
| [`integrations/n8n/`](integrations/n8n/) | workflow آمادهٔ n8n | [SDKها](https://netarz.ir/docs/ai/sdks?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=examples) |
| [`integrations/editors/`](integrations/editors/) | Cursor، Cline و Continue | [SDKها](https://netarz.ir/docs/ai/sdks?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=examples) |
| [`providers/`](providers/) | شناسهٔ مدل‌های OpenAI، Claude، Gemini و DeepSeek با یک نمونه برای هر کدام | [مدل‌ها و قیمت‌ها](https://netarz.ir/docs/ai/models-and-pricing?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=examples) |

ساخت ویدیو (Sora) و موسیقی (Lyria) نمونه‌کد جدا در این مخزن ندارند؛ نمونهٔ کامل هر دو در مستندات است:
[ویدیو](https://netarz.ir/docs/ai/video?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=examples) · [موسیقی](https://netarz.ir/docs/ai/music?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=examples).

<a id="more-languages"></a>

## Go، C# و Ruby

این سه نمونه فقط از کتابخانهٔ استاندارد همان زبان استفاده می‌کنند و کلید را از متغیر محیطی `NETARZ_API_KEY` می‌خوانند.
هر کدام یک گفت‌وگوی ساده و یک نمونهٔ استریم دارد.

```bash
export NETARZ_API_KEY="sk-ntz-v1-..."

# Go 1.21+
(cd go && go run ./chat && go run ./stream)

# .NET 8
(cd dotnet && dotnet run && dotnet run -- stream)

# Ruby 3.0+
(cd ruby && ruby chat.rb && ruby stream.rb)
```

اگر کتابخانهٔ رسمی OpenAI را برای Go یا .NET ترجیح می‌دهید، همان کتابخانه هم کار می‌کند؛ فقط نشانی پایه را
`https://netarz.ir/api/ai/v1` بگذارید. نمونهٔ کتابخانهٔ Go در [صفحهٔ SDKها](https://netarz.ir/docs/ai/sdks?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=more-languages) آمده است.

<a id="providers"></a>

## یک کلید، چهار سازنده

| سازنده | شناسهٔ نمونه | نکته | صفحه |
|---|---|---|---|
| OpenAI | `gpt-4o-mini` | مدل‌های Pro و Codex فقط با `/responses` | [API OpenAI در ایران](https://netarz.ir/ai-api/openai?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=providers) |
| Claude | `openrouter/anthropic/claude-sonnet-4.5` | فقط با پیشوند `openrouter/anthropic/`؛ کتابخانهٔ Anthropic کار نمی‌کند | [API کلود](https://netarz.ir/ai-api/claude?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=providers) |
| Gemini | `gemini-3.5-flash` | Imagen (تصویرساز گوگل) روی درگاه نیست | [API جمینای](https://netarz.ir/ai-api/gemini?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=providers) |
| DeepSeek | `deepseek-flash` | R1 و بقیه با پیشوند `openrouter/deepseek/` | [API دیپ‌سیک](https://netarz.ir/ai-api/deepseek?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=providers) |

جزئیات و قاعدهٔ شناسه‌ها در [`providers/README.md`](providers/README.md). فهرست زندهٔ مدل‌ها را بدون کلید بگیرید:
`curl "https://netarz.ir/api/ai/v1/models?type=chat"`. قیمت هر مدل به دلار و تومان در
[صفحهٔ مدل‌ها](https://netarz.ir/ai-api/models?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=providers) است.

<a id="cost"></a>

## هزینه را کنترل کنید

- **همیشه `max_tokens` بفرستید.** پیش از هر درخواست، درگاه مبلغ بلندترین جواب ممکن را از اعتبار شما کنار می‌گذارد؛
  با `max_tokens` این مبلغ کوچک می‌شود و با موجودی کم به خطای `insufficient_credit` نمی‌خورید. بعد از جواب،
  فقط مصرف واقعی کم می‌شود.
- درخواستی که پیش از تولید جواب با خطا تمام شود هزینه ندارد. اگر استریم وسط کار قطع شود، فقط آنچه تا آن لحظه تولید شده حساب می‌شود.
- برای هر کلید سقف هزینه و برای هر پروژه بودجهٔ ماهانه بگذارید تا یک باگ یا کلید لورفته کل اعتبار را خرج نکند.
- برای جواب‌های طولانی و مدل‌های استدلالی از استریم استفاده کنید تا اتصال وسط کار قطع نشود.

<a id="key-safety"></a>

## کلید را کجا نگه دارید

کلید `sk-ntz-v1-…` را **فقط روی سرور** نگه دارید؛ نه در کد مرورگر، نه در اپ موبایل، نه در مخزن عمومی.
هر کسی کلید را ببیند می‌تواند با اعتبار شما درخواست بفرستد. الگوی درست: مرورگر یا اپ به سرور خودتان
درخواست می‌دهد و سرور شما با کلید به نِت اَرز وصل می‌شود ([`node/server-proxy.mjs`](node/server-proxy.mjs)،
[`laravel/routes-example.php`](laravel/routes-example.php)). برای کلیدهای سرور، فهرست IPهای مجاز را هم در پنل پر کنید.

<a id="errors"></a>

## خطاهای رایج

| کد | یعنی | چه کنید |
|---|---|---|
| `401 missing_api_key` / `invalid_api_key` | کلید نرسیده یا اشتباه است | هدر `Authorization: Bearer sk-ntz-v1-…` را بررسی کنید |
| `402 insufficient_credit` | اعتبار برای رزرو این درخواست کافی نیست | شارژ کنید یا `max_tokens` را کم کنید |
| `403 model_not_allowed` | مدل در فهرست مجاز کلید یا پروژه نیست | هر دو فهرست را در پنل ببینید |
| `404 model_not_found` | شناسهٔ مدل پیدا نشد | برای Claude پیشوند `openrouter/anthropic/` را بگذارید |
| `429 rate_limit_exceeded` | بیش از سقف درخواست در دقیقه | به اندازهٔ `Retry-After` صبر کنید؛ سقف کلید را `GET /me` نشان می‌دهد |

فهرست کامل: [netarz.ir/docs/ai/errors](https://netarz.ir/docs/ai/errors?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=errors)

<a id="faq"></a>

## پرسش‌های رایج

**با کتابخانهٔ Anthropic یا مسیر `/v1/messages` کار می‌کند؟**
نه. Claude را با کتابخانهٔ OpenAI و مسیر `/chat/completions` صدا بزنید؛ تبدیل درخواست به قالب Claude با شما نیست.

**مدل رایگان دارید؟**
نه. مدل‌های رایگان روی ظرفیت مشترک ارائه‌دهنده بودند و وسط کار خطا می‌دادند، پس آن‌ها را برداشتیم. قیمت هر مدل را در [صفحهٔ مدل‌ها](https://netarz.ir/ai-api/models?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=faq) ببینید و مدلی را که به بودجهٔ پروژه‌تان می‌خورد انتخاب کنید.

**متن پیام‌هایم جایی ذخیره می‌شود؟**
درگاه فقط فراداده ثبت می‌کند، مثل مدل، تعداد توکن، هزینه، وضعیت و زمان. متن پیام‌ها و جواب‌ها در نِت اَرز ذخیره نمی‌شود. بدنهٔ درخواست بدون تغییر به سرویس‌دهندهٔ اصلی (مثل OpenAI، گوگل، DeepSeek یا OpenRouter) می‌رود و از آن‌جا سیاست نگهداری داده‌های همان شرکت حاکم است.
جزئیات: [حریم خصوصی داده در API هوش مصنوعی](https://netarz.ir/wiki/ai-api-privacy-iran?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=faq)

**برنامه‌نویس نیستم؛ فقط می‌خواهم با مدل‌ها گفت‌وگو کنم.**
وب‌سرویس برای وصل کردن سایت، اپ یا ربات است. برای گفت‌وگو در مرورگر [استودیو هوش مصنوعی](https://netarz.ir/ai-studio?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=faq) را ببینید.

<a id="ci"></a>

## بررسی خودکار کد و فهرست تغییرات

با هر Push و Pull Request، [گردش‌کار CI](.github/workflows/ci.yml) نحو (syntax) همهٔ نمونه‌ها را بررسی می‌کند و نمونه‌های Go و .NET را
می‌سازد (build). این بررسی هیچ درخواستی به API نمی‌فرستد و کلید لازم ندارد، پس هیچ اعتباری مصرف نمی‌کند.
Dependabot هم ماهی یک بار نسخهٔ تازهٔ وابستگی‌ها را پیشنهاد می‌دهد.

تغییرات هر نسخه در [CHANGELOG.md](CHANGELOG.md) آمده است.

<a id="related"></a>

## مخزن‌های دیگر نِت اَرز

| مخزن | چیست |
|---|---|
| [fx-api-examples](https://github.com/netarz/fx-api-examples) | نمونه‌کد وب‌سرویس نرخ ارز: نرخ دلار و ارزها به تومان در PHP، JavaScript، Python، Laravel، Google Sheets و Excel |
| [netarz-fx-wordpress](https://github.com/netarz/netarz-fx-wordpress) | افزونهٔ وردپرس نرخ ارز با شورت‌کد `[netarz_rate currency="usd"]` و ابزارک |
| [netarz](https://github.com/netarz/netarz) | معرفی همهٔ وب‌سرویس‌ها و مخزن‌های نِت اَرز |

همهٔ پروژه‌های متن‌باز ما یک‌جا: [netarz.ir/open-source](https://netarz.ir/open-source?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=related) · همهٔ مستندات فنی: [netarz.ir/docs](https://netarz.ir/docs?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=related)

<a id="support"></a>

## مشارکت و پشتیبانی

- **اشکال در کد همین مخزن:** یک [Issue](https://github.com/netarz/ai-api-examples/issues/new/choose) باز کنید. قالب گزارش اشکال می‌پرسد چه اجرا کردید و چه دیدید.
- **نمونهٔ تازه یا اصلاح:** Pull Request بفرستید. پیش از آن [راهنمای مشارکت](CONTRIBUTING.md) را ببینید.
- **حساب، اعتبار و کلید:** این‌ها جای Issue نیستند. از پنل نِت اَرز تیکت بزنید یا به `info@netarz.ir` ایمیل بفرستید.
- **مشکل امنیتی:** در Issue عمومی ننویسید؛ طبق [سیاست امنیتی](SECURITY.md) به `dev@netarz.ir` بفرستید.

«نِت اَرز» مرکز خرید سرویس‌های خارجی است و نمایندهٔ رسمی هیچ‌یک از شرکت‌هایی که نامشان در این مخزن آمده نیست.
نام‌ها و نشان‌های OpenAI، Anthropic، Google و DeepSeek متعلق به خود این شرکت‌هاست.

مجوز: [MIT](LICENSE) · [آیین رفتار](CODE_OF_CONDUCT.md)

---

<a id="english"></a>

## English

**NetArz AI API examples.** Ready-to-run code for the NetArz AI gateway, an OpenAI-compatible API that lets
developers in Iran call GPT, Claude, Gemini and DeepSeek models with one key, paying from credit bought in Toman.
There are no free models: every call is paid from your prepaid credit.

- [Quick start](#quick-start)
- [Examples](#examples-en)
- [Go, C# and Ruby](#go-c-and-ruby)
- [Facts](#facts)
- [CI and changelog](#ci-and-changelog)
- [Links](#links)

<a id="quick-start"></a>

### Quick start

```bash
# 1. No key needed: list the chat models
curl "https://netarz.ir/api/ai/v1/models?type=chat"

# 2. Create a key at https://netarz.ir/ai, then:
git clone https://github.com/netarz/ai-api-examples.git
cd ai-api-examples/python && pip install -r requirements.txt
export NETARZ_API_KEY="sk-ntz-v1-..."
python chat.py
```

<a id="examples-en"></a>

### Examples

| Folder / file | What it shows |
|---|---|
| [`python/`](python/) | Chat, streaming, JSON output, tool calling, embeddings, images, audio, Responses API, account and models, retries |
| [`python/vision.py`](python/vision.py) · [`node/vision.mjs`](node/vision.mjs) | Image input (vision) from a URL or a local file |
| [`python/rag_persian.py`](python/rag_persian.py) | A small Persian RAG: embeddings, cosine similarity in plain Python, grounded answer |
| [`python/usage_and_cost.py`](python/usage_and_cost.py) | Token `usage`, a cost estimate from `/models` prices, the charged amount from `/requests/{id}` and `/usage` |
| [`node/`](node/) | The same with Node.js, plus a server-side proxy that keeps the key off the browser |
| [`php/`](php/) · [`laravel/`](laravel/) | `openai-php/client`, plain cURL, and a Laravel service |
| [`go/`](go/) · [`dotnet/`](dotnet/) · [`ruby/`](ruby/) | Chat and streaming with each language's standard library only |
| [`curl/`](curl/) | Shell scripts for the main endpoints |
| [`langchain/`](langchain/) · [`telegram-bot/`](telegram-bot/) · [`integrations/`](integrations/) | LangChain, a Telegram bot, n8n, Cursor, Cline and Continue |

<a id="go-c-and-ruby"></a>

### Go, C# and Ruby

Standard library only; the key is read from `NETARZ_API_KEY`.

```bash
(cd go && go run ./chat && go run ./stream)          # Go 1.21+
(cd dotnet && dotnet run && dotnet run -- stream)    # .NET 8
(cd ruby && ruby chat.rb && ruby stream.rb)          # Ruby 3.0+
```

<a id="facts"></a>

### Facts

- Base URL: `https://netarz.ir/api/ai/v1`
- Auth: `Authorization: Bearer sk-ntz-v1-…` (or `X-API-Key`)
- Works with the official OpenAI SDKs (Python, Node), `openai-php/client`, LangChain, n8n, Continue, Cline, Cursor.
- Endpoints: `/chat/completions`, `/completions`, `/responses` (OpenAI models only), `/embeddings`,
  `/images/generations`, `/audio/speech`, `/audio/transcriptions`, `/audio/translations`, `/audio/music`,
  `/videos` (an async job: create, poll, download), `/models`, `/me`, `/usage`, `/requests/{id}`.
  `/moderations` exists but has no active model at the moment.
- Model ids: OpenAI, Gemini and DeepSeek direct ids have no prefix (`gpt-4o-mini`, `gemini-3.5-flash`,
  `deepseek-flash`); **Claude is available only via OpenRouter** as `openrouter/anthropic/<model>`;
  every other OpenRouter model is `openrouter/<vendor>/<model>`. Live list, no key needed:
  `GET https://netarz.ir/api/ai/v1/models?type=chat` (`type` = `chat`, `embedding`, `image`, `audio_tts`,
  `audio_stt`, `video`, `music`).
- Errors follow OpenAI's shape `{"error": {"message", "type", "code", "param"}}`; a call that fails before any output is not charged (an interrupted stream is billed for what was generated).
- Send `max_tokens`: credit for the largest possible answer is reserved before each call.
- Keep the key on your server. NetArz stores only metadata, not prompts or completions; the request body is forwarded unchanged to the upstream provider, whose own retention policy then applies.

<a id="ci-and-changelog"></a>

### CI and changelog

[CI](.github/workflows/ci.yml) checks the syntax of every example and builds the Go and .NET projects on each push and
pull request. It never calls the API and uses no key. Dependabot proposes dependency updates monthly. Release notes
are in [CHANGELOG.md](CHANGELOG.md).

<a id="links"></a>

### Links

- Service overview: [netarz.ir/ai-api](https://netarz.ir/ai-api?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=english)
- Docs: [netarz.ir/docs/ai](https://netarz.ir/docs/ai?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=english) · Migrating from OpenAI: [netarz.ir/docs/ai/migrating-from-openai](https://netarz.ir/docs/ai/migrating-from-openai?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=english)
- Models and prices: [netarz.ir/ai-api/models](https://netarz.ir/ai-api/models?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=english)
- All NetArz open-source projects: [netarz.ir/open-source](https://netarz.ir/open-source?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=english)
- Related repos: [fx-api-examples](https://github.com/netarz/fx-api-examples) (Toman exchange rate API) ·
  [netarz-fx-wordpress](https://github.com/netarz/netarz-fx-wordpress) (WordPress plugin)

Contributions are welcome: see [CONTRIBUTING.md](CONTRIBUTING.md). Report security issues privately to `dev@netarz.ir`
([SECURITY.md](SECURITY.md)). NetArz is a marketplace for buying foreign services and is not an official representative of
OpenAI, Anthropic, Google or DeepSeek. Licensed under MIT.
