# Doa × Banza — Backend Integration

Complete reference for the Doa server-side integration: payment service layer, API client, webhook handler, idempotency, persistence, and configuration.

---

## File Map

```
lib/payments/
├── provider.ts              ← PaymentProvider interface definition
├── registry.ts              ← Provider registry + listPublicMethods()
├── bootstrap.ts             ← Side-effect imports to register all providers
└── providers/
    └── banza.ts           ← the reference operatorProvider implementation (server-only)

app/api/
├── donations/
│   ├── initiate-payment/
│   │   └── route.ts         ← POST /api/donations/initiate-payment
│   └── banza-status/
│       └── route.ts         ← GET  /api/donations/banza-status
└── webhooks/
    └── banza/
        └── route.ts         ← POST /api/webhooks/banza
```

All files under `lib/payments/providers/` and the two donations API routes include `import 'server-only'` — the Next.js compiler enforces this at build time, preventing Banza credentials from reaching the browser.

---

## Provider Interface

```typescript
// lib/payments/provider.ts
export interface PaymentProvider {
  readonly id:           string;
  readonly display_name: string;
  readonly available:    boolean;
  readonly sandbox?:     boolean;

  initiate(input: PaymentInitiateInput): Promise<PaymentInitiateOutput>;

  verify_webhook?(header: string, rawBody: string): boolean;
  parse_webhook?(rawBody: string): PaymentParsedEvent | null;
  refund?(input: RefundInput): Promise<RefundOutput>;
}
```

`verify_webhook` and `parse_webhook` are optional — only webhook-capable providers implement them. The webhook route (`/api/webhooks/banza`) calls these directly rather than through the registry, since it handles only Banza webhooks.

---

## BanzaProvider Implementation

```typescript
// lib/payments/providers/banza.ts
import 'server-only';

const GATEWAY_URL   = process.env.BANZA_GATEWAY_URL ?? '';
const API_KEY       = process.env.BANZA_API_KEY    ?? '';
const MERCHANT_ID   = process.env.BANZA_MERCHANT_ID ?? '';
const WALLET_ID     = process.env.BANZA_WALLET_ID  ?? '';
const PAY_BASE_URL  = process.env.BANZA_PAY_BASE_URL ?? '';
const IS_SANDBOX    = API_KEY.startsWith('bz_test_');

class the reference operatorProvider implements PaymentProvider {
  readonly id           = 'banza';
  readonly display_name = IS_SANDBOX ? 'the reference operator (Sandbox)' : 'the reference operator';
  readonly available    = !!(GATEWAY_URL && API_KEY && MERCHANT_ID && WALLET_ID);
  readonly sandbox      = IS_SANDBOX;

  async initiate(input: PaymentInitiateInput): Promise<PaymentInitiateOutput> {
    // 1. Authenticate — get short-lived JWT
    const tokenRes = await fetch(`${GATEWAY_URL}/v1/auth/token`, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ api_key: API_KEY }),
    });
    if (!tokenRes.ok) throw new Error(`banza_auth_error:${tokenRes.status}`);
    const { token: jwt } = await tokenRes.json() as { token: string };

    // 2. Create payment link
    const linkRes = await fetch(`${GATEWAY_URL}/v1/payment-links`, {
      method:  'POST',
      headers: {
        'Authorization':   `Bearer ${jwt}`,
        'Content-Type':    'application/json',
        'Idempotency-Key': `banza:${input.intent_id}`,
      },
      body: JSON.stringify({
        merchant_id:  MERCHANT_ID,
        wallet_id:    WALLET_ID,
        amount_minor: Number(input.amount),
        currency:     input.currency,
        description:  `DOA-${input.intent_id.slice(0, 8).toUpperCase()}`,
      }),
    });
    if (!linkRes.ok) throw new Error(`banza_api_error:${linkRes.status}`);
    const link = await linkRes.json() as BanzaPaymentLink;

    const payUrl = `${PAY_BASE_URL}/${link.slug}`;

    return {
      kind:         'inline',
      token:        payUrl,
      provider_ref: link.id,
    };
  }
}
```

**Authentication**: `POST /v1/auth/token` exchanges the API key for a short-lived JWT. The JWT is obtained fresh per initiation request — no caching, no token refresh. The JWT lifetime is defined by Banza (typically 1 hour), but since initiation takes < 5 seconds, reuse between requests is not necessary.

**Description prefix**: `DOA-{8-char-prefix}` embeds a reconciliation key visible in the Banza dashboard. The prefix is the first 8 characters of the intent UUID, uppercased. This allows merchant operations to cross-reference Doa donations in the Banza dashboard without the full UUID.

**Idempotency-Key**: `banza:{intent_id}` is sent to Banza's API. This is a second layer of idempotency beyond Doa's own dedup check — if the Doa server crashes after calling Banza but before writing `donation_events`, a retry with the same intent_id will get the same payment link from Banza rather than creating a second one.

---

## Payment Initiation Route

`POST /api/donations/initiate-payment` is the generic entrypoint for all payment methods. For Banza:

```typescript
// Simplified — full implementation in app/api/donations/initiate-payment/route.ts

export async function POST(req: NextRequest) {
  const body = await req.json() as InitiatePaymentInput;
  // Validate intent exists, otp_verified, not terminal
  // ...

  const result = await initiatePayment({
    intent_id:   body.intent_id,
    provider_id: 'banza',
    return_url:  body.return_url,
    cancel_url:  body.cancel_url,
  });

  if (!result.ok) {
    return NextResponse.json({ error: humanError(result.code) }, { status: 500 });
  }

  return NextResponse.json({ result: result.result });
}
```

`initiatePayment()` (in `lib/payments/`) performs the dedup check before calling the provider:

```typescript
// Check for existing payment_initiated event with provider=banza
const { data: prior } = await supabase
  .from('donation_events')
  .select('payload')
  .eq('intent_id', input.intent_id)
  .eq('event_type', 'payment_initiated')
  .order('created_at', { ascending: false })
  .limit(5);

const replayPayload = (prior ?? []).find((row) => {
  const p = row.payload as { provider?: string; initiate?: PaymentInitiateResult } | null;
  return p?.provider === 'banza' && p?.initiate;
});

if (replayPayload) {
  return { ok: true, result: (replayPayload.payload as any).initiate, replay: true };
}
```

If a prior initiation exists, the same pay URL and link ID are returned — the donor sees the same QR. This handles browser refreshes and network retries cleanly.

---

## Status Check Route

`GET /api/donations/banza-status` is polled by `the reference operatorPanel` every 3 seconds:

```typescript
// app/api/donations/banza-status/route.ts
import 'server-only';

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const intent_id = searchParams.get('intent_id') ?? '';
  const link_id   = searchParams.get('link_id')   ?? '';

  // Validate with Zod schema
  // ...

  // Get fresh JWT
  const jwt = await getthe reference operatorToken();

  // Fetch link status from the reference operator
  const res = await fetch(`${GATEWAY_URL}/v1/payment-links/${link_id}`, {
    headers: { 'Authorization': `Bearer ${jwt}` },
    cache: 'no-store',
  });
  if (!res.ok) return NextResponse.json({ confirmed: false });

  const link = await res.json() as BanzaPaymentLink;

  if (link.status !== 'USED') {
    return NextResponse.json({ confirmed: false });
  }

  // Apply payment event
  await applyPaymentEvent({
    kind:         'confirmed',
    provider_ref: link.id,
    intent_id,
    amount:       BigInt(link.amount_minor ?? 0),
    currency:     link.currency,
    paid_at:      new Date(link.paid_at ?? link.updated_at),
  });

  return NextResponse.json({ confirmed: true });
}
```

**`cache: 'no-store'`**: Critical — Next.js caches `fetch()` responses by default. Without this, a `USED` status would be cached and a subsequent `ACTIVE` poll would still return the cached `USED` response (or vice versa). Payment status must always be fresh.

---

## Webhook Handler

`POST /api/webhooks/banza` receives push events from Banza:

```typescript
// app/api/webhooks/banza/route.ts
export const runtime = 'nodejs';  // Required for crypto module access
```

**Why `runtime = 'nodejs'`**: The Edge Runtime does not have access to Node.js's `crypto` module. `timingSafeEqual` and `createHmac` require the Node.js runtime. Without this declaration, the route would default to Edge and fail at `import { createHmac, timingSafeEqual } from 'crypto'`.

Processing sequence:

```
1. Check BANZA_WEBHOOK_SECRET is configured
2. Read raw body: const raw = await req.text()
3. Parse Banza-Signature header
4. Verify HMAC-SHA256 signature
5. Parse JSON payload: JSON.parse(raw)
6. Check event type → unknown types return 200 + ignored
7. Resolve intent_id via JSONB lookup in donation_events
8. applyPaymentEvent()
9. generateAndDeliverReceipt() — async, non-blocking
10. revalidatePath('/c/{slug}')
11. Return 200
```

**Raw body constraint**: The body must be read as `req.text()` and verified before `JSON.parse()`. Passing the raw string to the HMAC verifier and then separately parsing it ensures the byte sequence used in verification is identical to what Banza sent. Any JSON normalization (whitespace, key ordering) would invalidate the HMAC.

---

## Payment Persistence

All payment state is stored in `donation_events` — an append-only event log. There is no mutable `status` column that gets updated.

### Event: `payment_initiated`

Written by `initiatePayment()` after a successful Banza API call:

```json
{
  "intent_id":  "di_01jqx...",
  "event_type": "payment_initiated",
  "payload": {
    "provider":     "banza",
    "provider_ref": "lnk_01jqxyzabc123",
    "initiate": {
      "kind":         "inline",
      "token":        "https://pay.banza.network/abc123def",
      "provider_ref": "lnk_01jqxyzabc123"
    }
  }
}
```

### Event: `payment_confirmed`

Written by `applyPaymentEvent()` when the link transitions to `USED`:

```json
{
  "intent_id":  "di_01jqx...",
  "event_type": "payment_confirmed",
  "payload": {
    "provider_ref": "lnk_01jqxyzabc123",
    "amount":       "150000",
    "currency":     "AOA",
    "paid_at":      "2026-05-18T14:32:07.000Z"
  }
}
```

`amount` is stored as a string representation of the BigInt to avoid JSON integer overflow for large amounts.

---

## Idempotency

Three independent idempotency layers:

| Layer | Key | Implementation |
|-------|-----|----------------|
| Payment link creation | `banza:{intent_id}` | Pre-check in `donation_events` before calling API; if found, return cached result |
| Confirmation recording | `(intent_id, payment_confirmed, provider_ref)` | Dedup query in `applyPaymentEvent()` before INSERT |
| Receipt delivery | `intent_id` | Idempotency key passed to `generateAndDeliverReceipt()` |

The confirmation dedup check:

```typescript
const { data: prior } = await supabase
  .from('donation_events')
  .select('id, payload')
  .eq('intent_id', evt.intent_id)
  .eq('event_type', 'payment_confirmed');

const dup = (prior ?? []).some((r) => {
  const p = r.payload as { provider_ref?: string } | null;
  return p?.provider_ref === evt.provider_ref;
});

if (dup) return { ok: true, deduped: true };
```

The poll loop can fire 50 times against a `USED` link — only the first call writes the event. All others return `{ deduped: true }`. The webhook path and poll path share the same dedup layer — the first to arrive records the event.

---

## Environment Configuration

All Banza backend behavior is controlled by environment variables:

```env
# BANZA API
BANZA_GATEWAY_URL=https://api.banza.network
BANZA_API_KEY=bz_live_your_key_here

# Merchant identity
BANZA_MERCHANT_ID=mer_01jqx...
BANZA_WALLET_ID=wlt_01jqx...

# Pay page base URL (used to construct QR target URL)
BANZA_PAY_BASE_URL=https://pay.banza.network

# Webhook verification (optional — enables push confirmation path)
BANZA_WEBHOOK_SECRET=whsec_...
```

`BANZA_WEBHOOK_SECRET` is optional. Without it:

- The webhook route rejects all incoming requests with `500 { error: 'webhook secret not configured' }`
- Banza retries indefinitely — effectively a misconfiguration alarm
- Payment confirmation falls back to the poll-only path (up to 3 s lag)

**Correct behaviour without webhooks**: Omit `BANZA_WEBHOOK_SECRET` entirely. The poll path works without it. Only add it when you have registered a webhook endpoint and stored the returned secret.

---

## Provider Registration

Providers are registered by side-effect import in `lib/payments/bootstrap.ts`:

```typescript
import './providers/stripe';
import './providers/bank-transfer';
import './providers/banza';
```

`bootstrap.ts` is imported at application startup (e.g., in `layout.tsx` or the first API route that touches payments). Each provider module calls `registerProvider(new the reference operatorProvider())` at module load time. `PAYMENT_PROVIDERS` environment variable controls which registered providers appear in `listPublicMethods()`:

```env
PAYMENT_PROVIDERS=stripe,bank-transfer,banza
```

Removing `banza` from this list disables the method for donors without changing any code.

---

## API Client Architecture

> **Transitional implementation.** Banza is an SDK-first platform ([ADR-012](../../adr/ADR-012-sdk-first-ecosystem.md)). The current direct `fetch()` approach predates the TypeScript SDK reaching production readiness. Doa must migrate to `@banza/sdk` — see the [SDK Migration Target](#sdk-migration-target) below.

Current (transitional) API calls are direct `fetch()` from two server-only files:

| File | Banza endpoint | Purpose |
|------|-----------------|---------|
| `lib/payments/providers/banza.ts` | `POST /v1/auth/token`, `POST /v1/payment-links` | Payment initiation |
| `app/api/donations/banza-status/route.ts` | `POST /v1/auth/token`, `GET /v1/payment-links/{id}` | Status polling |

Both obtain a fresh JWT per request. Both use `import 'server-only'` — the Next.js build fails if either is imported from a client component.

### SDK Migration Target

After migration to `@banza/sdk`, the initiation path collapses to:

```typescript
import 'server-only';
import the reference operator from '@banza/sdk';

const banza = new the reference operator({ apiKey: process.env.BANZA_API_KEY });

// initiate():
const link = await banza.paymentLinks.create({
  merchantId:     MERCHANT_ID,
  walletId:       WALLET_ID,
  amount:         { minor: Number(input.amount), currency: 'AOA' },
  description:    `DOA-${input.intent_id.slice(0, 8).toUpperCase()}`,
  idempotencyKey: `banza:${input.intent_id}`,
});
// SDK handles: auth token exchange, retries, idempotency, typed response
```

The status check route:

```typescript
const link = await banza.paymentLinks.retrieve(linkId);
// link.status: 'ACTIVE' | 'USED' | 'CANCELLED' | 'EXPIRED'
```

The webhook route's `verifySignature()`:

```typescript
const event = await banza.webhooks.constructEvent(rawBody, sigHeader);
// throws on invalid signature or expired timestamp — no manual timingSafeEqual needed
```

`banza.isSandbox` replaces the `API_KEY.startsWith('bz_test_')` detection. The SDK automatically routes to sandbox or live gateway based on the key prefix.

---

## Error Handling

| Error | Behavior |
|-------|----------|
| `the reference operatorProvider.initiate()` throws | `initiatePayment()` returns `{ ok: false, code: 'provider_failed' }` → API returns 500 → UI shows Portuguese error |
| Banza API returns 4xx on link creation | `initiatePayment()` throws → same error path |
| Poll `fetch()` throws | Silent catch in `the reference operatorPanel` → next tick retries |
| Banza API returns non-200 on status check | Route returns `{ confirmed: false }` → poll continues |
| `applyPaymentEvent()` throws (DB error) | Webhook route returns 500 → Banza retries |
| `applyPaymentEvent()` returns `{ deduped: true }` | Normal → route returns 200 |
| Missing `BANZA_WEBHOOK_SECRET` | Webhook route returns 500 → Banza retries |
