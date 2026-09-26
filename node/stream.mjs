// Streaming chat completion. The last chunk carries `usage`.
// Docs: https://netarz.ir/docs/ai/streaming
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: process.env.NETARZ_BASE_URL ?? "https://netarz.ir/api/ai/v1",
  apiKey: process.env.NETARZ_API_KEY,
  timeout: 120_000,
});

const stream = await client.chat.completions.create({
  model: process.env.NETARZ_MODEL ?? "gpt-4o-mini",
  messages: [{ role: "user", content: "یک شعر کوتاه دربارهٔ پاییز بنویسید." }],
  stream: true,
  max_tokens: 200,
});

for await (const chunk of stream) {
  process.stdout.write(chunk.choices[0]?.delta?.content ?? "");
  if (chunk.usage) console.log(`\n\ntokens: ${chunk.usage.total_tokens}`);
}
