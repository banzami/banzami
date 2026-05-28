//! Operator manifest for GET /.well-known/banzami/operator.json
//!
//! The manifest declares what this operator supports, explicitly marks itself
//! as a sandbox, and blocks production use via `production_allowed: false`.

use serde::Serialize;

#[derive(Debug, Serialize)]
pub struct OperatorManifest {
    pub operator_id:             &'static str,
    pub display_name:            &'static str,
    pub environment:             &'static str,
    pub banzami_kernel_version:  &'static str,
    pub simulated:               bool,
    pub production_allowed:      bool,
    pub capabilities:            ManifestCapabilities,
    pub supported_currencies:    &'static [&'static str],
    pub endpoints:               ManifestEndpoints,
    pub providers:               ManifestProviders,
    pub seed_wallets:            SeedWalletIds,
    pub manifest_version:        u32,
}

#[derive(Debug, Serialize)]
pub struct ManifestCapabilities {
    pub supports_wallets:               bool,
    pub supports_transfers:             bool,
    pub supports_qr:                    bool,
    pub supports_payment_requests:      bool,
    pub supports_payment_links:         bool,
    pub supports_settlement_simulation: bool,
    pub supports_events_sse:            bool,
    pub supports_ledger_inspection:     bool,
    pub cross_operator_routing:         bool,
    pub offline_payments:               bool,
}

#[derive(Debug, Serialize)]
pub struct ManifestEndpoints {
    pub api:      &'static str,
    pub events:   &'static str,
    pub manifest: &'static str,
}

#[derive(Debug, Serialize)]
pub struct ManifestProviders {
    pub acquirer:     &'static str,
    pub settlement:   &'static str,
    pub notification: &'static str,
    pub all_simulated: bool,
}

#[derive(Debug, Serialize)]
pub struct SeedWalletIds {
    pub consumer:   &'static str,
    pub merchant:   &'static str,
    pub government: &'static str,
}

pub fn build_manifest() -> OperatorManifest {
    OperatorManifest {
        operator_id:            "banzami-sandbox",
        display_name:           "Banzami Sandbox Operator",
        environment:            "sandbox",
        banzami_kernel_version: "0.1.x",
        simulated:              true,
        production_allowed:     false,
        capabilities: ManifestCapabilities {
            supports_wallets:               true,
            supports_transfers:             true,
            supports_qr:                    true,
            supports_payment_requests:      true,
            supports_payment_links:         false,
            supports_settlement_simulation: true,
            supports_events_sse:            true,
            supports_ledger_inspection:     true,
            cross_operator_routing:         false,
            offline_payments:               false,
        },
        supported_currencies: &["AOA", "USD", "EUR"],
        endpoints: ManifestEndpoints {
            api:      "http://localhost:3100",
            events:   "http://localhost:3100/events",
            manifest: "http://localhost:3100/.well-known/banzami/operator.json",
        },
        providers: ManifestProviders {
            acquirer:      "FakeAcquirer",
            settlement:    "SimulatedSettlementProvider",
            notification:  "StdoutNotificationProvider",
            all_simulated: true,
        },
        seed_wallets: SeedWalletIds {
            consumer:   "sandbox-consumer-1",
            merchant:   "sandbox-merchant-1",
            government: "sandbox-government-1",
        },
        manifest_version: 1,
    }
}
