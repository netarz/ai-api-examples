// Chat and streaming through the NetArz AI gateway with HttpClient and System.Text.Json.
// No NuGet package is needed; the official OpenAI .NET package also works if you set its
// endpoint to https://netarz.ir/api/ai/v1.
//
// Run:
//   export NETARZ_API_KEY="sk-ntz-v1-..."
//   dotnet run            # plain chat completion
//   dotnet run -- stream  # streaming (Server-Sent Events)
//
// Docs: https://netarz.ir/docs/ai/chat-completions
//       https://netarz.ir/docs/ai/streaming
using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;
using System.Text.Json.Nodes;

var apiKey = Environment.GetEnvironmentVariable("NETARZ_API_KEY");
if (string.IsNullOrEmpty(apiKey))
{
    Console.Error.WriteLine("Set NETARZ_API_KEY first");
    return 1;
}

var baseUrl = Environment.GetEnvironmentVariable("NETARZ_BASE_URL") ?? "https://netarz.ir/api/ai/v1";
// Any id from https://netarz.ir/ai-api/models, e.g.
// "openrouter/anthropic/claude-sonnet-4.5", "gemini-3.5-flash", "deepseek-flash".
var model = Environment.GetEnvironmentVariable("NETARZ_MODEL") ?? "gpt-4o-mini";
var stream = args.Length > 0 && args[0] == "stream";

Console.OutputEncoding = Encoding.UTF8;

using var http = new HttpClient { Timeout = TimeSpan.FromMinutes(5) };
http.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", apiKey);

var payload = new JsonObject
{
    ["model"] = model,
    ["messages"] = new JsonArray
    {
        new JsonObject
        {
            ["role"] = "system",
            ["content"] = "شما دستیار فارسی‌زبان یک فروشگاه اینترنتی هستید. کوتاه و دقیق جواب بدهید.",
        },
        new JsonObject
        {
            ["role"] = "user",
            ["content"] = "برای یک فروشگاه لوازم ورزشی یک شعار کوتاه بنویسید.",
        },
    },
    // Always send max_tokens: the gateway reserves credit for the largest
    // possible answer before the call, so a cap keeps that reservation small.
    ["max_tokens"] = 200,
    ["stream"] = stream,
};

using var request = new HttpRequestMessage(HttpMethod.Post, $"{baseUrl}/chat/completions")
{
    Content = new StringContent(payload.ToJsonString(), Encoding.UTF8, "application/json"),
};

// ResponseHeadersRead lets us read the stream as it arrives instead of buffering it.
using var response = await http.SendAsync(request, HttpCompletionOption.ResponseHeadersRead);

if (!response.IsSuccessStatusCode)
{
    // Errors follow OpenAI's shape: {"error": {"message", "type", "code", "param"}}.
    var errorBody = await response.Content.ReadAsStringAsync();
    var error = JsonNode.Parse(errorBody)?["error"];
    Console.Error.WriteLine($"HTTP {(int)response.StatusCode} {error?["code"]}: {error?["message"]}");
    return 1;
}

if (!stream)
{
    var json = JsonNode.Parse(await response.Content.ReadAsStringAsync())!;
    Console.WriteLine(json["choices"]![0]!["message"]!["content"]);
    // "id" is the NetArz request id (same as the X-Request-Id header).
    Console.WriteLine($"\nrequest id: {json["id"]} | tokens: {json["usage"]?["total_tokens"]}");
    return 0;
}

// Each event is a line "data: {...}"; the stream ends with "data: [DONE]".
// The last chunk before [DONE] carries `usage`.
using var reader = new StreamReader(await response.Content.ReadAsStreamAsync());
while (await reader.ReadLineAsync() is { } line)
{
    if (!line.StartsWith("data:", StringComparison.Ordinal))
    {
        continue; // blank separators and ": keep-alive" comments
    }

    var data = line["data:".Length..].Trim();
    if (data == "[DONE]")
    {
        break;
    }

    JsonNode? chunk;
    try
    {
        chunk = JsonNode.Parse(data);
    }
    catch (JsonException)
    {
        continue;
    }

    var choices = chunk?["choices"]?.AsArray();
    if (choices is { Count: > 0 })
    {
        Console.Write(choices[0]?["delta"]?["content"]?.GetValue<string>());
    }

    if (chunk?["usage"] is JsonObject usage)
    {
        Console.WriteLine($"\n\ntokens: {usage["total_tokens"]}");
    }
}

return 0;
