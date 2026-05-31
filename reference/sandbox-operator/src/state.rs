//! In-memory state for the sandbox operator.
//!
//! All state resets on restart — intentional for a development sandbox.
//! The broadcast channel fans out events to SSE subscribers in real time.
//!
//! Every operation that mutates state generates a TraceContext that threads
//! trace_id/correlation_id/causation_id through all resulting ledger entries,
//! events, and derived operations, so the full causal chain is always queryable.

use std::collections::{HashMap, HashSet};
use std::sync::Mutex;

use banza_types::Currency;
use tokio::sync::broadcast;
use uuid::Uuid;

use crate::events::{types as ev, SandboxEvent};

// ---------------------------------------------------------------------------
// Trace context
// ---------------------------------------------------------------------------

/// Carries the causal chain through a payment flow.
///
/// `trace_id`      — one UUID per top-level operation (shared across all
///                   derived operations in the same flow).
/// `correlation_id`— identifies the current aggregate within the trace (changes
///                   as the operation moves through layers).
/// `causation_id`  — the ID of the operation that directly caused this one.
#[derive(Debug, Clone, serde::Serialize)]
pub struct TraceContext {
    pub trace_id:       String,
    pub correlation_id: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub causation_id:   Option<String>,
}

impl TraceContext {
    /// New root trace — used for top-level operations (direct transfer, PR creation, QR generation).
    pub fn root() -> Self {
        let id = format!("tr-{}", Uuid::new_v4());
        Self { trace_id: id.clone(), correlation_id: id, causation_id: None }
    }

    /// Derived trace — inherits trace_id from a parent, new correlation_id.
    pub fn child(trace_id: &str, correlation_id: &str, causation_id: &str) -> Self {
        Self {
            trace_id:       trace_id.to_string(),
            correlation_id: correlation_id.to_string(),
            causation_id:   Some(causation_id.to_string()),
        }
    }
}

// ---------------------------------------------------------------------------
// Wallet
// ---------------------------------------------------------------------------

#[derive(Debug, Clone, serde::Serialize)]
pub struct SandboxWallet {
    pub id:            String,
    pub label:         String,
    pub currency:      Currency,
    pub balance_minor: i64,
    pub wallet_type:   WalletType,
    pub created_at:    chrono::DateTime<chrono::Utc>,
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum WalletType { Consumer, Merchant, Government, Internal }

// ---------------------------------------------------------------------------
// Transfer
// ---------------------------------------------------------------------------

#[derive(Debug, Clone, serde::Serialize)]
pub struct SandboxTransfer {
    pub id:              String,
    pub from_wallet_id:  String,
    pub to_wallet_id:    String,
    pub amount_minor:    i64,
    pub currency:        Currency,
    pub note:            String,
    pub idempotency_key: Option<String>,
    /// Top-level trace identifier. Shared across all operations in the same flow.
    pub trace_id:       String,
    /// Correlation identifier for this specific aggregate step.
    pub correlation_id: String,
    /// The ID of the operation that directly caused this transfer (e.g. a payment request ID).
    #[serde(skip_serializing_if = "Option::is_none")]
    pub causation_id:   Option<String>,
    pub created_at:     chrono::DateTime<chrono::Utc>,
}

// ---------------------------------------------------------------------------
// Payment request
// ---------------------------------------------------------------------------

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum PaymentRequestStatus { Pending, Paid, Expired, Cancelled }

#[derive(Debug, Clone, serde::Serialize)]
pub struct SandboxPaymentRequest {
    pub id:             String,
    pub to_wallet_id:   String,
    pub from_wallet_id: Option<String>,
    pub amount_minor:   i64,
    pub currency:       Currency,
    pub description:    String,
    pub status:         PaymentRequestStatus,
    pub transfer_id:    Option<String>,
    /// Trace ID linking this request and all resulting operations.
    pub trace_id:      String,
    pub created_at:    chrono::DateTime<chrono::Utc>,
    pub paid_at:       Option<chrono::DateTime<chrono::Utc>>,
}

// ---------------------------------------------------------------------------
// QR code
// ---------------------------------------------------------------------------

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum QrStatus { Active, Paid, Expired }

#[derive(Debug, Clone, serde::Serialize)]
pub struct SandboxQrCode {
    pub id:                 String,
    pub merchant_wallet_id: String,
    pub amount_minor:       Option<i64>,
    pub currency:           Currency,
    pub description:        String,
    pub payload_data:       String,
    pub status:             QrStatus,
    pub paid_by_wallet:     Option<String>,
    pub transfer_id:        Option<String>,
    /// Trace ID linking this QR code and all resulting operations.
    pub trace_id:           String,
    pub created_at:         chrono::DateTime<chrono::Utc>,
    pub paid_at:            Option<chrono::DateTime<chrono::Utc>>,
}

// ---------------------------------------------------------------------------
// Ledger entries
// ---------------------------------------------------------------------------

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize, PartialEq, Eq)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum LedgerEntryKind { Debit, Credit }

#[derive(Debug, Clone, serde::Serialize)]
pub struct SandboxLedgerEntry {
    pub id:             String,
    pub wallet_id:      String,
    pub kind:           LedgerEntryKind,
    pub amount_minor:   i64,
    pub currency:       Currency,
    pub reference:      String,
    pub description:    String,
    /// Trace ID linking this entry to the payment flow that caused it.
    pub trace_id:       String,
    /// Correlation ID (usually the transfer ID that generated this entry).
    pub correlation_id: String,
    pub created_at:     chrono::DateTime<chrono::Utc>,
}

// ---------------------------------------------------------------------------
// Settlement
// ---------------------------------------------------------------------------

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum SettlementBatchStatus { Created, Processing, Completed, Failed }

#[derive(Debug, Clone, serde::Serialize)]
pub struct SandboxSettlementBatch {
    pub id:           String,
    pub wallet_id:    String,
    pub gross_minor:  i64,
    pub fee_minor:    i64,
    pub net_minor:    i64,
    pub currency:     Currency,
    pub tx_count:     usize,
    pub status:       SettlementBatchStatus,
    pub provider_ref: Option<String>,
    /// Trace ID for this settlement operation.
    pub trace_id:     String,
    pub created_at:   chrono::DateTime<chrono::Utc>,
    pub completed_at: Option<chrono::DateTime<chrono::Utc>>,
}

// ---------------------------------------------------------------------------
// Trace view — returned by GET /traces/{trace_id}
// ---------------------------------------------------------------------------

#[derive(Debug, serde::Serialize)]
pub struct TraceTimelineEntry {
    pub timestamp:      chrono::DateTime<chrono::Utc>,
    pub operation_type: String,
    pub id:             String,
    pub summary:        String,
}

#[derive(Debug, serde::Serialize)]
pub struct TraceView {
    pub trace_id:           String,
    pub timeline:           Vec<TraceTimelineEntry>,
    pub transfers:          Vec<SandboxTransfer>,
    pub ledger_entries:     Vec<SandboxLedgerEntry>,
    pub events:             Vec<SandboxEvent>,
    pub settlement_batches: Vec<SandboxSettlementBatch>,
    pub payment_requests:   Vec<SandboxPaymentRequest>,
    pub qr_codes:           Vec<SandboxQrCode>,
}

// ---------------------------------------------------------------------------
// App state
// ---------------------------------------------------------------------------

pub struct AppState {
    wallets:              Mutex<HashMap<String, SandboxWallet>>,
    transfers:            Mutex<Vec<SandboxTransfer>>,
    payment_requests:     Mutex<HashMap<String, SandboxPaymentRequest>>,
    qr_codes:             Mutex<HashMap<String, SandboxQrCode>>,
    ledger_entries:       Mutex<Vec<SandboxLedgerEntry>>,
    settlement_batches:   Mutex<Vec<SandboxSettlementBatch>>,
    settled_transfer_ids: Mutex<HashSet<String>>,
    event_history:        Mutex<Vec<SandboxEvent>>,
    pub event_tx:         broadcast::Sender<SandboxEvent>,
}

impl AppState {
    pub fn new() -> Self {
        let (event_tx, _) = broadcast::channel(256);

        let mut wallets = HashMap::new();
        let now = chrono::Utc::now();

        let seed = vec![
            ("sandbox-consumer-1",   "Sandbox Consumer",   Currency::AOA, WalletType::Consumer,    2_000_000i64),
            ("sandbox-merchant-1",   "Sandbox Merchant A", Currency::AOA, WalletType::Merchant,   10_000_000i64),
            ("sandbox-government-1", "Sandbox Government", Currency::AOA, WalletType::Government, 50_000_000i64),
            ("sandbox-merchant-2",   "Sandbox Merchant B", Currency::AOA, WalletType::Merchant,    5_000_000i64),
            ("sandbox-float",        "Float (Transit)",    Currency::AOA, WalletType::Internal,    0i64),
        ];

        for (id, label, currency, wallet_type, balance) in seed {
            wallets.insert(id.to_string(), SandboxWallet {
                id:            id.to_string(),
                label:         label.to_string(),
                currency,
                balance_minor: balance,
                wallet_type,
                created_at:    now,
            });
        }

        tracing::info!("Sandbox state initialised with {} seed wallets", wallets.len());

        Self {
            wallets:              Mutex::new(wallets),
            transfers:            Mutex::new(Vec::new()),
            payment_requests:     Mutex::new(HashMap::new()),
            qr_codes:             Mutex::new(HashMap::new()),
            ledger_entries:       Mutex::new(Vec::new()),
            settlement_batches:   Mutex::new(Vec::new()),
            settled_transfer_ids: Mutex::new(HashSet::new()),
            event_history:        Mutex::new(Vec::new()),
            event_tx,
        }
    }

    // -----------------------------------------------------------------------
    // Events
    // -----------------------------------------------------------------------

    fn emit(
        &self,
        event_type:     &str,
        aggregate_type: &str,
        aggregate_id:   &str,
        ctx:            &TraceContext,
        payload:        serde_json::Value,
    ) {
        let event = SandboxEvent::with_trace(
            event_type, aggregate_type, aggregate_id,
            &ctx.trace_id, &ctx.correlation_id, ctx.causation_id.clone(),
            payload,
        );
        let mut history = self.event_history.lock().unwrap();
        if history.len() >= 200 { history.remove(0); }
        history.push(event.clone());
        drop(history);
        let _ = self.event_tx.send(event);
    }

    pub fn event_history(&self) -> Vec<SandboxEvent> {
        self.event_history.lock().unwrap().clone()
    }

    // -----------------------------------------------------------------------
    // Wallets
    // -----------------------------------------------------------------------

    pub fn create_wallet(&self, label: String, currency: Currency, wallet_type: WalletType) -> SandboxWallet {
        // Sandbox: seed every new wallet with 1,000,000 minor units (10,000 AOA)
        // so developers can immediately test transfers without a separate fund step.
        let wallet = SandboxWallet {
            id:            format!("wallet-{}", Uuid::new_v4()),
            label:         label.clone(),
            currency,
            balance_minor: 1_000_000,
            wallet_type,
            created_at:    chrono::Utc::now(),
        };
        self.wallets.lock().unwrap().insert(wallet.id.clone(), wallet.clone());
        let ctx = TraceContext::root();
        self.emit(ev::WALLET_CREATED, "wallet", &wallet.id, &ctx, serde_json::json!({
            "wallet_id": wallet.id,
            "label":     label,
            "currency":  currency.code(),
        }));
        wallet
    }

    pub fn get_wallet(&self, id: &str) -> Option<SandboxWallet> {
        self.wallets.lock().unwrap().get(id).cloned()
    }

    pub fn list_wallets(&self) -> Vec<SandboxWallet> {
        let mut v: Vec<_> = self.wallets.lock().unwrap().values().cloned().collect();
        v.sort_by_key(|w| w.created_at);
        v
    }

    // -----------------------------------------------------------------------
    // Transfers
    // -----------------------------------------------------------------------

    pub fn create_transfer(
        &self,
        from_wallet_id:  String,
        to_wallet_id:    String,
        amount_minor:    i64,
        currency:        Currency,
        note:            String,
        idempotency_key: Option<String>,
        trace_ctx:       Option<TraceContext>,
    ) -> Result<SandboxTransfer, String> {
        // Idempotency: return existing transfer if key already used.
        if let Some(ref key) = idempotency_key {
            let existing = self.transfers.lock().unwrap()
                .iter()
                .find(|t| t.idempotency_key.as_deref() == Some(key.as_str()))
                .cloned();
            if let Some(t) = existing {
                return Ok(t);
            }
        }

        let mut wallets = self.wallets.lock().unwrap();

        if !wallets.contains_key(&from_wallet_id) {
            return Err(format!("wallet not found: {from_wallet_id}"));
        }
        if !wallets.contains_key(&to_wallet_id) {
            return Err(format!("wallet not found: {to_wallet_id}"));
        }
        if from_wallet_id == to_wallet_id {
            return Err("cannot transfer to the same wallet".into());
        }
        let from_balance = wallets[&from_wallet_id].balance_minor;
        if from_balance < amount_minor {
            return Err(format!("insufficient funds: have {from_balance}, need {amount_minor}"));
        }

        wallets.get_mut(&from_wallet_id).unwrap().balance_minor -= amount_minor;
        wallets.get_mut(&to_wallet_id).unwrap().balance_minor   += amount_minor;
        drop(wallets);

        let now = chrono::Utc::now();
        let ctx = trace_ctx.unwrap_or_else(TraceContext::root);
        let transfer_id = format!("txfr-{}", Uuid::new_v4());

        // Use the transfer's own ID as the correlation_id for ledger entries.
        let ledger_ctx = TraceContext::child(&ctx.trace_id, &transfer_id, &transfer_id);

        let transfer = SandboxTransfer {
            id:              transfer_id.clone(),
            from_wallet_id:  from_wallet_id.clone(),
            to_wallet_id:    to_wallet_id.clone(),
            amount_minor,
            currency,
            note:            note.clone(),
            idempotency_key,
            trace_id:        ctx.trace_id.clone(),
            correlation_id:  ctx.correlation_id.clone(),
            causation_id:    ctx.causation_id.clone(),
            created_at:      now,
        };

        // Double-entry ledger entries.
        self.append_ledger_entry(
            &from_wallet_id, LedgerEntryKind::Debit,
            amount_minor, currency, &transfer_id, &note,
            &ctx.trace_id, &ledger_ctx.correlation_id, now,
        );
        self.append_ledger_entry(
            &to_wallet_id, LedgerEntryKind::Credit,
            amount_minor, currency, &transfer_id, &note,
            &ctx.trace_id, &ledger_ctx.correlation_id, now,
        );

        self.transfers.lock().unwrap().push(transfer.clone());

        // Events share the transfer's trace and use the transfer ID as correlation.
        let event_ctx = TraceContext { trace_id: ctx.trace_id.clone(), correlation_id: transfer_id.clone(), causation_id: ctx.causation_id.clone() };
        self.emit(ev::PAYMENT_SENT, "transfer", &transfer_id, &event_ctx, serde_json::json!({
            "transfer_id":    transfer_id,
            "from_wallet_id": from_wallet_id,
            "amount_minor":   amount_minor,
            "currency":       currency.code(),
        }));
        self.emit(ev::PAYMENT_RECEIVED, "transfer", &transfer_id, &event_ctx, serde_json::json!({
            "transfer_id":  transfer_id,
            "to_wallet_id": to_wallet_id,
            "amount_minor": amount_minor,
            "currency":     currency.code(),
        }));

        Ok(transfer)
    }

    pub fn list_transfers(&self) -> Vec<SandboxTransfer> {
        self.transfers.lock().unwrap().clone()
    }

    pub fn get_transfer(&self, id: &str) -> Option<SandboxTransfer> {
        self.transfers.lock().unwrap().iter().find(|t| t.id == id).cloned()
    }

    // -----------------------------------------------------------------------
    // Payment requests
    // -----------------------------------------------------------------------

    pub fn create_payment_request(
        &self,
        to_wallet_id: String,
        amount_minor: i64,
        currency:     Currency,
        description:  String,
    ) -> Result<SandboxPaymentRequest, String> {
        if !self.wallets.lock().unwrap().contains_key(&to_wallet_id) {
            return Err(format!("wallet not found: {to_wallet_id}"));
        }
        let ctx = TraceContext::root();
        let pr = SandboxPaymentRequest {
            id:             format!("pr-{}", Uuid::new_v4()),
            to_wallet_id:   to_wallet_id.clone(),
            from_wallet_id: None,
            amount_minor,
            currency,
            description:    description.clone(),
            status:         PaymentRequestStatus::Pending,
            transfer_id:    None,
            trace_id:       ctx.trace_id.clone(),
            created_at:     chrono::Utc::now(),
            paid_at:        None,
        };
        self.payment_requests.lock().unwrap().insert(pr.id.clone(), pr.clone());
        self.emit(ev::PAYMENT_REQUEST_CREATED, "payment_request", &pr.id, &ctx, serde_json::json!({
            "pr_id":        pr.id,
            "to_wallet_id": to_wallet_id,
            "amount_minor": amount_minor,
            "currency":     currency.code(),
            "description":  description,
        }));
        Ok(pr)
    }

    pub fn get_payment_request(&self, id: &str) -> Option<SandboxPaymentRequest> {
        self.payment_requests.lock().unwrap().get(id).cloned()
    }

    pub fn list_payment_requests(&self) -> Vec<SandboxPaymentRequest> {
        let mut v: Vec<_> = self.payment_requests.lock().unwrap().values().cloned().collect();
        v.sort_by_key(|pr| pr.created_at);
        v
    }

    pub fn pay_payment_request(
        &self,
        pr_id:          &str,
        from_wallet_id: String,
    ) -> Result<SandboxPaymentRequest, String> {
        let pr = {
            let map = self.payment_requests.lock().unwrap();
            map.get(pr_id).cloned().ok_or_else(|| format!("payment request not found: {pr_id}"))?
        };
        if pr.status != PaymentRequestStatus::Pending {
            return Err(format!("payment request is {status:?}, not pending", status = pr.status));
        }

        // The transfer inherits the PR's trace. The PR's ID is the causation.
        let transfer_ctx = TraceContext::child(&pr.trace_id, &pr.trace_id, pr_id);
        let transfer = self.create_transfer(
            from_wallet_id.clone(),
            pr.to_wallet_id.clone(),
            pr.amount_minor,
            pr.currency,
            format!("PR payment: {}", pr.description),
            None,
            Some(transfer_ctx),
        )?;

        let now = chrono::Utc::now();
        let updated = SandboxPaymentRequest {
            status:         PaymentRequestStatus::Paid,
            from_wallet_id: Some(from_wallet_id),
            transfer_id:    Some(transfer.id.clone()),
            paid_at:        Some(now),
            ..pr.clone()
        };
        self.payment_requests.lock().unwrap().insert(updated.id.clone(), updated.clone());

        let pr_ctx = TraceContext { trace_id: pr.trace_id.clone(), correlation_id: pr.id.clone(), causation_id: None };
        self.emit(ev::PAYMENT_REQUEST_PAID, "payment_request", &pr.id, &pr_ctx, serde_json::json!({
            "pr_id":        updated.id,
            "transfer_id":  transfer.id,
            "amount_minor": updated.amount_minor,
        }));
        Ok(updated)
    }

    // -----------------------------------------------------------------------
    // QR codes
    // -----------------------------------------------------------------------

    pub fn create_qr(
        &self,
        merchant_wallet_id: String,
        amount_minor:       Option<i64>,
        currency:           Currency,
        description:        String,
    ) -> Result<SandboxQrCode, String> {
        if !self.wallets.lock().unwrap().contains_key(&merchant_wallet_id) {
            return Err(format!("wallet not found: {merchant_wallet_id}"));
        }
        let ctx = TraceContext::root();
        let qr_id = format!("qr-{}", Uuid::new_v4());
        let payload_data = {
            let raw = serde_json::json!({
                "sandbox": true,
                "v": 1,
                "qr_id": qr_id,
                "merchant_wallet_id": merchant_wallet_id,
                "amount_minor": amount_minor,
                "currency": currency.code(),
                "description": description,
            });
            let enc = base64_encode(serde_json::to_string(&raw).unwrap().as_bytes());
            format!("BANZAMI-SBX:{enc}")
        };
        let qr = SandboxQrCode {
            id:                 qr_id.clone(),
            merchant_wallet_id: merchant_wallet_id.clone(),
            amount_minor,
            currency,
            description:        description.clone(),
            payload_data,
            status:             QrStatus::Active,
            paid_by_wallet:     None,
            transfer_id:        None,
            trace_id:           ctx.trace_id.clone(),
            created_at:         chrono::Utc::now(),
            paid_at:            None,
        };
        self.qr_codes.lock().unwrap().insert(qr_id.clone(), qr.clone());
        self.emit(ev::QR_GENERATED, "qr", &qr_id, &ctx, serde_json::json!({
            "qr_id":              qr_id,
            "merchant_wallet_id": merchant_wallet_id,
            "amount_minor":       amount_minor,
            "currency":           currency.code(),
        }));
        Ok(qr)
    }

    pub fn get_qr(&self, id: &str) -> Option<SandboxQrCode> {
        self.qr_codes.lock().unwrap().get(id).cloned()
    }

    pub fn pay_qr(
        &self,
        qr_id:                 &str,
        consumer_wallet_id:    String,
        consumer_amount_minor: Option<i64>,
    ) -> Result<SandboxQrCode, String> {
        let qr = {
            let map = self.qr_codes.lock().unwrap();
            map.get(qr_id).cloned().ok_or_else(|| format!("QR not found: {qr_id}"))?
        };
        if qr.status != QrStatus::Active {
            return Err(format!("QR code is {status:?}, not active", status = qr.status));
        }
        let amount = qr.amount_minor
            .or(consumer_amount_minor)
            .ok_or("QR is open-amount: supply amount_minor in request")?;
        if amount <= 0 {
            return Err("amount_minor must be positive".into());
        }

        // Transfer inherits the QR's trace. The QR's ID is the causation.
        let transfer_ctx = TraceContext::child(&qr.trace_id, &qr.trace_id, qr_id);
        let transfer = self.create_transfer(
            consumer_wallet_id.clone(),
            qr.merchant_wallet_id.clone(),
            amount,
            qr.currency,
            format!("QR payment: {}", qr.description),
            None,
            Some(transfer_ctx),
        )?;

        let now = chrono::Utc::now();
        let updated = SandboxQrCode {
            status:         QrStatus::Paid,
            paid_by_wallet: Some(consumer_wallet_id),
            transfer_id:    Some(transfer.id.clone()),
            paid_at:        Some(now),
            ..qr.clone()
        };
        self.qr_codes.lock().unwrap().insert(updated.id.clone(), updated.clone());

        let qr_ctx = TraceContext { trace_id: qr.trace_id.clone(), correlation_id: qr.id.clone(), causation_id: None };
        self.emit(ev::QR_PAID, "qr", &qr.id, &qr_ctx, serde_json::json!({
            "qr_id":       updated.id,
            "transfer_id": transfer.id,
            "amount_minor": amount,
        }));
        Ok(updated)
    }

    // -----------------------------------------------------------------------
    // Ledger entries
    // -----------------------------------------------------------------------

    #[allow(clippy::too_many_arguments)]
    fn append_ledger_entry(
        &self,
        wallet_id:      &str,
        kind:           LedgerEntryKind,
        amount_minor:   i64,
        currency:       Currency,
        reference:      &str,
        description:    &str,
        trace_id:       &str,
        correlation_id: &str,
        ts:             chrono::DateTime<chrono::Utc>,
    ) {
        let entry = SandboxLedgerEntry {
            id:             format!("le-{}", Uuid::new_v4()),
            wallet_id:      wallet_id.to_string(),
            kind,
            amount_minor,
            currency,
            reference:      reference.to_string(),
            description:    description.to_string(),
            trace_id:       trace_id.to_string(),
            correlation_id: correlation_id.to_string(),
            created_at:     ts,
        };
        self.ledger_entries.lock().unwrap().push(entry);
    }

    pub fn list_ledger_entries(&self) -> Vec<SandboxLedgerEntry> {
        self.ledger_entries.lock().unwrap().clone()
    }

    pub fn ledger_entries_for_wallet(&self, wallet_id: &str) -> Vec<SandboxLedgerEntry> {
        self.ledger_entries.lock().unwrap()
            .iter()
            .filter(|e| e.wallet_id == wallet_id)
            .cloned()
            .collect()
    }

    // -----------------------------------------------------------------------
    // Settlement
    // -----------------------------------------------------------------------

    pub fn create_settlement_batch(&self, wallet_id: &str) -> Result<SandboxSettlementBatch, String> {
        if !self.wallets.lock().unwrap().contains_key(wallet_id) {
            return Err(format!("wallet not found: {wallet_id}"));
        }

        let already_settled = self.settled_transfer_ids.lock().unwrap().clone();
        let transfers = self.transfers.lock().unwrap();
        let credits: Vec<_> = transfers.iter()
            .filter(|t| t.to_wallet_id == wallet_id && !already_settled.contains(&t.id))
            .collect();

        if credits.is_empty() {
            return Err("no unsettled receipts for this wallet".into());
        }

        let currency        = credits[0].currency;
        let gross_minor: i64 = credits.iter().map(|t| t.amount_minor).sum();
        let tx_count         = credits.len();
        let settled_ids: Vec<String> = credits.iter().map(|t| t.id.clone()).collect();
        drop(transfers);

        // Simulated sandbox fee: 1% of gross, minimum 100 AOA minor units.
        let fee_minor = (gross_minor / 100).max(100);
        let net_minor = gross_minor - fee_minor;

        let ctx = TraceContext::root();
        let now = chrono::Utc::now();
        let batch = SandboxSettlementBatch {
            id:           format!("settle-{}", Uuid::new_v4()),
            wallet_id:    wallet_id.to_string(),
            gross_minor,
            fee_minor,
            net_minor,
            currency,
            tx_count,
            status:       SettlementBatchStatus::Completed,
            provider_ref: Some(format!("SBX-SETTLE-{}", Uuid::new_v4())),
            trace_id:     ctx.trace_id.clone(),
            created_at:   now,
            completed_at: Some(now),
        };

        self.settled_transfer_ids.lock().unwrap().extend(settled_ids);
        self.settlement_batches.lock().unwrap().push(batch.clone());

        self.emit(ev::SETTLEMENT_CREATED, "settlement", &batch.id, &ctx, serde_json::json!({
            "batch_id":    batch.id,
            "wallet_id":   wallet_id,
            "gross_minor": gross_minor,
            "net_minor":   net_minor,
            "tx_count":    tx_count,
        }));
        self.emit(ev::SETTLEMENT_COMPLETED, "settlement", &batch.id, &ctx, serde_json::json!({
            "batch_id":     batch.id,
            "provider_ref": batch.provider_ref,
        }));
        Ok(batch)
    }

    pub fn list_settlement_batches(&self) -> Vec<SandboxSettlementBatch> {
        self.settlement_batches.lock().unwrap().clone()
    }

    pub fn get_settlement_batch(&self, id: &str) -> Option<SandboxSettlementBatch> {
        self.settlement_batches.lock().unwrap()
            .iter()
            .find(|b| b.id == id)
            .cloned()
    }

    // -----------------------------------------------------------------------
    // Traces
    // -----------------------------------------------------------------------

    /// Reconstruct the full causal chain for a given trace ID.
    pub fn get_trace(&self, trace_id: &str) -> Option<TraceView> {
        let transfers: Vec<SandboxTransfer> = self.transfers.lock().unwrap()
            .iter().filter(|t| t.trace_id == trace_id).cloned().collect();
        let ledger_entries: Vec<SandboxLedgerEntry> = self.ledger_entries.lock().unwrap()
            .iter().filter(|e| e.trace_id == trace_id).cloned().collect();
        let events: Vec<SandboxEvent> = self.event_history.lock().unwrap()
            .iter().filter(|e| e.trace_id == trace_id).cloned().collect();
        let settlement_batches: Vec<SandboxSettlementBatch> = self.settlement_batches.lock().unwrap()
            .iter().filter(|b| b.trace_id == trace_id).cloned().collect();
        let payment_requests: Vec<SandboxPaymentRequest> = self.payment_requests.lock().unwrap()
            .values().filter(|pr| pr.trace_id == trace_id).cloned().collect();
        let qr_codes: Vec<SandboxQrCode> = self.qr_codes.lock().unwrap()
            .values().filter(|qr| qr.trace_id == trace_id).cloned().collect();

        if transfers.is_empty() && payment_requests.is_empty()
            && qr_codes.is_empty() && settlement_batches.is_empty()
            && events.is_empty()
        {
            return None;
        }

        let mut timeline: Vec<TraceTimelineEntry> = Vec::new();

        for pr in &payment_requests {
            timeline.push(TraceTimelineEntry {
                timestamp:      pr.created_at,
                operation_type: "payment_request.created".into(),
                id:             pr.id.clone(),
                summary:        format!("Payment request created — {} → {}", pr.amount_minor, pr.to_wallet_id),
            });
            if pr.status == PaymentRequestStatus::Paid {
                if let Some(ts) = pr.paid_at {
                    timeline.push(TraceTimelineEntry {
                        timestamp:      ts,
                        operation_type: "payment_request.paid".into(),
                        id:             pr.id.clone(),
                        summary:        format!("Payment request fulfilled via transfer {:?}", pr.transfer_id),
                    });
                }
            }
        }

        for qr in &qr_codes {
            timeline.push(TraceTimelineEntry {
                timestamp:      qr.created_at,
                operation_type: "qr.generated".into(),
                id:             qr.id.clone(),
                summary:        format!("QR generated for {} ({})", qr.merchant_wallet_id, qr.amount_minor.map(|a| a.to_string()).unwrap_or_else(|| "open".into())),
            });
            if qr.status == QrStatus::Paid {
                if let Some(ts) = qr.paid_at {
                    timeline.push(TraceTimelineEntry {
                        timestamp:      ts,
                        operation_type: "qr.paid".into(),
                        id:             qr.id.clone(),
                        summary:        format!("QR paid via transfer {:?}", qr.transfer_id),
                    });
                }
            }
        }

        for t in &transfers {
            timeline.push(TraceTimelineEntry {
                timestamp:      t.created_at,
                operation_type: "transfer.executed".into(),
                id:             t.id.clone(),
                summary:        format!("{} → {} : {} minor units {}", t.from_wallet_id, t.to_wallet_id, t.amount_minor, t.currency.code()),
            });
        }

        for e in &ledger_entries {
            let kind_str = match e.kind { LedgerEntryKind::Debit => "DEBIT", LedgerEntryKind::Credit => "CREDIT" };
            timeline.push(TraceTimelineEntry {
                timestamp:      e.created_at,
                operation_type: format!("ledger.{}", kind_str.to_lowercase()),
                id:             e.id.clone(),
                summary:        format!("{} {} {} on {}", kind_str, e.amount_minor, e.currency.code(), e.wallet_id),
            });
        }

        for ev in &events {
            timeline.push(TraceTimelineEntry {
                timestamp:      ev.created_at,
                operation_type: format!("event.{}", ev.event_type),
                id:             ev.id.clone(),
                summary:        format!("Event emitted: {}", ev.event_type),
            });
        }

        for b in &settlement_batches {
            timeline.push(TraceTimelineEntry {
                timestamp:      b.created_at,
                operation_type: "settlement.batch_created".into(),
                id:             b.id.clone(),
                summary:        format!("Settlement batch: gross {} → fee {} → net {} {}", b.gross_minor, b.fee_minor, b.net_minor, b.currency.code()),
            });
        }

        timeline.sort_by_key(|e| e.timestamp);

        Some(TraceView {
            trace_id: trace_id.to_string(),
            timeline,
            transfers,
            ledger_entries,
            events,
            settlement_batches,
            payment_requests,
            qr_codes,
        })
    }

    /// List all distinct trace IDs currently in memory.
    pub fn list_trace_ids(&self) -> Vec<String> {
        let mut ids: HashSet<String> = HashSet::new();
        for t in self.transfers.lock().unwrap().iter() { ids.insert(t.trace_id.clone()); }
        for pr in self.payment_requests.lock().unwrap().values() { ids.insert(pr.trace_id.clone()); }
        for qr in self.qr_codes.lock().unwrap().values() { ids.insert(qr.trace_id.clone()); }
        for b in self.settlement_batches.lock().unwrap().iter() { ids.insert(b.trace_id.clone()); }
        for e in self.event_history.lock().unwrap().iter() { ids.insert(e.trace_id.clone()); }
        let mut v: Vec<_> = ids.into_iter().collect();
        v.sort();
        v
    }
}

fn base64_encode(data: &[u8]) -> String {
    const TABLE: &[u8] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    let mut out = String::new();
    for chunk in data.chunks(3) {
        let b0 = chunk[0] as usize;
        let b1 = if chunk.len() > 1 { chunk[1] as usize } else { 0 };
        let b2 = if chunk.len() > 2 { chunk[2] as usize } else { 0 };
        out.push(TABLE[b0 >> 2] as char);
        out.push(TABLE[((b0 & 3) << 4) | (b1 >> 4)] as char);
        out.push(if chunk.len() > 1 { TABLE[((b1 & 0xf) << 2) | (b2 >> 6)] as char } else { '=' });
        out.push(if chunk.len() > 2 { TABLE[b2 & 0x3f] as char } else { '=' });
    }
    out
}
