<?php

// routes/web.php (or api.php): a server-side endpoint your front-end calls.
// The NetArz key stays in .env; the browser never sees it.
// Add your own auth + rate limit middleware before exposing this publicly.

use App\Services\NetArzAi;
use Illuminate\Http\Client\RequestException;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

Route::post('/assistant', function (Request $request, NetArzAi $ai) {
    $data = $request->validate(['message' => ['required', 'string', 'max:4000']]);

    try {
        $answer = $ai->chat([
            ['role' => 'system', 'content' => 'شما دستیار پشتیبانی یک فروشگاه هستید. کوتاه و دقیق جواب بدهید.'],
            ['role' => 'user', 'content' => $data['message']],
        ], maxTokens: 400);
    } catch (RequestException $e) {
        report($e);

        return response()->json(['error' => $e->response->json('error.code')], 502);
    }

    return response()->json(['answer' => $answer]);
})->middleware('throttle:20,1');
