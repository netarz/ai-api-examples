<?php

/**
 * Chat completion with plain PHP cURL, no Composer packages.
 * Works on shared hosting that only has ext-curl.
 *
 * NETARZ_API_KEY=sk-ntz-v1-... php curl-chat.php
 *
 * Docs: https://netarz.ir/docs/ai/chat-completions
 */

declare(strict_types=1);

function netarz_chat(array $messages, string $model = 'gpt-4o-mini', int $maxTokens = 300): array
{
    $apiKey = getenv('NETARZ_API_KEY');
    if (! $apiKey) {
        throw new RuntimeException('Set NETARZ_API_KEY first.');
    }

    $ch = curl_init((getenv('NETARZ_BASE_URL') ?: 'https://netarz.ir/api/ai/v1').'/chat/completions');
    curl_setopt_array($ch, [
        CURLOPT_POST => true,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT => 120,
        CURLOPT_HTTPHEADER => [
            'Authorization: Bearer '.$apiKey,
            'Content-Type: application/json',
        ],
        CURLOPT_POSTFIELDS => json_encode([
            'model' => $model,
            'messages' => $messages,
            'max_tokens' => $maxTokens,
        ], JSON_UNESCAPED_UNICODE),
    ]);

    $body = curl_exec($ch);
    $status = (int) curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
    $error = curl_error($ch);
    curl_close($ch);

    if ($body === false) {
        throw new RuntimeException('Network error: '.$error);
    }

    $json = json_decode($body, true);

    if ($status >= 400) {
        // Errors use OpenAI's shape: {"error": {"message", "type", "code", "param"}}.
        $code = $json['error']['code'] ?? 'unknown';
        throw new RuntimeException("HTTP {$status} {$code}: ".($json['error']['message'] ?? $body));
    }

    return $json;
}

$response = netarz_chat([
    ['role' => 'user', 'content' => 'سه ایده برای عنوان یک مقاله دربارهٔ خرید گیفت کارت بنویسید.'],
]);

echo $response['choices'][0]['message']['content'], PHP_EOL;
