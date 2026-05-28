//! Simulated settlement execution provider for local development.
//!
//! This is NOT a real bank integration. It accepts all settlements instantly
//! and logs them to stdout. No external banking system is contacted.

use banzami_settlement::{
    SettlementExecutionProvider, SettlementProviderError,
    SettlementSubmissionResult, SubmitSettlementRequest,
};
use banzami_settlement::provider::SettlementStatus;

/// A settlement provider that simulates immediate bank acceptance.
///
/// All submissions succeed with a fake provider reference.
/// Suitable for: local development, testing settlement lifecycle.
/// NOT suitable for: any production deployment.
pub struct SimulatedSettlementProvider;

impl SettlementExecutionProvider for SimulatedSettlementProvider {
    fn provider_name(&self) -> &'static str {
        "SIMULATED_SETTLEMENT"
    }

    async fn submit(
        &self,
        req: SubmitSettlementRequest,
    ) -> Result<SettlementSubmissionResult, SettlementProviderError> {
        let provider_ref = format!("SBX-SETTLE-{}", req.settlement_id.as_uuid());

        tracing::info!(
            settlement_id = %req.settlement_id,
            merchant_id   = %req.merchant_id,
            amount        = %req.amount,
            provider_ref  = %provider_ref,
            "[SANDBOX SETTLEMENT] settlement submitted (no real bank transfer)"
        );

        Ok(SettlementSubmissionResult { provider_ref })
    }

    async fn check_status(
        &self,
        settlement_id: banzami_types::SettlementId,
        provider_ref:  &str,
    ) -> Result<SettlementStatus, SettlementProviderError> {
        tracing::info!(
            settlement_id = %settlement_id,
            provider_ref  = %provider_ref,
            "[SANDBOX SETTLEMENT] status check — always returns Completed"
        );
        Ok(SettlementStatus::Completed)
    }
}
