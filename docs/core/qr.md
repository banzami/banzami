# banzami-qr — QR Code Runtime

The QR crate manages the lifecycle of QR payment codes — generation, expiry, and the link between a QR code and its underlying payment link.

---

## What it is

`banzami-qr` provides:
- QR code record creation and storage
- QR expiry (time-bound codes with configurable TTL)
- Resolution: given a QR payload, find the associated payment link
- Background expiry worker that marks stale codes

QR codes are not payment links themselves — they are references to payment links. The QR payload encodes enough information for the customer's device to resolve the payment link and initiate payment.

---

## QR payload format

The canonical QR payload format is defined in [`contracts/qr/`](../../contracts/qr/). The QR crate generates and validates payloads conforming to that specification.

Key fields:
- `version` — payload version for backwards compatibility
- `merchant_id` — identifies the merchant
- `qr_id` — unique code identifier (UUID)
- `environment` — `sandbox` or `live` (sandbox codes must never be processed in production)

---

## Sandbox / live isolation

QR codes carry an `environment` field. The engine refuses to process a sandbox-environment QR in a production context and vice versa. This is enforced in the resolution step.

**Invariant**: a QR code with `environment = "sandbox"` must never result in a real wallet credit.

---

## Expiry

QR codes have a configurable TTL (time-to-live). The `run_expiry_worker` background task periodically marks expired codes as EXPIRED. Once expired, a code cannot be used to initiate a new payment.

Expiry is eventually consistent — there is a window between the TTL and the expiry worker's next tick. Operators should set their TTL conservatively.

---

## QR payload versioning

The QR payload format is versioned. All parsers must support the versions documented in `contracts/qr/`. Version bumps that change the payload structure require an ADR and a transition period where both old and new versions are accepted.

---

## Operator note

The `QrEngine` trait is generic over its repository. Operators inject their own storage backend. The engine logic (expiry, resolution, environment validation) is independent of storage.
