# Acquiring Domain

Acquiring handles integration with external payment networks for merchant payment collection. It bridges Banzami payment links to a payment provider and processes confirmation callbacks.

The acquiring crate (`banzami-acquiring`) provides the engine trait and generic types. Operators bring their own provider implementations by implementing `AcquirerProvider`.

## Architecture

```
Customer scans QR / opens payment link
        ↓
Acquiring engine: initiate_payment()
        ↓
Provider returns external_ref + instructions
        ↓
Customer completes payment via provider's app/channel
        ↓
Provider sends HMAC-signed callback
        ↓
Acquiring engine: process_callback()
        ↓
Wallet credit: system:transit DR / wallet:available CR
```

## Provider Strategy

Operators implement `AcquirerProvider` for their payment rails. The engine is provider-agnostic:

```rust
impl AcquirerProvider for MyProvider {
    async fn initiate_payment(&self, req: InitiatePaymentRequest)
        -> Result<ExternalPaymentRef, AcquirerError> { ... }

    async fn validate_callback(&self, raw: &[u8], sig: &str)
        -> Result<PaymentConfirmation, AcquirerError> { ... }

    fn provider_name(&self) -> &str { "MY_PROVIDER" }
}
```

The provider is injected at startup via `PostgresAcquiringEngine::new(provider, repo)`.

**Safety principle**: Operators should implement a startup guard that refuses to boot in production mode with a simulated/test provider active. This prevents accidental production deployment with fake payments.

## Tables

### `acquiring_payments`
Tracks one payment attempt per payment link. States:
- `PENDING` → payment initiated, awaiting customer action
- `CONFIRMED` → callback received and validated
- `FAILED` → payment failed or expired

### `acquiring_callbacks`
Stores the raw callback payload for every inbound event. Provides:
- **Audit trail**: full callback body + signature preserved
- **Idempotency**: `UNIQUE` on `idempotency_key` prevents double-processing

## Wallet Settlement on Callback

When a callback confirms a payment (`CONFIRMED`), the acquiring engine immediately:
1. Checks idempotency (`ledger_postings.idempotency_key = "acquiring-settle-{payment_id}"`)
2. Looks up `payment_links.wallet_id` from the acquiring payment
3. Posts double-entry:
   - **DR** `system:transit` (ASSET) — provider paid the platform
   - **CR** `wallet:available` (LIABILITY) — merchant can now withdraw

This is idempotent: duplicate callbacks are ignored via `ON CONFLICT (idempotency_key) DO NOTHING`.

## Sandbox / Development

Operators should implement a `SimulatedProvider` (or equivalent) for development and sandbox environments. The `generate_test_callback` method on `AcquirerProvider` allows test providers to generate valid signed callback payloads for integration testing.

## Invariants

- Every wallet credit is preceded by an acquiring_payment confirmation in the same database
- A wallet is never credited twice for the same acquiring_payment (idempotency_key uniqueness)
- Callbacks are validated via HMAC-SHA256 before any state change
- Wallet credit failures are logged but do not fail the HTTP response (callback acknowledged)
