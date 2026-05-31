# banza-acquiring — Acquiring Abstraction

The acquiring crate bridges Banza payment links to external payment networks. It is fully operator-defined: Banza provides the engine and trait; operators bring their own provider implementations.

---

## What it is

`banza-acquiring` provides:
- The `AcquirerProvider` trait — the interface operators implement for their payment rails
- `PostgresAcquiringEngine` — a generic PostgreSQL-backed engine that orchestrates payment initiation and callback processing
- Domain types: `AcquiringPayment`, `AcquiringCallback`, `PaymentInstructions`

The crate contains **no** built-in payment provider. There is no EMIS-specific code, no Multicaixa-specific code, no bank-specific code. All of that lives in private operator implementations.

---

## Provider interface

```rust
pub trait AcquirerProvider: Send + Sync {
    fn provider_name(&self) -> &'static str;

    async fn initiate_payment(
        &self,
        req: InitiatePaymentRequest,
    ) -> Result<ExternalPaymentRef, AcquirerError>;

    async fn validate_callback(
        &self,
        raw_body:  &[u8],
        signature: &str,
    ) -> Result<PaymentConfirmation, AcquirerError>;

    // Optional — sandbox/test providers override this
    fn generate_test_callback(...) -> Option<(Vec<u8>, String)> { None }
}
```

Operators implement this trait for their payment rail and inject it at startup:

```rust
let engine = PostgresAcquiringEngine::new(MyProvider::new(config), repo);
```

---

## Engine operation

### Initiate payment

1. Calls `provider.initiate_payment()` with the internal payment ID and amount
2. Provider returns `ExternalPaymentRef` (external ref + instructions + expiry)
3. Engine stores an `acquiring_payment` record in PENDING state
4. Returns the payment with instructions for the customer

### Process callback

1. Calls `provider.validate_callback()` — HMAC signature verified
2. If invalid signature: request rejected, no state change
3. Checks idempotency: if callback already processed, returns current state
4. Persists raw callback in `acquiring_callbacks` (full audit trail)
5. Marks `acquiring_payment` as CONFIRMED
6. Returns the confirmed payment for downstream orchestration (wallet credit)

---

## Invariants

- Signature is validated **before** any state change
- Duplicate callbacks are detected via `UNIQUE ON idempotency_key` in `acquiring_callbacks`
- Wallet credit happens **after** the acquiring payment is CONFIRMED — never before
- The raw callback body and signature are preserved in `acquiring_callbacks` for audit

---

## Sandbox / development

For sandbox environments, operators implement a provider that:
- Generates realistic external references locally
- Signs test callbacks using HMAC with the test webhook secret
- Makes no external HTTP calls
- Implements `generate_test_callback()` to support test-confirm endpoints

The sandbox safety rule: **refuse to start in production mode with a simulated provider**. Implement this as a startup panic:

```rust
if app_env == Environment::Production && provider.is_simulated() {
    panic!("Refusing to start: production requires a real provider");
}
```

---

## Tables

| Table | Purpose |
|---|---|
| `acquiring_payments` | One row per payment attempt; tracks status lifecycle |
| `acquiring_callbacks` | Raw callback payloads, audit trail, idempotency store |

For operator details, see [docs/domains/acquiring/README.md](../domains/acquiring/README.md).
