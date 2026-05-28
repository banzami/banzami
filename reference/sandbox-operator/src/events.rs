//! Sandbox event stream.
//!
//! Events are broadcast via a tokio broadcast channel. The SSE endpoint
//! at GET /events subscribes to this channel and streams events to clients.
//! The last 200 events are kept in memory for GET /events/history.
//!
//! Every event carries trace/correlation IDs so callers can reconstruct
//! the full causal chain of a payment flow.

use uuid::Uuid;

/// An event emitted by the sandbox operator.
///
/// Every state-changing operation emits one or more events. Each event is
/// linked to the operation that caused it via `trace_id`, `correlation_id`,
/// and `causation_id`, allowing consumers to reconstruct the full lifecycle
/// of a payment flow.
#[derive(Debug, Clone, serde::Serialize)]
pub struct SandboxEvent {
    /// Unique event identifier.
    pub id: String,
    /// Event type (e.g. "payment.sent", "wallet.created").
    pub event_type: String,
    /// The primary entity kind this event describes ("transfer", "payment_request", "qr", "wallet", "settlement").
    pub aggregate_type: String,
    /// The primary entity ID this event describes.
    pub aggregate_id: String,
    /// Traces all operations in the same payment flow (same for the whole flow).
    pub trace_id: String,
    /// Narrows the trace to the current aggregate (changes per operation step).
    pub correlation_id: String,
    /// The ID of the direct cause of this event, if any.
    #[serde(skip_serializing_if = "Option::is_none")]
    pub causation_id: Option<String>,
    /// Arbitrary event payload.
    pub payload: serde_json::Value,
    pub created_at: chrono::DateTime<chrono::Utc>,
}

impl SandboxEvent {
    /// Create an event with full trace context (preferred).
    pub fn with_trace(
        event_type:     impl Into<String>,
        aggregate_type: impl Into<String>,
        aggregate_id:   impl Into<String>,
        trace_id:       impl Into<String>,
        correlation_id: impl Into<String>,
        causation_id:   Option<String>,
        payload:        serde_json::Value,
    ) -> Self {
        Self {
            id:             format!("evt-{}", Uuid::new_v4()),
            event_type:     event_type.into(),
            aggregate_type: aggregate_type.into(),
            aggregate_id:   aggregate_id.into(),
            trace_id:       trace_id.into(),
            correlation_id: correlation_id.into(),
            causation_id,
            payload,
            created_at:     chrono::Utc::now(),
        }
    }
}

/// Well-known event type names emitted by the sandbox operator.
pub mod types {
    pub const WALLET_CREATED:          &str = "wallet.created";
    pub const PAYMENT_SENT:            &str = "payment.sent";
    pub const PAYMENT_RECEIVED:        &str = "payment.received";
    pub const PAYMENT_REQUEST_CREATED: &str = "payment_request.created";
    pub const PAYMENT_REQUEST_PAID:    &str = "payment_request.paid";
    pub const QR_GENERATED:            &str = "qr.generated";
    pub const QR_PAID:                 &str = "qr.paid";
    pub const SETTLEMENT_CREATED:      &str = "settlement.created";
    pub const SETTLEMENT_COMPLETED:    &str = "settlement.completed";
}
