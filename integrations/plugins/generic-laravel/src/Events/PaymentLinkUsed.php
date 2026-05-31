<?php

declare(strict_types=1);

namespace Banza\Laravel\Events;

class PaymentLinkUsed
{
    public function __construct(public readonly array $payload) {}
}
