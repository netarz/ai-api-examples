# نمونه‌کد وب‌سرویس هوش مصنوعی (API) نِت اَرز

نمونه‌کدهای آماده برای وصل شدن به **API هوش مصنوعی نِت اَرز** (وب سرویس هوش مصنوعی): یک نشانی سازگار با OpenAI که با یک کلید،
مدل‌های GPT، Claude، Gemini و DeepSeek را صدا می‌زند. اعتبار را به تومان می‌خرید و هزینهٔ هر درخواست
به دلار از همان اعتبار کم می‌شود؛ کارت ارزی لازم نیست.

اگر با کتابخانهٔ رسمی OpenAI کار کرده‌اید، کد شما تقریباً همان است. فقط دو مقدار عوض می‌شود:

| مقدار | در OpenAI | در نِت اَرز |
|---|---|---|
| نشانی پایه (base URL) | `https://api.openai.com/v1` | `https://netarz.ir/api/ai/v1` |
| کلید دسترسی (API Key) | `sk-proj-…` | `sk-ntz-v1-…` |

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

معرفی سرویس: [netarz.ir/ai-api](https://netarz.ir/ai-api) · مستندات کامل: [netarz.ir/docs/ai](https://netarz.ir/docs/ai)

## پیش از اجرای نمونه‌ها

1. در [نِت اَرز](https://netarz.ir) ثبت‌نام کنید و از پنل [/ai](https://netarz.ir/ai) اعتبار بخرید.
   حداقل مبلغ شارژ و مالیات بر ارزش افزوده را پیش از پرداخت می‌بینید.
2. در همان پنل یک پروژه و برای آن یک کلید بسازید. کلید کامل را فقط همان یک بار می‌بینید.
3. کلید را در متغیر محیطی بگذارید (فایل `.env.example` را ببینید):

```bash
export NETARZ_API_KEY="sk-ntz-v1-..."
```

در هیچ فایلی از این مخزن کلید واقعی نیست. کلید خودتان را هم در گیت کامیت نکنید.

## فهرست نمونه‌ها

| پوشه / فایل | چه کاری می‌کند | راهنمای مربوط |
|---|---|---|
| [`python/chat.py`](python/chat.py) | گفت‌وگوی ساده با کتابخانهٔ `openai` | [Chat Completions](https://netarz.ir/docs/ai/chat-completions) |
| [`python/stream.py`](python/stream.py) · [`node/stream.mjs`](node/stream.mjs) · [`curl/stream.sh`](curl/stream.sh) | پاسخ تکه‌به‌تکه (استریم، SSE) | [استریم](https://netarz.ir/docs/ai/streaming) |
| [`python/structured_output.py`](python/structured_output.py) · [`node/structured-output.mjs`](node/structured-output.mjs) | خروجی JSON و JSON Schema | [Chat Completions](https://netarz.ir/docs/ai/chat-completions) |
| [`python/tool_calling.py`](python/tool_calling.py) · [`node/tools.mjs`](node/tools.mjs) | فراخوانی تابع (tools) با چرخهٔ کامل | [Chat Completions](https://netarz.ir/docs/ai/chat-completions) |
| [`python/embeddings.py`](python/embeddings.py) · [`node/embeddings.mjs`](node/embeddings.mjs) | امبدینگ و جست‌وجوی معنایی ساده | [امبدینگ](https://netarz.ir/docs/ai/embeddings) |
| [`python/images.py`](python/images.py) | ساخت تصویر با مدل‌های GPT Image | [تصویر](https://netarz.ir/docs/ai/images) |
| [`python/audio.py`](python/audio.py) | متن به گفتار و گفتار به متن | [صوت](https://netarz.ir/docs/ai/audio) |
| [`python/responses_api.py`](python/responses_api.py) | Responses API (فقط مدل‌های OpenAI) | [Responses API](https://netarz.ir/docs/ai/responses-api) |
| [`python/account_and_models.py`](python/account_and_models.py) · [`curl/models-and-account.sh`](curl/models-and-account.sh) | فهرست مدل‌ها (بدون کلید) و موجودی حساب | [احراز هویت](https://netarz.ir/docs/ai/authentication) |
| [`python/retry_and_errors.py`](python/retry_and_errors.py) | مدیریت خطا و تلاش دوباره | [خطاها](https://netarz.ir/docs/ai/errors) |
| [`node/`](node/) | همین نمونه‌ها با Node.js، به‌علاوهٔ [`server-proxy.mjs`](node/server-proxy.mjs) که کلید را روی سرور نگه می‌دارد | [SDKها](https://netarz.ir/docs/ai/sdks) |
| [`php/`](php/) | `openai-php/client`، و cURL خالص برای هاست اشتراکی (معمولی و استریم) | [SDKها](https://netarz.ir/docs/ai/sdks) |
| [`laravel/`](laravel/) | سرویس `NetArzAi` با Http لاراول و یک route نمونه | [SDKها](https://netarz.ir/docs/ai/sdks) |
| [`curl/`](curl/) | همهٔ endpointهای اصلی با cURL | [مرجع تعاملی](https://netarz.ir/docs/ai/reference) |
| [`langchain/`](langchain/) | LangChain پایتون: گفت‌وگو، عوض کردن مدل، RAG کوچک | [SDKها](https://netarz.ir/docs/ai/sdks) |
| [`telegram-bot/`](telegram-bot/) | ربات تلگرام که با مدل جواب می‌دهد | [راهنمای ربات تلگرام](https://netarz.ir/wiki/ai-telegram-bot-webservice) |
| [`integrations/n8n/`](integrations/n8n/) | workflow آمادهٔ n8n | [SDKها](https://netarz.ir/docs/ai/sdks) |
| [`integrations/editors/`](integrations/editors/) | Cursor، Cline و Continue | [SDKها](https://netarz.ir/docs/ai/sdks) |
| [`providers/`](providers/) | شناسهٔ مدل‌های OpenAI، Claude، Gemini و DeepSeek با یک نمونه برای هر کدام | [مدل‌ها و قیمت‌ها](https://netarz.ir/docs/ai/models-and-pricing) |

## یک کلید، چهار سازنده

| سازنده | شناسهٔ نمونه | نکته | صفحه |
|---|---|---|---|
| OpenAI | `gpt-4o-mini` | مدل‌های Pro و Codex فقط با `/responses` | [API OpenAI در ایران](https://netarz.ir/ai-api/openai) |
| Claude | `openrouter/anthropic/claude-sonnet-4.5` | فقط با پیشوند `openrouter/anthropic/`؛ کتابخانهٔ Anthropic کار نمی‌کند | [API کلود](https://netarz.ir/ai-api/claude) |
| Gemini | `gemini-3.5-flash` | Imagen (تصویرساز گوگل) روی درگاه نیست | [API جمینای](https://netarz.ir/ai-api/gemini) |
| DeepSeek | `deepseek-flash` | R1 و بقیه با پیشوند `openrouter/deepseek/` | [API دیپ‌سیک](https://netarz.ir/ai-api/deepseek) |

جزئیات و قاعدهٔ شناسه‌ها در [`providers/README.md`](providers/README.md). فهرست زندهٔ مدل‌ها را بدون کلید بگیرید:
`curl "https://netarz.ir/api/ai/v1/models?type=chat"`. قیمت هر مدل به دلار و تومان در
[صفحهٔ مدل‌ها](https://netarz.ir/ai-api/models) است.

## هزینه را کنترل کنید

- **همیشه `max_tokens` بفرستید.** پیش از هر درخواست، درگاه مبلغ بلندترین جواب ممکن را از اعتبار شما کنار می‌گذارد؛
  با `max_tokens` این مبلغ کوچک می‌شود و با موجودی کم به خطای `insufficient_credit` نمی‌خورید. بعد از جواب،
  فقط مصرف واقعی کم می‌شود.
- درخواستی که پیش از تولید جواب با خطا تمام شود هزینه ندارد. اگر استریم وسط کار قطع شود، فقط آنچه تا آن لحظه تولید شده حساب می‌شود.
- برای هر کلید سقف هزینه و برای هر پروژه بودجهٔ ماهانه بگذارید تا یک باگ یا کلید لورفته کل اعتبار را خرج نکند.
- برای جواب‌های طولانی و مدل‌های استدلالی از استریم استفاده کنید تا اتصال وسط کار قطع نشود.

## کلید را کجا نگه دارید

کلید `sk-ntz-v1-…` را **فقط روی سرور** نگه دارید؛ نه در کد مرورگر، نه در اپ موبایل، نه در مخزن عمومی.
هر کسی کلید را ببیند می‌تواند با اعتبار شما درخواست بفرستد. الگوی درست: مرورگر یا اپ به سرور خودتان
درخواست می‌دهد و سرور شما با کلید به نِت اَرز وصل می‌شود ([`node/server-proxy.mjs`](node/server-proxy.mjs)،
[`laravel/routes-example.php`](laravel/routes-example.php)). برای کلیدهای سرور، فهرست IPهای مجاز را هم در پنل پر کنید.

## خطاهای رایج

| کد | یعنی | چه کنید |
|---|---|---|
| `401 missing_api_key` / `invalid_api_key` | کلید نرسیده یا اشتباه است | هدر `Authorization: Bearer sk-ntz-v1-…` را بررسی کنید |
| `402 insufficient_credit` | اعتبار برای رزرو این درخواست کافی نیست | شارژ کنید یا `max_tokens` را کم کنید |
| `403 model_not_allowed` | مدل در فهرست مجاز کلید یا پروژه نیست | هر دو فهرست را در پنل ببینید |
| `404 model_not_found` | شناسهٔ مدل پیدا نشد | برای Claude پیشوند `openrouter/anthropic/` را بگذارید |
| `429 rate_limit_exceeded` | بیش از سقف درخواست در دقیقه | به اندازهٔ `Retry-After` صبر کنید؛ سقف کلید را `GET /me` نشان می‌دهد |

فهرست کامل: [netarz.ir/docs/ai/errors](https://netarz.ir/docs/ai/errors)

## پرسش‌های رایج

**با کتابخانهٔ Anthropic یا مسیر `/v1/messages` کار می‌کند؟**
نه. Claude را با کتابخانهٔ OpenAI و مسیر `/chat/completions` صدا بزنید؛ تبدیل درخواست به قالب Claude با شما نیست.

**مدل رایگان دارید؟**
نه. مدل‌های رایگان روی ظرفیت مشترک ارائه‌دهنده بودند و وسط کار خطا می‌دادند، پس آن‌ها را برداشتیم. قیمت هر مدل را در [صفحهٔ مدل‌ها](https://netarz.ir/ai-api/models) ببینید و مدلی را که به بودجهٔ پروژه‌تان می‌خورد انتخاب کنید.

**متن پیام‌هایم جایی ذخیره می‌شود؟**
درگاه فقط فراداده ثبت می‌کند، مثل مدل، تعداد توکن، هزینه، وضعیت و زمان. متن پیام‌ها و جواب‌ها در نِت اَرز ذخیره نمی‌شود. بدنهٔ درخواست بدون تغییر به سرویس‌دهندهٔ اصلی (مثل OpenAI، گوگل، DeepSeek یا OpenRouter) می‌رود و از آن‌جا سیاست نگهداری داده‌های همان شرکت حاکم است.
جزئیات: [حریم خصوصی داده در API هوش مصنوعی](https://netarz.ir/wiki/ai-api-privacy-iran)

**برنامه‌نویس نیستم؛ فقط می‌خواهم با مدل‌ها گفت‌وگو کنم.**
وب‌سرویس برای وصل کردن سایت، اپ یا ربات است. برای گفت‌وگو در مرورگر [استودیو هوش مصنوعی](https://netarz.ir/ai-studio) را ببینید.

## پشتیبانی

- اشکال در کد همین مخزن: بخش Issues.
- حساب، اعتبار و کلید: تیکت از پنل نِت اَرز یا ایمیل `support@netarz.ir`.

«نِت اَرز» واسط خرید است و نمایندهٔ رسمی OpenAI، Anthropic، Google یا DeepSeek نیست. نام‌ها و نشان‌های این شرکت‌ها
متعلق به خودشان است.

مجوز: [MIT](LICENSE)

---

## English

**NetArz AI API examples.** Ready-to-run code for the NetArz AI gateway, an OpenAI-compatible API that lets
developers in Iran call GPT, Claude, Gemini and DeepSeek models with one key, paying from credit bought in Toman.

- Base URL: `https://netarz.ir/api/ai/v1`
- Auth: `Authorization: Bearer sk-ntz-v1-…` (or `X-API-Key`)
- Works with the official OpenAI SDKs (Python, Node), `openai-php/client`, LangChain, n8n, Continue, Cline, Cursor.
- Endpoints: `/chat/completions`, `/completions`, `/responses` (OpenAI models only), `/embeddings`,
  `/images/generations`, `/audio/speech`, `/audio/transcriptions`, `/audio/translations`, `/models`, `/me`, `/usage`.
- Model ids: OpenAI and Gemini and DeepSeek direct ids have no prefix (`gpt-4o-mini`, `gemini-3.5-flash`,
  `deepseek-flash`); **Claude is available only via OpenRouter** as `openrouter/anthropic/<model>`;
  every other OpenRouter model is `openrouter/<vendor>/<model>`. Live list, no key needed:
  `GET https://netarz.ir/api/ai/v1/models?type=chat`.
- Errors follow OpenAI's shape `{"error": {"message", "type", "code", "param"}}`; a call that fails before any output is not charged (an interrupted stream is billed for what was generated).
- Send `max_tokens`: credit for the largest possible answer is reserved before each call.
- Keep the key on your server. NetArz stores only metadata, not prompts or completions; the request body is forwarded unchanged to the upstream provider, whose own retention policy then applies.

Run any example with `NETARZ_API_KEY` set. See the table above for the file list; each file links to its docs page.
Docs: <https://netarz.ir/docs/ai> · Models and prices: <https://netarz.ir/ai-api/models> · Service: <https://netarz.ir/ai-api>

NetArz is an independent reseller, not an official partner of OpenAI, Anthropic, Google or DeepSeek.
Licensed under MIT.
