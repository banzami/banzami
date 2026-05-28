use sqlx::PgPool;
use uuid::Uuid;

use banzami_types::{ReconciliationRunId, SettlementId, TransactionId};

use crate::{
    ReconciliationError, ReconciliationRecord, ReconciliationReport, ReconciliationStatus,
};

// ---------------------------------------------------------------------------
// Trait
// ---------------------------------------------------------------------------

#[allow(async_fn_in_trait)]
pub trait ReconciliationRepository: Send + Sync {
    async fn save_report(&self, report: &ReconciliationReport) -> Result<(), ReconciliationError>;
    async fn get_report(
        &self,
        run_id: ReconciliationRunId,
    ) -> Result<ReconciliationReport, ReconciliationError>;
}

// ---------------------------------------------------------------------------
// Row projections
// ---------------------------------------------------------------------------

#[derive(sqlx::FromRow)]
struct RunRow {
    #[allow(dead_code)]
    id:                      Uuid,
    total_checked:           i64,
    matched:                 i64,
    missing_external:        i64,
    missing_internal:        i64,
    amount_mismatches:       i64,
    total_discrepancy_minor: i64,
    generated_at:            chrono::DateTime<chrono::Utc>,
}

#[derive(sqlx::FromRow)]
struct RecordRow {
    #[allow(dead_code)]
    id:               Uuid,
    run_id:           Uuid,
    settlement_id:    Option<Uuid>,
    transaction_id:   Option<Uuid>,
    external_ref:     Option<String>,
    internal_minor:   Option<i64>,
    external_minor:   Option<i64>,
    currency:         String,
    status:           String,
    discrepancy_minor: i64,
    reconciled_at:    chrono::DateTime<chrono::Utc>,
}

fn row_to_record(r: RecordRow) -> Result<ReconciliationRecord, ReconciliationError> {
    let status = ReconciliationStatus::try_from_str(&r.status)
        .ok_or_else(|| ReconciliationError::UnknownStatus(r.status.clone()))?;
    Ok(ReconciliationRecord {
        run_id:            ReconciliationRunId::from_uuid(r.run_id),
        settlement_id:     r.settlement_id.map(SettlementId::from_uuid),
        transaction_id:    r.transaction_id.map(TransactionId::from_uuid),
        external_ref:      r.external_ref,
        internal_minor:    r.internal_minor,
        external_minor:    r.external_minor,
        currency:          r.currency,
        status,
        discrepancy_minor: r.discrepancy_minor,
        reconciled_at:     r.reconciled_at,
    })
}

// ---------------------------------------------------------------------------
// PostgreSQL implementation
// ---------------------------------------------------------------------------

pub struct PostgresReconciliationRepository {
    pool: PgPool,
}

impl PostgresReconciliationRepository {
    pub fn new(pool: PgPool) -> Self {
        Self { pool }
    }
}

impl ReconciliationRepository for PostgresReconciliationRepository {
    async fn save_report(&self, report: &ReconciliationReport) -> Result<(), ReconciliationError> {
        let mut tx = self.pool.begin().await?;

        sqlx::query(r#"
            INSERT INTO reconciliation_runs (
                id, total_checked, matched, missing_external, missing_internal,
                amount_mismatches, total_discrepancy_minor, generated_at
            ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8)
        "#)
        .bind(report.run_id.as_uuid())
        .bind(report.total_checked as i64)
        .bind(report.matched as i64)
        .bind(report.missing_external as i64)
        .bind(report.missing_internal as i64)
        .bind(report.amount_mismatches as i64)
        .bind(report.total_discrepancy_minor)
        .bind(report.generated_at)
        .execute(&mut *tx)
        .await?;

        for record in &report.records {
            sqlx::query(r#"
                INSERT INTO reconciliation_records (
                    run_id, settlement_id, transaction_id, external_ref,
                    internal_minor, external_minor, currency, status,
                    discrepancy_minor, reconciled_at
                ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10)
            "#)
            .bind(record.run_id.as_uuid())
            .bind(record.settlement_id.map(|id| id.as_uuid()))
            .bind(record.transaction_id.map(|id| id.as_uuid()))
            .bind(record.external_ref.as_deref())
            .bind(record.internal_minor)
            .bind(record.external_minor)
            .bind(&record.currency)
            .bind(record.status.as_str())
            .bind(record.discrepancy_minor)
            .bind(record.reconciled_at)
            .execute(&mut *tx)
            .await?;
        }

        tx.commit().await?;
        Ok(())
    }

    async fn get_report(
        &self,
        run_id: ReconciliationRunId,
    ) -> Result<ReconciliationReport, ReconciliationError> {
        let run = sqlx::query_as::<_, RunRow>(
            "SELECT id, total_checked, matched, missing_external, missing_internal,
                    amount_mismatches, total_discrepancy_minor, generated_at
             FROM reconciliation_runs WHERE id = $1"
        )
        .bind(run_id.as_uuid())
        .fetch_optional(&self.pool)
        .await?
        .ok_or(ReconciliationError::NotFound(run_id))?;

        let record_rows = sqlx::query_as::<_, RecordRow>(
            "SELECT id, run_id, settlement_id, transaction_id, external_ref,
                    internal_minor, external_minor, currency, status,
                    discrepancy_minor, reconciled_at
             FROM reconciliation_records WHERE run_id = $1 ORDER BY reconciled_at"
        )
        .bind(run_id.as_uuid())
        .fetch_all(&self.pool)
        .await?;

        let records: Result<Vec<_>, _> = record_rows.into_iter().map(row_to_record).collect();
        let records = records?;

        Ok(ReconciliationReport {
            run_id,
            total_checked:           run.total_checked as u64,
            matched:                 run.matched as u64,
            missing_external:        run.missing_external as u64,
            missing_internal:        run.missing_internal as u64,
            amount_mismatches:       run.amount_mismatches as u64,
            records,
            total_discrepancy_minor: run.total_discrepancy_minor,
            generated_at:            run.generated_at,
        })
    }
}
