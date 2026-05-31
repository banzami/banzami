<?php

declare(strict_types=1);

namespace Banza\Laravel\Tests;

use Banza\BanzaClient;
use Banza\Laravel\BanzaServiceProvider;
use Banza\Laravel\Facades\Banza;
use Orchestra\Testbench\TestCase;

class ServiceProviderTest extends TestCase
{
    protected function getPackageProviders($app): array
    {
        return [BanzaServiceProvider::class];
    }

    protected function getEnvironmentSetUp($app): void
    {
        $app['config']->set('banza.gateway_url', 'https://api.banza.ao');
        $app['config']->set('banza.api_key', 'test-api-key');
    }

    public function test_banza_client_is_bound_as_singleton(): void
    {
        $a = $this->app->make(BanzaClient::class);
        $b = $this->app->make(BanzaClient::class);

        $this->assertInstanceOf(BanzaClient::class, $a);
        $this->assertSame($a, $b, 'BanzaClient must be a singleton');
    }

    public function test_facade_resolves_to_banza_client(): void
    {
        $resolved = Banza::getFacadeRoot();

        $this->assertInstanceOf(BanzaClient::class, $resolved);
    }

    public function test_config_is_merged_with_defaults(): void
    {
        $this->assertSame('https://api.banza.ao', config('banza.gateway_url'));
        $this->assertSame('test-api-key', config('banza.api_key'));
        $this->assertArrayHasKey('webhook_secret', config('banza'));
        $this->assertArrayHasKey('merchant_id', config('banza'));
        $this->assertArrayHasKey('wallet_id', config('banza'));
    }

    public function test_config_is_publishable(): void
    {
        $paths = BanzaServiceProvider::pathsToPublish(BanzaServiceProvider::class, 'banza-config');

        $this->assertNotEmpty($paths, 'banza-config tag must register at least one publishable path');

        $sourceFile = array_key_first($paths);
        $this->assertFileExists($sourceFile, 'The published config source file must exist');
    }
}
