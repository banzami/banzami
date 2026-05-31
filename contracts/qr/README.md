# contracts/qr/

Canonical QR payment payload format specification for the BANZA protocol.

## Files

| File | Purpose |
|---|---|
| `payload-format.json` | Canonical QR payload grammar, prefix rules, encoding, HMAC signing for dynamic QR |
| `lifecycle.json` | QR code lifecycle FSM — states, transitions, invariants |

## The two QR types

| Type | Use case | Amount | Reusable | Expiry |
|---|---|---|---|---|
| `STATIC` | Personal @handle, shop counter | Payer sets | Yes | None |
| `DYNAMIC` | Invoice, e-commerce, POS terminal | Pre-set | No (single-use) | Mandatory |

## Payload prefix rule

| Environment | Prefix |
|---|---|
| Sandbox (`simulated=true`) | `BANZA-SBX:` (legacy: `BANZA-SBX:`) |
| Production (`simulated=false`) | `BANZA:` (legacy: `BANZA:`) |

An operator MUST NOT use `BANZA:` (production prefix) in a sandbox environment. This is a certification FAIL.

## Known divergence

The Rust kernel (`core/crates/banza-qr/src/engine.rs`) implements a compact protocol format.  
The sandbox operator (`reference/sandbox-operator/src/state.rs`) implements a verbose debug format.

**The compact kernel format is the canonical protocol format.** `payload-format.json` specifies it. The sandbox debug format is acceptable in sandbox environments only (where `simulated=true`).
