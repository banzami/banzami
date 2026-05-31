# Banza Laravel SDK

Official Laravel integration for the Banza payment gateway. Provides a service provider, facade, webhook verification middleware, and typed Laravel events for all Banza webhook types.

---

## Requirements

- PHP 8.1 or higher
- Laravel 10 or Laravel 11

---

## Installation

```bash
composer require banza/banza-laravel
```

Laravel auto-discovery registers `BanzaServiceProvider` and the `Banza` facade automatically. No manual registration is needed.

---

## Configuration

Publish the config file:

```bash
php artisan vendor:publish --tag=banza-config
```

This creates `config/banza.php`. Set your credentials in `.env`:

```env
BANZA_GATEWAY_URL=https://api.banzami.com
BANZA_API_KEY=your_api_key_here
BANZA_WEBHOOK_SECRET=your_webhook_secret_here
BANZA_MERCHANT_ID=your_merchant_id
BANZA_WALLET_ID=your_default_wallet_id
```

| Variable | Description |
|---|---|
| `BANZA_GATEWAY_URL` | Banza API base URL (default: `https://api.banzami.com`) |
| `BANZA_API_KEY` | Your merchant API key |
| `BANZA_WEBHOOK_SECRET` | HMAC secret for webhook signature verification |
| `BANZA_MERCHANT_ID` | Default merchant ID (optional, can be passed per-request) |
| `BANZA_WALLET_ID` | Default wallet ID (optional, can be passed per-request) |

---

## Facade Usage

The `Banza` facade proxies all calls to the underlying `BanzaClient`.

### Payment Links

```php
use Banza\Laravel\Facades\Banza;

// Create a payment link
$link = Banza::createPaymentLink([
    'merchant_id' => config('banza.merchant_id'),
    'amount'      => 5000,
    'currency'    => 'AOA',
    'reference'   => 'order-123',
    'description' => 'Order #123',
]);

// Retrieve a payment link
$link = Banza::getPaymentLink($linkId);

// List payment links for a merchant
$links = Banza::listPaymentLinks($merchantId, limit: 20);

// Cancel a payment link
Banza::cancelPaymentLink($linkId);
```

### Transactions

```php
// Create a transaction
$txn = Banza::createTransaction([
    'merchant_id' => config('banza.merchant_id'),
    'wallet_id'   => config('banza.wallet_id'),
    'amount'      => 5000,
    'currency'    => 'AOA',
    'reference'   => 'order-123',
]);

// Retrieve a transaction
$txn = Banza::getTransaction($transactionId);

// List transactions
$txns = Banza::listTransactions($merchantId, limit: 50);
```

### Wallets

```php
// Provision a wallet for a merchant
$wallet = Banza::provisionWallet([
    'merchant_id' => $merchantId,
    'currency'    => 'AOA',
]);

// Get wallet details
$wallet = Banza::getWallet($walletId);

// Get wallet balance
$balance = Banza::getWalletBalance($walletId);
```

### Payouts

```php
// Request a payout
$payout = Banza::createPayout([
    'merchant_id' => $merchantId,
    'wallet_id'   => $walletId,
    'amount'      => 10000,
    'currency'    => 'AOA',
    'destination' => 'bank_account_id',
]);

// List payouts
$payouts = Banza::listPayouts($merchantId, limit: 20);

// Get a specific payout
$payout = Banza::getPayout($payoutId);
```

### Merchants

```php
$merchant = Banza::getMerchant($merchantId);
```

---

## Webhooks

Banza sends webhook events to your application when payment state changes occur. The SDK automatically verifies the HMAC-SHA256 signature on every incoming request.

### 1. Register the webhook route

The SDK registers `POST /banza/webhook` automatically. You must **exclude this route from CSRF verification** since it receives external POST requests.

In `app/Http/Middleware/VerifyCsrfToken.php`:

```php
protected $except = [
    'banza/webhook',
];
```

### 2. Configure the webhook URL in your Banza dashboard

Point your webhook URL to:

```
https://yourdomain.com/banza/webhook
```

### 3. Listen for events

Register event listeners in `app/Providers/EventServiceProvider.php`:

```php
use Banza\Laravel\Events\TransactionCompleted;
use Banza\Laravel\Events\TransactionFailed;
use Banza\Laravel\Events\PaymentLinkUsed;
use Banza\Laravel\Events\WalletProvisioned;
use Banza\Laravel\Events\PayoutRequested;

protected $listen = [
    TransactionCompleted::class => [
        \App\Listeners\HandleTransactionCompleted::class,
    ],
    TransactionFailed::class => [
        \App\Listeners\HandleTransactionFailed::class,
    ],
    PaymentLinkUsed::class => [
        \App\Listeners\HandlePaymentLinkUsed::class,
    ],
    WalletProvisioned::class => [
        \App\Listeners\HandleWalletProvisioned::class,
    ],
    PayoutRequested::class => [
        \App\Listeners\HandlePayoutRequested::class,
    ],
];
```

You can also listen for all Banza webhooks generically:

```php
use Illuminate\Support\Facades\Event;

Event::listen('banza.webhook', function (array $event) {
    // $event contains the full parsed webhook payload
});
```

---

## Events Reference

All typed events are dispatched with the data from the `payload` field of the webhook body.

| Event class | Webhook type | Constructor property |
|---|---|---|
| `TransactionCompleted` | `transaction.completed` | `$payload` (array) |
| `TransactionFailed` | `transaction.failed` | `$payload` (array) |
| `PaymentLinkUsed` | `payment_link.used` | `$payload` (array) |
| `WalletProvisioned` | `wallet.provisioned` | `$wallet` (array) |
| `PayoutRequested` | `payout.requested` | `$payout` (array) |

---

## Error Handling

All API calls throw `Banza\BanzaException` on failure. Wrap calls accordingly:

```php
use Banza\BanzaException;
use Banza\Laravel\Facades\Banza;

try {
    $link = Banza::createPaymentLink([...]);
} catch (BanzaException $e) {
    // Log, retry, or surface error to the user
    logger()->error('Banza API error', ['message' => $e->getMessage()]);
}
```

Invalid webhook signatures return HTTP 401 immediately before any event is dispatched.

---

## Complete Example: Checkout Flow

This example shows a WooCommerce-style order checkout using the facade.

```php
<?php

namespace App\Http\Controllers;

use App\Models\Order;
use Banza\BanzaException;
use Banza\Laravel\Facades\Banza;
use Illuminate\Http\Request;

class CheckoutController extends Controller
{
    public function createPaymentLink(Request $request): \Illuminate\Http\JsonResponse
    {
        $validated = $request->validate([
            'order_id'  => ['required', 'exists:orders,id'],
            'amount'    => ['required', 'integer', 'min:1'],
        ]);

        $order = Order::findOrFail($validated['order_id']);

        try {
            $link = Banza::createPaymentLink([
                'merchant_id' => config('banza.merchant_id'),
                'amount'      => $validated['amount'],
                'currency'    => 'AOA',
                'reference'   => (string) $order->id,
                'description' => "Order #{$order->id}",
                'redirect_url' => route('checkout.success', $order),
            ]);
        } catch (BanzaException $e) {
            return response()->json(['error' => 'Payment gateway error. Please try again.'], 502);
        }

        $order->update(['payment_link_id' => $link['id'], 'status' => 'awaiting_payment']);

        return response()->json(['url' => $link['url']]);
    }
}
```

```php
// app/Listeners/HandleTransactionCompleted.php

namespace App\Listeners;

use App\Models\Order;
use Banza\Laravel\Events\TransactionCompleted;

class HandleTransactionCompleted
{
    public function handle(TransactionCompleted $event): void
    {
        $order = Order::where('payment_link_id', $event->payload['payment_link_id'] ?? null)->first();

        if ($order === null) {
            return;
        }

        $order->update(['status' => 'paid', 'paid_at' => now()]);

        // Dispatch fulfillment job, send receipt email, etc.
    }
}
```

---

## Local Development & Testing

Install dev dependencies:

```bash
composer install
```

Run the test suite:

```bash
./vendor/bin/phpunit
```

The test suite uses [Orchestra Testbench](https://orchestraplatform.com/docs/testbench/) and does not require a running Banza instance. Webhook signatures are verified using the same HMAC-SHA256 logic as production.

To test webhooks locally, use a tunnelling tool such as [ngrok](https://ngrok.com/) or [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/) to expose your local server, then configure the resulting URL in your Banza dashboard.
