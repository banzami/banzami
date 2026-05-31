//! HTTP routes for the sandbox operator.

use std::convert::Infallible;
use std::sync::Arc;
use std::time::Duration;

use axum::{
    Json, Router,
    extract::{Path, State},
    http::StatusCode,
    response::sse::{Event, KeepAlive, Sse},
    routing::{get, post},
};
use banza_types::Currency;
use futures::StreamExt as _;
use tokio_stream::wrappers::BroadcastStream;

use crate::manifest::build_manifest;
use crate::state::{AppState, TraceView, WalletType};

// ---------------------------------------------------------------------------
// Router
// ---------------------------------------------------------------------------

pub fn build_router() -> Router {
    let state = Arc::new(AppState::new());

    Router::new()
        // Health & manifest
        .route("/health",      get(health))
        .route("/.well-known/banza/operator.json", get(operator_manifest))
        // Wallets
        .route("/wallets",     get(list_wallets).post(create_wallet))
        .route("/wallets/:id", get(get_wallet))
        // Transfers
        .route("/transfers",     get(list_transfers).post(create_transfer))
        .route("/transfers/:id", get(get_transfer))
        // Payment requests
        .route("/payment-requests",      get(list_payment_requests).post(create_payment_request))
        .route("/payment-requests/:id",  get(get_payment_request))
        .route("/payment-requests/:id/pay", post(pay_payment_request))
        // QR codes
        .route("/qr",          post(create_qr))
        .route("/qr/:id",      get(get_qr))
        .route("/qr/:id/pay",  post(pay_qr))
        // Ledger inspection
        .route("/ledger",              get(list_ledger_entries))
        .route("/ledger/:wallet_id",   get(ledger_for_wallet))
        // Settlement simulation
        .route("/settlement/batches",      get(list_settlement_batches).post(create_settlement_batch))
        .route("/settlement/batches/:id",  get(get_settlement_batch))
        // Events
        .route("/events",         get(sse_events))
        .route("/events/history", get(events_history))
        // Traces
        .route("/traces",         get(list_traces))
        .route("/traces/:id",     get(get_trace))
        .with_state(state)
}

// ---------------------------------------------------------------------------
// Health
// ---------------------------------------------------------------------------

async fn health(State(state): State<Arc<AppState>>) -> Json<serde_json::Value> {
    let wallet_count    = state.list_wallets().len();
    let transfer_count  = state.list_transfers().len();
    Json(serde_json::json!({
        "status":             "ok",
        "environment":        "sandbox",
        "operator":           "banza-sandbox",
        "simulated":          true,
        "production_allowed": false,
        "wallet_count":       wallet_count,
        "transfer_count":     transfer_count,
        "note": "Sandbox operator — all providers are simulated. No real payments are processed."
    }))
}

// ---------------------------------------------------------------------------
// Operator manifest
// ---------------------------------------------------------------------------

async fn operator_manifest() -> Json<serde_json::Value> {
    Json(serde_json::to_value(build_manifest()).unwrap())
}

// ---------------------------------------------------------------------------
// Wallets
// ---------------------------------------------------------------------------

#[derive(serde::Deserialize)]
struct CreateWalletRequest {
    label:       String,
    currency:    String,
    #[serde(default = "default_wallet_type")]
    wallet_type: WalletType,
}

fn default_wallet_type() -> WalletType { WalletType::Consumer }

async fn list_wallets(
    State(state): State<Arc<AppState>>,
) -> Json<serde_json::Value> {
    Json(serde_json::json!({ "wallets": state.list_wallets() }))
}

async fn create_wallet(
    State(state): State<Arc<AppState>>,
    Json(req):    Json<CreateWalletRequest>,
) -> Result<(StatusCode, Json<serde_json::Value>), (StatusCode, Json<serde_json::Value>)> {
    let currency = Currency::from_code(&req.currency)
        .ok_or_else(|| err(StatusCode::BAD_REQUEST, format!("unknown currency: {}", req.currency)))?;
    let wallet = state.create_wallet(req.label, currency, req.wallet_type);
    Ok((StatusCode::CREATED, Json(serde_json::to_value(&wallet).unwrap())))
}

async fn get_wallet(
    State(state): State<Arc<AppState>>,
    Path(id):     Path<String>,
) -> Result<Json<serde_json::Value>, (StatusCode, Json<serde_json::Value>)> {
    let wallet = state.get_wallet(&id)
        .ok_or_else(|| err(StatusCode::NOT_FOUND, format!("wallet {id} not found")))?;
    Ok(Json(serde_json::to_value(&wallet).unwrap()))
}

// ---------------------------------------------------------------------------
// Transfers
// ---------------------------------------------------------------------------

#[derive(serde::Deserialize)]
struct CreateTransferRequest {
    from_wallet_id:  String,
    to_wallet_id:    String,
    amount_minor:    i64,
    currency:        String,
    note:            Option<String>,
    idempotency_key: Option<String>,
}

async fn list_transfers(
    State(state): State<Arc<AppState>>,
) -> Json<serde_json::Value> {
    Json(serde_json::json!({ "transfers": state.list_transfers() }))
}

async fn get_transfer(
    State(state): State<Arc<AppState>>,
    Path(id):     Path<String>,
) -> Result<Json<serde_json::Value>, (StatusCode, Json<serde_json::Value>)> {
    let transfer = state.get_transfer(&id)
        .ok_or_else(|| err(StatusCode::NOT_FOUND, format!("transfer {id} not found")))?;
    Ok(Json(serde_json::to_value(&transfer).unwrap()))
}

async fn create_transfer(
    State(state): State<Arc<AppState>>,
    Json(req):    Json<CreateTransferRequest>,
) -> Result<(StatusCode, Json<serde_json::Value>), (StatusCode, Json<serde_json::Value>)> {
    let currency = Currency::from_code(&req.currency)
        .ok_or_else(|| err(StatusCode::BAD_REQUEST, format!("unknown currency: {}", req.currency)))?;
    if req.amount_minor <= 0 {
        return Err(err(StatusCode::BAD_REQUEST, "amount_minor must be positive".into()));
    }
    let transfer = state
        .create_transfer(
            req.from_wallet_id,
            req.to_wallet_id,
            req.amount_minor,
            currency,
            req.note.unwrap_or_default(),
            req.idempotency_key,
            None,
        )
        .map_err(|e| err(StatusCode::UNPROCESSABLE_ENTITY, e))?;

    tracing::info!(
        transfer_id = %transfer.id,
        from        = %transfer.from_wallet_id,
        to          = %transfer.to_wallet_id,
        amount      = transfer.amount_minor,
        "[SANDBOX] transfer created"
    );
    Ok((StatusCode::CREATED, Json(serde_json::to_value(&transfer).unwrap())))
}

// ---------------------------------------------------------------------------
// Payment requests
// ---------------------------------------------------------------------------

#[derive(serde::Deserialize)]
struct CreatePaymentRequestRequest {
    to_wallet_id: String,
    amount_minor: i64,
    currency:     String,
    description:  Option<String>,
}

async fn list_payment_requests(
    State(state): State<Arc<AppState>>,
) -> Json<serde_json::Value> {
    Json(serde_json::json!({ "payment_requests": state.list_payment_requests() }))
}

async fn create_payment_request(
    State(state): State<Arc<AppState>>,
    Json(req):    Json<CreatePaymentRequestRequest>,
) -> Result<Json<serde_json::Value>, (StatusCode, Json<serde_json::Value>)> {
    let currency = Currency::from_code(&req.currency)
        .ok_or_else(|| err(StatusCode::BAD_REQUEST, format!("unknown currency: {}", req.currency)))?;
    if req.amount_minor <= 0 {
        return Err(err(StatusCode::BAD_REQUEST, "amount_minor must be positive".into()));
    }
    let pr = state.create_payment_request(
        req.to_wallet_id,
        req.amount_minor,
        currency,
        req.description.unwrap_or_default(),
    ).map_err(|e| err(StatusCode::UNPROCESSABLE_ENTITY, e))?;

    tracing::info!(pr_id = %pr.id, "[SANDBOX] payment request created");
    Ok(Json(serde_json::to_value(&pr).unwrap()))
}

async fn get_payment_request(
    State(state): State<Arc<AppState>>,
    Path(id):     Path<String>,
) -> Result<Json<serde_json::Value>, (StatusCode, Json<serde_json::Value>)> {
    let pr = state.get_payment_request(&id)
        .ok_or_else(|| err(StatusCode::NOT_FOUND, format!("payment request {id} not found")))?;
    Ok(Json(serde_json::to_value(&pr).unwrap()))
}

#[derive(serde::Deserialize)]
struct PayPaymentRequestRequest {
    from_wallet_id: String,
}

async fn pay_payment_request(
    State(state): State<Arc<AppState>>,
    Path(id):     Path<String>,
    Json(req):    Json<PayPaymentRequestRequest>,
) -> Result<Json<serde_json::Value>, (StatusCode, Json<serde_json::Value>)> {
    let pr = state.pay_payment_request(&id, req.from_wallet_id)
        .map_err(|e| err(StatusCode::UNPROCESSABLE_ENTITY, e))?;
    tracing::info!(pr_id = %pr.id, transfer_id = ?pr.transfer_id, "[SANDBOX] payment request paid");
    Ok(Json(serde_json::to_value(&pr).unwrap()))
}

// ---------------------------------------------------------------------------
// QR codes
// ---------------------------------------------------------------------------

#[derive(serde::Deserialize)]
struct CreateQrRequest {
    merchant_wallet_id: String,
    amount_minor:       Option<i64>,
    currency:           String,
    description:        Option<String>,
}

async fn create_qr(
    State(state): State<Arc<AppState>>,
    Json(req):    Json<CreateQrRequest>,
) -> Result<Json<serde_json::Value>, (StatusCode, Json<serde_json::Value>)> {
    let currency = Currency::from_code(&req.currency)
        .ok_or_else(|| err(StatusCode::BAD_REQUEST, format!("unknown currency: {}", req.currency)))?;
    let qr = state.create_qr(
        req.merchant_wallet_id,
        req.amount_minor,
        currency,
        req.description.unwrap_or_default(),
    ).map_err(|e| err(StatusCode::UNPROCESSABLE_ENTITY, e))?;

    tracing::info!(qr_id = %qr.id, "[SANDBOX] QR generated");
    Ok(Json(serde_json::to_value(&qr).unwrap()))
}

async fn get_qr(
    State(state): State<Arc<AppState>>,
    Path(id):     Path<String>,
) -> Result<Json<serde_json::Value>, (StatusCode, Json<serde_json::Value>)> {
    let qr = state.get_qr(&id)
        .ok_or_else(|| err(StatusCode::NOT_FOUND, format!("QR {id} not found")))?;
    Ok(Json(serde_json::to_value(&qr).unwrap()))
}

#[derive(serde::Deserialize)]
struct PayQrRequest {
    consumer_wallet_id: String,
    amount_minor:       Option<i64>,
}

async fn pay_qr(
    State(state): State<Arc<AppState>>,
    Path(id):     Path<String>,
    Json(req):    Json<PayQrRequest>,
) -> Result<Json<serde_json::Value>, (StatusCode, Json<serde_json::Value>)> {
    let qr = state.pay_qr(&id, req.consumer_wallet_id, req.amount_minor)
        .map_err(|e| err(StatusCode::UNPROCESSABLE_ENTITY, e))?;
    tracing::info!(qr_id = %qr.id, transfer_id = ?qr.transfer_id, "[SANDBOX] QR paid");
    Ok(Json(serde_json::to_value(&qr).unwrap()))
}

// ---------------------------------------------------------------------------
// Ledger inspection
// ---------------------------------------------------------------------------

async fn list_ledger_entries(
    State(state): State<Arc<AppState>>,
) -> Json<serde_json::Value> {
    Json(serde_json::json!({ "entries": state.list_ledger_entries() }))
}

async fn ledger_for_wallet(
    State(state): State<Arc<AppState>>,
    Path(wallet_id): Path<String>,
) -> Json<serde_json::Value> {
    let entries = state.ledger_entries_for_wallet(&wallet_id);
    let balance: i64 = entries.iter().map(|e| match e.kind {
        crate::state::LedgerEntryKind::Credit =>  e.amount_minor,
        crate::state::LedgerEntryKind::Debit  => -e.amount_minor,
    }).sum();
    Json(serde_json::json!({
        "wallet_id": wallet_id,
        "derived_balance_minor": balance,
        "entry_count": entries.len(),
        "entries": entries,
    }))
}

// ---------------------------------------------------------------------------
// Settlement
// ---------------------------------------------------------------------------

#[derive(serde::Deserialize)]
struct CreateSettlementBatchRequest {
    wallet_id: String,
}

async fn list_settlement_batches(
    State(state): State<Arc<AppState>>,
) -> Json<serde_json::Value> {
    Json(serde_json::json!({ "batches": state.list_settlement_batches() }))
}

async fn create_settlement_batch(
    State(state): State<Arc<AppState>>,
    Json(req):    Json<CreateSettlementBatchRequest>,
) -> Result<Json<serde_json::Value>, (StatusCode, Json<serde_json::Value>)> {
    let batch = state.create_settlement_batch(&req.wallet_id)
        .map_err(|e| err(StatusCode::UNPROCESSABLE_ENTITY, e))?;
    tracing::info!(
        batch_id    = %batch.id,
        gross_minor = batch.gross_minor,
        net_minor   = batch.net_minor,
        "[SANDBOX] settlement batch completed"
    );
    Ok(Json(serde_json::to_value(&batch).unwrap()))
}

async fn get_settlement_batch(
    State(state): State<Arc<AppState>>,
    Path(id):     Path<String>,
) -> Result<Json<serde_json::Value>, (StatusCode, Json<serde_json::Value>)> {
    let batch = state.get_settlement_batch(&id)
        .ok_or_else(|| err(StatusCode::NOT_FOUND, format!("settlement batch {id} not found")))?;
    Ok(Json(serde_json::to_value(&batch).unwrap()))
}

// ---------------------------------------------------------------------------
// Events
// ---------------------------------------------------------------------------

async fn sse_events(
    State(state): State<Arc<AppState>>,
) -> Sse<impl futures::Stream<Item = Result<Event, Infallible>>> {
    let rx = state.event_tx.subscribe();
    let stream = BroadcastStream::new(rx).filter_map(|result| async move {
        result.ok().map(|event| {
            let data = serde_json::to_string(&event).unwrap_or_default();
            Ok(Event::default()
                .id(event.id.as_str())
                .event(event.event_type.as_str())
                .data(data))
        })
    });
    Sse::new(stream).keep_alive(
        KeepAlive::new()
            .interval(Duration::from_secs(15))
            .text("ping"),
    )
}

async fn events_history(
    State(state): State<Arc<AppState>>,
) -> Json<serde_json::Value> {
    let history = state.event_history();
    Json(serde_json::json!({
        "count":  history.len(),
        "events": history,
    }))
}

// ---------------------------------------------------------------------------
// Traces
// ---------------------------------------------------------------------------

async fn list_traces(
    State(state): State<Arc<AppState>>,
) -> Json<serde_json::Value> {
    let ids = state.list_trace_ids();
    Json(serde_json::json!({ "count": ids.len(), "trace_ids": ids }))
}

async fn get_trace(
    State(state): State<Arc<AppState>>,
    Path(id):     Path<String>,
) -> Result<Json<TraceView>, (StatusCode, Json<serde_json::Value>)> {
    let view = state.get_trace(&id)
        .ok_or_else(|| err(StatusCode::NOT_FOUND, format!("trace {id} not found")))?;
    Ok(Json(view))
}

// ---------------------------------------------------------------------------
// Error helper
// ---------------------------------------------------------------------------

fn err(status: StatusCode, message: String) -> (StatusCode, Json<serde_json::Value>) {
    (status, Json(serde_json::json!({ "error": message })))
}
