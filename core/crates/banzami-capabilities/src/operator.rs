//! Operator-level capability declarations.
//!
//! An `OperatorManifest` is the top-level capability document published by an
//! operator. It declares the operator's identity, kernel version compatibility,
//! and supported feature set.
//!
//! This is the groundwork for RFC-0005 (Operator Discovery). The manifest
//! format is designed to be publishable as a well-known JSON document at
//! `/.well-known/banzami-operator.json`.

use banzami_types::Currency;

/// Top-level capability declaration for a Banzami operator.
///
/// Operators construct and publish this manifest. The kernel uses it at startup
/// to log what is active. In a multi-operator context (RFC-0001, RFC-0005),
/// routing engines fetch and cache remote operator manifests to make routing
/// decisions.
#[derive(Debug, Clone)]
#[derive(serde::Serialize, serde::Deserialize)]
pub struct OperatorManifest {
    /// Unique, stable identifier for this operator.
    ///
    /// Format: `<org>-<deployment>`, e.g. `banza-prod`, `mybank-sandbox`.
    pub operator_id: String,

    /// Semantic version of this operator deployment.
    pub operator_version: String,

    /// Banzami kernel version range this operator is compatible with.
    ///
    /// Format: semver range, e.g. `"0.1.x"` or `">=0.1.0,<0.2.0"`.
    pub banzami_kernel_version: String,

    /// Interoperability endpoint for cross-operator flows.
    ///
    /// `None` = operator does not participate in cross-operator routing.
    pub interop_endpoint: Option<String>,

    /// Capability flags for this operator.
    pub capabilities: OperatorCapabilityFlags,

    /// Currencies this operator supports.
    pub supported_currencies: Vec<Currency>,

    /// Whether this operator is a sandbox/simulated deployment.
    ///
    /// Production routing engines must not route real payments to sandbox operators.
    pub is_sandbox: bool,

    /// Manifest schema version.
    pub manifest_version: u32,
}

impl OperatorManifest {
    /// Create a manifest for the reference sandbox operator.
    pub fn sandbox(operator_id: impl Into<String>) -> Self {
        Self {
            operator_id:             operator_id.into(),
            operator_version:        "0.1.0".into(),
            banzami_kernel_version:  "0.1.x".into(),
            interop_endpoint:        None,
            capabilities:            OperatorCapabilityFlags::sandbox_defaults(),
            supported_currencies:    vec![Currency::AOA],
            is_sandbox:              true,
            manifest_version:        1,
        }
    }
}

/// Boolean capability flags for an operator.
///
/// New flags are added with a `// @since version X` comment. Deserialising a
/// manifest from an older version uses `false` for missing flags.
#[derive(Debug, Clone, Default)]
#[derive(serde::Serialize, serde::Deserialize)]
pub struct OperatorCapabilityFlags {
    /// Operator supports QR payment flows.
    pub qr_payments: bool,

    /// Operator supports P2P wallet-to-wallet transfers.
    pub p2p_transfers: bool,

    /// Operator supports merchant settlement payouts.
    pub settlement: bool,

    /// Operator supports refund flows.
    pub refunds: bool,

    /// Operator hosts consumer wallets.
    pub consumer_wallets: bool,

    /// Operator hosts merchant wallets.
    pub merchant_wallets: bool,

    /// Operator supports payment links.
    pub payment_links: bool,

    /// Operator can participate in cross-operator routing (RFC-0001).
    pub cross_operator_routing: bool,

    /// Operator can settle cross-operator obligations (RFC-0002).
    pub cross_operator_settlement: bool,

    /// Operator supports offline payment pre-authorization (RFC-0006).
    pub offline_payments: bool,

    /// Operator has CBDC integration.
    pub cbdc: bool,
}

impl OperatorCapabilityFlags {
    /// Capability set for the reference sandbox operator.
    pub const fn sandbox_defaults() -> Self {
        Self {
            qr_payments:               false,
            p2p_transfers:             true,
            settlement:                true,
            refunds:                   false,
            consumer_wallets:          false,
            merchant_wallets:          true,
            payment_links:             false,
            cross_operator_routing:    false,
            cross_operator_settlement: false,
            offline_payments:          false,
            cbdc:                      false,
        }
    }
}

/// Trait that operator implementations implement to expose their capabilities.
///
/// The kernel calls `manifest()` at startup to build the `KernelCapabilityMap`
/// and log the active operator configuration.
pub trait OperatorCapabilities: Send + Sync {
    /// Return the capability manifest for this operator deployment.
    fn manifest(&self) -> OperatorManifest;

    /// Convenience: return `true` if this operator can handle QR payments.
    fn supports_qr_payments(&self) -> bool {
        self.manifest().capabilities.qr_payments
    }

    /// Convenience: return `true` if this operator hosts consumer wallets.
    fn supports_consumer_wallets(&self) -> bool {
        self.manifest().capabilities.consumer_wallets
    }

    /// Convenience: return `true` if this is a sandbox operator.
    fn is_sandbox(&self) -> bool {
        self.manifest().is_sandbox
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    struct SandboxOp;
    impl OperatorCapabilities for SandboxOp {
        fn manifest(&self) -> OperatorManifest {
            OperatorManifest::sandbox("test-sandbox")
        }
    }

    #[test]
    fn sandbox_manifest_is_marked_sandbox() {
        let op = SandboxOp;
        assert!(op.is_sandbox());
    }

    #[test]
    fn sandbox_defaults_have_no_consumer_wallets() {
        let op = SandboxOp;
        assert!(!op.supports_consumer_wallets());
    }

    #[test]
    fn manifest_is_serializable() {
        let m = OperatorManifest::sandbox("test");
        let json = serde_json::to_string(&m).unwrap();
        assert!(json.contains("test"));
    }
}
