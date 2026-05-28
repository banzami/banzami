//! HTTP routes for the sandbox operator.
//!
//! All routes use in-memory state (no database required).
//! This is a minimal API surface for exploring the Banzami kernel.

use axum::{
    Json, Router,
    extract::{Path, State},
    http::StatusCode,
    routing::{get, post},
};
use std::sync::Arc;

use banzami_types::Currency;

use crate::state::AppState;

// ---------------------------------------------------------------------------
// Router
// ---------------------------------------------------------------------------

pub fn build_router() -> Router {
    let state = Arc::new(AppState::new());

    Router::new()
        .route("/health",      get(health))
        .route("/wallets",     post(create_wallet))
        .route("/wallets/:id", get(get_wallet))
        .route("/transfers",   post(create_transfer))
        .route("/transfers",   get(list_transfers))
        .with_state(state)
}

// ---------------------------------------------------------------------------
// Health
// ---------------------------------------------------------------------------

async fn health() -> Json<serde_json::Value> {
    Json(serde_json::json!({
        "status": "ok",
        "environment": "sandbox",
        "operator": "banzami-sandbox",
        "note": "This is a local development sandbox — not a production system."
    }))
}

// ---------------------------------------------------------------------------
// Wallets
// ---------------------------------------------------------------------------

#[derive(serde::Deserialize)]
struct CreateWalletRequest {
    label:    String,
    currency: String,
}

async fn create_wallet(
    State(state): State<Arc<AppState>>,
    Json(req):    Json<CreateWalletRequest>,
) -> Result<Json<serde_json::Value>, (StatusCode, Json<serde_json::Value>)> {
    let currency = Currency::from_code(&req.currency)
        .ok_or_else(|| error(StatusCode::BAD_REQUEST, format!("unknown currency: {}", req.currency)))?;

    let wallet = state.create_wallet(req.label, currency);

    Ok(Json(serde_json::json!({
        "id":       wallet.id,
        "label":    wallet.label,
        "currency": wallet.currency.code(),
        "balance_minor": wallet.balance_minor,
        "note": "Sandbox wallet — balances are in-memory and reset on restart."
    })))
}

async fn get_wallet(
    State(state): State<Arc<AppState>>,
    Path(id):     Path<String>,
) -> Result<Json<serde_json::Value>, (StatusCode, Json<serde_json::Value>)> {
    let wallet = state.get_wallet(&id)
        .ok_or_else(|| error(StatusCode::NOT_FOUND, format!("wallet {id} not found")))?;

    Ok(Json(serde_json::json!({
        "id":            wallet.id,
        "label":         wallet.label,
        "currency":      wallet.currency.code(),
        "balance_minor": wallet.balance_minor,
    })))
}

// ---------------------------------------------------------------------------
// Transfers
// ---------------------------------------------------------------------------

#[derive(serde::Deserialize)]
struct CreateTransferRequest {
    from_wallet_id: String,
    to_wallet_id:   String,
    amount_minor:   i64,
    currency:       String,
    note:           Option<String>,
}

async fn create_transfer(
    State(state): State<Arc<AppState>>,
    Json(req):    Json<CreateTransferRequest>,
) -> Result<Json<serde_json::Value>, (StatusCode, Json<serde_json::Value>)> {
    let currency = Currency::from_code(&req.currency)
        .ok_or_else(|| error(StatusCode::BAD_REQUEST, format!("unknown currency: {}", req.currency)))?;

    if req.amount_minor <= 0 {
        return Err(error(StatusCode::BAD_REQUEST, "amount_minor must be positive".into()));
    }

    let transfer = state
        .create_transfer(
            req.from_wallet_id.clone(),
            req.to_wallet_id.clone(),
            req.amount_minor,
            currency,
            req.note.unwrap_or_default(),
        )
        .map_err(|e| error(StatusCode::UNPROCESSABLE_ENTITY, e))?;

    tracing::info!(
        transfer_id = %transfer.id,
        from        = %transfer.from_wallet_id,
        to          = %transfer.to_wallet_id,
        amount      = transfer.amount_minor,
        currency    = %transfer.currency.code(),
        "[SANDBOX TRANSFER] created"
    );

    Ok(Json(serde_json::json!({
        "id":             transfer.id,
        "from_wallet_id": transfer.from_wallet_id,
        "to_wallet_id":   transfer.to_wallet_id,
        "amount_minor":   transfer.amount_minor,
        "currency":       transfer.currency.code(),
        "note":           transfer.note,
        "created_at":     transfer.created_at,
    })))
}

async fn list_transfers(
    State(state): State<Arc<AppState>>,
) -> Json<serde_json::Value> {
    let transfers = state.list_transfers();
    Json(serde_json::json!({ "transfers": transfers }))
}

// ---------------------------------------------------------------------------
// Error helper
// ---------------------------------------------------------------------------

fn error(status: StatusCode, message: String) -> (StatusCode, Json<serde_json::Value>) {
    (status, Json(serde_json::json!({ "error": message })))
}
