// Embeddings + cosine similarity, no dependencies beyond the SDK.
// Docs: https://netarz.ir/docs/ai/embeddings
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: process.env.NETARZ_BASE_URL ?? "https://netarz.ir/api/ai/v1",
  apiKey: process.env.NETARZ_API_KEY,
});
const MODEL = "text-embedding-3-small";

const docs = [
  "برای تحویل سفارش، یک بار احراز هویت لازم است.",
  "کش‌بک بعد از تکمیل سفارش حساب می‌شود.",
  "کلید API را فقط روی سرور نگه دارید.",
];

const embed = async (input) => (await client.embeddings.create({ model: MODEL, input })).data.map((d) => d.embedding);
const cosine = (a, b) => {
  let dot = 0, na = 0, nb = 0;
  for (let i = 0; i < a.length; i++) { dot += a[i] * b[i]; na += a[i] ** 2; nb += b[i] ** 2; }
  return dot / (Math.sqrt(na) * Math.sqrt(nb));
};

const docVectors = await embed(docs);
const [query] = await embed(["کلیدم را کجا بگذارم؟"]);
const best = docs
  .map((text, i) => ({ text, score: cosine(query, docVectors[i]) }))
  .sort((a, b) => b.score - a.score)[0];

console.log("best match:", best.text, best.score.toFixed(3));
