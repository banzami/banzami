//! Wallet capability declarations.
//!
//! A `WalletCapabilitySet` is attached to a wallet at creation time and declares
//! which operations the wallet supports. The kernel checks capabilities before
//! initiating any flow; an unsupported operation returns
//! `WalletCapabilityError::CapabilityNotSupported`.
//!
//! See RFC-0003 for the full design rationale.

use banza_types::Currency;

/// Broad classification of the wallet's intended use.
///
/// This is informational — the kernel enforces capabilities via the
/// `WalletCapabilitySet` fields, not the kind tag.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
#[derive(serde::Serialize, serde::Deserialize)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum WalletKind {
    /// Standard consumer wallet — full feature set.
    Consumer,
    /// Merchant receiving wallet — no withdraw, limited reserve.
    Merchant,
    /// Escrow wallet — funds locked, time-release or condition-release only.
    Escrow,
    /// CBDC wallet — government-controlled compliance rules apply.
    Cbdc,
    /// Fee collection wallet — internal accounting only.
    FeeCollection,
    /// Operator float / transit account — internal only.
    Transit,
    /// Custom wallet kind defined by the operator.
    Custom(#[serde(skip)] u16),
}

/// Declarative capability set for a single wallet.
///
/// Constructed by the operator at wallet creation time. The kernel never
/// mutates this after creation — changes require issuing a new wallet or
/// a formal capability upgrade process.
///
/// Default (via `WalletCapabilitySet::minimal()`) is credit + debit only.
#[derive(Debug, Clone)]
#[derive(serde::Serialize, serde::Deserialize)]
pub struct WalletCapabilitySet {
    /// Schema version — increment when adding new fields.
    pub version: u32,

    /// Wallet kind (informational).
    pub kind: WalletKind,

    // -----------------------------------------------------------------------
    // Balance operations
    // -----------------------------------------------------------------------

    /// Can receive inbound credits from another wallet or external source.
    pub credit: bool,

    /// Can send outbound debits to another wallet or external destination.
    pub debit: bool,

    /// Can hold a reserved (locked) balance pending payment confirmation.
    pub reserve: bool,

    /// Can release a reserved balance back to available (payment cancelled).
    pub release: bool,

    /// Can settle a reserved balance to the merchant (payment confirmed).
    pub settle: bool,

    // -----------------------------------------------------------------------
    // Payment flows
    // -----------------------------------------------------------------------

    /// Can be used as the source wallet in a QR payment flow.
    pub qr_payments: bool,

    /// Can send and receive P2P transfers between wallets.
    pub p2p_transfers: bool,

    /// Can be used as the destination for settlement payouts.
    pub payout_target: bool,

    /// Supports the refund flow (partial or full reversal of a settled payment).
    pub refunds: bool,

    /// Supports pre-authorized offline payments (RFC-0006).
    pub offline_payments: bool,

    // -----------------------------------------------------------------------
    // Limits
    // -----------------------------------------------------------------------

    /// Maximum balance the wallet is permitted to hold.
    ///
    /// `None` = no limit enforced by the kernel (operator may apply their own).
    pub max_balance_minor: Option<i64>,

    /// Currency restriction.
    ///
    /// `None` = wallet accepts any currency the operator supports.
    /// `Some(c)` = wallet only accepts the specified currency.
    pub currency_lock: Option<Currency>,

    /// Maximum single-payment amount allowed.
    ///
    /// `None` = no kernel-enforced limit.
    pub max_payment_minor: Option<i64>,
}

impl WalletCapabilitySet {
    /// A minimal wallet that can only receive and send money — no payment flows.
    ///
    /// Use this as a starting point and enable additional capabilities explicitly.
    pub const fn minimal() -> Self {
        Self {
            version:            1,
            kind:               WalletKind::Consumer,
            credit:             true,
            debit:              true,
            reserve:            false,
            release:            false,
            settle:             false,
            qr_payments:        false,
            p2p_transfers:      false,
            payout_target:      false,
            refunds:            false,
            offline_payments:   false,
            max_balance_minor:  None,
            currency_lock:      None,
            max_payment_minor:  None,
        }
    }

    /// Full consumer wallet — all standard flows enabled.
    pub const fn full_consumer() -> Self {
        Self {
            version:          1,
            kind:             WalletKind::Consumer,
            credit:           true,
            debit:            true,
            reserve:          true,
            release:          true,
            settle:           true,
            qr_payments:      true,
            p2p_transfers:    true,
            payout_target:    false,
            refunds:          true,
            offline_payments: false,
            max_balance_minor: None,
            currency_lock:    None,
            max_payment_minor: None,
        }
    }

    /// Standard merchant receiving wallet.
    ///
    /// Can receive payments (credit) and be used as a payout target.
    /// Cannot initiate consumer-side flows (no debit, no reserve).
    pub const fn merchant() -> Self {
        Self {
            version:          1,
            kind:             WalletKind::Merchant,
            credit:           true,
            debit:            false,
            reserve:          false,
            release:          false,
            settle:           true,
            qr_payments:      false,
            p2p_transfers:    false,
            payout_target:    true,
            refunds:          true,
            offline_payments: false,
            max_balance_minor: None,
            currency_lock:    None,
            max_payment_minor: None,
        }
    }

    /// Internal float / transit wallet — not usable for external flows.
    pub const fn transit() -> Self {
        Self {
            version:          1,
            kind:             WalletKind::Transit,
            credit:           true,
            debit:            true,
            reserve:          false,
            release:          false,
            settle:           false,
            qr_payments:      false,
            p2p_transfers:    false,
            payout_target:    false,
            refunds:          false,
            offline_payments: false,
            max_balance_minor: None,
            currency_lock:    None,
            max_payment_minor: None,
        }
    }

    /// Returns `true` if the capability set supports the named operation.
    pub fn supports(&self, operation: WalletOperation) -> bool {
        match operation {
            WalletOperation::Credit          => self.credit,
            WalletOperation::Debit           => self.debit,
            WalletOperation::Reserve         => self.reserve,
            WalletOperation::Release         => self.release,
            WalletOperation::Settle          => self.settle,
            WalletOperation::QrPayment       => self.qr_payments,
            WalletOperation::P2pTransfer     => self.p2p_transfers,
            WalletOperation::PayoutTarget    => self.payout_target,
            WalletOperation::Refund          => self.refunds,
            WalletOperation::OfflinePayment  => self.offline_payments,
        }
    }
}

/// Named wallet operations that may be guarded by capability checks.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum WalletOperation {
    Credit,
    Debit,
    Reserve,
    Release,
    Settle,
    QrPayment,
    P2pTransfer,
    PayoutTarget,
    Refund,
    OfflinePayment,
}

impl std::fmt::Display for WalletOperation {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let s = match self {
            Self::Credit         => "credit",
            Self::Debit          => "debit",
            Self::Reserve        => "reserve",
            Self::Release        => "release",
            Self::Settle         => "settle",
            Self::QrPayment      => "qr_payment",
            Self::P2pTransfer    => "p2p_transfer",
            Self::PayoutTarget   => "payout_target",
            Self::Refund         => "refund",
            Self::OfflinePayment => "offline_payment",
        };
        f.write_str(s)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn merchant_wallet_cannot_qr_pay() {
        let caps = WalletCapabilitySet::merchant();
        assert!(!caps.supports(WalletOperation::QrPayment));
        assert!(caps.supports(WalletOperation::Credit));
        assert!(caps.supports(WalletOperation::PayoutTarget));
    }

    #[test]
    fn transit_wallet_has_no_payment_flows() {
        let caps = WalletCapabilitySet::transit();
        assert!(caps.supports(WalletOperation::Credit));
        assert!(caps.supports(WalletOperation::Debit));
        assert!(!caps.supports(WalletOperation::QrPayment));
        assert!(!caps.supports(WalletOperation::P2pTransfer));
        assert!(!caps.supports(WalletOperation::Refund));
    }

    #[test]
    fn full_consumer_supports_all_standard_flows() {
        let caps = WalletCapabilitySet::full_consumer();
        let flows = [
            WalletOperation::Credit,
            WalletOperation::Debit,
            WalletOperation::Reserve,
            WalletOperation::Release,
            WalletOperation::Settle,
            WalletOperation::QrPayment,
            WalletOperation::P2pTransfer,
            WalletOperation::Refund,
        ];
        for op in flows {
            assert!(caps.supports(op), "{op} should be supported");
        }
    }

    #[test]
    fn capability_set_is_serializable() {
        let caps = WalletCapabilitySet::full_consumer();
        let json = serde_json::to_string(&caps).unwrap();
        let _: WalletCapabilitySet = serde_json::from_str(&json).unwrap();
    }
}
