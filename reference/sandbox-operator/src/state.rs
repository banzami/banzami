//! In-memory state for the sandbox operator.
//!
//! All state resets on restart — intentional for a development sandbox.
//! The broadcast channel fans out events to SSE subscribers in real time.

use std::collections::{HashMap, HashSet};
use std::sync::Mutex;

use banzami_types::Currency;
use tokio::sync::broadcast;
use uuid::Uuid;

use crate::events::{types as ev, SandboxEvent};

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
    pub created_at:      chrono::DateTime<chrono::Utc>,
}

// ---------------------------------------------------------------------------
// Payment request
// ---------------------------------------------------------------------------

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum PaymentRequestStatus { Pending, Paid, Expired, Cancelled }

#[derive(Debug, Clone, serde::Serialize)]
pub struct SandboxPaymentRequest {
    pub id:              String,
    pub to_wallet_id:    String,
    pub from_wallet_id:  Option<String>,
    pub amount_minor:    i64,
    pub currency:        Currency,
    pub description:     String,
    pub status:          PaymentRequestStatus,
    pub transfer_id:     Option<String>,
    pub created_at:      chrono::DateTime<chrono::Utc>,
    pub paid_at:         Option<chrono::DateTime<chrono::Utc>>,
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
    pub id:           String,
    pub wallet_id:    String,
    pub kind:         LedgerEntryKind,
    pub amount_minor: i64,
    pub currency:     Currency,
    pub reference:    String,
    pub description:  String,
    pub created_at:   chrono::DateTime<chrono::Utc>,
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
    pub created_at:   chrono::DateTime<chrono::Utc>,
    pub completed_at: Option<chrono::DateTime<chrono::Utc>>,
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
            ("sandbox-consumer-1",  "Sandbox Consumer",  Currency::AOA, WalletType::Consumer,   2_000_000i64),
            ("sandbox-merchant-1",  "Sandbox Merchant A",Currency::AOA, WalletType::Merchant,  10_000_000i64),
            ("sandbox-government-1","Sandbox Government", Currency::AOA, WalletType::Government, 50_000_000i64),
            ("sandbox-merchant-2",  "Sandbox Merchant B",Currency::AOA, WalletType::Merchant,   5_000_000i64),
            ("sandbox-float",       "Float (Transit)",   Currency::AOA, WalletType::Internal,   0i64),
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

    pub fn emit(&self, event_type: &str, payload: serde_json::Value) {
        let event = SandboxEvent::new(event_type, payload);
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
        let wallet = SandboxWallet {
            id:            format!("wallet-{}", Uuid::new_v4()),
            label:         label.clone(),
            currency,
            balance_minor: 0,
            wallet_type,
            created_at:    chrono::Utc::now(),
        };
        self.wallets.lock().unwrap().insert(wallet.id.clone(), wallet.clone());
        self.emit(ev::WALLET_CREATED, serde_json::json!({
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
    ) -> Result<SandboxTransfer, String> {
        // Idempotency: return existing transfer if key matches.
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
        let transfer = SandboxTransfer {
            id:              format!("txfr-{}", Uuid::new_v4()),
            from_wallet_id:  from_wallet_id.clone(),
            to_wallet_id:    to_wallet_id.clone(),
            amount_minor,
            currency,
            note:            note.clone(),
            idempotency_key,
            created_at:      now,
        };

        // Double-entry ledger entries.
        self.append_ledger_entry(&from_wallet_id, LedgerEntryKind::Debit,  amount_minor, currency, &transfer.id, &note, now);
        self.append_ledger_entry(&to_wallet_id,   LedgerEntryKind::Credit, amount_minor, currency, &transfer.id, &note, now);

        self.transfers.lock().unwrap().push(transfer.clone());

        self.emit(ev::PAYMENT_SENT, serde_json::json!({
            "transfer_id":    transfer.id,
            "from_wallet_id": from_wallet_id,
            "amount_minor":   amount_minor,
            "currency":       currency.code(),
        }));
        self.emit(ev::PAYMENT_RECEIVED, serde_json::json!({
            "transfer_id":  transfer.id,
            "to_wallet_id": to_wallet_id,
            "amount_minor": amount_minor,
            "currency":     currency.code(),
        }));

        Ok(transfer)
    }

    pub fn list_transfers(&self) -> Vec<SandboxTransfer> {
        self.transfers.lock().unwrap().clone()
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
        let pr = SandboxPaymentRequest {
            id:             format!("pr-{}", Uuid::new_v4()),
            to_wallet_id:   to_wallet_id.clone(),
            from_wallet_id: None,
            amount_minor,
            currency,
            description:    description.clone(),
            status:         PaymentRequestStatus::Pending,
            transfer_id:    None,
            created_at:     chrono::Utc::now(),
            paid_at:        None,
        };
        self.payment_requests.lock().unwrap().insert(pr.id.clone(), pr.clone());
        self.emit(ev::PAYMENT_REQUEST_CREATED, serde_json::json!({
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

        let transfer = self.create_transfer(
            from_wallet_id.clone(),
            pr.to_wallet_id.clone(),
            pr.amount_minor,
            pr.currency,
            format!("PR payment: {}", pr.description),
            None,
        )?;

        let now = chrono::Utc::now();
        let updated = SandboxPaymentRequest {
            status:         PaymentRequestStatus::Paid,
            from_wallet_id: Some(from_wallet_id),
            transfer_id:    Some(transfer.id.clone()),
            paid_at:        Some(now),
            ..pr
        };
        self.payment_requests.lock().unwrap().insert(updated.id.clone(), updated.clone());

        self.emit(ev::PAYMENT_REQUEST_PAID, serde_json::json!({
            "pr_id":       updated.id,
            "transfer_id": transfer.id,
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
            payload_data:       payload_data.clone(),
            status:             QrStatus::Active,
            paid_by_wallet:     None,
            transfer_id:        None,
            created_at:         chrono::Utc::now(),
            paid_at:            None,
        };
        self.qr_codes.lock().unwrap().insert(qr_id.clone(), qr.clone());
        self.emit(ev::QR_GENERATED, serde_json::json!({
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
        qr_id:            &str,
        consumer_wallet_id: String,
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

        let transfer = self.create_transfer(
            consumer_wallet_id.clone(),
            qr.merchant_wallet_id.clone(),
            amount,
            qr.currency,
            format!("QR payment: {}", qr.description),
            None,
        )?;

        let now = chrono::Utc::now();
        let updated = SandboxQrCode {
            status:         QrStatus::Paid,
            paid_by_wallet: Some(consumer_wallet_id),
            transfer_id:    Some(transfer.id.clone()),
            paid_at:        Some(now),
            ..qr
        };
        self.qr_codes.lock().unwrap().insert(updated.id.clone(), updated.clone());

        self.emit(ev::QR_PAID, serde_json::json!({
            "qr_id":       updated.id,
            "transfer_id": transfer.id,
            "amount_minor": amount,
        }));
        Ok(updated)
    }

    // -----------------------------------------------------------------------
    // Ledger entries
    // -----------------------------------------------------------------------

    fn append_ledger_entry(
        &self,
        wallet_id:    &str,
        kind:         LedgerEntryKind,
        amount_minor: i64,
        currency:     Currency,
        reference:    &str,
        description:  &str,
        ts:           chrono::DateTime<chrono::Utc>,
    ) {
        let entry = SandboxLedgerEntry {
            id:           format!("le-{}", Uuid::new_v4()),
            wallet_id:    wallet_id.to_string(),
            kind,
            amount_minor,
            currency,
            reference:    reference.to_string(),
            description:  description.to_string(),
            created_at:   ts,
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

        let currency = credits[0].currency;
        let gross_minor: i64  = credits.iter().map(|t| t.amount_minor).sum();
        let tx_count          = credits.len();
        let settled_ids: Vec<String> = credits.iter().map(|t| t.id.clone()).collect();
        drop(transfers);

        // Simulated sandbox fee: 1% of gross, minimum 100 AOA minor units.
        let fee_minor = (gross_minor / 100).max(100);
        let net_minor = gross_minor - fee_minor;

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
            created_at:   now,
            completed_at: Some(now),
        };

        self.settled_transfer_ids.lock().unwrap().extend(settled_ids);
        self.settlement_batches.lock().unwrap().push(batch.clone());

        self.emit(ev::SETTLEMENT_CREATED, serde_json::json!({
            "batch_id":    batch.id,
            "wallet_id":   wallet_id,
            "gross_minor": gross_minor,
            "net_minor":   net_minor,
            "tx_count":    tx_count,
        }));
        self.emit(ev::SETTLEMENT_COMPLETED, serde_json::json!({
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
}

fn base64_encode(data: &[u8]) -> String {
    // Simple base64 encoding without an extra dep.
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
