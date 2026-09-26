// Strict JSON Schema output (use an OpenAI model for the schema form).
// Docs: https://netarz.ir/docs/ai/chat-completions
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: process.env.NETARZ_BASE_URL ?? "https://netarz.ir/api/ai/v1",
  apiKey: process.env.NETARZ_API_KEY,
});

const response = await client.chat.completions.create({
  model: "gpt-4o-mini",
  response_format: {
    type: "json_schema",
    json_schema: {
      name: "ticket_triage",
      strict: true,
      schema: {
        type: "object",
        properties: {
          topic: { type: "string", enum: ["payment", "delivery", "account", "other"] },
          urgent: { type: "boolean" },
          summary: { type: "string" },
        },
        required: ["topic", "urgent", "summary"],
        additionalProperties: false,
      },
    },
  },
  messages: [
    { role: "system", content: "پیام مشتری را دسته‌بندی کنید." },
    { role: "user", content: "پول از کارتم کم شد ولی سفارشم هنوز «در انتظار پرداخت» است." },
  ],
  max_tokens: 200,
});

const triage = JSON.parse(response.choices[0].message.content);
console.log(triage);
