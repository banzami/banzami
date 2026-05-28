//! In-memory state for the sandbox operator.
//!
//! No database required — everything is kept in memory.
//! State resets on restart, which is intentional for a development sandbox.

use std::sync::Mutex;
use std::collections::HashMap;

use banzami_types::Currency;

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

#[derive(Debug, Clone, serde::Serialize)]
pub struct SandboxWallet {
    pub id:            String,
    pub label:         String,
    pub currency:      Currency,
    pub balance_minor: i64,
}

#[derive(Debug, Clone, serde::Serialize)]
pub struct SandboxTransfer {
    pub id:             String,
    pub from_wallet_id: String,
    pub to_wallet_id:   String,
    pub amount_minor:   i64,
    pub currency:       Currency,
    pub note:           String,
    pub created_at:     chrono::DateTime<chrono::Utc>,
}

// ---------------------------------------------------------------------------
// State
// ---------------------------------------------------------------------------

pub struct AppState {
    wallets:   Mutex<HashMap<String, SandboxWallet>>,
    transfers: Mutex<Vec<SandboxTransfer>>,
}

impl AppState {
    pub fn new() -> Self {
        let mut wallets = HashMap::new();

        // Seed wallets with sandbox balances for immediate experimentation.
        let seed = vec![
            ("sandbox-merchant-1", "Sandbox Merchant A", Currency::AOA, 10_000_000i64),
            ("sandbox-merchant-2", "Sandbox Merchant B", Currency::AOA,  5_000_000i64),
            ("sandbox-consumer-1", "Sandbox Consumer",   Currency::AOA,  2_000_000i64),
        ];

        for (id, label, currency, balance) in seed {
            wallets.insert(id.to_string(), SandboxWallet {
                id:            id.to_string(),
                label:         label.to_string(),
                currency,
                balance_minor: balance,
            });
        }

        tracing::info!("Sandbox state initialised with {} seed wallets", wallets.len());

        Self {
            wallets:   Mutex::new(wallets),
            transfers: Mutex::new(Vec::new()),
        }
    }

    pub fn create_wallet(&self, label: String, currency: Currency) -> SandboxWallet {
        let id = format!("wallet-{}", uuid::Uuid::new_v4());
        let wallet = SandboxWallet {
            id: id.clone(),
            label,
            currency,
            balance_minor: 0,
        };
        self.wallets.lock().unwrap().insert(id, wallet.clone());
        wallet
    }

    pub fn get_wallet(&self, id: &str) -> Option<SandboxWallet> {
        self.wallets.lock().unwrap().get(id).cloned()
    }

    pub fn create_transfer(
        &self,
        from_wallet_id: String,
        to_wallet_id:   String,
        amount_minor:   i64,
        currency:       Currency,
        note:           String,
    ) -> Result<SandboxTransfer, String> {
        let mut wallets = self.wallets.lock().unwrap();

        // Validate both wallets exist.
        if !wallets.contains_key(&from_wallet_id) {
            return Err(format!("wallet not found: {from_wallet_id}"));
        }
        if !wallets.contains_key(&to_wallet_id) {
            return Err(format!("wallet not found: {to_wallet_id}"));
        }
        if from_wallet_id == to_wallet_id {
            return Err("cannot transfer to the same wallet".into());
        }

        // Check balance.
        let from_balance = wallets[&from_wallet_id].balance_minor;
        if from_balance < amount_minor {
            return Err(format!(
                "insufficient funds: have {from_balance}, need {amount_minor}"
            ));
        }

        // Apply transfer (double-entry: debit from, credit to).
        wallets.get_mut(&from_wallet_id).unwrap().balance_minor -= amount_minor;
        wallets.get_mut(&to_wallet_id).unwrap().balance_minor   += amount_minor;

        let transfer = SandboxTransfer {
            id:             format!("txfr-{}", uuid::Uuid::new_v4()),
            from_wallet_id,
            to_wallet_id,
            amount_minor,
            currency,
            note,
            created_at: chrono::Utc::now(),
        };

        drop(wallets);
        self.transfers.lock().unwrap().push(transfer.clone());
        Ok(transfer)
    }

    pub fn list_transfers(&self) -> Vec<SandboxTransfer> {
        self.transfers.lock().unwrap().clone()
    }
}
