# BANZA Federation Sequence Diagrams

**Document ID:** FEDERATION-PROTOCOL-FLOW-DESIGN-001  
**Date:** 2026-05-31  
**Status:** Canonical — behavioral sequence diagrams for all federation flows.  
**Authority:** FEDERATION_PROTOCOL_FLOW.md, ADR-026

---

## Diagram Conventions

```
Actor A           Actor B
   │                 │
   │──── message ───▶│     Operator A sends a message to Operator B
   │◀─── response ───│     Operator B responds
   │                 │
   │── action        │     Actor performs a local action (no message)
   │                 │
   ·  ·  ·  ·  ·  ·  ·     Time passes (async / waiting)
   │                 │
  [X]               │     Actor fails or exits
   │                 │
   │ ══ ATOMIC ══════│     Block of operations that are one atomic transaction
   │                 │
```

**Actors used:**

```
Consumer    = payer; wallet on Operator A
Op-A        = Operator A (originating operator)
BANZA       = BANZA protocol services (BRL endpoint, public key distribution)
Op-B        = Operator B (destination operator)
Merchant    = payee; wallet on Operator B
Bank        = external banking rail (used for settlement only)
```

---

## Diagram 1 — Complete Happy Path

This diagram shows all ten phases of a successful federation transaction from consumer intent to final settlement. The trust verification detail is collapsed into a single block; see Diagram 3 for the full trust verification sequence.

```
Consumer     Op-A              BANZA           Op-B         Merchant      Bank
   │            │                │                │               │          │
   │──initiate──▶               │                │               │          │
   │   payment  │                │                │               │          │
   │            │                │                │               │          │
   │            │  ═══════ PHASE 1: DISCOVERY ════════════════════│          │
   │            │                │                │               │          │
   │            │──GET manifest──────────────────▶               │          │
   │            │◀──manifest─────────────────────│               │          │
   │            │  validate manifest              │               │          │
   │            │  check supports_federation      │               │          │
   │            │  check currency + limits        │               │          │
   │            │                │                │               │          │
   │            │  ═══════ PHASE 2: TRUST VERIFICATION ══════════│          │
   │            │                │                │               │          │
   │            │──GET BRL───────▶               │               │          │
   │            │◀──BRL (signed)─│               │               │          │
   │            │  verify BRL signature           │               │          │
   │            │──GET certificate───────────────▶               │          │
   │            │◀──certificate──────────────────│               │          │
   │            │  verify signature (BANZA key)   │               │          │
   │            │  verify expiry                  │               │          │
   │            │  verify cert level ≥ 3          │               │          │
   │            │  check BRL: operator-b not in   │               │          │
   │            │  verify federation capabilities │               │          │
   │            │  bind cert.operator_id == manifest.operator_id  │          │
   │            │   → TRUSTED                     │               │          │
   │            │                │                │               │          │
   │            │  ═══════ PHASE 3: ROUTING NEGOTIATION ══════════│          │
   │            │                │                │               │          │
   │            │  assign routing_request_id      │               │          │
   │            │  propagate trace_id             │               │          │
   │            │  sign request (Op-A private key)│               │          │
   │            │──POST /federation/route (signed)────────────────▶          │
   │            │                │         verify Banza-Federation-Signature  │
   │            │                │         fetch Op-A certificate ─▶ Op-A    │
   │            │                │         verify Op-A trust                  │
   │            │                │         resolve recipient ─────────────────▶
   │            │                │         ══ ATOMIC: credit payee ══════════│
   │            │                │         DEBIT  fed_receivable:op-a        │
   │            │                │         CREDIT payee_wallet ──────────────▶
   │            │                │         assign interop_transfer_id         │
   │            │                │         record routing_request as accepted  │
   │            │                │         emit federation.routing.accepted   │
   │            │                │         ════════════════════════════════════│
   │            │◀──status:accepted, interop_transfer_id, trace_id (echo)──  │
   │            │                │                │               │          │
   │            │  ═══════ PHASE 4 + 5: TRANSFER EXECUTION + OBLIGATION ═════│
   │            │                │                │               │          │
   │            │  ══ ATOMIC: debit + obligation ══               │          │
   │            │  DEBIT  payer_wallet             │               │          │
   │            │  CREDIT federation_payable:op-b  │               │          │
   │            │  create obligation (ob-uuid)     │               │          │
   │            │  sign obligation                 │               │          │
   │            │  payment_state → complete        │               │          │
   │            │  ═════════════════════════════════               │          │
   │            │  emit federation.payment.initiated               │          │
   │◀──confirmed│                │                │               │          │
   │            │                │         emit federation.payment.completed  │
   │            │                │         emit federation.obligation.recorded│
   │            │                │                │───notify──────▶          │
   │            │                │                │               │          │
   ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  [netting interval]  ·  │
   │            │                │                │               │          │
   │            │  ═══════ PHASE 6: NETTING + SETTLEMENT ══════════│          │
   │            │                │                │               │          │
   │            │  advance obligation → in_netting│               │          │
   │            │──obligation export─────────────▶               │          │
   │            │◀──obligation export (B→A)───────│               │          │
   │            │                │                │               │          │
   │            │  compute gross_A_to_B            │               │          │
   │            │                │         compute gross_B_to_A   │          │
   │            │  compute net position (both independently)       │          │
   │            │──signed net position ──────────▶               │          │
   │            │◀──net position agreed ──────────│               │          │
   │            │                │                │               │          │
   │            │  DEBIT  fed_payable:op-b         │               │          │
   │            │  CREDIT fed_settlement_clearing  │               │          │
   │            │──bank transfer (net amount)──────────────────────────────▶│
   │            │                │                │               │     ▼   │
   │            │                │                │               │   bank  │
   │            │                │                │               │ transfer│
   │            │                │                │               │    ▼    │
   │            │                │                │◀──bank credit────────────│
   │            │                │                │  DEBIT  fed_settlement_clearing        │
   │            │                │                │  CREDIT fed_receivable:op-a            │
   │            │                │                │               │          │
   │            │  obligations → settled           │               │          │
   │            │                │         obligations → settled  │          │
   │            │  emit federation.settlement.completed            │          │
   │            │                │         emit federation.settlement.completed│          │
   │            │                │                │               │          │
   ▼            ▼                ▼                ▼               ▼          ▼
              [FINALLY COMPLETE — all obligations settled]
```

---

## Diagram 2 — Phase 1: Discovery Flow

Shown independently to clarify the manifest validation decision tree.

```
Consumer     Op-A                              Op-B
   │            │                                │
   │──initiate──▶                               │
   │   payment  │                                │
   │            │ resolve recipient → op-b        │
   │            │──GET /.well-known/banza/operator.json──────────▶
   │            │                                │
   │            │             [manifest response]│
   │            │◀──HTTP 200, manifest JSON───────│
   │            │                                │
   │            │ VALIDATE MANIFEST:             │
   │            │   schema valid?                │
   │            │     NO → fail                  │
   │            │     YES ↓                      │
   │            │   supports_federation == true? │
   │            │     NO → fail (not a federation member)          │
   │            │     YES ↓                      │
   │            │   cross_operator_routing == true?               │
   │            │     NO → fail                  │
   │            │     YES ↓                      │
   │            │   certificate_url present?     │
   │            │     NO → fail                  │
   │            │     YES ↓                      │
   │            │   interop_endpoint present?    │
   │            │     NO → fail                  │
   │            │     YES ↓                      │
   │            │   currency in supported_currencies?             │
   │            │     NO → fail (or try alternate operator)       │
   │            │     YES ↓                      │
   │            │   amount ≤ max_transaction_amount_minor?        │
   │            │     NO → fail (or try alternate operator)       │
   │            │     YES ↓                      │
   │            │   cache manifest (TTL = min(expires_at, now+1h))│
   │            │   → CONTINUE TO TRUST VERIFICATION              │
   │            │                                │
```

---

## Diagram 3 — Phase 2: Trust Verification Flow (9 Steps)

```
Op-A                    BANZA (BRL)              Op-B
   │                        │                       │
   │── STEP 2.1: BRL CHECK ──────────────────────── │
   │                        │                       │
   │ [if cached BRL < 6h: skip fetch]               │
   │──GET /federation/revocation-list.json──▶       │
   │◀──BRL JSON (signed)────│                       │
   │ verify BRL.signature against BANZA_PUBLIC_KEY  │
   │   FAIL → treat BRL as absent; fail-closed      │
   │   PASS ↓                                       │
   │ cache BRL until BRL.expires_at                 │
   │                        │                       │
   │── STEP 2.2: FETCH CERTIFICATE ─────────────────│
   │                        │                       │
   │──GET {certificate_url}─────────────────────────▶
   │◀──certificate JSON─────────────────────────────│
   │ validate schema                                │
   │                        │                       │
   │── STEP 2.3: VERIFY SIGNATURE (INV-TRUST-001) ──│
   │                        │                       │
   │ canonical = sort_keys(cert fields excl. sig)   │
   │ BANZA_PK = BANZA_PUBLIC_KEY[cert.issuer_key_id]│
   │ verified = ed25519_verify(BANZA_PK, canonical, │
   │                     decode(cert.signature))    │
   │   FAIL → ABORT: certificate tampered or forged │
   │   PASS ↓                                       │
   │                        │                       │
   │── STEP 2.4: VERIFY EXPIRY (INV-TRUST-002) ─────│
   │                        │                       │
   │ if cert.expires_at < now(): ABORT: expired     │
   │ if cert.issued_at > now(): ABORT: future-dated │
   │ PASS ↓                                         │
   │                        │                       │
   │── STEP 2.5: VERIFY CERTIFICATION LEVEL ─────── │
   │                        │                       │
   │ if cert.certification_level < 3: ABORT         │
   │ PASS ↓                                         │
   │                        │                       │
   │── STEP 2.6: CHECK BRL (INV-TRUST-003) ─────────│
   │                        │                       │
   │ if cert.operator_id in BRL.revoked: ABORT      │
   │ PASS ↓                                         │
   │                        │                       │
   │── STEP 2.7: VERIFY FEDERATION FLAG ────────────│
   │                        │                       │
   │ if manifest.supports_federation != true: ABORT │
   │ if manifest.cross_operator_routing != true: ABORT│
   │ PASS ↓                                         │
   │                        │                       │
   │── STEP 2.8: VERIFY CERTIFIED CAPABILITIES ─────│
   │                        │                       │
   │ if "cross_operator_routing" not in             │
   │    cert.capabilities: ABORT                    │
   │ PASS ↓                                         │
   │                        │                       │
   │── STEP 2.9: BIND CERT TO MANIFEST ─────────────│
   │                        │                       │
   │ if cert.operator_id != manifest.operator_id:   │
   │   ABORT: cert and manifest mismatch            │
   │ PASS ↓                                         │
   │                        │                       │
   │ → TRUSTED              │                       │
   │ cache trust until min(cert.expires_at,         │
   │                   BRL.expires_at)              │
   │                        │                       │
```

---

## Diagram 4 — Phase 3: Routing Negotiation (Happy Path)

```
Op-A                                              Op-B
   │                                                 │
   │ assign routing_request_id = "rr-<uuid>"         │
   │ propagate trace_id (from originating payment)   │
   │ construct RoutingRequest JSON                   │
   │ sign: Banza-Federation-Signature: t=T,v1=sig   │
   │──POST /federation/route (signed)────────────────▶
   │                                          parse + validate schema
   │                                          check to_operator_id == self
   │                                          ── VERIFY OPERATOR A SIGNATURE ──
   │                                          parse t from signature header
   │                                          if abs(now-t) > 300: reject
   │                                          GET {request.certificate_url} → fetch Op-A cert
   │                                          run trust steps 2.3–2.9 on Op-A cert
   │                                          extract op_a_public_key
   │                                          verify ed25519(sig, op_a_pk, t+"."+body)
   │                                          ── VALIDATE BUSINESS RULES ──
   │                                          resolve recipient_identifier → wallet
   │                                          check wallet status (active)
   │                                          check currency in supported_currencies
   │                                          check amount within limits
   │                                          check idempotency (routing_request_id new)
   │                                          ══ ATOMIC ══════════════════════════
   │                                          DEBIT  federation_receivable:op-a
   │                                          CREDIT payee_wallet
   │                                          assign interop_transfer_id = "itx-<uuid>"
   │                                          record routing_request → accepted
   │                                          emit federation.routing.accepted
   │                                          ═══════════════════════════════════
   │◀──HTTP 200: { status:"accepted",                │
   │    routing_request_id: (echo),                  │
   │    trace_id: (echo),                            │
   │    interop_transfer_id: "itx-<uuid>",           │
   │    accepted_at: "..." }                         │
   │                                                 │
   │ verify trace_id == original trace_id (INV-FED-001)         │
   │ store interop_transfer_id                       │
   │ → PROCEED TO PHASE 4                            │
   │                                                 │
```

---

## Diagram 5 — Phase 3: Routing Negotiation (Rejection Paths)

```
Op-A                                              Op-B
   │                                                 │
   │──POST /federation/route (signed)────────────────▶
   │                                                 │
   │          SCENARIO A: Recipient not found        │
   │                                          resolve recipient_identifier → NOT FOUND
   │◀──HTTP 200: { status:"rejected",                │
   │    rejection_code: "recipient_not_found",       │
   │    rejection_reason: "No wallet matches..." }   │
   │ → DO NOT debit payer; DO NOT record obligation  │
   │ → Notify consumer: payee not found              │
   │                                                 │
   │          SCENARIO B: Operator A not trusted     │
   │                                          GET Op-A certificate
   │                                          trust verification → FAIL (cert expired)
   │◀──HTTP 200: { status:"rejected",                │
   │    rejection_code: "operator_trust_failure" }   │
   │ → Alert operations; own certificate may be expired         │
   │                                                 │
   │          SCENARIO C: Currency not supported     │
   │                                          amount.currency not in supported_currencies
   │◀──HTTP 200: { status:"rejected",                │
   │    rejection_code: "currency_not_supported" }   │
   │ → Try alternate operator that supports currency │
   │                                                 │
   │          SCENARIO D: Idempotent replay          │
   │ (same routing_request_id, same content, retried)│
   │──POST /federation/route (same routing_request_id)──────────▶
   │                                          routing_request_id found in store
   │                                          return ORIGINAL response (accepted or rejected)
   │◀──HTTP 200: (same response as original)         │
   │ → Use this response as if it was the first      │
   │                                                 │
```

---

## Diagram 6 — Phases 4 + 5: Transfer Execution and Obligation Creation

```
Consumer     Op-A                              Op-B         Merchant
   │            │                                │               │
   │            │ [received: status=accepted, interop_transfer_id]│
   │            │                                │               │
   │            │ ══ ATOMIC TRANSACTION ══════════               │
   │            │ DEBIT  payer_wallet             │               │
   │            │ CREDIT federation_payable:op-b  │               │
   │            │ (idempotency_key = routing_request_id)          │
   │            │                                │               │
   │            │ CREATE obligation:             │               │
   │            │   obligation_id = "ob-<uuid>"  │               │
   │            │   from = "operator-a"           │               │
   │            │   to   = "operator-b"           │               │
   │            │   amount = (same as routing_req)│  ← INV-FED-005│
   │            │   routing_request_id = (echo)   │               │
   │            │   interop_transfer_id = (echo)  │               │
   │            │   trace_id = (same)             │  ← INV-FED-001│
   │            │   settlement_state = "pending"  │               │
   │            │   sign: obligor_signature       │               │
   │            │                                │               │
   │            │ payment_state → "provisionally_complete"        │
   │            │ ══ COMMIT ══════════════════════               │
   │            │                                │               │
   │            │ emit federation.payment.initiated (trace_id)    │
   │            │ emit federation.obligation.recorded (obligation_id, trace_id)│
   │◀──confirmed│                                │               │
   │            │                                │               │
   │            │                         [already credited in Phase 3 Step 3.12]
   │            │                                │               │
   │            │                         emit federation.payment.completed (trace_id)│
   │            │                                │───notify payment──▶
   │            │                                │               │
```

---

## Diagram 7 — Phase 6: Netting and Settlement

This diagram shows one bilateral netting cycle for a single counterparty pair (A ↔ B).

```
Op-A                                              Op-B             Bank
   │                  [at netting cutoff time]       │                │
   │                                                 │                │
   │ compute pending A→B obligations for period      │                │
   │ advance all to settlement_state = "in_netting"  │                │
   │──POST /federation/obligations/netting (signed)──▶               │
   │                                          receive A→B obligations │
   │                                          compute pending B→A obligations│
   │                                          advance all to "in_netting"    │
   │◀──B→A obligations (signed)──────────────────────│                │
   │                                                 │                │
   │ gross_A_to_B = sum(A→B obligations)             │                │
   │                                          gross_B_to_A = sum(B→A obligations)│
   │                                                 │                │
   │ net = gross_A_to_B - gross_B_to_A               │                │
   │                                          net = gross_A_to_B - gross_B_to_A│
   │                  (both compute independently)   │                │
   │                                                 │                │
   │ [net > 0: A is net obligor]                     │                │
   │──signed net position assertion─────────────────▶               │
   │                                          compare to own computation│
   │                                          [if mismatch → F-501 disagreement]│
   │◀──net position agreed (signed)──────────────────│                │
   │                                                 │                │
   │ ══ LEDGER: INITIATE SETTLEMENT ══               │                │
   │ DEBIT  federation_payable:op-b      net         │                │
   │ CREDIT federation_settlement_clearing net        │                │
   │ emit federation.settlement.initiated            │                │
   │──bank transfer: net amount to Op-B─────────────────────────────▶│
   │                                                 │ [transfer in progress]│
   ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  [bank settles]│
   │                                                 │◀──credit confirmed──│
   │                                                 │                │
   │                                          DEBIT  federation_settlement_clearing net│
   │                                          CREDIT federation_receivable:op-a  net   │
   │                                                 │                │
   │◀──settlement_batch_id confirmed─────────────────│                │
   │                                                 │                │
   │ ══ MARK OBLIGATIONS SETTLED ══                  │                │
   │ all A→B obligations → settlement_state="settled"│                │
   │ settled_at = now()                              │                │
   │ settlement_batch_id = "stl-..."                 │                │
   │                                          all B→A obligations → "settled"│
   │                                                 │                │
   │ emit federation.settlement.completed            │                │
   │                                          emit federation.settlement.completed│
   │                                                 │                │
   │ DEBIT  federation_settlement_clearing  net      │                │
   │ CREDIT bank_settlement_account         net      │                │
   │                                                 │                │
```

---

## Diagram 8 — Phase 7: Network Failure and Retry (F-101)

```
Consumer     Op-A                              Op-B
   │            │                                │
   │──initiate──▶                               │
   │            │ [discovery + trust: complete]  │
   │            │ routing_request_id = "rr-abc"  │
   │            │──POST /federation/route ───────▶
   │            │                                │
   ·  ·  ·  ·  ·  ·  ·  ·  [timeout: no response within 30s]
   │            │                                │
   │            │ [RETRY 1: wait 2s]             │
   │            │──POST /federation/route (same rr-abc)──────────▶
   │            │                         [Op-B did not receive first request]
   │            │                         process normally
   │            │                         ATOMIC: credit payee, assign itx-xyz
   │            │◀──HTTP 200: status=accepted, itx-xyz──────────│
   │            │                                │
   │            │ ══ ATOMIC: debit + obligation  │
   │            │ ... (normal Phase 4+5)         │
   │◀──confirmed│                                │
   │            │                                │
```

Alternative: Op-B DID process the first request (credit already happened):

```
Op-A                              Op-B
   │                                │
   │ [RETRY 1: wait 2s]             │
   │──POST /federation/route (same rr-abc)──────▶
   │                         routing_request_id "rr-abc" found in store
   │                         return ORIGINAL response (idempotent, INV-FED-004)
   │                         [payee is NOT credited again]
   │◀──HTTP 200: status=accepted, itx-xyz (same as before)──
   │                                │
   │ ══ ATOMIC: debit + obligation  │
   │ ... (normal Phase 4+5)         │
   │                                │
```

Alternative: All 3 retries fail (Op-B offline):

```
Op-A                              Op-B
   │                                │
   │ [RETRY 1: 2s] ─────────────────[no response]
   │ [RETRY 2: 8s] ─────────────────[no response]
   │ [RETRY 3: 32s]─────────────────[no response]
   │                                │
   │ PAYMENT FAILS                  │
   │ → DO NOT debit payer           │
   │ → DO NOT record obligation     │
   │ → payment_state = "failed"     │
   │ → emit payment.failed event    │
   │◀──payment failed notification──│
   │                                │
Consumer
   │◀──"Payment could not be processed"──Op-A
```

---

## Diagram 9 — Phase 8: Revocation Handling

**Scenario A: Operator B revoked before routing attempt**

```
Op-A                   BANZA              Op-B
   │                     │                  │
   │ [BANZA revokes Op-B]│                  │
   │                     │ publish new BRL  │
   │                     │ (with op-b revoked, expires 1h)
   │                     │                  │
   │──GET BRL─────────────▶               │
   │◀──BRL (op-b in revoked list)─────────│
   │                     │                  │
   │ TRUST VERIFICATION: │                  │
   │ Step 2.6: check BRL │                  │
   │ "operator-b" in BRL.revoked → ABORT   │
   │                     │                  │
   │ → routing fails     │                  │
   │ → payer NOT debited │                  │
   │ → no obligation     │                  │
   │                     │                  │
```

**Scenario B: Operator B revoked between trust verification and routing response**

```
Op-A                   BANZA              Op-B
   │                     │                  │
   │ Phase 2: trust verified (Op-B trusted) │
   │──POST /federation/route────────────────▶
   │                     │[BANZA revokes Op-B mid-flight]
   │                     │publish new BRL   │
   │                     │                  │ [Op-B processing...]
   │◀──status: accepted, itx-xyz────────────│
   │                     │                  │
   │ [Op-A refreshes BRL before Phase 4]    │
   │──GET BRL─────────────▶               │
   │◀──BRL (op-b revoked)─│               │
   │                     │                  │
   │ [acceptance is irrevocable: Op-B has credited payee]
   │ → Op-A MUST still complete Phase 4+5  │
   │ → debit payer; record obligation      │
   │ → obligation will be settled via BANZA dispute resolution
   │                     │                  │
```

**Scenario C: Op-A revoked; Op-B receives routing request from Op-A**

```
Op-B                   BANZA              Op-A (revoked)
   │                     │                  │
   │                     │ [BANZA revokes Op-A]
   │                     │ publish new BRL   │
   │                     │                  │
   │◀──POST /federation/route (from Op-A)───│
   │                     │                  │
   │ verify Op-A signature:                 │
   │ GET {request.certificate_url} → fetch Op-A cert
   │ run trust steps 2.3–2.9:              │
   │   Step 2.6: check BRL                 │
   │   "operator-a" in BRL.revoked → FAIL  │
   │                     │                  │
   │──HTTP 200: { status:"rejected",        │
   │    rejection_code:"operator_trust_failure" }────▶
   │                     │                  │
   │ log attempt; report to BANZA          │
   │                     │                  │
```

---

## Diagram 10 — Phase 9: Reconciliation (Discrepancy Detected)

This shows what happens when Operator B accepted a routing request but Operator A has no corresponding obligation (F-402 recovery path).

```
BanzAI       Op-A                              Op-B
   │            │                                │
   │──run reconciliation for period 2026-06-01──▶│
   │──run reconciliation for period 2026-06-01───▶
   │            │                                │
   │            │──export obligations (A→B)──────▶
   │            │◀──accepted routing requests (B received from A)──
   │            │                                │
   │            │ CROSS-REFERENCE by routing_request_id:          │
   │            │                                │
   │            │ rr-abc: B accepted, A has obligation ✓          │
   │            │ rr-def: B accepted, A has no obligation ← DISCREPANCY
   │            │ rr-ghi: B accepted, A has obligation ✓          │
   │            │                                │
   │◀──discrepancy: rr-def (B accepted, A missing obligation)──   │
   │                                             │
   │──INSTRUCT Op-A: create obligation for rr-def▶               │
   │            │                                │
   │            │ [RECOVERY: Phase 4 completion for rr-def]       │
   │            │ DEBIT  payer_wallet (idempotent)│               │
   │            │ CREDIT federation_payable:op-b  │               │
   │            │ CREATE obligation for rr-def   │               │
   │            │                                │
   │◀──reconciliation complete: 1 discrepancy resolved, 0 open──  │
   │                                             │
   │ [if amount mismatch: HALT netting, escalate to BANZA]        │
   │                                             │
```

---

## Diagram 11 — Phase 6 Failure: Netting Disagreement (F-501)

```
Op-A                                              Op-B
   │                                                 │
   │──obligation export (A→B)────────────────────────▶
   │◀──obligation export (B→A)───────────────────────│
   │                                                 │
   │ compute: gross_A_to_B = 1,000,000               │
   │ compute: gross_B_to_A =   400,000               │
   │ compute: net = 600,000 (A owes B)               │
   │                                          compute: gross_A_to_B = 1,000,000
   │                                          compute: gross_B_to_A =   450,000  ← DIFFERENT
   │                                          compute: net = 550,000
   │                                                 │
   │──signed net: 600,000────────────────────────────▶
   │                                          compare: 550,000 ≠ 600,000
   │◀──DISAGREEMENT: B computed 550,000──────────────│
   │                                                 │
   │ HALT SETTLEMENT                                 │
   │                                                 │
   │ EXPORT full obligation list with obligor signatures──────────▶
   │◀──full obligation list (B→A) with signatures────│
   │                                                 │
   │ IDENTIFY DISCREPANCY:                           │
   │   Op-A obligation list does not contain rr-xyz  │
   │   Op-B accepted rr-xyz (B→A) for 50,000        │
   │   → Op-A missing a B→A obligation              │
   │                                                 │
   │ [RESOLUTION: Op-A records missing obligation]   │
   │ re-compute: gross_B_to_A = 450,000             │
   │ net = 550,000 (now matches B)                   │
   │                                                 │
   │──signed net: 550,000 ───────────────────────────▶
   │◀──net position agreed ──────────────────────────│
   │                                                 │
   │ [proceed with settlement]                       │
   │                                                 │
   │ [if discrepancy is unresolvable: escalate to BANZA]          │
   │                                                 │
```
