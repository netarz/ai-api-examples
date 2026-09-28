# frozen_string_literal: true

# Basic chat completion through the NetArz AI gateway, Ruby standard library only.
#
# Run:
#   export NETARZ_API_KEY="sk-ntz-v1-..."
#   ruby chat.rb
#
# Docs: https://netarz.ir/docs/ai/chat-completions
require "json"
require "net/http"
require "uri"

api_key = ENV.fetch("NETARZ_API_KEY") { abort "Set NETARZ_API_KEY first" }
base_url = ENV.fetch("NETARZ_BASE_URL", "https://netarz.ir/api/ai/v1")
# Any id from https://netarz.ir/ai-api/models, e.g.
# "openrouter/anthropic/claude-sonnet-4.5", "gemini-3.5-flash", "deepseek-flash".
model = ENV.fetch("NETARZ_MODEL", "gpt-4o-mini")

uri = URI("#{base_url}/chat/completions")
request = Net::HTTP::Post.new(uri)
request["Authorization"] = "Bearer #{api_key}"
request["Content-Type"] = "application/json"
request.body = JSON.generate(
  model: model,
  messages: [
    { role: "system", content: "شما دستیار فارسی‌زبان یک فروشگاه اینترنتی هستید. کوتاه و دقیق جواب بدهید." },
    { role: "user", content: "برای یک فروشگاه لوازم ورزشی یک شعار کوتاه بنویسید." }
  ],
  # Always send max_tokens: the gateway reserves credit for the largest
  # possible answer before the call, so a cap keeps that reservation small.
  max_tokens: 200
)

response = Net::HTTP.start(uri.host, uri.port, use_ssl: uri.scheme == "https", read_timeout: 120) do |http|
  http.request(request)
end

body = JSON.parse(response.body)
unless response.is_a?(Net::HTTPSuccess)
  # Errors follow OpenAI's shape: {"error": {"message", "type", "code", "param"}}.
  error = body.fetch("error", {})
  abort "HTTP #{response.code} #{error['code']}: #{error['message']}"
end

puts body.dig("choices", 0, "message", "content")
# "id" is the NetArz request id (same as the X-Request-Id header).
puts "\nrequest id: #{body['id']} | tokens: #{body.dig('usage', 'total_tokens')}"
