# Changelog

All notable changes to this repository are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2026-09-28

### Added

- `go/`: chat and streaming examples using only the standard library (`net/http`), with a `go.mod`.
- `dotnet/`: a .NET 8 console app for chat and streaming with `HttpClient` and `System.Text.Json`, no NuGet dependency.
- `ruby/`: chat and streaming examples using only the standard library (`net/http`, `json`).
- `python/vision.py` and `node/vision.mjs`: image input as an `image_url` part, from a URL or a local file (base64 data URL).
- `python/rag_persian.py`: a small Persian RAG example with embeddings and cosine similarity in plain Python.
- `python/usage_and_cost.py`: reads `usage` from a response, estimates cost from `/models` prices, and reads the charged amount from `GET /requests/{id}` and `GET /usage`.
- CI workflow (`.github/workflows/ci.yml`) with syntax and build checks for Python, Node.js, PHP 8.1 to 8.4, Go, .NET, Ruby, shell scripts and JSON files. It never calls the API.
- Dependabot configuration for pip, npm, composer, gomod, nuget and GitHub Actions, checked monthly.
- This changelog.

### Changed

- README: new sections in the table of contents and the examples table, CI badge, and a reworded disclaimer.
- `.gitignore`: ignore .NET `bin/` and `obj/` folders.

## [1.0.0] - 2026-09-26

### Added

- Python examples: chat, streaming, structured output, tool calling, embeddings, images, audio, Responses API, account and models, retries and errors.
- Node.js examples: chat, streaming, structured output, tools, embeddings and a server-side proxy that keeps the key off the browser.
- PHP examples with `openai-php/client` and plain cURL (normal and streaming), and a Laravel service with an example route.
- cURL scripts for the main endpoints.
- LangChain chat and small RAG example, a Telegram bot, an n8n workflow and editor setups (Cursor, Cline, Continue).
- `providers/`: model ids and one example each for OpenAI, Claude, Gemini and DeepSeek.
- README in Persian with an English section, contributing guide, code of conduct, security policy, issue and pull request templates.

[Unreleased]: https://github.com/netarz/ai-api-examples/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/netarz/ai-api-examples/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/netarz/ai-api-examples/releases/tag/v1.0.0
