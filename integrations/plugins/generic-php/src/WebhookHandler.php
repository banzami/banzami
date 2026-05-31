<?php

declare(strict_types=1);

namespace Banza;

/**
 * Helper for processing BANZA webhook events.
 *
 * Usage:
 *   $handler = new WebhookHandler('your-webhook-secret');
 *
 *   try {
 *       $event = $handler->parse(
 *           file_get_contents('php://input'),
 *           $_SERVER['HTTP_BANZA_SIGNATURE'] ?? ''
 *       );
 *   } catch (BanzaException $e) {
 *       http_response_code(401);
 *       exit('Invalid signature');
 *   }
 *
 *   switch ($event['type']) {
 *       case 'transaction.completed':
 *           // mark order as paid
 *           break;
 *       case 'payment_link.used':
 *           // mark link as fulfilled
 *           break;
 *   }
 */
class WebhookHandler
{
    private string $secret;

    public function __construct(string $secret)
    {
        $this->secret = $secret;
    }

    /**
     * Verify the signature and decode the event payload.
     *
     * @return array{type: string, payload: array}
     * @throws BanzaException if signature is invalid or body is malformed.
     */
    public function parse(string $rawBody, string $signature): array
    {
        if (!BanzaClient::verifyWebhookSignature($rawBody, $signature, $this->secret)) {
            throw new BanzaException('Invalid webhook signature', 401);
        }

        $data = json_decode($rawBody, true, 512, JSON_THROW_ON_ERROR);
        if (!is_array($data) || !isset($data['type'])) {
            throw new BanzaException('Invalid webhook payload', 400);
        }

        return $data;
    }
}
