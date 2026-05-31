<?php

return [
    /*
    |--------------------------------------------------------------------------
    | Banza API Key
    |--------------------------------------------------------------------------
    |
    | Your Banza secret API key. Prefix determines the environment:
    |   bz_live_... → live (real money)
    |   bz_test_... → sandbox (virtual funds)
    |
    | Never commit this value. Store it in .env as BANZA_API_KEY.
    |
    */
    'api_key' => env('BANZA_API_KEY'),

    /*
    |--------------------------------------------------------------------------
    | Environment
    |--------------------------------------------------------------------------
    |
    | 'live' or 'sandbox'. Defaults to 'live' in production.
    | If your API key prefix is bz_test_, use 'sandbox' here.
    |
    */
    'environment' => env('BANZA_ENVIRONMENT', 'live'),

    /*
    |--------------------------------------------------------------------------
    | Webhook Secret
    |--------------------------------------------------------------------------
    |
    | The signing secret for your webhook endpoint, obtained from the
    | operator dashboard when you register an endpoint. Used with
    | Webhooks::constructEvent() to verify incoming webhook signatures.
    |
    */
    'webhook_secret' => env('BANZA_WEBHOOK_SECRET'),

    /*
    |--------------------------------------------------------------------------
    | Base URL Override
    |--------------------------------------------------------------------------
    |
    | Override the default API base URL (e.g., for local development or
    | staging environments). Leave null to use the canonical Banza URL.
    |
    */
    'base_url' => env('BANZA_BASE_URL'),

    /*
    |--------------------------------------------------------------------------
    | Max Retries
    |--------------------------------------------------------------------------
    |
    | Number of automatic retries on retryable errors (429, 502, 503, 504).
    |
    */
    'max_retries' => (int) env('BANZA_MAX_RETRIES', 3),
];
