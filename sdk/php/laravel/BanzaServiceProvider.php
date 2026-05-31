<?php

declare(strict_types=1);

namespace Banza\Laravel;

use Banza\BanzaClient;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\ServiceProvider;

class BanzaServiceProvider extends ServiceProvider
{
    public function register(): void
    {
        $this->mergeConfigFrom(__DIR__ . '/config/banza.php', 'banza');

        $this->app->singleton(BanzaClient::class, function (Application $app): BanzaClient {
            $config = $app['config']['banza'];
            return new BanzaClient(
                apiKey:      $config['api_key'],
                environment: $config['environment'] ?? 'live',
                baseUrl:     $config['base_url'] ?? null,
                maxRetries:  $config['max_retries'] ?? 3,
            );
        });

        $this->app->alias(BanzaClient::class, 'banza');
    }

    public function boot(): void
    {
        if ($this->app->runningInConsole()) {
            $this->publishes([
                __DIR__ . '/config/banza.php' => $this->app->configPath('banza.php'),
            ], 'banza-config');
        }
    }

    public function provides(): array
    {
        return [BanzaClient::class, 'banza'];
    }
}
