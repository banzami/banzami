# BANZA ALLOWED OPERATOR REFERENCES

**Audit ID:** BANZA-BANZAMI-CONTAMINATION-AUDIT-001  
**Date:** 2026-05-31

This document lists every Banzami reference in the BANZA repo that is **correct and should be preserved**. It exists to prevent over-eager cleanup from removing legitimate operator citations.

---

## Rule for allowed references

A Banzami reference is **allowed** in the BANZA repo if it:
1. Cites Banzami as a reference operator, example operator, or commercial implementation
2. Explains the relationship between BANZA (protocol) and Banzami (operator)
3. Provides contact details for the current reference operator (emails, domains) — explicitly deferred per ADR-025
4. Documents historical decisions that involved Banzami by name (ADRs, audit reports)
5. Is a crate name explicitly protected by `CLAUDE_BASE.md`

A Banzami reference is **NOT allowed** if it:
- Makes Banzami the governance authority, owner, or canonical source of the protocol
- Embeds Banzami's domain/namespace into an active protocol API URL
- Attributes the kernel or protocol to Banzami Engineering
- Directs operators to Banzami's repo as the source of the BANZA kernel

---

## Canonical governance statements (preserve verbatim)

| File | Content | Reason allowed |
|---|---|---|
| `BANZA_GOVERNANCE.md:9-17` | "Banzami is an independent commercial company. It is not the protocol's governing body…" | Defines the separation — must stay |
| `BANZA_GOVERNANCE.md:156-166` | "Banzami — one operator among many" | Correct architectural framing |
| `BANZA_MANIFESTO.md:75-83` | "O que acontece se o Banzami desaparecer?" | Protocol independence test case — essential to the manifesto |
| `BANZA_MANIFESTO.md:156` | "BANZA é o protocolo. Banzami é como Angola paga." | Canonical tagline — correct |
| `BANZA_REFERENCE.md:174` | "O Banzami é um operador — o primeiro e a implementação de referência. Não é o protocolo." | Definitive statement |
| `docs/governance/CLAUDE_BASE.md:41-48` | Forbidden assumption table | Classification rules for future use |
| `CLAUDE.md:22,25,51,55,127,135` | Correct framing of BANZA vs Banzami boundary | Operating instructions for this repo |

---

## Reference operator citations (preserve)

These cite Banzami as the reference operator, which is factually correct.

| File | Line(s) | Content |
|---|---|---|
| `README.md:5` | "Banzami = reference operator (independent commercial startup)" | Correct |
| `README.md:471` | "Banzami — reference operator implementation" | Correct |
| `BANZA_ARCHITECTURE.md:103` | "O Banzami implementa estes providers — como qualquer outro operador certificado" | Correct framing |
| `BANZA_ARCHITECTURE.md:232-234` | "O Banzami é a implementação de referência… Estas são responsabilidades separadas" | Correct |
| `BANZA_CERTIFICATION.md:163` | "Use the Banzami reference operator as your reference" | Accurate instruction |
| `BANZA_CONFORMANCE.md:34` | "The reference sandbox operator (Banzami) is certified at Level 2" | Accurate |
| `BANZA_REFERENCE.md:255` | "O Banzami é a implementação de referência do protocolo completo" | Correct |

---

## Contact details and infrastructure (protected per ADR-025)

Per `docs/governance/CLAUDE_BASE.md:87-90`, these are explicitly marked as deferred — do not rename.

| Reference | ADR-025 status |
|---|---|
| `security@banzami.com` | Protected — deferred |
| `conduct@banzami.com` | Protected — deferred |
| `contact@banzami.com` | Protected — deferred |
| `banzami.com` (domain) | Protected — deferred |
| `github.com/banzami` | Protected — deferred (90-day namespace lock) |
| `banzami.com/banzai` (BanzAI access URL) | Protected — BanzAI is deployed by Banzami |

---

## Rust crate names (protected per CLAUDE_BASE.md)

Per `docs/governance/CLAUDE_BASE.md:90`: "Rust crate names `banzami-types`, `banzami-ledger`, etc. — explicitly out of scope."

All 19 `banzami-*` crates are protected from renaming until a coordinated migration plan is executed. References to them by current name are correct in the current codebase context.

---

## Banzami product URLs and domains in operator-facing examples

URLs like `https://api.banzami.com`, `https://pay.banzami.com`, `https://sandbox-api.banzami.com` appear in:
- `sdk/typescript/src/client.ts:32-33` (default API base URLs)
- `sdk/php/src/BanzamiClient.php:24-25`
- `sdk/checkout-web/README.md`
- `integrations/plugins/generic-node/` examples
- `integrations/plugins/generic-php/README.md`

**Status:** These are valid operator endpoint URLs. Banzami is the reference operator that deploys these endpoints. Operators who use the BANZA SDK against Banzami's deployment will use these URLs. They are NOT protocol-level URLs — they are operator-level infrastructure. They are allowed.

---

## QR payload prefixes `BANZAMI:` and `BANZAMI-SBX:`

Occurrences in `contracts/qr/`, `conformance/`, `BANZA_CONFORMANCE.md`, `.github/workflows/conformance.yml`.

**Status:** These are active protocol constants. The prefix `BANZAMI:` was defined when the protocol and operator shared a name. This is STRUCTURAL_DEBT (not critical contamination). The fact that these are protocol constants makes them harder to change than docs. A prefix change requires an ADR, a conformance migration period, and coordination with all operators. Until an ADR approves the rename to `BANZA:` and `BANZA-SBX:`, these are allowed by necessity.

---

## `docs/BANZAMI_REFERENCE.md` — NOT allowed (see A-005)

Despite being a document, `docs/BANZAMI_REFERENCE.md` is classified as CRITICAL_CONTAMINATION (A-005), not a valid reference. It describes Banzami's commercial product in detail and belongs in `~/banzami/docs/`, not in the BANZA protocol repo.
