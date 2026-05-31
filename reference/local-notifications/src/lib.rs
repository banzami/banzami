//! Local notification provider for development — writes to stdout/tracing.
//!
//! This is NOT a real push notification system. It replaces Firebase FCM and
//! APNs for local development, allowing contributors to observe notification
//! events without any external service credentials.

use banza_notifications::{NotificationError, NotificationEvent, NotificationProvider};

/// A notification provider that logs all events to stdout via `tracing`.
///
/// Suitable for: local development, integration tests, the reference sandbox.
/// NOT suitable for: production, staging, any real user delivery.
pub struct StdoutNotificationProvider;

impl NotificationProvider for StdoutNotificationProvider {
    fn provider_name(&self) -> &'static str {
        "SIMULATED_STDOUT"
    }

    async fn send(&self, event: NotificationEvent) -> Result<(), NotificationError> {
        tracing::info!(
            recipient_id = %event.recipient_id,
            event_type   = ?event.event_type,
            title        = %event.title,
            body         = %event.body,
            payload      = %serde_json::to_string(&event.payload).unwrap_or_default(),
            "[SANDBOX NOTIFICATION] event delivered to stdout"
        );
        Ok(())
    }

    fn is_simulated(&self) -> bool {
        true
    }
}

/// A notification provider that discards all events silently.
///
/// Useful for tests where notification side-effects should be suppressed.
pub struct NullNotificationProvider;

impl NotificationProvider for NullNotificationProvider {
    fn provider_name(&self) -> &'static str {
        "NULL"
    }

    async fn send(&self, _event: NotificationEvent) -> Result<(), NotificationError> {
        Ok(())
    }

    fn is_simulated(&self) -> bool {
        true
    }
}
