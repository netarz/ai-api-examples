<?php

/**
 * Chat completion with openai-php/client pointed at the NetArz gateway.
 *
 * composer install
 * NETARZ_API_KEY=sk-ntz-v1-... php openai-php-client.php
 *
 * Docs: https://netarz.ir/docs/ai/sdks
 */

declare(strict_types=1);

require __DIR__.'/vendor/autoload.php';

$apiKey = getenv('NETARZ_API_KEY') ?: exit("Set NETARZ_API_KEY first.\n");

$client = OpenAI::factory()
    ->withApiKey($apiKey)
    ->withBaseUri(getenv('NETARZ_BASE_URL') ?: 'https://netarz.ir/api/ai/v1')
    ->withHttpClient(new GuzzleHttp\Client(['timeout' => 120]))
    ->make();

$result = $client->chat()->create([
    'model' => getenv('NETARZ_MODEL') ?: 'gpt-4o-mini',
    'messages' => [
        ['role' => 'system', 'content' => 'شما دستیار فارسی‌زبان یک فروشگاه اینترنتی هستید. کوتاه و دقیق جواب بدهید.'],
        ['role' => 'user', 'content' => 'برای یک فروشگاه لوازم ورزشی یک شعار کوتاه بنویسید.'],
    ],
    'max_tokens' => 200,
]);

echo $result->choices[0]->message->content, PHP_EOL;
echo 'tokens: ', $result->usage->totalTokens, PHP_EOL;

// Streaming with the same client:
$stream = $client->chat()->createStreamed([
    'model' => 'gpt-4o-mini',
    'messages' => [['role' => 'user', 'content' => 'یک جملهٔ کوتاه دربارهٔ پاییز بنویسید.']],
    'max_tokens' => 100,
]);

foreach ($stream as $response) {
    echo $response->choices[0]->delta->content ?? '';
}
echo PHP_EOL;
