// Ask a model about an image (vision input): a public URL or a local file as a base64 data URL.
// Only models with capabilities.vision = true in GET /models accept images.
// Run: npm install && NETARZ_API_KEY=sk-ntz-v1-... node vision.mjs [path-or-url]
// Docs: https://netarz.ir/docs/ai/chat-completions
import { readFile } from "node:fs/promises";
import { extname } from "node:path";
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: process.env.NETARZ_BASE_URL ?? "https://netarz.ir/api/ai/v1",
  apiKey: process.env.NETARZ_API_KEY,
});

const SAMPLE = "https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png";
const MIME = { ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp", ".gif": "image/gif" };

async function imageUrl(source) {
  if (/^(https?:|data:)/.test(source)) return source;
  const mime = MIME[extname(source).toLowerCase()] ?? "image/jpeg";
  return `data:${mime};base64,${(await readFile(source)).toString("base64")}`;
}

const response = await client.chat.completions.create({
  model: process.env.NETARZ_MODEL ?? "gpt-4o-mini",
  messages: [
    {
      role: "user",
      content: [
        { type: "text", text: "در این تصویر چه می‌بینید؟ در دو جمله بگویید." },
        { type: "image_url", image_url: { url: await imageUrl(process.argv[2] ?? SAMPLE) } },
      ],
    },
  ],
  max_tokens: 200,
});

console.log(response.choices[0].message.content);
console.log(`\ninput tokens (text + image): ${response.usage?.prompt_tokens}`);
