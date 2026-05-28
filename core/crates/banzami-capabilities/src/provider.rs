//! Provider capability declarations.
//!
//! Every provider in the Banzami ecosystem declares a `ProviderCapabilityDescriptor`
//! that the kernel uses to:
//!
//! - Log what is active at startup.
//! - Determine whether a provider failure is fatal or degraded-but-acceptable.
//! - Guard against simulated providers shipping to production (RFC-0004).

/// Broad classification of what a provider does.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[derive(serde::Serialize, serde::Deserialize)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum ProviderKind {
    Acquirer,
    Settlement,
    Notification,
    Routing,
    Risk,
    Identity,
    Wallet,
    Custom,
}

/// Capability descriptor that every provider implementation must return.
///
/// See RFC-0004 for the full rationale.
///
/// # Example
///
/// ```
/// use banzami_capabilities::provider::{ProviderCapabilityDescriptor, ProviderKind};
///
/// let desc = ProviderCapabilityDescriptor {
///     name:                        "FakeAcquirer".into(),
///     kind:                        ProviderKind::Acquirer,
///     version:                     "0.1.0".into(),
///     supported_protocol_versions: vec![1],
///     required_for_payment_flow:   true,
///     is_simulated:                true,
///     features:                    vec!["hmac-callbacks".into()],
/// };
/// assert!(desc.is_simulated);
/// ```
#[derive(Debug, Clone)]
#[derive(serde::Serialize, serde::Deserialize)]
pub struct ProviderCapabilityDescriptor {
    /// Human-readable name identifying this provider implementation.
    pub name: String,

    /// What kind of provider this is.
    pub kind: ProviderKind,

    /// Semantic version of this provider implementation.
    pub version: String,

    /// Protocol versions this provider can handle.
    ///
    /// Empty = provider does not participate in version negotiation.
    pub supported_protocol_versions: Vec<u32>,

    /// Whether this provider is required for a core payment flow to succeed.
    ///
    /// `false` = the kernel may continue a payment even if this provider
    /// returns an error (graceful degradation). Example: notifications.
    ///
    /// `true` = a provider failure must fail the payment. Example: acquirer.
    pub required_for_payment_flow: bool,

    /// Whether this is a simulated/sandbox implementation.
    ///
    /// A kernel configured for production mode must refuse to start if any
    /// provider has `is_simulated: true`. This prevents accidental deployment
    /// of reference implementations to production.
    pub is_simulated: bool,

    /// Named features this provider supports.
    ///
    /// Free-form strings for extensibility. Examples: "hmac-callbacks",
    /// "bilateral-netting", "push-notifications", "websocket-events".
    pub features: Vec<String>,
}

impl ProviderCapabilityDescriptor {
    /// Returns `true` if this provider is safe for a production deployment.
    pub fn is_production_safe(&self) -> bool {
        !self.is_simulated
    }

    /// Returns `true` if this provider supports a given named feature.
    pub fn has_feature(&self, feature: &str) -> bool {
        self.features.iter().any(|f| f.as_str() == feature)
    }

    /// Returns `true` if this provider supports the given protocol version.
    pub fn supports_protocol_version(&self, version: u32) -> bool {
        self.supported_protocol_versions.contains(&version)
    }
}

/// A collection of provider descriptors for a running operator.
///
/// Built at startup by collecting descriptors from all registered providers.
/// The kernel logs this map and uses it for capability checks.
#[derive(Debug, Default)]
pub struct KernelCapabilityMap {
    providers: Vec<ProviderCapabilityDescriptor>,
}

impl KernelCapabilityMap {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn register(&mut self, descriptor: ProviderCapabilityDescriptor) {
        self.providers.push(descriptor);
    }

    /// Returns `true` if all registered providers are production-safe.
    pub fn is_production_safe(&self) -> bool {
        self.providers.iter().all(|p| p.is_production_safe())
    }

    /// Returns all providers that are simulated.
    pub fn simulated_providers(&self) -> Vec<&ProviderCapabilityDescriptor> {
        self.providers.iter().filter(|p| p.is_simulated).collect()
    }

    /// Returns the descriptor for the provider matching the given kind and name.
    pub fn find(&self, kind: ProviderKind, name: &str) -> Option<&ProviderCapabilityDescriptor> {
        self.providers.iter().find(|p| p.kind == kind && p.name == name)
    }

    /// Returns all registered descriptors.
    pub fn all(&self) -> &[ProviderCapabilityDescriptor] {
        &self.providers
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn fake_acquirer() -> ProviderCapabilityDescriptor {
        ProviderCapabilityDescriptor {
            name:                        "FakeAcquirer".into(),
            kind:                        ProviderKind::Acquirer,
            version:                     "0.1.0".into(),
            supported_protocol_versions: vec![1],
            required_for_payment_flow:   true,
            is_simulated:                true,
            features:                    vec!["hmac-callbacks".into()],
        }
    }

    #[test]
    fn simulated_provider_is_not_production_safe() {
        assert!(!fake_acquirer().is_production_safe());
    }

    #[test]
    fn capability_map_detects_simulated_providers() {
        let mut map = KernelCapabilityMap::new();
        map.register(fake_acquirer());
        assert!(!map.is_production_safe());
        assert_eq!(map.simulated_providers().len(), 1);
    }

    #[test]
    fn has_feature_works() {
        let d = fake_acquirer();
        assert!(d.has_feature("hmac-callbacks"));
        assert!(!d.has_feature("real-bank-api"));
    }

    #[test]
    fn descriptor_is_serializable() {
        let d = fake_acquirer();
        let json = serde_json::to_string(&d).unwrap();
        let _: ProviderCapabilityDescriptor = serde_json::from_str(&json).unwrap();
    }
}
