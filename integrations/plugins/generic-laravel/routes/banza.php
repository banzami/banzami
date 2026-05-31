<?php

use Banza\Laravel\Http\WebhookController;
use Illuminate\Support\Facades\Route;

Route::post('/banza/webhook', [WebhookController::class, 'handle'])
    ->name('banza.webhook');
