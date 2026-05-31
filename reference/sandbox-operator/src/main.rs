//! Banzami Sandbox Operator — local development runtime.
//!
//! NOT a production financial system. All providers are simulated.
//!
//! Usage:
//! ```bash
//! cargo run --bin sandbox-operator
//! # or
//! docker compose up   # from reference/ directory
//! ```

use tower_http::trace::TraceLayer;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    tracing_subscriber::fmt()
        .with_env_filter(
            std::env::var("RUST_LOG")
                .unwrap_or_else(|_| "sandbox_operator=debug,banza=debug,info".into())
        )
        .init();

    // Safety check: refuse to start if BANZAMI_ALLOW_PRODUCTION is set.
    // This variable would indicate someone is trying to run the sandbox in a
    // production context — which is explicitly not supported.
    if std::env::var("BANZAMI_ALLOW_PRODUCTION").is_ok() {
        anyhow::bail!(
            "BANZAMI_ALLOW_PRODUCTION is set. The sandbox operator cannot run in production. \
             Use a real operator implementation with production providers."
        );
    }

    tracing::info!("╔══════════════════════════════════════════════════╗");
    tracing::info!("║  Banzami Sandbox Operator                        ║");
    tracing::info!("║  Local development environment — NOT production  ║");
    tracing::info!("║  simulated=true  production_allowed=false        ║");
    tracing::info!("╚══════════════════════════════════════════════════╝");
    tracing::info!("");
    tracing::info!("Providers (all simulated — no external calls):");
    tracing::info!("  acquirer     → FakeAcquirer");
    tracing::info!("  settlement   → SimulatedSettlementProvider");
    tracing::info!("  notifications→ StdoutNotificationProvider");
    tracing::info!("");
    tracing::info!("Seed wallets:");
    tracing::info!("  sandbox-consumer-1   (Consumer,    2 000 000 AOA)");
    tracing::info!("  sandbox-merchant-1   (Merchant,   10 000 000 AOA)");
    tracing::info!("  sandbox-government-1 (Government, 50 000 000 AOA)");
    tracing::info!("  sandbox-merchant-2   (Merchant,    5 000 000 AOA)");

    let port = std::env::var("PORT")
        .ok()
        .and_then(|p| p.parse::<u16>().ok())
        .unwrap_or(3100);

    let addr     = format!("0.0.0.0:{port}");
    let listener = tokio::net::TcpListener::bind(&addr).await?;

    tracing::info!("");
    tracing::info!("Listening on http://localhost:{port}");
    tracing::info!("");
    tracing::info!("Endpoints:");
    tracing::info!("  GET  /health");
    tracing::info!("  GET  /.well-known/banza/operator.json");
    tracing::info!("  GET  /wallets            POST /wallets");
    tracing::info!("  GET  /wallets/:id");
    tracing::info!("  GET  /transfers          POST /transfers");
    tracing::info!("  GET  /payment-requests   POST /payment-requests");
    tracing::info!("  POST /payment-requests/:id/pay");
    tracing::info!("  POST /qr                 GET  /qr/:id");
    tracing::info!("  POST /qr/:id/pay");
    tracing::info!("  GET  /ledger             GET  /ledger/:wallet_id");
    tracing::info!("  GET  /settlement/batches POST /settlement/batches");
    tracing::info!("  GET  /events             GET  /events/history");
    tracing::info!("");
    tracing::info!("Demo wallet: open reference/demo-wallet/index.html in your browser");

    let app = sandbox_operator::build_router()
        .layer(TraceLayer::new_for_http());

    axum::serve(listener, app).await?;
    Ok(())
}
