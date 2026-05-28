//! Integration tests for the sandbox operator.
//!
//! Tests use axum's `tower::ServiceExt::oneshot` — no running server needed.
//! Each test gets a fresh router with its own AppState.

use axum::body::Body;
use axum::http::{Request, StatusCode};
use tower::ServiceExt;

use sandbox_operator::build_router;

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

async fn body_json(body: axum::body::Body) -> serde_json::Value {
    let bytes = axum::body::to_bytes(body, 1_000_000).await.unwrap();
    serde_json::from_slice(&bytes).unwrap()
}

fn get(uri: &str) -> Request<Body> {
    Request::builder().uri(uri).body(Body::empty()).unwrap()
}

fn post_json(uri: &str, body: serde_json::Value) -> Request<Body> {
    Request::builder()
        .method("POST")
        .uri(uri)
        .header("content-type", "application/json")
        .body(Body::from(body.to_string()))
        .unwrap()
}

// ---------------------------------------------------------------------------
// Health
// ---------------------------------------------------------------------------

#[tokio::test]
async fn health_endpoint_returns_ok() {
    let app = build_router();
    let res = app.oneshot(get("/health")).await.unwrap();
    assert_eq!(res.status(), StatusCode::OK);
    let json = body_json(res.into_body()).await;
    assert_eq!(json["status"], "ok");
    assert_eq!(json["environment"], "sandbox");
    assert_eq!(json["simulated"], true);
    assert_eq!(json["production_allowed"], false);
}

// ---------------------------------------------------------------------------
// Operator manifest
// ---------------------------------------------------------------------------

#[tokio::test]
async fn operator_manifest_is_valid() {
    let app = build_router();
    let res = app.oneshot(get("/.well-known/banzami/operator.json")).await.unwrap();
    assert_eq!(res.status(), StatusCode::OK);
    let json = body_json(res.into_body()).await;
    assert_eq!(json["operator_id"], "banzami-sandbox");
    assert_eq!(json["environment"], "sandbox");
    assert_eq!(json["simulated"], true);
    assert_eq!(json["production_allowed"], false);
    assert_eq!(json["providers"]["all_simulated"], true);
    assert!(json["capabilities"]["supports_wallets"].as_bool().unwrap());
    assert!(json["capabilities"]["supports_qr"].as_bool().unwrap());
    assert!(!json["capabilities"]["cross_operator_routing"].as_bool().unwrap());
}

#[tokio::test]
async fn manifest_explicitly_blocks_production() {
    let app = build_router();
    let res = app.oneshot(get("/.well-known/banzami/operator.json")).await.unwrap();
    let json = body_json(res.into_body()).await;
    assert_eq!(json["production_allowed"], false,
        "manifest must explicitly set production_allowed=false");
    assert_eq!(json["simulated"], true,
        "manifest must explicitly set simulated=true");
}

// ---------------------------------------------------------------------------
// Wallet creation
// ---------------------------------------------------------------------------

#[tokio::test]
async fn create_wallet_returns_wallet_with_zero_balance() {
    let app = build_router();
    let res = app.oneshot(post_json("/wallets", serde_json::json!({
        "label": "Test Wallet",
        "currency": "AOA",
    }))).await.unwrap();
    assert_eq!(res.status(), StatusCode::OK);
    let json = body_json(res.into_body()).await;
    assert_eq!(json["label"], "Test Wallet");
    assert_eq!(json["currency"], "AOA");
    assert_eq!(json["balance_minor"], 0);
    assert!(json["id"].as_str().unwrap().starts_with("wallet-"));
}

#[tokio::test]
async fn create_wallet_with_unknown_currency_is_rejected() {
    let app = build_router();
    let res = app.oneshot(post_json("/wallets", serde_json::json!({
        "label": "Bad Currency",
        "currency": "XYZ",
    }))).await.unwrap();
    assert_eq!(res.status(), StatusCode::BAD_REQUEST);
}

#[tokio::test]
async fn list_wallets_includes_seed_wallets() {
    let app = build_router();
    let res = app.oneshot(get("/wallets")).await.unwrap();
    assert_eq!(res.status(), StatusCode::OK);
    let json = body_json(res.into_body()).await;
    let wallets = json["wallets"].as_array().unwrap();
    assert!(wallets.len() >= 4, "should have at least 4 seed wallets");
    let ids: Vec<_> = wallets.iter().map(|w| w["id"].as_str().unwrap()).collect();
    assert!(ids.contains(&"sandbox-consumer-1"));
    assert!(ids.contains(&"sandbox-merchant-1"));
    assert!(ids.contains(&"sandbox-government-1"));
}

#[tokio::test]
async fn get_seed_wallet_has_nonzero_balance() {
    let app = build_router();
    let res = app.oneshot(get("/wallets/sandbox-consumer-1")).await.unwrap();
    assert_eq!(res.status(), StatusCode::OK);
    let json = body_json(res.into_body()).await;
    assert!(json["balance_minor"].as_i64().unwrap() > 0);
}

// ---------------------------------------------------------------------------
// Transfer
// ---------------------------------------------------------------------------

#[tokio::test]
async fn transfer_moves_balance_between_wallets() {
    let app = build_router();
    let res = app.oneshot(post_json("/transfers", serde_json::json!({
        "from_wallet_id": "sandbox-consumer-1",
        "to_wallet_id":   "sandbox-merchant-1",
        "amount_minor":   50_000,
        "currency":       "AOA",
        "note":           "integration test",
    }))).await.unwrap();
    assert_eq!(res.status(), StatusCode::OK);
    let json = body_json(res.into_body()).await;
    assert!(json["id"].as_str().unwrap().starts_with("txfr-"));
    assert_eq!(json["amount_minor"], 50_000);
    assert_eq!(json["from_wallet_id"], "sandbox-consumer-1");
    assert_eq!(json["to_wallet_id"],   "sandbox-merchant-1");
}

#[tokio::test]
async fn transfer_with_insufficient_funds_is_rejected() {
    let app = build_router();
    let res = app.oneshot(post_json("/transfers", serde_json::json!({
        "from_wallet_id": "sandbox-consumer-1",
        "to_wallet_id":   "sandbox-merchant-1",
        "amount_minor":   999_999_999,
        "currency":       "AOA",
    }))).await.unwrap();
    assert_eq!(res.status(), StatusCode::UNPROCESSABLE_ENTITY);
    let json = body_json(res.into_body()).await;
    assert!(json["error"].as_str().unwrap().contains("insufficient"));
}

#[tokio::test]
async fn transfer_is_idempotent_with_same_key() {
    let app = build_router();
    let body = serde_json::json!({
        "from_wallet_id":  "sandbox-consumer-1",
        "to_wallet_id":    "sandbox-merchant-1",
        "amount_minor":    1_000,
        "currency":        "AOA",
        "idempotency_key": "idem-test-abc123",
    });

    // First call.
    let res1 = app.clone().oneshot(post_json("/transfers", body.clone())).await.unwrap();
    assert_eq!(res1.status(), StatusCode::OK);
    let json1 = body_json(res1.into_body()).await;

    // Second call with same key — same transfer ID, no balance change.
    let res2 = app.oneshot(post_json("/transfers", body)).await.unwrap();
    assert_eq!(res2.status(), StatusCode::OK);
    let json2 = body_json(res2.into_body()).await;

    assert_eq!(json1["id"], json2["id"], "idempotent transfer must return same ID");
}

// ---------------------------------------------------------------------------
// Payment requests
// ---------------------------------------------------------------------------

#[tokio::test]
async fn payment_request_lifecycle() {
    let app = build_router();

    // Create payment request.
    let res = app.clone().oneshot(post_json("/payment-requests", serde_json::json!({
        "to_wallet_id": "sandbox-merchant-1",
        "amount_minor": 25_000,
        "currency":     "AOA",
        "description":  "test PR",
    }))).await.unwrap();
    assert_eq!(res.status(), StatusCode::OK);
    let pr = body_json(res.into_body()).await;
    assert_eq!(pr["status"], "pending");
    let pr_id = pr["id"].as_str().unwrap().to_string();

    // Verify pending via GET.
    let res = app.clone().oneshot(get(&format!("/payment-requests/{pr_id}"))).await.unwrap();
    assert_eq!(res.status(), StatusCode::OK);
    let fetched = body_json(res.into_body()).await;
    assert_eq!(fetched["status"], "pending");

    // Pay the request.
    let res = app.clone().oneshot(post_json(
        &format!("/payment-requests/{pr_id}/pay"),
        serde_json::json!({ "from_wallet_id": "sandbox-consumer-1" }),
    )).await.unwrap();
    assert_eq!(res.status(), StatusCode::OK);
    let paid = body_json(res.into_body()).await;
    assert_eq!(paid["status"], "paid");
    assert!(paid["transfer_id"].as_str().is_some());

    // Verify paid via GET.
    let res = app.oneshot(get(&format!("/payment-requests/{pr_id}"))).await.unwrap();
    let final_pr = body_json(res.into_body()).await;
    assert_eq!(final_pr["status"], "paid");
}

#[tokio::test]
async fn paying_already_paid_request_is_rejected() {
    let app = build_router();

    let res = app.clone().oneshot(post_json("/payment-requests", serde_json::json!({
        "to_wallet_id": "sandbox-merchant-1",
        "amount_minor": 1_000,
        "currency":     "AOA",
    }))).await.unwrap();
    let pr = body_json(res.into_body()).await;
    let pr_id = pr["id"].as_str().unwrap().to_string();

    // Pay once.
    app.clone().oneshot(post_json(
        &format!("/payment-requests/{pr_id}/pay"),
        serde_json::json!({ "from_wallet_id": "sandbox-consumer-1" }),
    )).await.unwrap();

    // Pay again — must fail.
    let res = app.oneshot(post_json(
        &format!("/payment-requests/{pr_id}/pay"),
        serde_json::json!({ "from_wallet_id": "sandbox-consumer-1" }),
    )).await.unwrap();
    assert_eq!(res.status(), StatusCode::UNPROCESSABLE_ENTITY);
}

// ---------------------------------------------------------------------------
// QR payment
// ---------------------------------------------------------------------------

#[tokio::test]
async fn qr_payment_flow() {
    let app = build_router();

    // Merchant generates QR.
    let res = app.clone().oneshot(post_json("/qr", serde_json::json!({
        "merchant_wallet_id": "sandbox-merchant-1",
        "amount_minor":       30_000,
        "currency":           "AOA",
        "description":        "QR test",
    }))).await.unwrap();
    assert_eq!(res.status(), StatusCode::OK);
    let qr = body_json(res.into_body()).await;
    assert_eq!(qr["status"], "active");
    let qr_id = qr["id"].as_str().unwrap().to_string();
    assert!(qr["payload_data"].as_str().unwrap().starts_with("BANZAMI-SBX:"));

    // Consumer pays QR.
    let res = app.clone().oneshot(post_json(
        &format!("/qr/{qr_id}/pay"),
        serde_json::json!({ "consumer_wallet_id": "sandbox-consumer-1" }),
    )).await.unwrap();
    assert_eq!(res.status(), StatusCode::OK);
    let paid = body_json(res.into_body()).await;
    assert_eq!(paid["status"], "paid");
    assert!(paid["transfer_id"].as_str().is_some());

    // QR cannot be paid twice.
    let res = app.oneshot(post_json(
        &format!("/qr/{qr_id}/pay"),
        serde_json::json!({ "consumer_wallet_id": "sandbox-consumer-1" }),
    )).await.unwrap();
    assert_eq!(res.status(), StatusCode::UNPROCESSABLE_ENTITY);
}

// ---------------------------------------------------------------------------
// Ledger inspection
// ---------------------------------------------------------------------------

#[tokio::test]
async fn transfer_creates_ledger_entries() {
    let app = build_router();

    app.clone().oneshot(post_json("/transfers", serde_json::json!({
        "from_wallet_id": "sandbox-consumer-1",
        "to_wallet_id":   "sandbox-merchant-1",
        "amount_minor":   10_000,
        "currency":       "AOA",
    }))).await.unwrap();

    let res = app.oneshot(get("/ledger/sandbox-consumer-1")).await.unwrap();
    let json = body_json(res.into_body()).await;
    assert!(json["entry_count"].as_i64().unwrap() > 0);
    let entries = json["entries"].as_array().unwrap();
    assert!(entries.iter().any(|e| e["kind"] == "DEBIT"));
    // Derived balance should be negative (debit from consumer).
    assert!(json["derived_balance_minor"].as_i64().unwrap() < 0);
}

// ---------------------------------------------------------------------------
// Settlement simulation
// ---------------------------------------------------------------------------

#[tokio::test]
async fn settlement_batch_creates_and_completes() {
    let app = build_router();

    // First make a transfer so there's something to settle.
    app.clone().oneshot(post_json("/transfers", serde_json::json!({
        "from_wallet_id": "sandbox-consumer-1",
        "to_wallet_id":   "sandbox-merchant-1",
        "amount_minor":   100_000,
        "currency":       "AOA",
    }))).await.unwrap();

    // Create settlement batch.
    let res = app.clone().oneshot(post_json("/settlement/batches", serde_json::json!({
        "wallet_id": "sandbox-merchant-1",
    }))).await.unwrap();
    assert_eq!(res.status(), StatusCode::OK);
    let batch = body_json(res.into_body()).await;
    assert_eq!(batch["status"], "completed");
    assert_eq!(batch["gross_minor"], 100_000);
    assert!(batch["fee_minor"].as_i64().unwrap() > 0);
    assert!(batch["net_minor"].as_i64().unwrap() < 100_000);
    assert!(batch["provider_ref"].as_str().unwrap().starts_with("SBX-SETTLE-"));

    // Verify via GET.
    let batch_id = batch["id"].as_str().unwrap().to_string();
    let res = app.oneshot(get(&format!("/settlement/batches/{batch_id}"))).await.unwrap();
    assert_eq!(res.status(), StatusCode::OK);
}

#[tokio::test]
async fn settlement_batch_without_receipts_is_rejected() {
    let app = build_router();
    // sandbox-float has no inbound transfers by default.
    let res = app.oneshot(post_json("/settlement/batches", serde_json::json!({
        "wallet_id": "sandbox-float",
    }))).await.unwrap();
    assert_eq!(res.status(), StatusCode::UNPROCESSABLE_ENTITY);
}

// ---------------------------------------------------------------------------
// Trace API
// ---------------------------------------------------------------------------

#[tokio::test]
async fn list_traces_empty_initially() {
    let app = build_router();
    let res = app.oneshot(get("/traces")).await.unwrap();
    assert_eq!(res.status(), StatusCode::OK);
    let json = body_json(res.into_body()).await;
    assert_eq!(json["count"], 0);
    assert_eq!(json["trace_ids"].as_array().unwrap().len(), 0);
}

#[tokio::test]
async fn transfer_creates_trace_entry() {
    let app = build_router();

    app.clone().oneshot(post_json("/transfers", serde_json::json!({
        "from_wallet_id": "sandbox-consumer-1",
        "to_wallet_id":   "sandbox-merchant-1",
        "amount_minor":   1_000,
        "currency":       "AOA",
    }))).await.unwrap();

    let res = app.oneshot(get("/traces")).await.unwrap();
    let json = body_json(res.into_body()).await;
    assert!(json["count"].as_i64().unwrap() > 0, "trace list must be non-empty after transfer");
}

#[tokio::test]
async fn transfer_response_includes_trace_id() {
    let app = build_router();

    let res = app.oneshot(post_json("/transfers", serde_json::json!({
        "from_wallet_id": "sandbox-consumer-1",
        "to_wallet_id":   "sandbox-merchant-1",
        "amount_minor":   2_000,
        "currency":       "AOA",
    }))).await.unwrap();
    let json = body_json(res.into_body()).await;
    let trace_id = json["trace_id"].as_str().expect("transfer must have trace_id");
    assert!(trace_id.starts_with("tr-"), "trace_id must start with tr-");
}

#[tokio::test]
async fn get_trace_returns_full_view() {
    let app = build_router();

    // Create transfer and capture trace_id.
    let res = app.clone().oneshot(post_json("/transfers", serde_json::json!({
        "from_wallet_id": "sandbox-consumer-1",
        "to_wallet_id":   "sandbox-merchant-1",
        "amount_minor":   5_000,
        "currency":       "AOA",
    }))).await.unwrap();
    let txfr = body_json(res.into_body()).await;
    let trace_id = txfr["trace_id"].as_str().unwrap().to_string();

    let res = app.oneshot(get(&format!("/traces/{trace_id}"))).await.unwrap();
    assert_eq!(res.status(), StatusCode::OK);
    let trace = body_json(res.into_body()).await;
    assert_eq!(trace["trace_id"], trace_id);
    assert!(trace["timeline"].as_array().unwrap().len() > 0);
    assert_eq!(trace["transfers"].as_array().unwrap().len(), 1);
}

#[tokio::test]
async fn get_unknown_trace_returns_404() {
    let app = build_router();
    let res = app.oneshot(get("/traces/tr-does-not-exist")).await.unwrap();
    assert_eq!(res.status(), StatusCode::NOT_FOUND);
}

#[tokio::test]
async fn trace_view_contains_both_ledger_entries() {
    let app = build_router();

    let res = app.clone().oneshot(post_json("/transfers", serde_json::json!({
        "from_wallet_id": "sandbox-consumer-1",
        "to_wallet_id":   "sandbox-merchant-1",
        "amount_minor":   3_000,
        "currency":       "AOA",
    }))).await.unwrap();
    let txfr = body_json(res.into_body()).await;
    let trace_id = txfr["trace_id"].as_str().unwrap().to_string();

    let res = app.oneshot(get(&format!("/traces/{trace_id}"))).await.unwrap();
    let trace = body_json(res.into_body()).await;
    let entries = trace["ledger_entries"].as_array().unwrap();
    assert_eq!(entries.len(), 2, "one DEBIT and one CREDIT per transfer");
    let kinds: Vec<_> = entries.iter().map(|e| e["kind"].as_str().unwrap()).collect();
    assert!(kinds.contains(&"DEBIT"),  "must have DEBIT entry");
    assert!(kinds.contains(&"CREDIT"), "must have CREDIT entry");
}

#[tokio::test]
async fn trace_view_contains_payment_events() {
    let app = build_router();

    let res = app.clone().oneshot(post_json("/transfers", serde_json::json!({
        "from_wallet_id": "sandbox-consumer-1",
        "to_wallet_id":   "sandbox-merchant-1",
        "amount_minor":   4_000,
        "currency":       "AOA",
    }))).await.unwrap();
    let txfr = body_json(res.into_body()).await;
    let trace_id = txfr["trace_id"].as_str().unwrap().to_string();

    let res = app.oneshot(get(&format!("/traces/{trace_id}"))).await.unwrap();
    let trace = body_json(res.into_body()).await;
    let events = trace["events"].as_array().unwrap();
    let event_types: Vec<_> = events.iter().map(|e| e["event_type"].as_str().unwrap()).collect();
    assert!(event_types.contains(&"payment.sent"),     "must include payment.sent event");
    assert!(event_types.contains(&"payment.received"), "must include payment.received event");
}

#[tokio::test]
async fn payment_request_has_trace_id() {
    let app = build_router();

    let res = app.oneshot(post_json("/payment-requests", serde_json::json!({
        "to_wallet_id": "sandbox-merchant-1",
        "amount_minor": 7_500,
        "currency":     "AOA",
        "description":  "trace test PR",
    }))).await.unwrap();
    let pr = body_json(res.into_body()).await;
    let trace_id = pr["trace_id"].as_str().expect("payment_request must have trace_id");
    assert!(trace_id.starts_with("tr-"));
}

#[tokio::test]
async fn payment_request_payment_shares_trace_id_with_transfer() {
    let app = build_router();

    // Create PR.
    let res = app.clone().oneshot(post_json("/payment-requests", serde_json::json!({
        "to_wallet_id": "sandbox-merchant-1",
        "amount_minor": 6_000,
        "currency":     "AOA",
    }))).await.unwrap();
    let pr = body_json(res.into_body()).await;
    let pr_trace_id = pr["trace_id"].as_str().unwrap().to_string();
    let pr_id       = pr["id"].as_str().unwrap().to_string();

    // Pay the PR.
    let res = app.clone().oneshot(post_json(
        &format!("/payment-requests/{pr_id}/pay"),
        serde_json::json!({ "from_wallet_id": "sandbox-consumer-1" }),
    )).await.unwrap();
    let paid_pr = body_json(res.into_body()).await;
    let transfer_id = paid_pr["transfer_id"].as_str().unwrap().to_string();

    // Lookup trace — transfer must be under the same trace_id as the PR.
    let res = app.oneshot(get(&format!("/traces/{pr_trace_id}"))).await.unwrap();
    assert_eq!(res.status(), StatusCode::OK);
    let trace = body_json(res.into_body()).await;
    let transfers = trace["transfers"].as_array().unwrap();
    assert!(
        transfers.iter().any(|t| t["id"] == transfer_id),
        "trace must contain the transfer that paid the PR"
    );
}

#[tokio::test]
async fn pr_payment_transfer_has_causation_id_of_pr() {
    let app = build_router();

    // Create and pay a PR.
    let res = app.clone().oneshot(post_json("/payment-requests", serde_json::json!({
        "to_wallet_id": "sandbox-merchant-1",
        "amount_minor": 8_000,
        "currency":     "AOA",
    }))).await.unwrap();
    let pr = body_json(res.into_body()).await;
    let pr_id = pr["id"].as_str().unwrap().to_string();

    let res = app.clone().oneshot(post_json(
        &format!("/payment-requests/{pr_id}/pay"),
        serde_json::json!({ "from_wallet_id": "sandbox-consumer-1" }),
    )).await.unwrap();
    let paid = body_json(res.into_body()).await;
    let transfer_id = paid["transfer_id"].as_str().unwrap().to_string();

    // Fetch the transfer and check causation_id.
    let res = app.oneshot(get("/transfers")).await.unwrap();
    let list = body_json(res.into_body()).await;
    let transfers = list["transfers"].as_array().unwrap();
    let txfr = transfers.iter().find(|t| t["id"] == transfer_id).expect("transfer not found");
    assert_eq!(txfr["causation_id"], pr_id,
        "transfer caused by PR must carry the PR id as causation_id");
}

#[tokio::test]
async fn qr_payment_shares_trace_id_with_transfer() {
    let app = build_router();

    // Generate QR.
    let res = app.clone().oneshot(post_json("/qr", serde_json::json!({
        "merchant_wallet_id": "sandbox-merchant-1",
        "amount_minor":       9_000,
        "currency":           "AOA",
        "description":        "trace-qr test",
    }))).await.unwrap();
    let qr = body_json(res.into_body()).await;
    let qr_trace_id = qr["trace_id"].as_str().unwrap().to_string();
    let qr_id       = qr["id"].as_str().unwrap().to_string();

    // Pay QR.
    let res = app.clone().oneshot(post_json(
        &format!("/qr/{qr_id}/pay"),
        serde_json::json!({ "consumer_wallet_id": "sandbox-consumer-1" }),
    )).await.unwrap();
    let paid = body_json(res.into_body()).await;
    let transfer_id = paid["transfer_id"].as_str().unwrap().to_string();

    // Trace must contain the transfer.
    let res = app.oneshot(get(&format!("/traces/{qr_trace_id}"))).await.unwrap();
    assert_eq!(res.status(), StatusCode::OK);
    let trace = body_json(res.into_body()).await;
    let transfers = trace["transfers"].as_array().unwrap();
    assert!(
        transfers.iter().any(|t| t["id"] == transfer_id),
        "trace must contain the transfer that paid the QR"
    );
}

#[tokio::test]
async fn qr_payment_transfer_has_causation_id_of_qr() {
    let app = build_router();

    let res = app.clone().oneshot(post_json("/qr", serde_json::json!({
        "merchant_wallet_id": "sandbox-merchant-1",
        "amount_minor":       11_000,
        "currency":           "AOA",
    }))).await.unwrap();
    let qr = body_json(res.into_body()).await;
    let qr_id = qr["id"].as_str().unwrap().to_string();

    let res = app.clone().oneshot(post_json(
        &format!("/qr/{qr_id}/pay"),
        serde_json::json!({ "consumer_wallet_id": "sandbox-consumer-1" }),
    )).await.unwrap();
    let paid = body_json(res.into_body()).await;
    let transfer_id = paid["transfer_id"].as_str().unwrap().to_string();

    let res = app.oneshot(get("/transfers")).await.unwrap();
    let list = body_json(res.into_body()).await;
    let transfers = list["transfers"].as_array().unwrap();
    let txfr = transfers.iter().find(|t| t["id"] == transfer_id).expect("transfer not found");
    assert_eq!(txfr["causation_id"], qr_id,
        "transfer caused by QR payment must carry the QR id as causation_id");
}

#[tokio::test]
async fn settlement_batch_has_trace_id() {
    let app = build_router();

    // Create incoming transfer first.
    app.clone().oneshot(post_json("/transfers", serde_json::json!({
        "from_wallet_id": "sandbox-consumer-1",
        "to_wallet_id":   "sandbox-merchant-1",
        "amount_minor":   20_000,
        "currency":       "AOA",
    }))).await.unwrap();

    let res = app.oneshot(post_json("/settlement/batches", serde_json::json!({
        "wallet_id": "sandbox-merchant-1",
    }))).await.unwrap();
    assert_eq!(res.status(), StatusCode::OK);
    let batch = body_json(res.into_body()).await;
    let trace_id = batch["trace_id"].as_str().expect("settlement batch must have trace_id");
    assert!(trace_id.starts_with("tr-"));
}

// ---------------------------------------------------------------------------
// Event history
// ---------------------------------------------------------------------------

#[tokio::test]
async fn events_history_records_actions() {
    let app = build_router();

    // Trigger an event.
    app.clone().oneshot(post_json("/wallets", serde_json::json!({
        "label": "Event Test Wallet",
        "currency": "AOA",
    }))).await.unwrap();

    let res = app.oneshot(get("/events/history")).await.unwrap();
    assert_eq!(res.status(), StatusCode::OK);
    let json = body_json(res.into_body()).await;
    assert!(json["count"].as_i64().unwrap() > 0);
    let events = json["events"].as_array().unwrap();
    assert!(events.iter().any(|e| e["event_type"] == "wallet.created"));
}
