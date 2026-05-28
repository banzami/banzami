# Sandbox vs Production

Banzami-based systems must maintain strict environment isolation. Mixing sandbox and production data is a hard error.

## Environment Variables

Operators configure the acquiring provider at startup:

| Variable                    | Sandbox / Dev              | Production                  |
|-----------------------------|----------------------------|-----------------------------|
| `APP_ENV`                   | `development` (default)    | `production`                |
| `ACQUIRING_PROVIDER`        | (unset = SIMULATED)        | `<your-provider-name>`      |
| `ACQUIRING_WEBHOOK_SECRET`  | dev / test secret          | Provider-issued HMAC secret |

## Boot Safety Guard

Operators should implement a startup guard that refuses to boot in production mode with a simulated provider active:

```rust
if app_env == Environment::Production && provider.is_simulated() {
    panic!("Refusing to start: production environment requires a real acquiring provider");
}
```

This prevents accidentally deploying simulated payments to production.

## Provider Behaviour

### Simulated provider (sandbox / development)

A simulated `AcquirerProvider` implementation for sandbox environments typically:
- Generates realistic payment reference numbers locally
- Signs callbacks with HMAC using a test `ACQUIRING_WEBHOOK_SECRET`
- Makes no external HTTP calls — fully deterministic
- Supports test-confirm endpoints for instant settlement simulation

### Production provider

A production `AcquirerProvider` implementation:
- Calls the live external payment rail API
- Validates inbound HMAC signatures from the provider
- Registers a production webhook URL with the provider

## API Keys and Environment

Banzami API keys are prefixed to indicate environment:
- `bz_test_...` → Sandbox keys → routed to simulated provider
- `bz_live_...` → Production keys → routed to production provider

**Rule**: Secret API keys (`bz_live_...`) NEVER appear in frontend, mobile, or browser code.

## Sandbox Credit (Sandboxed Merchants)

For sandbox merchant accounts (QA, testing), operators can implement a sandbox credit endpoint:

```
POST /internal/v1/wallets/{wallet_id}/sandbox-credit
```

Recommended: cap sandbox credits (e.g. 100,000,000 AOA per request). The sandbox credit route should only be reachable when `APP_ENV != production`.

## Admin Manual Credit

For beta testing or pilot merchant onboarding, an admin credit endpoint seeds wallets directly via the ledger. Example:

```
POST /admin/v1/wallets/{wallet_id}/credit
Authorization: Bearer <admin-key>
{
  "amount_minor": 5000000,
  "currency": "AOA",
  "reason": "Pilot merchant onboarding credit"
}
```

- Reason field is required and embedded in the ledger posting description
- Creates auditable double-entry in the ledger
- Admin-only — protected by admin API key authentication
