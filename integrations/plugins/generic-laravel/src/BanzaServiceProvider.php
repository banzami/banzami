<?php

declare(strict_types=1);

namespace Banza\Laravel;

use Banza\BanzaClient;
use Illuminate\Support\ServiceProvider;

class BanzaServiceProvider extends ServiceProvider
{
    public function register(): void
    {
        $this->mergeConfigFrom(__DIR__ . '/../config/banza.php', 'banza');

        $this->app->singleton(BanzaClient::class, function ($app) {
            $config = $app['config']['banza'];
            return new BanzaClient(
                $config['gateway_url'],
                $config['api_key'],
            );
        });

        $this->app->alias(BanzaClient::class, 'banza');
    }

    public function boot(): void
    {
        if ($this->app->runningInConsole()) {
            $this->publishes([
                __DIR__ . '/../config/banza.php' => config_path('banza.php'),
            ], 'banza-config');
        }

        $this->loadRoutesFrom(__DIR__ . '/../routes/banza.php');
    }
}
