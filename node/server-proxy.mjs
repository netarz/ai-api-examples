// A minimal server-side proxy so the API key never reaches the browser.
//
// The browser calls POST /api/chat on YOUR server with {"message": "..."};
// this server adds the key, picks the model, caps max_tokens, and streams the
// answer back as plain text. Put your own auth and per-user limits in front
// of it before going live.
//
// Run: NETARZ_API_KEY=sk-ntz-v1-... node server-proxy.mjs
// Test: curl -N -X POST localhost:3000/api/chat -H 'Content-Type: application/json' -d '{"message":"سلام"}'
import http from "node:http";
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: process.env.NETARZ_BASE_URL ?? "https://netarz.ir/api/ai/v1",
  apiKey: process.env.NETARZ_API_KEY,
  timeout: 90_000,
});
const MODEL = process.env.NETARZ_MODEL ?? "gpt-4o-mini";
const PORT = Number(process.env.PORT ?? 3000);

async function readJson(req) {
  let raw = "";
  for await (const part of req) {
    raw += part;
    if (raw.length > 16_384) throw new Error("body too large");
  }
  return JSON.parse(raw || "{}");
}

http
  .createServer(async (req, res) => {
    if (req.method !== "POST" || req.url !== "/api/chat") {
      res.writeHead(404).end();
      return;
    }

    let message;
    try {
      ({ message } = await readJson(req));
    } catch {
      res.writeHead(400).end("invalid JSON");
      return;
    }
    if (typeof message !== "string" || !message.trim()) {
      res.writeHead(422).end("message is required");
      return;
    }

    try {
      const stream = await client.chat.completions.create({
        model: MODEL,
        messages: [{ role: "user", content: message.slice(0, 4000) }],
        max_tokens: 500,
        stream: true,
      });
      res.writeHead(200, { "Content-Type": "text/plain; charset=utf-8", "Cache-Control": "no-cache" });
      for await (const chunk of stream) res.write(chunk.choices[0]?.delta?.content ?? "");
      res.end();
    } catch (err) {
      // Log err.status / err.error?.code on your side; do not leak details to visitors.
      console.error(err.status, err.error?.code ?? err.message);
      if (!res.headersSent) res.writeHead(502);
      res.end("upstream error");
    }
  })
  .listen(PORT, () => console.log(`proxy on http://localhost:${PORT}/api/chat`));
