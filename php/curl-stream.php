<?php

/**
 * Streaming (SSE) with plain PHP cURL: prints tokens as they arrive.
 *
 * NETARZ_API_KEY=sk-ntz-v1-... php curl-stream.php
 *
 * Docs: https://netarz.ir/docs/ai/streaming
 */

declare(strict_types=1);

$apiKey = getenv('NETARZ_API_KEY') ?: exit("Set NETARZ_API_KEY first.\n");
$buffer = '';

$ch = curl_init((getenv('NETARZ_BASE_URL') ?: 'https://netarz.ir/api/ai/v1').'/chat/completions');
curl_setopt_array($ch, [
    CURLOPT_POST => true,
    CURLOPT_TIMEOUT => 120,
    CURLOPT_HTTPHEADER => [
        'Authorization: Bearer '.$apiKey,
        'Content-Type: application/json',
        'Accept: text/event-stream',
    ],
    CURLOPT_POSTFIELDS => json_encode([
        'model' => getenv('NETARZ_MODEL') ?: 'gpt-4o-mini',
        'messages' => [['role' => 'user', 'content' => 'یک شعر کوتاه دربارهٔ پاییز بنویسید.']],
        'max_tokens' => 200,
        'stream' => true,
    ], JSON_UNESCAPED_UNICODE),
    CURLOPT_WRITEFUNCTION => function ($ch, string $chunk) use (&$buffer): int {
        $buffer .= $chunk;

        // Events are separated by a blank line: "data: {...}\n\n".
        while (($pos = strpos($buffer, "\n\n")) !== false) {
            $event = trim(substr($buffer, 0, $pos));
            $buffer = substr($buffer, $pos + 2);

            if (! str_starts_with($event, 'data:')) {
                continue;
            }

            $data = trim(substr($event, 5));
            if ($data === '[DONE]') {
                continue;
            }

            $json = json_decode($data, true);

            if (isset($json['error'])) {
                // A mid-stream failure arrives as an event, not an HTTP status.
                fwrite(STDERR, PHP_EOL.'stream error: '.$json['error']['code'].PHP_EOL);
                continue;
            }

            echo $json['choices'][0]['delta']['content'] ?? '';

            if (! empty($json['usage'])) {
                echo PHP_EOL.PHP_EOL.'tokens: '.$json['usage']['total_tokens'].PHP_EOL;
            }
        }

        return strlen($chunk);
    },
]);

curl_exec($ch);

$status = (int) curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
if ($status >= 400) {
    // On an HTTP error the body is plain JSON, not SSE; it is left in $buffer.
    fwrite(STDERR, "HTTP {$status}: {$buffer}".PHP_EOL);
}
curl_close($ch);
