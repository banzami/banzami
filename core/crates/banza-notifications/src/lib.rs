use thiserror::Error;

// ---------------------------------------------------------------------------
// Event types
// ---------------------------------------------------------------------------

/// The category of notification event.
///
/// Operators use this to route events to the correct channel and template.
/// New event types are added here as the kernel grows.
#[derive(Debug, Clone, PartialEq, Eq)]
#[derive(serde::Serialize, serde::Deserialize)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum NotificationEventType {
    /// A wallet received funds (credit).
    WalletCredited,
    /// A wallet was debited (debit or payout).
    WalletDebited,
    /// A payment was confirmed.
    PaymentConfirmed,
    /// A payment failed.
    PaymentFailed,
    /// A QR code payment was initiated.
    QrPaymentInitiated,
    /// A transfer was received.
    TransferReceived,
    /// A settlement batch was completed.
    SettlementCompleted,
    /// A payout was sent.
    PayoutSent,
    /// Arbitrary operator-defined event.
    Custom(String),
}

/// A notification event to be delivered to a recipient.
#[derive(Debug, Clone)]
#[derive(serde::Serialize, serde::Deserialize)]
pub struct NotificationEvent {
    /// Operator-assigned ID of the recipient (consumer ID, merchant ID, device token, etc.).
    /// The operator implementation is responsible for resolving this to a delivery address.
    pub recipient_id: String,
    pub event_type:   NotificationEventType,
    /// Structured event payload — the provider implementation formats this for delivery.
    pub payload:      serde_json::Value,
    /// Human-readable title (for push notifications, log entries, etc.).
    pub title:        String,
    /// Human-readable body text.
    pub body:         String,
}

// ---------------------------------------------------------------------------
// Error
// ---------------------------------------------------------------------------

#[derive(Debug, Error)]
pub enum NotificationError {
    #[error("recipient not found: {0}")]
    RecipientNotFound(String),

    #[error("provider unavailable: {0}")]
    Unavailable(String),

    #[error("notification rejected by provider: {0}")]
    Rejected(String),
}

// ---------------------------------------------------------------------------
// Trait
// ---------------------------------------------------------------------------

/// Operator-implemented interface for notification delivery.
///
/// The kernel emits `NotificationEvent` values after significant financial
/// events. The operator implements this trait to deliver them via their
/// preferred channel: FCM, APNs, WebSocket, email, stdout (for development), etc.
///
/// # Invariants
/// - Delivery is best-effort: a `NotificationError` does not roll back the
///   financial operation that triggered the event.
/// - Implementations must not block the calling async task for more than a
///   few milliseconds. Use background queues for slow delivery channels.
/// - A simulated implementation for development/testing should write to stdout
///   or a local WebSocket — never call FCM, APNs, or any external service.
#[allow(async_fn_in_trait)]
pub trait NotificationProvider: Send + Sync {
    fn provider_name(&self) -> &'static str;

    /// Deliver a notification event to the recipient.
    ///
    /// Errors are logged but do not fail the calling operation.
    async fn send(&self, event: NotificationEvent) -> Result<(), NotificationError>;

    /// Returns `true` if this is a sandbox/simulated provider.
    /// Used in startup guards to prevent production deployment with fake delivery.
    fn is_simulated(&self) -> bool {
        false
    }
}

// ---------------------------------------------------------------------------
// Builder
// ---------------------------------------------------------------------------

impl NotificationEvent {
    pub fn new(
        recipient_id: impl Into<String>,
        event_type:   NotificationEventType,
        title:        impl Into<String>,
        body:         impl Into<String>,
        payload:      serde_json::Value,
    ) -> Self {
        Self {
            recipient_id: recipient_id.into(),
            event_type,
            payload,
            title: title.into(),
            body:  body.into(),
        }
    }
}
