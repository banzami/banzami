<?php

declare(strict_types=1);

namespace Banza\Laravel\Http;

use Banza\BanzaException;
use Banza\WebhookHandler;
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Illuminate\Routing\Controller;
use Illuminate\Support\Facades\Event;

/**
 * Handles incoming Banza webhook events.
 *
 * Register in config/banzami.php and publish routes via the service provider.
 * The route is automatically registered at POST /banzami/webhook.
 *
 * Dispatches a Laravel event for each received type:
 *   - \Banza\Laravel\Events\TransactionCompleted
 *   - \Banza\Laravel\Events\TransactionFailed
 *   - \Banza\Laravel\Events\PaymentLinkUsed
 *   - \Banza\Laravel\Events\WalletProvisioned
 *   - \Banza\Laravel\Events\PayoutRequested
 *
 * Or listen for the raw event type string via:
 *   Event::listen('banzami.webhook', function ($event) { ... });
 */
class WebhookController extends Controller
{
    public function handle(Request $request): Response
    {
        $secret = config('banzami.webhook_secret', '');

        $handler = new WebhookHandler($secret);

        try {
            $event = $handler->parse(
                $request->getContent(),
                $request->header('Banza-Signature', '')
            );
        } catch (BanzaException $e) {
            return response('Invalid signature', 401);
        }

        // Fire a generic event for any listener
        Event::dispatch('banzami.webhook', [$event]);

        // Fire typed events for specific handlers
        $typed = self::typedEventClass($event['type'] ?? '');
        if ($typed !== null && class_exists($typed)) {
            Event::dispatch(new $typed($event['payload'] ?? $event));
        }

        return response('OK', 200);
    }

    private static function typedEventClass(string $type): ?string
    {
        return match ($type) {
            'transaction.completed' => \Banza\Laravel\Events\TransactionCompleted::class,
            'transaction.failed'    => \Banza\Laravel\Events\TransactionFailed::class,
            'payment_link.used'     => \Banza\Laravel\Events\PaymentLinkUsed::class,
            'wallet.provisioned'    => \Banza\Laravel\Events\WalletProvisioned::class,
            'payout.requested'      => \Banza\Laravel\Events\PayoutRequested::class,
            default                 => null,
        };
    }
}
