# شناسهٔ مدل‌ها به تفکیک سازنده: API OpenAI، کلود، جمینای و دیپ‌سیک

روی درگاه نِت اَرز همهٔ سازنده‌ها با یک کلید و یک نشانی کار می‌کنند؛ فقط مقدار `model` عوض می‌شود.
ولی شکل شناسه برای هر سازنده قاعدهٔ خودش را دارد و بیشتر خطاهای ۴۰۴ از همین‌جاست.

| سازنده | نمونهٔ شناسه | قاعده | نمونه‌کد | صفحه در نِت اَرز |
|---|---|---|---|---|
| OpenAI (GPT) | `gpt-4o-mini`، `gpt-4.1-mini`، `gpt-5-mini` | بدون پیشوند. مدل‌های Pro و Codex (مثل `gpt-5.4-pro`) فقط با مسیر `/responses` جواب می‌دهند | [openai/chat.py](openai/chat.py) | [API OpenAI در ایران](https://netarz.ir/ai-api/openai?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=providers-readme) |
| Anthropic (Claude) | `openrouter/anthropic/claude-sonnet-4.5`، `openrouter/anthropic/claude-haiku-4.5` | **فقط از راه OpenRouter**؛ بدون پیشوند `openrouter/anthropic/` پیدا نمی‌شود. کتابخانهٔ Anthropic و مسیر `/v1/messages` روی درگاه کار نمی‌کند | [claude/chat.py](claude/chat.py) | [API کلود](https://netarz.ir/ai-api/claude?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=providers-readme) |
| Google (Gemini) | `gemini-3.5-flash`، `gemini-3.1-flash-lite`، `gemini-embedding-001` | بدون پیشوند. همتای همین مدل‌ها با `openrouter/google/` هم هست. مدل‌های تصویرساز گوگل (Imagen) روی درگاه نیست | [gemini/chat.py](gemini/chat.py) | [API جمینای](https://netarz.ir/ai-api/gemini?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=providers-readme) |
| DeepSeek | `deepseek-flash`، `deepseek-v4-pro` | این دو مستقیم وصل‌اند؛ بقیه (مثل R1) با پیشوند `openrouter/deepseek/` | [deepseek/chat.py](deepseek/chat.py) | [API دیپ‌سیک](https://netarz.ir/ai-api/deepseek?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=providers-readme) |
| مدل‌های دیگر OpenRouter | `openrouter/meta-llama/llama-3.3-70b-instruct` | `openrouter/` + شناسهٔ خودِ OpenRouter | همان کد بالا | [فهرست مدل‌ها](https://netarz.ir/ai-api/models?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=providers-readme) |

شناسه‌های بالا را هنگام نوشتن این راهنما از فهرست زندهٔ درگاه برداشته‌ایم. مدل‌ها اضافه و کم می‌شوند؛
فهرست همین لحظه را بدون کلید از این نشانی بگیرید:

```bash
curl "https://netarz.ir/api/ai/v1/models?type=chat"
```

در پاسخ، برای هر مدل `capabilities` آمده (tools، json، vision، reasoning، streaming). پیش از این‌که
ابزار (tools) یا خروجی JSON را روی مدلی امتحان کنید، همین‌جا ببینید پشتیبانی می‌کند یا نه.
قیمت دلاری و تومانی هر مدل در [صفحهٔ مدل‌ها](https://netarz.ir/ai-api/models?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=providers-readme) است.

---

## Model ids per provider (English)

One key and one base URL for every provider; only `model` changes. The id format differs per provider:

| Provider | Example ids | Rule |
|---|---|---|
| OpenAI | `gpt-4o-mini`, `gpt-4.1-mini`, `gpt-5-mini` | No prefix. Pro/Codex models (e.g. `gpt-5.4-pro`) answer only on `/responses`. |
| Anthropic Claude | `openrouter/anthropic/claude-sonnet-4.5` | **Only via OpenRouter**; the `openrouter/anthropic/` prefix is required. The Anthropic SDK and `/v1/messages` are not supported, use Chat Completions. |
| Google Gemini | `gemini-3.5-flash`, `gemini-embedding-001` | No prefix; OpenRouter twins exist as `openrouter/google/...`. No Imagen image models. |
| DeepSeek | `deepseek-flash`, `deepseek-v4-pro` | Direct; other DeepSeek models (R1) use `openrouter/deepseek/...`. |
| Other OpenRouter models | `openrouter/meta-llama/llama-3.3-70b-instruct` | `openrouter/` + the OpenRouter id. |

Ids were taken from the live catalogue when this was written. Always check `GET https://netarz.ir/api/ai/v1/models` (no key needed) or [netarz.ir/ai-api/models](https://netarz.ir/ai-api/models?utm_source=github&utm_medium=referral&utm_campaign=ai-api-examples&utm_content=providers-readme).
