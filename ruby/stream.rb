# frozen_string_literal: true

# Streaming chat completion (Server-Sent Events), Ruby standard library only.
#
# Each event is a line "data: {...}" and the stream ends with "data: [DONE]".
# The last chunk before [DONE] carries `usage`.
#
# Run:
#   export NETARZ_API_KEY="sk-ntz-v1-..."
#   ruby stream.rb
#
# Docs: https://netarz.ir/docs/ai/streaming
require "json"
require "net/http"
require "uri"

api_key = ENV.fetch("NETARZ_API_KEY") { abort "Set NETARZ_API_KEY first" }
base_url = ENV.fetch("NETARZ_BASE_URL", "https://netarz.ir/api/ai/v1")

uri = URI("#{base_url}/chat/completions")
request = Net::HTTP::Post.new(uri)
request["Authorization"] = "Bearer #{api_key}"
request["Content-Type"] = "application/json"
request["Accept"] = "text/event-stream"
request.body = JSON.generate(
  model: ENV.fetch("NETARZ_MODEL", "gpt-4o-mini"),
  messages: [{ role: "user", content: "یک شعر کوتاه دربارهٔ پاییز بنویسید." }],
  stream: true,
  max_tokens: 200
)

$stdout.sync = true

Net::HTTP.start(uri.host, uri.port, use_ssl: uri.scheme == "https", read_timeout: 300) do |http|
  http.request(request) do |response|
    unless response.is_a?(Net::HTTPSuccess)
      abort "HTTP #{response.code}: #{response.read_body}"
    end

    buffer = +""
    response.read_body do |part|
      buffer << part.force_encoding(Encoding::UTF_8)
      # A network read can end in the middle of a line; handle whole lines only.
      while (newline = buffer.index("\n"))
        line = buffer.slice!(0..newline).strip
        next unless line.start_with?("data:")

        data = line.delete_prefix("data:").strip
        break if data == "[DONE]"

        chunk = JSON.parse(data)
        print chunk.dig("choices", 0, "delta", "content").to_s
        puts "\n\ntokens: #{chunk['usage']['total_tokens']}" if chunk["usage"]
      end
    end
  end
end
