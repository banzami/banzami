<?php

return [
    /*
    |--------------------------------------------------------------------------
    | Banza Gateway URL
    |--------------------------------------------------------------------------
    | The base URL of the Banza API gateway.
    */
    'gateway_url' => env('BANZA_GATEWAY_URL', 'https://api.banzami.ao'),

    /*
    |--------------------------------------------------------------------------
    | API Key
    |--------------------------------------------------------------------------
    | Your Banza merchant API key. Keep this in your .env file — never
    | commit it to source control.
    */
    'api_key' => env('BANZA_API_KEY', ''),

    /*
    |--------------------------------------------------------------------------
    | Webhook Secret
    |--------------------------------------------------------------------------
    | Used to verify the HMAC-SHA256 signature on incoming webhook events.
    */
    'webhook_secret' => env('BANZA_WEBHOOK_SECRET', ''),

    /*
    |--------------------------------------------------------------------------
    | Merchant / Wallet IDs
    |--------------------------------------------------------------------------
    | Pre-configure the default merchant and wallet if your app serves a
    | single merchant. You can also set these per-request.
    */
    'merchant_id' => env('BANZA_MERCHANT_ID', ''),
    'wallet_id'   => env('BANZA_WALLET_ID', ''),
];
