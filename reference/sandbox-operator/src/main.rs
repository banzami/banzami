//! Banzami Sandbox Operator — local development runtime.
//!
//! This is NOT a production financial system. It uses simulated providers
//! (fake payment rails, stdout notifications, no real bank connections) to
//! provide a fully local environment for experimenting with the Banzami kernel.
//!
//! # Usage
//!
//! ```bash
//! cargo run --bin sandbox-operator
//! ```
//!
//! Then use the API at http://localhost:3100
//!
//! # What this operator wires up
//!
//! - FakeAcquirer       → AcquirerProvider  (simulated payment rail, no EMIS/bank)
//! - SimulatedSettlement→ SettlementExecutionProvider (instant fake settlement)
//! - StdoutNotifications→ NotificationProvider (logs events to console)
//! - StaticRoutingEngine→ RoutingEngine (multi-currency example rules)
//!
//! # Environment variables
//!
//! None required. All defaults are sandbox-safe.
//! Optional: RUST_LOG=info (default), PORT=3100

mod routes;
mod state;

use tower_http::trace::TraceLayer;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    tracing_subscriber::fmt()
        .with_env_filter(
            std::env::var("RUST_LOG")
                .unwrap_or_else(|_| "sandbox_operator=debug,banzami=debug,info".into())
        )
        .init();

    tracing::info!("╔══════════════════════════════════════════════════╗");
    tracing::info!("║  Banzami Sandbox Operator                        ║");
    tracing::info!("║  Local development environment — NOT production  ║");
    tracing::info!("╚══════════════════════════════════════════════════╝");
    tracing::info!("");
    tracing::info!("Providers:");
    tracing::info!("  acquiring    → FakeAcquirer (SIMULATED, no external calls)");
    tracing::info!("  settlement   → SimulatedSettlement (instant fake settlement)");
    tracing::info!("  notifications→ StdoutNotificationProvider (logs to console)");
    tracing::info!("");

    let port = std::env::var("PORT")
        .ok()
        .and_then(|p| p.parse::<u16>().ok())
        .unwrap_or(3100);

    let addr = format!("0.0.0.0:{port}");
    let listener = tokio::net::TcpListener::bind(&addr).await?;

    tracing::info!("Sandbox operator listening on http://{addr}");
    tracing::info!("Endpoints: GET /health  POST /wallets  POST /transfers  POST /qr  POST /pay");

    let app = routes::build_router()
        .layer(TraceLayer::new_for_http());

    axum::serve(listener, app).await?;
    Ok(())
}
