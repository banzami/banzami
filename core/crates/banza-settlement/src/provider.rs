use thiserror::Error;

use banza_types::{MerchantId, Money, WalletId};

use crate::SettlementId;

// ---------------------------------------------------------------------------
// Request / response types
// ---------------------------------------------------------------------------

/// Request to submit a settlement batch for external bank execution.
pub struct SubmitSettlementRequest {
    pub settlement_id: SettlementId,
    pub merchant_id:   MerchantId,
    pub wallet_id:     WalletId,
    /// Net amount to transfer to the merchant's bank account.
    pub amount:        Money,
    /// Operator-assigned reference for the external transfer.
    pub reference:     String,
}

/// Outcome of a settlement submission to an external provider.
pub struct SettlementSubmissionResult {
    /// Provider's own reference for this transfer (for reconciliation).
    pub provider_ref: String,
}

// ---------------------------------------------------------------------------
// Error
// ---------------------------------------------------------------------------

#[derive(Debug, Error)]
pub enum SettlementProviderError {
    #[error("settlement provider rejected submission: {0}")]
    Rejected(String),

    #[error("settlement provider unavailable: {0}")]
    Unavailable(String),

    #[error("settlement {0} not found by provider")]
    NotFound(SettlementId),
}

// ---------------------------------------------------------------------------
// Trait
// ---------------------------------------------------------------------------

/// Operator-implemented interface for executing settlement payouts.
///
/// The kernel handles batch creation and lifecycle tracking. The operator
/// implements this trait to connect the kernel to their bank / payment rail.
///
/// # Invariants the implementor must uphold
/// - Submission must be idempotent: submitting the same `settlement_id` twice
///   must not create duplicate bank transfers.
/// - `provider_ref` must be stable across retries for the same settlement.
/// - A simulated (sandbox) implementation must never make real bank calls.
#[allow(async_fn_in_trait)]
pub trait SettlementExecutionProvider: Send + Sync {
    fn provider_name(&self) -> &'static str;

    /// Submit a settlement batch for external bank transfer.
    async fn submit(
        &self,
        req: SubmitSettlementRequest,
    ) -> Result<SettlementSubmissionResult, SettlementProviderError>;

    /// Check the status of a previously submitted settlement.
    async fn check_status(
        &self,
        settlement_id: SettlementId,
        provider_ref:  &str,
    ) -> Result<SettlementStatus, SettlementProviderError>;
}

/// External settlement status — what the bank/provider reports.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum SettlementStatus {
    Pending,
    Completed,
    Failed { reason: String },
}

