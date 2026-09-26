// Basic chat completion through the NetArz AI gateway.
// Run: npm install && NETARZ_API_KEY=sk-ntz-v1-... node chat.mjs
// Docs: https://netarz.ir/docs/ai/chat-completions
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: process.env.NETARZ_BASE_URL ?? "https://netarz.ir/api/ai/v1",
  apiKey: process.env.NETARZ_API_KEY,
});

// Any id from https://netarz.ir/ai-api/models, e.g.
// "openrouter/anthropic/claude-sonnet-4.5", "gemini-3.5-flash", "deepseek-flash".
const model = process.env.NETARZ_MODEL ?? "gpt-4o-mini";

const response = await client.chat.completions.create({
  model,
  messages: [
    { role: "system", content: "شما دستیار فارسی‌زبان یک فروشگاه اینترنتی هستید. کوتاه و دقیق جواب بدهید." },
    { role: "user", content: "برای یک فروشگاه لوازم ورزشی یک شعار کوتاه بنویسید." },
  ],
  max_tokens: 200, // keeps the credit reservation small
});

console.log(response.choices[0].message.content);
console.log(`\nrequest id: ${response.id} | tokens: ${response.usage?.total_tokens}`);
