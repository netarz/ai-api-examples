<?php

namespace App\Services;

use Illuminate\Http\Client\RequestException;
use Illuminate\Support\Facades\Http;

/**
 * A thin Laravel wrapper around the NetArz AI gateway (OpenAI-compatible).
 *
 * Needs only the framework's Http client. Configure in config/services.php:
 *
 *     'netarz_ai' => [
 *         'key' => env('NETARZ_API_KEY'),
 *         'base_url' => env('NETARZ_BASE_URL', 'https://netarz.ir/api/ai/v1'),
 *         'model' => env('NETARZ_MODEL', 'gpt-4o-mini'),
 *     ],
 *
 * Docs: https://netarz.ir/docs/ai/sdks
 */
class NetArzAi
{
    /**
     * One chat turn. Returns the assistant's text.
     *
     * @param  array<int, array{role: string, content: mixed}>  $messages
     *
     * @throws RequestException on 4xx/5xx (read $e->response->json('error.code'))
     */
    public function chat(array $messages, ?string $model = null, int $maxTokens = 500): string
    {
        return (string) $this->request()
            ->post('/chat/completions', [
                'model' => $model ?? config('services.netarz_ai.model'),
                'messages' => $messages,
                'max_tokens' => $maxTokens,
            ])
            ->throw()
            ->json('choices.0.message.content');
    }

    /**
     * Embeddings for one or many texts.
     *
     * @param  string|array<int, string>  $input
     * @return array<int, array<int, float>>
     */
    public function embed(string|array $input, string $model = 'text-embedding-3-small'): array
    {
        $data = $this->request()
            ->post('/embeddings', ['model' => $model, 'input' => $input])
            ->throw()
            ->json('data');

        return array_map(fn (array $row) => $row['embedding'], $data);
    }

    /** Balance and the key's effective limits (GET /me). */
    public function me(): array
    {
        return $this->request()->get('/me')->throw()->json();
    }

    private function request()
    {
        return Http::baseUrl(rtrim((string) config('services.netarz_ai.base_url'), '/'))
            ->withToken((string) config('services.netarz_ai.key'))
            ->acceptJson()
            ->timeout(120)
            // Retry only what is safe to retry: 429 and provider-side 5xx.
            // A 402 (credit) or 4xx will not get better by trying again.
            ->retry(2, 1000, function ($exception) {
                $status = $exception instanceof RequestException ? $exception->response->status() : 0;

                return $status === 429 || $status >= 500;
            }, throw: true);
    }
}
