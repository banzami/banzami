use chrono::{DateTime, Utc};
use sqlx::PgPool;

use banzami_types::{AcquiringPaymentId, PaymentLinkId};

use crate::{AcquiringCallback, AcquiringError, AcquiringPayment, AcquiringPaymentStatus};
use crate::provider::PaymentInstructions;

// ---------------------------------------------------------------------------
// Trait
// ---------------------------------------------------------------------------

#[allow(async_fn_in_trait)]
pub trait AcquiringRepository: Send + Sync {
    async fn create_payment(&self, p: &AcquiringPayment) -> Result<(), AcquiringError>;

    async fn get_payment(
        &self,
        id: AcquiringPaymentId,
    ) -> Result<AcquiringPayment, AcquiringError>;

    async fn get_payment_by_external_ref(
        &self,
        external_ref: &str,
    ) -> Result<AcquiringPayment, AcquiringError>;

    async fn confirm_payment(
        &self,
        id:           AcquiringPaymentId,
        confirmed_at: DateTime<Utc>,
    ) -> Result<AcquiringPayment, AcquiringError>;

    async fn fail_payment(
        &self,
        id:     AcquiringPaymentId,
        reason: String,
    ) -> Result<AcquiringPayment, AcquiringError>;

    async fn record_callback(&self, cb: &AcquiringCallback) -> Result<(), AcquiringError>;

    async fn callback_already_processed(
        &self,
        idempotency_key: &str,
    ) -> Result<bool, AcquiringError>;
}

// ---------------------------------------------------------------------------
// Row projections
// ---------------------------------------------------------------------------

#[derive(sqlx::FromRow)]
struct AcquiringPaymentRow {
    id:              uuid::Uuid,
    payment_link_id: uuid::Uuid,
    provider:        String,
    external_ref:    String,
    status:          String,
    amount_minor:    i64,
    currency:        String,
    instructions:    serde_json::Value,
    confirmed_at:    Option<DateTime<Utc>>,
    failed_at:       Option<DateTime<Utc>>,
    failure_reason:  Option<String>,
    expires_at:      DateTime<Utc>,
    created_at:      DateTime<Utc>,
}

fn row_to_payment(row: AcquiringPaymentRow) -> Result<AcquiringPayment, AcquiringError> {
    let status = match row.status.as_str() {
        "PENDING"   => AcquiringPaymentStatus::Pending,
        "CONFIRMED" => AcquiringPaymentStatus::Confirmed,
        "FAILED"    => AcquiringPaymentStatus::Failed,
        other       => return Err(AcquiringError::UnknownStatus(other.to_string())),
    };

    let currency = banzami_types::Currency::from_code(&row.currency)
        .ok_or_else(|| AcquiringError::Internal(format!("unknown currency: {}", row.currency)))?;

    let instructions: PaymentInstructions = serde_json::from_value(row.instructions)
        .map_err(|e| AcquiringError::Internal(e.to_string()))?;

    Ok(AcquiringPayment {
        id:              AcquiringPaymentId::from_uuid(row.id),
        payment_link_id: PaymentLinkId::from_uuid(row.payment_link_id),
        provider:        row.provider,
        external_ref:    row.external_ref,
        status,
        amount:          banzami_types::Money::new(row.amount_minor, currency),
        instructions,
        confirmed_at:    row.confirmed_at,
        failed_at:       row.failed_at,
        failure_reason:  row.failure_reason,
        expires_at:      row.expires_at,
        created_at:      row.created_at,
    })
}

// ---------------------------------------------------------------------------
// PostgreSQL implementation
// ---------------------------------------------------------------------------

pub struct PostgresAcquiringRepository {
    pool: PgPool,
}

impl PostgresAcquiringRepository {
    pub fn new(pool: PgPool) -> Self {
        Self { pool }
    }
}

impl AcquiringRepository for PostgresAcquiringRepository {
    async fn create_payment(&self, p: &AcquiringPayment) -> Result<(), AcquiringError> {
        let instructions = serde_json::to_value(&p.instructions)
            .map_err(|e| AcquiringError::Internal(e.to_string()))?;

        sqlx::query(r#"
            INSERT INTO acquiring_payments
                (id, payment_link_id, provider, external_ref, status,
                 amount_minor, currency, instructions, expires_at, created_at)
            VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10)
        "#)
        .bind(p.id.as_uuid())
        .bind(p.payment_link_id.as_uuid())
        .bind(&p.provider)
        .bind(&p.external_ref)
        .bind(p.status.as_str())
        .bind(p.amount.amount_minor())
        .bind(p.amount.currency.code())
        .bind(instructions)
        .bind(p.expires_at)
        .bind(p.created_at)
        .execute(&self.pool)
        .await
        .map_err(AcquiringError::Database)?;
        Ok(())
    }

    async fn get_payment(
        &self,
        id: AcquiringPaymentId,
    ) -> Result<AcquiringPayment, AcquiringError> {
        sqlx::query_as::<_, AcquiringPaymentRow>(r#"
            SELECT id, payment_link_id, provider, external_ref, status,
                   amount_minor, currency, instructions,
                   confirmed_at, failed_at, failure_reason, expires_at, created_at
            FROM acquiring_payments WHERE id = $1
        "#)
        .bind(id.as_uuid())
        .fetch_optional(&self.pool)
        .await
        .map_err(AcquiringError::Database)?
        .ok_or(AcquiringError::NotFound(id))
        .and_then(row_to_payment)
    }

    async fn get_payment_by_external_ref(
        &self,
        external_ref: &str,
    ) -> Result<AcquiringPayment, AcquiringError> {
        sqlx::query_as::<_, AcquiringPaymentRow>(r#"
            SELECT id, payment_link_id, provider, external_ref, status,
                   amount_minor, currency, instructions,
                   confirmed_at, failed_at, failure_reason, expires_at, created_at
            FROM acquiring_payments WHERE external_ref = $1
        "#)
        .bind(external_ref)
        .fetch_optional(&self.pool)
        .await
        .map_err(AcquiringError::Database)?
        .ok_or_else(|| AcquiringError::ExternalRefNotFound(external_ref.to_string()))
        .and_then(row_to_payment)
    }

    async fn confirm_payment(
        &self,
        id:           AcquiringPaymentId,
        confirmed_at: DateTime<Utc>,
    ) -> Result<AcquiringPayment, AcquiringError> {
        sqlx::query_as::<_, AcquiringPaymentRow>(r#"
            UPDATE acquiring_payments
            SET status = 'CONFIRMED', confirmed_at = $2
            WHERE id = $1
            RETURNING id, payment_link_id, provider, external_ref, status,
                      amount_minor, currency, instructions,
                      confirmed_at, failed_at, failure_reason, expires_at, created_at
        "#)
        .bind(id.as_uuid())
        .bind(confirmed_at)
        .fetch_optional(&self.pool)
        .await
        .map_err(AcquiringError::Database)?
        .ok_or(AcquiringError::NotFound(id))
        .and_then(row_to_payment)
    }

    async fn fail_payment(
        &self,
        id:     AcquiringPaymentId,
        reason: String,
    ) -> Result<AcquiringPayment, AcquiringError> {
        let now = Utc::now();
        sqlx::query_as::<_, AcquiringPaymentRow>(r#"
            UPDATE acquiring_payments
            SET status = 'FAILED', failed_at = $2, failure_reason = $3
            WHERE id = $1
            RETURNING id, payment_link_id, provider, external_ref, status,
                      amount_minor, currency, instructions,
                      confirmed_at, failed_at, failure_reason, expires_at, created_at
        "#)
        .bind(id.as_uuid())
        .bind(now)
        .bind(reason)
        .fetch_optional(&self.pool)
        .await
        .map_err(AcquiringError::Database)?
        .ok_or(AcquiringError::NotFound(id))
        .and_then(row_to_payment)
    }

    async fn record_callback(&self, cb: &AcquiringCallback) -> Result<(), AcquiringError> {
        sqlx::query(r#"
            INSERT INTO acquiring_callbacks
               (id, provider, raw_payload, signature, external_ref, idempotency_key,
                processed, received_at)
            VALUES ($1,$2,$3,$4,$5,$6,false,$7)
            ON CONFLICT (idempotency_key) DO NOTHING
        "#)
        .bind(cb.id)
        .bind(&cb.provider)
        .bind(&cb.raw_payload)
        .bind(&cb.signature)
        .bind(&cb.external_ref)
        .bind(&cb.idempotency_key)
        .bind(cb.received_at)
        .execute(&self.pool)
        .await
        .map_err(AcquiringError::Database)?;
        Ok(())
    }

    async fn callback_already_processed(
        &self,
        idempotency_key: &str,
    ) -> Result<bool, AcquiringError> {
        let processed: Option<bool> = sqlx::query_scalar(
            "SELECT processed FROM acquiring_callbacks WHERE idempotency_key = $1"
        )
        .bind(idempotency_key)
        .fetch_optional(&self.pool)
        .await
        .map_err(AcquiringError::Database)?;
        Ok(processed.unwrap_or(false))
    }
}
