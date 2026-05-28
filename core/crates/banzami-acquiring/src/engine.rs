use chrono::Utc;
use banzami_types::{AcquiringPaymentId, Money, PaymentLinkId};

use crate::{
    AcquiringCallback, AcquiringError, AcquiringPayment, AcquiringPaymentStatus,
};
use crate::provider::{AcquirerProvider, InitiatePaymentRequest};
use crate::repository::{AcquiringRepository, PostgresAcquiringRepository};

// ---------------------------------------------------------------------------
// Trait
// ---------------------------------------------------------------------------

#[allow(async_fn_in_trait)]
pub trait AcquiringEngine: Send + Sync {
    /// Initiate a new payment for the given payment link.
    /// Calls the configured provider, stores the acquiring record, and returns
    /// the payment with instructions the customer will use to complete payment.
    async fn initiate_payment(
        &self,
        payment_link_id: PaymentLinkId,
        amount:          Money,
    ) -> Result<AcquiringPayment, AcquiringError>;

    /// Process an inbound provider callback (HMAC-validated, idempotent).
    /// Records the raw callback, marks the acquiring payment as confirmed,
    /// and returns the updated payment record for downstream orchestration.
    async fn process_callback(
        &self,
        raw_body:  &[u8],
        signature: &str,
    ) -> Result<AcquiringPayment, AcquiringError>;

    /// Retrieve a single acquiring payment by its internal ID.
    async fn get_payment(
        &self,
        id: AcquiringPaymentId,
    ) -> Result<AcquiringPayment, AcquiringError>;

    /// Retrieve an acquiring payment by the provider's external reference.
    async fn get_payment_by_external_ref(
        &self,
        external_ref: &str,
    ) -> Result<AcquiringPayment, AcquiringError>;

    /// Returns the name of the currently configured provider.
    fn provider_name(&self) -> &str;

    /// Initiate a payment without a payment link — used for consumer deposits.
    /// Returns `(external_ref, instructions, expires_at)` directly from the provider.
    async fn initiate_raw(
        &self,
        internal_ref: &str,
        amount:       Money,
    ) -> Result<crate::provider::ExternalPaymentRef, AcquiringError>;

    /// Validate an inbound callback without storing or updating acquiring_payments.
    /// Used by the consumer deposit handler which manages its own table.
    async fn validate_callback_raw(
        &self,
        raw_body:  &[u8],
        signature: &str,
    ) -> Result<crate::provider::PaymentConfirmation, AcquiringError>;

    /// Generate a signed test callback payload (sandbox / simulated providers only).
    /// Returns `None` for production providers.
    fn generate_test_callback(
        &self,
        external_ref: &str,
        amount_minor: i64,
        currency:     &str,
    ) -> Option<(Vec<u8>, String)>;
}

// ---------------------------------------------------------------------------
// PostgreSQL implementation — generic over any AcquirerProvider
//
// Operators bring their own provider implementation. Example:
//
//   let engine = PostgresAcquiringEngine::new(MyProvider::new(...), repo);
//
// where `MyProvider` implements `AcquirerProvider`.
// ---------------------------------------------------------------------------

pub struct PostgresAcquiringEngine<P: AcquirerProvider> {
    provider: P,
    repo:     PostgresAcquiringRepository,
}

impl<P: AcquirerProvider> PostgresAcquiringEngine<P> {
    pub fn new(provider: P, repo: PostgresAcquiringRepository) -> Self {
        Self { provider, repo }
    }
}

impl<P: AcquirerProvider + Send + Sync> AcquiringEngine for PostgresAcquiringEngine<P> {
    async fn initiate_payment(
        &self,
        payment_link_id: PaymentLinkId,
        amount:          Money,
    ) -> Result<AcquiringPayment, AcquiringError> {
        let payment_id = AcquiringPaymentId::new();

        let req = InitiatePaymentRequest {
            internal_ref: payment_id.as_uuid().to_string(),
            amount:       amount.clone(),
            description:  None,
        };

        let ext = self.provider
            .initiate_payment(req)
            .await
            .map_err(AcquiringError::Provider)?;

        let payment = AcquiringPayment {
            id:              payment_id,
            payment_link_id,
            provider:        self.provider.provider_name().to_string(),
            external_ref:    ext.external_ref,
            status:          AcquiringPaymentStatus::Pending,
            amount,
            instructions:    ext.instructions,
            confirmed_at:    None,
            failed_at:       None,
            failure_reason:  None,
            expires_at:      ext.expires_at,
            created_at:      Utc::now(),
        };

        self.repo.create_payment(&payment).await?;

        tracing::info!(
            payment_id    = %payment.id,
            external_ref  = %payment.external_ref,
            provider      = %payment.provider,
            "acquiring: payment initiated"
        );

        Ok(payment)
    }

    async fn process_callback(
        &self,
        raw_body:  &[u8],
        signature: &str,
    ) -> Result<AcquiringPayment, AcquiringError> {
        let confirmation = self.provider
            .validate_callback(raw_body, signature)
            .await
            .map_err(AcquiringError::Provider)?;

        // Idempotency: if this callback was already processed, return the
        // current payment state without re-running confirmation logic.
        if self.repo.callback_already_processed(&confirmation.idempotency_key).await? {
            tracing::info!(
                idempotency_key = %confirmation.idempotency_key,
                "acquiring: duplicate callback, skipping"
            );
            return self.repo.get_payment_by_external_ref(&confirmation.external_ref).await;
        }

        // Persist the raw callback before touching the payment record.
        let raw_json: serde_json::Value = serde_json::from_slice(raw_body)
            .unwrap_or(serde_json::Value::Null);

        let cb = AcquiringCallback {
            id:              uuid::Uuid::new_v4(),
            provider:        self.provider.provider_name().to_string(),
            raw_payload:     raw_json,
            signature:       signature.to_string(),
            external_ref:    Some(confirmation.external_ref.clone()),
            idempotency_key: confirmation.idempotency_key.clone(),
            received_at:     Utc::now(),
        };
        self.repo.record_callback(&cb).await?;

        // Resolve the internal payment record and confirm it.
        let payment = self.repo
            .get_payment_by_external_ref(&confirmation.external_ref)
            .await?;

        let confirmed = self.repo
            .confirm_payment(payment.id, confirmation.confirmed_at)
            .await?;

        tracing::info!(
            payment_id   = %confirmed.id,
            external_ref = %confirmed.external_ref,
            "acquiring: payment confirmed via callback"
        );

        Ok(confirmed)
    }

    async fn get_payment(
        &self,
        id: AcquiringPaymentId,
    ) -> Result<AcquiringPayment, AcquiringError> {
        self.repo.get_payment(id).await
    }

    async fn get_payment_by_external_ref(
        &self,
        external_ref: &str,
    ) -> Result<AcquiringPayment, AcquiringError> {
        self.repo.get_payment_by_external_ref(external_ref).await
    }

    fn provider_name(&self) -> &str {
        self.provider.provider_name()
    }

    async fn initiate_raw(
        &self,
        internal_ref: &str,
        amount:       Money,
    ) -> Result<crate::provider::ExternalPaymentRef, AcquiringError> {
        let req = crate::provider::InitiatePaymentRequest {
            internal_ref: internal_ref.to_string(),
            amount,
            description:  Some("Consumer deposit".to_string()),
        };
        self.provider.initiate_payment(req).await.map_err(AcquiringError::Provider)
    }

    async fn validate_callback_raw(
        &self,
        raw_body:  &[u8],
        signature: &str,
    ) -> Result<crate::provider::PaymentConfirmation, AcquiringError> {
        self.provider
            .validate_callback(raw_body, signature)
            .await
            .map_err(AcquiringError::Provider)
    }

    fn generate_test_callback(
        &self,
        external_ref: &str,
        amount_minor: i64,
        currency:     &str,
    ) -> Option<(Vec<u8>, String)> {
        self.provider.generate_test_callback(external_ref, amount_minor, currency)
    }
}
