=== Banza Payment Gateway ===
Contributors:      banzami
Tags:              payment, gateway, angola, kwanza, mobile, qr
Requires at least: 6.0
Tested up to:      6.5
Requires PHP:      7.4
WC requires at least: 7.0
WC tested up to: 8.9
License:           UNLICENSED

Accept payments via the BANZA protocol in WooCommerce.

== Description ==

The **Banza Payment Gateway** allows your WooCommerce store to accept payments via the BANZA payment network, Angola's modern financial infrastructure.

**How it works:**

1. Customer selects Banza at checkout and places their order.
2. A payment page is shown with a QR code and a deep link to a BANZA-compatible app.
3. The customer scans the QR with their BANZA-compatible app and confirms the amount.
4. BANZA sends a webhook to your store confirming the payment.
5. The order is automatically marked as paid and the customer is redirected to the thank-you page.

**Features:**

* QR code display on the payment page (generated client-side)
* Mobile deep-link for direct app opening
* HMAC-SHA256 webhook signature verification
* Supports AOA (Angolan Kwanza) and USD
* Compatible with WooCommerce High-Performance Order Storage (HPOS)
* Clean uninstall — removes all plugin settings

== Installation ==

1. Upload the `banzami-payment` folder to `/wp-content/plugins/`.
2. Activate the plugin through the **Plugins** menu in WordPress.
3. Go to **WooCommerce → Settings → Payments** and click *Banza*.
4. Enter your **API Key** and **Webhook Secret** from the operator dashboard.
5. Set the **Webhook URL** in the operator dashboard to:
   `https://your-store.com/wc-api/banzami`

== Changelog ==

= 1.0.0 =
* Initial release.
