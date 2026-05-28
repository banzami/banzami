# banzami-payment-links — Payment Link Engine

Payment links are reusable, shareable URLs (and QR-backing objects) that customers use to pay a specific merchant a specific amount.

---

## What it is

`banzami-payment-links` provides:
- Payment link creation and storage
- Link expiry management
- Resolution: given a link ID, return the link details for the payment UI

Payment links are the primary commercial surface. QR codes reference payment links. The checkout flow resolves a payment link to display the amount and merchant details to the customer.

---

## Payment link types

| Type | Description |
|---|---|
| Fixed-amount | A specific amount in a specific currency |
| Open | Customer enters the amount at payment time |

The link type determines what the customer sees and what validation the payment engine performs.

---

## Lifecycle

```
ACTIVE    — link is valid, can be used to initiate payments
EXPIRED   — TTL elapsed, link can no longer initiate payments
CANCELLED — merchant cancelled, link is inactive
```

A link can be used for multiple payments (unless configured as single-use). Each payment attempt creates an `acquiring_payment` record that references the link.

---

## Relationship to acquiring

The acquiring engine uses the payment link to:
1. Determine the wallet to credit after payment
2. Retrieve the amount and currency for the provider request
3. Log which link originated the payment (for reporting)

The connection:

```
payment_link.wallet_id → acquiring_payment.wallet_id → ledger credit
```

---

## Operator note

Operators can configure link TTLs, single-use enforcement, and minimum/maximum amount constraints. These are passed at link creation time and stored with the link record.
