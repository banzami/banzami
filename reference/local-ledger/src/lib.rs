//! SQLite-backed double-entry ledger for local development.
//!
//! This is a reference implementation of the the reference operator ledger semantics using
//! SQLite. It is NOT a production financial system — balances reset when you
//! delete the database file (or use `LocalLedger::open_in_memory()`).
//!
//! # Invariants
//!
//! The same financial invariants as the production ledger apply:
//! - Every posting must sum to zero (debits == credits per currency).
//! - Ledger entries are immutable after commit (never updated or deleted).
//! - `balance()` is always derived from entries, never stored separately.
//! - Posting with the same `idempotency_key` is idempotent.
//!
//! # Usage
//!
//! ```no_run
//! use local_ledger::LocalLedger;
//!
//! #[tokio::main]
//! async fn main() {
//!     let ledger = LocalLedger::open_in_memory().await.unwrap();
//!     ledger.seed().await.unwrap();
//!     let balance = ledger.balance("merchant-a").await.unwrap();
//!     println!("balance: {balance} minor units");
//! }
//! ```

use thiserror::Error;
use uuid::Uuid;

// ---------------------------------------------------------------------------
// Error
// ---------------------------------------------------------------------------

#[derive(Debug, Error)]
pub enum LocalLedgerError {
    #[error("posting is unbalanced: debits {debits} ≠ credits {credits} for currency {currency}")]
    UnbalancedPosting { debits: i64, credits: i64, currency: String },

    #[error("posting must have at least two entries")]
    InsufficientEntries,

    #[error("account not found: {0}")]
    AccountNotFound(String),

    #[error("duplicate idempotency key: {0}")]
    DuplicateIdempotencyKey(String),

    #[error("amount must be positive")]
    NonPositiveAmount,

    #[error("database error: {0}")]
    Database(#[from] sqlx::Error),
}

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

#[derive(Debug, Clone, serde::Serialize)]
pub struct LocalAccount {
    pub id:         String,
    pub label:      String,
    pub currency:   String,
    pub created_at: chrono::DateTime<chrono::Utc>,
}

#[derive(Debug, Clone, serde::Serialize)]
pub enum EntryKind { Debit, Credit }

#[derive(Debug, Clone, serde::Serialize)]
pub struct LocalEntry {
    pub account_id:   String,
    pub kind:         EntryKind,
    pub amount_minor: i64,
    pub currency:     String,
}

impl LocalEntry {
    pub fn debit(account_id: impl Into<String>, amount_minor: i64, currency: impl Into<String>) -> Self {
        Self { account_id: account_id.into(), kind: EntryKind::Debit, amount_minor, currency: currency.into() }
    }
    pub fn credit(account_id: impl Into<String>, amount_minor: i64, currency: impl Into<String>) -> Self {
        Self { account_id: account_id.into(), kind: EntryKind::Credit, amount_minor, currency: currency.into() }
    }
}

#[derive(Debug, Clone, serde::Serialize)]
pub struct LedgerRow {
    pub id:           String,
    pub account_id:   String,
    pub kind:         String,
    pub amount_minor: i64,
    pub currency:     String,
    pub posting_id:   String,
    pub created_at:   String,
}

// ---------------------------------------------------------------------------
// Ledger
// ---------------------------------------------------------------------------

pub struct LocalLedger {
    pool: sqlx::SqlitePool,
}

impl LocalLedger {
    /// Open (or create) a ledger at the given file path.
    pub async fn open(path: &str) -> Result<Self, LocalLedgerError> {
        let pool = sqlx::SqlitePool::connect(path).await?;
        let ledger = Self { pool };
        ledger.init_schema().await?;
        Ok(ledger)
    }

    /// Open an ephemeral in-memory ledger (resets when dropped).
    pub async fn open_in_memory() -> Result<Self, LocalLedgerError> {
        let pool = sqlx::SqlitePool::connect("sqlite::memory:").await?;
        let ledger = Self { pool };
        ledger.init_schema().await?;
        Ok(ledger)
    }

    async fn init_schema(&self) -> Result<(), LocalLedgerError> {
        sqlx::query(r#"
            CREATE TABLE IF NOT EXISTS accounts (
                id         TEXT PRIMARY KEY,
                label      TEXT NOT NULL,
                currency   TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS postings (
                id              TEXT PRIMARY KEY,
                idempotency_key TEXT NOT NULL UNIQUE,
                description     TEXT NOT NULL,
                created_at      TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS entries (
                id            TEXT PRIMARY KEY,
                posting_id    TEXT NOT NULL REFERENCES postings(id),
                account_id    TEXT NOT NULL REFERENCES accounts(id),
                kind          TEXT NOT NULL CHECK(kind IN ('DEBIT','CREDIT')),
                amount_minor  INTEGER NOT NULL CHECK(amount_minor > 0),
                currency      TEXT NOT NULL,
                created_at    TEXT NOT NULL
            );
        "#).execute(&self.pool).await?;
        Ok(())
    }

    /// Drop all data and recreate the schema (useful for test resets).
    pub async fn reset(&self) -> Result<(), LocalLedgerError> {
        sqlx::query("DROP TABLE IF EXISTS entries").execute(&self.pool).await?;
        sqlx::query("DROP TABLE IF EXISTS postings").execute(&self.pool).await?;
        sqlx::query("DROP TABLE IF EXISTS accounts").execute(&self.pool).await?;
        self.init_schema().await
    }

    // -----------------------------------------------------------------------
    // Accounts
    // -----------------------------------------------------------------------

    pub async fn create_account(
        &self,
        id:       impl Into<String>,
        label:    impl Into<String>,
        currency: impl Into<String>,
    ) -> Result<LocalAccount, LocalLedgerError> {
        let account = LocalAccount {
            id:         id.into(),
            label:      label.into(),
            currency:   currency.into(),
            created_at: chrono::Utc::now(),
        };
        sqlx::query(
            "INSERT OR IGNORE INTO accounts (id, label, currency, created_at) VALUES (?1, ?2, ?3, ?4)"
        )
        .bind(&account.id)
        .bind(&account.label)
        .bind(&account.currency)
        .bind(account.created_at.to_rfc3339())
        .execute(&self.pool)
        .await?;
        Ok(account)
    }

    pub async fn get_account(&self, id: &str) -> Result<Option<LocalAccount>, LocalLedgerError> {
        let row = sqlx::query_as::<_, (String, String, String, String)>(
            "SELECT id, label, currency, created_at FROM accounts WHERE id = ?1"
        )
        .bind(id)
        .fetch_optional(&self.pool)
        .await?;

        Ok(row.map(|(id, label, currency, created_at)| LocalAccount {
            id,
            label,
            currency,
            created_at: created_at.parse().unwrap_or_else(|_| chrono::Utc::now()),
        }))
    }

    pub async fn list_accounts(&self) -> Result<Vec<LocalAccount>, LocalLedgerError> {
        let rows = sqlx::query_as::<_, (String, String, String, String)>(
            "SELECT id, label, currency, created_at FROM accounts ORDER BY created_at ASC"
        )
        .fetch_all(&self.pool)
        .await?;

        Ok(rows.into_iter().map(|(id, label, currency, created_at)| LocalAccount {
            id, label, currency,
            created_at: created_at.parse().unwrap_or_else(|_| chrono::Utc::now()),
        }).collect())
    }

    // -----------------------------------------------------------------------
    // Postings
    // -----------------------------------------------------------------------

    /// Post a balanced journal entry atomically.
    ///
    /// `entries` must contain at least two entries and must balance
    /// (debits == credits for each currency). Posting with an existing
    /// `idempotency_key` returns the existing posting ID without creating
    /// duplicate entries.
    pub async fn post(
        &self,
        idempotency_key: impl Into<String>,
        description:     impl Into<String>,
        entries:         Vec<LocalEntry>,
    ) -> Result<String, LocalLedgerError> {
        let key = idempotency_key.into();
        let desc = description.into();

        if entries.len() < 2 {
            return Err(LocalLedgerError::InsufficientEntries);
        }
        for e in &entries {
            if e.amount_minor <= 0 {
                return Err(LocalLedgerError::NonPositiveAmount);
            }
        }

        // Balance check per currency.
        let mut sums: std::collections::HashMap<&str, i64> = std::collections::HashMap::new();
        for e in &entries {
            let sign = match e.kind { EntryKind::Debit => 1i64, EntryKind::Credit => -1i64 };
            *sums.entry(e.currency.as_str()).or_default() += sign * e.amount_minor;
        }
        for (currency, sum) in &sums {
            if *sum != 0 {
                let debits  = entries.iter().filter(|e| matches!(e.kind, EntryKind::Debit)  && e.currency.as_str() == *currency).map(|e| e.amount_minor).sum();
                let credits = entries.iter().filter(|e| matches!(e.kind, EntryKind::Credit) && e.currency.as_str() == *currency).map(|e| e.amount_minor).sum();
                return Err(LocalLedgerError::UnbalancedPosting {
                    debits, credits, currency: currency.to_string(),
                });
            }
        }

        // Idempotency: return existing if already posted.
        let existing: Option<(String,)> = sqlx::query_as(
            "SELECT id FROM postings WHERE idempotency_key = ?1"
        ).bind(&key).fetch_optional(&self.pool).await?;
        if let Some((id,)) = existing {
            return Ok(id);
        }

        let posting_id = Uuid::new_v4().to_string();
        let now = chrono::Utc::now().to_rfc3339();

        let mut tx = self.pool.begin().await?;

        sqlx::query(
            "INSERT INTO postings (id, idempotency_key, description, created_at) VALUES (?1,?2,?3,?4)"
        )
        .bind(&posting_id).bind(&key).bind(&desc).bind(&now)
        .execute(&mut *tx).await?;

        for entry in &entries {
            let kind_str = match entry.kind { EntryKind::Debit => "DEBIT", EntryKind::Credit => "CREDIT" };
            sqlx::query(
                "INSERT INTO entries (id, posting_id, account_id, kind, amount_minor, currency, created_at) VALUES (?1,?2,?3,?4,?5,?6,?7)"
            )
            .bind(Uuid::new_v4().to_string())
            .bind(&posting_id)
            .bind(&entry.account_id)
            .bind(kind_str)
            .bind(entry.amount_minor)
            .bind(&entry.currency)
            .bind(&now)
            .execute(&mut *tx).await?;
        }

        tx.commit().await?;

        tracing::debug!(
            posting_id = %posting_id,
            entries    = entries.len(),
            "[LOCAL LEDGER] posting committed"
        );

        Ok(posting_id)
    }

    // -----------------------------------------------------------------------
    // Queries
    // -----------------------------------------------------------------------

    /// Derive the current balance of an account from its entries.
    ///
    /// Credits increase the balance; debits decrease it. Returns 0 for accounts
    /// with no entries.
    pub async fn balance(&self, account_id: &str) -> Result<i64, LocalLedgerError> {
        let row: Option<(Option<i64>,)> = sqlx::query_as(r#"
            SELECT SUM(CASE kind WHEN 'CREDIT' THEN amount_minor ELSE -amount_minor END)
            FROM entries WHERE account_id = ?1
        "#).bind(account_id).fetch_optional(&self.pool).await?;

        Ok(row.and_then(|(v,)| v).unwrap_or(0))
    }

    pub async fn entries_for_account(&self, account_id: &str) -> Result<Vec<LedgerRow>, LocalLedgerError> {
        sqlx::query_as::<_, (String, String, String, String, i64, String, String)>(r#"
            SELECT e.id, e.account_id, e.kind, e.posting_id, e.amount_minor, e.currency, e.created_at
            FROM entries e WHERE e.account_id = ?1 ORDER BY e.created_at ASC
        "#)
        .bind(account_id)
        .fetch_all(&self.pool)
        .await
        .map(|rows| rows.into_iter().map(|(id, account_id, kind, posting_id, amount_minor, currency, created_at)| {
            LedgerRow { id, account_id, kind, posting_id, amount_minor, currency, created_at }
        }).collect())
        .map_err(LocalLedgerError::from)
    }

    // -----------------------------------------------------------------------
    // Seed data
    // -----------------------------------------------------------------------

    /// Populate the ledger with deterministic seed accounts and transactions.
    ///
    /// Safe to call multiple times (idempotent via INSERT OR IGNORE / idempotency keys).
    pub async fn seed(&self) -> Result<(), LocalLedgerError> {
        // Chart of accounts
        self.create_account("float",      "Float (Transit)",       "AOA").await?;
        self.create_account("merchant-a", "Sandbox Merchant A",    "AOA").await?;
        self.create_account("merchant-b", "Sandbox Merchant B",    "AOA").await?;
        self.create_account("consumer-1", "Sandbox Consumer 1",    "AOA").await?;
        self.create_account("consumer-2", "Sandbox Consumer 2",    "AOA").await?;
        self.create_account("fees",       "Fee Collection",        "AOA").await?;

        // Seed: fund merchant-a from float (10 000 000 AOA = 100 000.00 AOA)
        self.post("seed-merchant-a-init", "Initial seed — Merchant A", vec![
            LocalEntry::debit("float",      10_000_000, "AOA"),
            LocalEntry::credit("merchant-a", 10_000_000, "AOA"),
        ]).await?;

        // Seed: fund merchant-b (5 000 000 AOA)
        self.post("seed-merchant-b-init", "Initial seed — Merchant B", vec![
            LocalEntry::debit("float",       5_000_000, "AOA"),
            LocalEntry::credit("merchant-b",  5_000_000, "AOA"),
        ]).await?;

        // Seed: fund consumer-1 (2 000 000 AOA)
        self.post("seed-consumer-1-init", "Initial seed — Consumer 1", vec![
            LocalEntry::debit("float",       2_000_000, "AOA"),
            LocalEntry::credit("consumer-1", 2_000_000, "AOA"),
        ]).await?;

        // Seed: fund consumer-2 (500 000 AOA)
        self.post("seed-consumer-2-init", "Initial seed — Consumer 2", vec![
            LocalEntry::debit("float",       500_000, "AOA"),
            LocalEntry::credit("consumer-2",  500_000, "AOA"),
        ]).await?;

        // Seed: a payment from consumer-1 to merchant-a (50 000 AOA + 500 fee)
        self.post("seed-payment-001", "Demo payment — Consumer 1 → Merchant A", vec![
            LocalEntry::debit("consumer-1", 50_500, "AOA"),
            LocalEntry::credit("merchant-a", 50_000, "AOA"),
            LocalEntry::credit("fees",           500, "AOA"),
        ]).await?;

        tracing::info!("[LOCAL LEDGER] seed data applied — 5 accounts, 5 postings");
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    async fn seeded() -> LocalLedger {
        let l = LocalLedger::open_in_memory().await.unwrap();
        l.seed().await.unwrap();
        l
    }

    #[tokio::test]
    async fn balance_after_seed_is_correct() {
        let l = seeded().await;
        assert_eq!(l.balance("merchant-a").await.unwrap(), 10_050_000);
        assert_eq!(l.balance("consumer-1").await.unwrap(), 1_949_500);
    }

    #[tokio::test]
    async fn posting_is_idempotent() {
        let l = seeded().await;
        let id1 = l.post("idem-test", "test", vec![
            LocalEntry::debit("consumer-1",   1_000, "AOA"),
            LocalEntry::credit("merchant-a",  1_000, "AOA"),
        ]).await.unwrap();
        let id2 = l.post("idem-test", "test", vec![
            LocalEntry::debit("consumer-1",   1_000, "AOA"),
            LocalEntry::credit("merchant-a",  1_000, "AOA"),
        ]).await.unwrap();
        assert_eq!(id1, id2);
    }

    #[tokio::test]
    async fn unbalanced_posting_is_rejected() {
        let l = seeded().await;
        let result = l.post("bad", "bad", vec![
            LocalEntry::debit("consumer-1",   1_000, "AOA"),
            LocalEntry::credit("merchant-a",    999, "AOA"),
        ]).await;
        assert!(matches!(result, Err(LocalLedgerError::UnbalancedPosting { .. })));
    }

    #[tokio::test]
    async fn balance_is_derived_not_stored() {
        let l = LocalLedger::open_in_memory().await.unwrap();
        l.create_account("a", "A", "AOA").await.unwrap();
        l.create_account("b", "B", "AOA").await.unwrap();
        assert_eq!(l.balance("a").await.unwrap(), 0);

        l.post("p1", "fund a", vec![
            LocalEntry::debit("b",  1_000, "AOA"),
            LocalEntry::credit("a", 1_000, "AOA"),
        ]).await.unwrap();
        assert_eq!(l.balance("a").await.unwrap(),  1_000);
        assert_eq!(l.balance("b").await.unwrap(), -1_000);
    }
}
