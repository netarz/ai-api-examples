// Function calling (tools). Works the same for GPT, Gemini, DeepSeek and
// Claude via OpenRouter ids: the gateway translates the format.
// Docs: https://netarz.ir/docs/ai/chat-completions
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: process.env.NETARZ_BASE_URL ?? "https://netarz.ir/api/ai/v1",
  apiKey: process.env.NETARZ_API_KEY,
});
const model = process.env.NETARZ_MODEL ?? "gpt-4.1-mini";

// Your own function; a stub here.
const getOrderStatus = ({ order_number }) => ({ order_number, status: "delivered", delivered_at: "2026-08-29" });

const tools = [
  {
    type: "function",
    function: {
      name: "get_order_status",
      description: "وضعیت یک سفارش را با شمارهٔ سفارش برمی‌گرداند.",
      parameters: {
        type: "object",
        properties: { order_number: { type: "string" } },
        required: ["order_number"],
      },
    },
  },
];

const messages = [{ role: "user", content: "سفارش NZ-10422 در چه وضعیتی است؟" }];

const first = await client.chat.completions.create({ model, messages, tools, max_tokens: 300 });
const reply = first.choices[0].message;

if (!reply.tool_calls?.length) {
  console.log(reply.content);
  process.exit(0);
}

messages.push(reply);
for (const call of reply.tool_calls) {
  const args = JSON.parse(call.function.arguments || "{}");
  const result = call.function.name === "get_order_status" ? getOrderStatus(args) : { error: "unknown tool" };
  messages.push({ role: "tool", tool_call_id: call.id, content: JSON.stringify(result) });
}

const final = await client.chat.completions.create({ model, messages, tools, max_tokens: 300 });
console.log(final.choices[0].message.content);
