# اتصال n8n به وب‌سرویس هوش مصنوعی نِت اَرز

دو راه دارید. هر دو با همان کلید `sk-ntz-v1-…` کار می‌کنند.

## راه ۱: نود HTTP Request (فایل آماده)

1. در n8n یک credential از نوع **Header Auth** بسازید:
   نام `NetArz AI key`، Name برابر `Authorization` و Value برابر `Bearer sk-ntz-v1-…`.
2. فایل [`netarz-ai-chat.workflow.json`](netarz-ai-chat.workflow.json) را با **Import from File** وارد کنید.
3. در نود «NetArz AI» همان credential را انتخاب کنید و workflow را اجرا کنید. متن جواب در نود «Answer» است.

مدل را در بدنهٔ JSON عوض کنید؛ مثلاً `openrouter/anthropic/claude-sonnet-4.5` یا `gemini-3.5-flash`.
کلید داخل فایل نیست و نباید باشد.

## راه ۲: نودهای OpenAI خودِ n8n

در **Credentials ← New ← OpenAI** کلید نِت اَرز را بگذارید و **Base URL** را
`https://netarz.ir/api/ai/v1` بنویسید. بعد نود «OpenAI Chat Model» (برای AI Agent) یا «Embeddings OpenAI»
را با همین credential به کار ببرید و شناسهٔ مدل را دستی بنویسید.

راهنمای کامل ابزارها: [netarz.ir/docs/ai/sdks](https://netarz.ir/docs/ai/sdks)

---

**English.** Two options: (1) import `netarz-ai-chat.workflow.json`, create a *Header Auth* credential
(`Authorization: Bearer sk-ntz-v1-…`) and select it on the HTTP Request node; (2) use n8n's built-in OpenAI
credential with Base URL `https://netarz.ir/api/ai/v1` and type the model id by hand. The workflow file
contains no key.
