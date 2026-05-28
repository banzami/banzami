//! Configurable mock routing engine for local development and testing.
//!
//! This crate provides two implementations of the [`RoutingEngine`] trait
//! suitable for development and automated testing:
//!
//! - [`MockRoutingEngine`] — always succeeds, logs decisions verbosely, lets
//!   you inspect which rail would be selected for any request.
//! - [`FailingRoutingEngine`] — always returns `NoEligibleRail`, useful for
//!   testing upstream error handling in the sandbox operator.
//!
//! Neither implementation makes any assumption about which payment rails exist
//! in a given country or operator deployment. The rail list is injected at
//! construction time.
//!
//! # Usage
//!
//! ```
//! use mock_routing::{MockRoutingEngine, RailConfig};
//! use banzami_types::Currency;
//! use banzami_routing::PaymentRail;
//!
//! let engine = MockRoutingEngine::with_rails(vec![
//!     RailConfig { currency: Currency::AOA, rail: PaymentRail::MulticaixaExpress, priority: 100 },
//! ]);
//! ```

use banzami_routing::{
    PaymentRail, RouteRequest, RoutingDecision, RoutingEngine, RoutingError, RoutingRule,
    StaticRoutingEngine,
};
use banzami_types::Currency;

// ---------------------------------------------------------------------------
// RailConfig
// ---------------------------------------------------------------------------

/// A routing rule supplied at engine construction time.
///
/// Mirrors [`RoutingRule`] from `banzami-routing` but is local to this crate
/// so callers don't need to depend on the routing crate's internals.
pub struct RailConfig {
    pub currency: Currency,
    pub rail:     PaymentRail,
    pub priority: u8,
}

// ---------------------------------------------------------------------------
// MockRoutingEngine
// ---------------------------------------------------------------------------

/// A routing engine that always selects a rail and logs the decision verbosely.
///
/// This is the development-default engine. It delegates to `StaticRoutingEngine`
/// for the actual selection logic, then logs the full decision including all
/// considered (but not selected) rails.
pub struct MockRoutingEngine {
    inner: StaticRoutingEngine,
}

impl MockRoutingEngine {
    /// Build a mock engine with the given per-currency rail configurations.
    pub fn with_rails(rails: Vec<RailConfig>) -> Self {
        let rules: Vec<RoutingRule> = rails.into_iter().map(|r| RoutingRule {
            currency: r.currency,
            rail:     r.rail,
            priority: r.priority,
        }).collect();
        Self { inner: StaticRoutingEngine::new(rules) }
    }

    /// Build a mock engine with a representative multi-currency example ruleset.
    ///
    /// Uses whatever rails `StaticRoutingEngine::with_example_rules()` provides.
    /// Suitable for sandbox experimentation; not operator-specific.
    pub fn with_example_rules() -> Self {
        Self { inner: StaticRoutingEngine::with_example_rules() }
    }
}

impl RoutingEngine for MockRoutingEngine {
    async fn route(&self, req: RouteRequest) -> Result<RoutingDecision, RoutingError> {
        let decision = self.inner.route(RouteRequest {
            transaction_id: req.transaction_id,
            merchant_id:    req.merchant_id.clone(),
            amount:         req.amount.clone(),
        }).await?;

        tracing::info!(
            transaction_id = %decision.transaction_id,
            selected_rail  = %decision.selected_rail.as_str(),
            currency       = %decision.currency,
            considered     = decision.considered.len(),
            "[MOCK ROUTING] decision logged"
        );

        for (rail, reason) in &decision.considered {
            tracing::debug!(
                rail   = %rail.as_str(),
                reason = %reason,
                "[MOCK ROUTING] rail considered but not selected"
            );
        }

        Ok(decision)
    }
}

// ---------------------------------------------------------------------------
// FailingRoutingEngine
// ---------------------------------------------------------------------------

/// A routing engine that always fails with `NoEligibleRail`.
///
/// Use this in tests or sandbox scenarios where you want to verify that
/// upstream callers handle routing failures gracefully.
pub struct FailingRoutingEngine {
    reason: String,
}

impl FailingRoutingEngine {
    pub fn new(reason: impl Into<String>) -> Self {
        Self { reason: reason.into() }
    }
}

impl RoutingEngine for FailingRoutingEngine {
    async fn route(&self, req: RouteRequest) -> Result<RoutingDecision, RoutingError> {
        tracing::warn!(
            transaction_id = %req.transaction_id,
            reason         = %self.reason,
            "[MOCK ROUTING] simulated routing failure"
        );
        let currency = req.amount.currency;
        Err(RoutingError::NoEligibleRail {
            currency,
            amount: req.amount,
        })
    }
}

// ---------------------------------------------------------------------------
// DegradedRoutingEngine
// ---------------------------------------------------------------------------

/// A routing engine that reports all eligible rails as degraded.
///
/// Useful for testing the `AllRailsDegraded` error path.
pub struct DegradedRoutingEngine;

impl RoutingEngine for DegradedRoutingEngine {
    async fn route(&self, req: RouteRequest) -> Result<RoutingDecision, RoutingError> {
        tracing::warn!(
            transaction_id = %req.transaction_id,
            "[MOCK ROUTING] simulated: all rails degraded"
        );
        Err(RoutingError::AllRailsDegraded)
    }
}

// ---------------------------------------------------------------------------
// SandboxRoutingEngine — convenience alias for the reference operator
// ---------------------------------------------------------------------------

/// The default routing engine for the Banzami sandbox.
///
/// Uses `StaticRoutingEngine::with_example_rules()` under the hood — a
/// multi-currency example ruleset with no operator-specific assumptions.
/// Logs every routing decision via `tracing`.
pub type SandboxRoutingEngine = MockRoutingEngine;

/// Create the default sandbox routing engine.
pub fn sandbox_routing_engine() -> SandboxRoutingEngine {
    MockRoutingEngine::with_example_rules()
}

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------

#[cfg(test)]
mod tests {
    use super::*;
    use banzami_types::{Currency, Money, MerchantId, TransactionId};

    fn aoa_request() -> RouteRequest {
        RouteRequest {
            transaction_id: TransactionId::new(),
            merchant_id:    MerchantId::new(),
            amount:         Money::new(100_000, Currency::AOA),
        }
    }

    #[tokio::test]
    async fn mock_engine_routes_aoa() {
        let engine = MockRoutingEngine::with_example_rules();
        let result = engine.route(aoa_request()).await;
        assert!(result.is_ok());
    }

    #[tokio::test]
    async fn failing_engine_returns_no_eligible_rail() {
        let engine = FailingRoutingEngine::new("unit test");
        let result = engine.route(aoa_request()).await;
        assert!(matches!(result, Err(RoutingError::NoEligibleRail { .. })));
    }

    #[tokio::test]
    async fn degraded_engine_returns_all_degraded() {
        let engine = DegradedRoutingEngine;
        let result = engine.route(aoa_request()).await;
        assert!(matches!(result, Err(RoutingError::AllRailsDegraded)));
    }

    #[tokio::test]
    async fn custom_rails_are_respected() {
        let engine = MockRoutingEngine::with_rails(vec![
            RailConfig { currency: Currency::USD, rail: PaymentRail::Visa, priority: 100 },
        ]);
        let req = RouteRequest {
            transaction_id: TransactionId::new(),
            merchant_id:    MerchantId::new(),
            amount:         Money::new(50_000, Currency::USD),
        };
        let decision = engine.route(req).await.unwrap();
        assert_eq!(decision.selected_rail, PaymentRail::Visa);
    }
}
