//! Simulated AcquirerProvider for local development.
//!
//! This is NOT a real payment provider. It generates fake references,
//! signs callbacks with a local HMAC secret, and makes zero external calls.
//! Use it to experiment with the Banzami acquiring flow without any credentials.

use chrono::Utc;
use hmac::{Hmac, Mac};
use sha2::Sha256;

use banzami_acquiring::provider::{
    AcquirerError, AcquirerProvider, ExternalPaymentRef, InitiatePaymentRequest,
    PaymentConfirmation, PaymentInstructions,
};

const FAKE_SECRET: &[u8] = b"banzami-sandbox-hmac-secret-not-for-production";

/// A simulated acquiring provider for local development.
///
/// Generates deterministic-looking payment references and produces
/// HMAC-signed callback payloads that the acquiring engine can validate.
pub struct FakeAcquirer {
    entity_id: String,
}

impl FakeAcquirer {
    pub fn new() -> Self {
        Self { entity_id: "99999".to_string() }
    }

    pub fn with_entity_id(entity_id: impl Into<String>) -> Self {
        Self { entity_id: entity_id.into() }
    }

    fn sign(&self, payload: &[u8]) -> String {
        let mut mac = Hmac::<Sha256>::new_from_slice(FAKE_SECRET)
            .expect("HMAC accepts any key size");
        mac.update(payload);
        hex::encode(mac.finalize().into_bytes())
    }

    fn fake_reference() -> String {
        use rand::Rng;
        let mut rng = rand::thread_rng();
        format!("SBX{:09}", rng.gen_range(100_000_000u64..999_999_999))
    }
}

impl Default for FakeAcquirer {
    fn default() -> Self {
        Self::new()
    }
}

impl AcquirerProvider for FakeAcquirer {
    fn provider_name(&self) -> &'static str {
        "SIMULATED"
    }

    async fn initiate_payment(
        &self,
        req: InitiatePaymentRequest,
    ) -> Result<ExternalPaymentRef, AcquirerError> {
        let external_ref = Self::fake_reference();

        tracing::info!(
            internal_ref = %req.internal_ref,
            external_ref = %external_ref,
            amount       = %req.amount,
            "fake-acquirer: payment initiated (no real network call)"
        );

        Ok(ExternalPaymentRef {
            external_ref: external_ref.clone(),
            instructions: PaymentInstructions {
                method:    "SIMULATED".into(),
                entity:    self.entity_id.clone(),
                reference: external_ref,
            },
            expires_at: Utc::now() + chrono::Duration::minutes(30),
        })
    }

    async fn validate_callback(
        &self,
        raw_body:  &[u8],
        signature: &str,
    ) -> Result<PaymentConfirmation, AcquirerError> {
        let expected = self.sign(raw_body);
        if expected != signature {
            return Err(AcquirerError::InvalidSignature);
        }

        let body: serde_json::Value = serde_json::from_slice(raw_body)
            .map_err(|e| AcquirerError::MalformedPayload(e.to_string()))?;

        let external_ref = body["external_ref"]
            .as_str()
            .ok_or_else(|| AcquirerError::MalformedPayload("missing external_ref".into()))?
            .to_string();

        let idempotency_key = body["idempotency_key"]
            .as_str()
            .ok_or_else(|| AcquirerError::MalformedPayload("missing idempotency_key".into()))?
            .to_string();

        let amount_minor = body["amount_minor"]
            .as_i64()
            .ok_or_else(|| AcquirerError::MalformedPayload("missing amount_minor".into()))?;

        let currency = body["currency"]
            .as_str()
            .ok_or_else(|| AcquirerError::MalformedPayload("missing currency".into()))?
            .to_string();

        Ok(PaymentConfirmation {
            external_ref,
            idempotency_key,
            amount_minor,
            currency,
            confirmed_at: Utc::now(),
        })
    }

    fn generate_test_callback(
        &self,
        external_ref:  &str,
        amount_minor:  i64,
        currency:      &str,
    ) -> Option<(Vec<u8>, String)> {
        let idempotency_key = format!("sandbox-cb-{external_ref}");
        let payload = serde_json::json!({
            "external_ref":     external_ref,
            "idempotency_key":  idempotency_key,
            "amount_minor":     amount_minor,
            "currency":         currency,
            "confirmed_at":     Utc::now().to_rfc3339(),
        });

        let raw = serde_json::to_vec(&payload).expect("serialization cannot fail");
        let signature = self.sign(&raw);
        Some((raw, signature))
    }
}
