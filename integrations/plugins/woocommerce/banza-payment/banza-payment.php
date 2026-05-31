<?php
/**
 * Plugin Name:  Banza Payment Gateway
 * Plugin URI:   https://banza.network
 * Description:  Accept payments via the Banza payment gateway in WooCommerce.
 * Version:      1.0.0
 * Author:       BANZA Protocol Contributors
 * Author URI:   https://banza.network
 * License:      UNLICENSED
 * Text Domain:  banza-payment
 * Requires PHP: 7.4
 * WC requires at least: 7.0
 * WC tested up to: 8.9
 */

defined( 'ABSPATH' ) || exit;

define( 'BANZA_PLUGIN_VERSION', '1.0.0' );
define( 'BANZA_PLUGIN_DIR', plugin_dir_path( __FILE__ ) );
define( 'BANZA_PLUGIN_URL', plugin_dir_url( __FILE__ ) );

// Bail if WooCommerce is not active.
function banza_check_woocommerce(): void {
    if ( ! class_exists( 'WooCommerce' ) ) {
        add_action( 'admin_notices', function () {
            echo '<div class="error"><p><strong>Banza Payment Gateway</strong> requires WooCommerce to be installed and active.</p></div>';
        } );
    }
}
add_action( 'plugins_loaded', 'banza_check_woocommerce' );

// Register the gateway with WooCommerce.
add_filter( 'woocommerce_payment_gateways', function ( array $gateways ): array {
    $gateways[] = 'WC_Banza_Gateway';
    return $gateways;
} );

// Initialise the gateway class after WooCommerce loads.
add_action( 'plugins_loaded', function (): void {
    if ( ! class_exists( 'WC_Payment_Gateway' ) ) {
        return;
    }
    require_once BANZA_PLUGIN_DIR . 'includes/class-banza-api.php';
    require_once BANZA_PLUGIN_DIR . 'includes/class-banza-gateway.php';
    require_once BANZA_PLUGIN_DIR . 'includes/class-banza-webhook.php';
    Banza_Webhook_Handler::init();
} );

// Declare HPOS compatibility.
add_action( 'before_woocommerce_init', function (): void {
    if ( class_exists( \Automattic\WooCommerce\Utilities\FeaturesUtil::class ) ) {
        \Automattic\WooCommerce\Utilities\FeaturesUtil::declare_compatibility( 'custom_order_tables', __FILE__, true );
    }
} );

register_uninstall_hook( __FILE__, 'banza_uninstall' );
function banza_uninstall(): void {
    delete_option( 'woocommerce_banza_settings' );
}
