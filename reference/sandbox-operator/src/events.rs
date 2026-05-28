//! Sandbox event stream.
//!
//! Events are broadcast via a tokio broadcast channel. The SSE endpoint
//! at GET /events subscribes to this channel and streams events to clients.
//! The last 200 events are kept in memory for GET /events/history.

use uuid::Uuid;

/// An event emitted by the sandbox operator.
///
/// All significant state changes emit an event. Consumers can subscribe via
/// SSE (GET /events) or query recent history (GET /events/history).
#[derive(Debug, Clone, serde::Serialize)]
pub struct SandboxEvent {
    pub id:         String,
    pub event_type: String,
    pub payload:    serde_json::Value,
    pub created_at: chrono::DateTime<chrono::Utc>,
}

impl SandboxEvent {
    pub fn new(event_type: impl Into<String>, payload: serde_json::Value) -> Self {
        Self {
            id:         format!("evt-{}", Uuid::new_v4()),
            event_type: event_type.into(),
            payload,
            created_at: chrono::Utc::now(),
        }
    }
}

/// Well-known event type names emitted by the sandbox operator.
pub mod types {
    pub const WALLET_CREATED:           &str = "wallet.created";
    pub const PAYMENT_SENT:             &str = "payment.sent";
    pub const PAYMENT_RECEIVED:         &str = "payment.received";
    pub const PAYMENT_REQUEST_CREATED:  &str = "payment_request.created";
    pub const PAYMENT_REQUEST_PAID:     &str = "payment_request.paid";
    pub const QR_GENERATED:             &str = "qr.generated";
    pub const QR_PAID:                  &str = "qr.paid";
    pub const SETTLEMENT_CREATED:       &str = "settlement.created";
    pub const SETTLEMENT_COMPLETED:     &str = "settlement.completed";
}
