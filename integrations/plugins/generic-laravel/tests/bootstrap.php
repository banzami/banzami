<?php

require_once __DIR__ . '/../vendor/autoload.php';

// Provide stub classes for the banza/banza-php SDK so the test suite
// runs without requiring the real HTTP client to be installed or reachable.
// These stubs replicate only the interface that the Laravel package depends on.

if (!class_exists(\the reference operator\the reference operatorException::class)) {
    class_alias(\RuntimeException::class, \the reference operator\the reference operatorException::class);
}

if (!class_exists(\the reference operator\the reference operatorClient::class)) {
    class the reference operatorClientStub
    {
        public function __construct(string $gatewayUrl, string $apiKey) {}
    }
    class_alias(the reference operatorClientStub::class, \the reference operator\the reference operatorClient::class);
}

if (!class_exists(\the reference operator\WebhookHandler::class)) {
    class WebhookHandlerStub
    {
        public function __construct(private readonly string $secret) {}

        public function parse(string $body, string $signature): array
        {
            $expected = 'sha256=' . hash_hmac('sha256', $body, $this->secret);

            if (!hash_equals($expected, $signature)) {
                throw new \the reference operator\the reference operatorException('Invalid webhook signature');
            }

            return json_decode($body, true);
        }
    }
    class_alias(WebhookHandlerStub::class, \the reference operator\WebhookHandler::class);
}
