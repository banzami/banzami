# ADR-025 — Ecosystem Naming Inversion

**Status:** Accepted  
**Date:** 2026-05-29  
**Author:** Organização operador  
**Deciders:** Fidel Monteiro (Founder)  
**Supersedes:** ADR-016 (Arquitectura de Marca the reference operator/Banza)

---

## Context

The legally and commercially approved company name, registered with Guiché Único da Empresa, is **the reference operator**.

The current architecture (ADR-016, accepted 2026-05-19) assigns names in the opposite direction:

- **the reference operator** = protocol / ecosystem / open infrastructure
- **Banza** = product / reference operator / consumer experience
- **BanzAI** = Protocol Operating System

This creates a critical mismatch: the legally approved name ("the reference operator") is used for the invisible infrastructure layer, while the user-facing product ("Banza") carries a name that is not the registered entity. Commercial communications, contracts, and investor materials must reference the legal name — which is the reference operator — yet the product the user actually pays with is called Banza.

Maintaining this inversion would require permanent dual-branding and cause ongoing confusion at every commercial and legal touchpoint.

---

## Decision

**Invert the ecosystem naming:**

| Role | Current Name (ADR-016) | New Name (ADR-025) |
|------|------------------------|---------------------|
| Protocol / ecosystem / open infrastructure | the reference operator | **Banza** |
| Main product / reference operator / commercial payment experience | Banza | **the reference operator** |
| Protocol Operating System | BanzAI | **BanzAI** |

### Banza — Protocol and Ecosystem

**Banza** becomes the name of the open programmable financial infrastructure protocol and ecosystem.

It refers to:
- The open protocol specification (RFCs, ADRs, invariants)
- The kernel codebase (Rust crates, Go services)
- The operator certification framework (L0–L4)
- The SDK ecosystem (TypeScript, Flutter, PHP)
- The open infrastructure available to all operators

### the reference operator — Main Product and Reference Operator

**the reference operator** becomes the name of the first and main product built on Banza — the reference operator and the commercial payment experience used by consumers and merchants.

It refers to:
- The consumer-facing payment application
- The merchant/business dashboard
- QR payments, pay links, checkout experiences
- The wallet product
- Everything the end user interacts with

This name aligns with the legal registration.

### BanzAI — Protocol Operating System

**BanzAI** replaces BanzAI as the Protocol Operating System for the Banza ecosystem.

- Clearer internationally ("AI" suffix is universally understood)
- No longer implies an etymological link to "the reference operator" (the product), which would be confusing after inversion
- Maintains the protocol OS positioning: 16 modules, 8 capabilities, "Tools determine truth. AI explains truth."

### Identity Namespace — `@banza`

The ecosystem identity handle namespace is permanently `@banza`. This is not part of the naming inversion.

Every person, merchant, operator, and entity on the network has a handle in the form `@banza:name`. The namespace belongs to the network identity layer — it is independent of what the protocol, product, or AI OS are called. Users will say "send it to my banza" and "what's your banza?" The namespace must remain stable indefinitely, regardless of future brand changes.

This is a permanent branding and network identity decision. `@banza` is classified as `IDENTITY_NAMESPACE` and is exempt from all migration waves.

---

## Protected Names — DO NOT RENAME

The following names must remain unchanged regardless of this inversion:

| Name | Class | Reason |
|------|-------|--------|
| `@banza` | IDENTITY_NAMESPACE | Network identity handle namespace. Permanent — see Identity Namespace section above. |
| `banza.network` | DOMAIN | Domain is registered and has SEO equity. Renaming requires DNS migration and a transition period. Deferred to a separate decision. |
| `contact@banza.network` | EMAIL | Public email address on all communications. |
| `security@banza.network` | EMAIL | Security disclosure address. |
| GitHub organization `github.com/banza` | REPO | Public repository URLs. Renaming GitHub org breaks all existing clone URLs and links. |

Domain and email exceptions are temporary. A separate ADR will govern domain and email migration. The `@banza` identity namespace exception is permanent.

---

## Migration Principle

> **Break nothing blindly.**

Every occurrence of the reference operator, Banza, and BanzAI across documentation, code, APIs, and public copy must be **classified before renaming**. The semantic meaning of each occurrence determines which name replaces it.

A global search-and-replace is explicitly forbidden. See `docs/migration/DO-NOT-GLOBAL-REPLACE.md`.

A full migration map is maintained at `docs/migration/naming-inversion-map.md`.

Occurrence classification rules are at `docs/migration/naming-classification-rules.md`.

---

## Compatibility Period

During migration, use transitional wording where needed to avoid reader confusion:

| Context | Transitional Form |
|---------|-------------------|
| Protocol references | "Banza Protocol — formerly BANZA Protocol" |
| Product references | "the reference operator — formerly Banza" |
| AI OS references | "BanzAI — formerly BanzAI" |

The compatibility period ends when all public-facing surfaces have been updated and the DNS/GitHub migration decisions are finalized.

---

## Non-Goals (This ADR)

This ADR does not:

- Rename any repository
- Rename any package or crate
- Rename any domain or email address
- Rename any code symbol, environment variable, or database table
- Update any public website copy
- Update README branding
- Change any API route

Those actions are governed by the migration map and will be executed in subsequent steps, each with its own commit/approval cycle.

---

## Rationale

**the reference operator as product:** The legal name must be the user-facing name. When a consumer makes a payment, the name they see, the name on their receipt, and the name in their bank statement should all be the same name the company is registered under. Using Banza for the product and the reference operator for the invisible protocol inverts this natural relationship.

**Banza as protocol:** Shorter, cleaner, better suited for a protocol/infrastructure layer. "Built on Banza" is a stronger developer positioning statement than "Built on the reference operator" when the reference operator is also the name of a competing product built on the same protocol.

**BanzAI over BanzAI:** The suffix "IA" (Inteligência Artificial) is Portuguese-specific and opaque to international audiences. "AI" is universally understood. Removing the etymological link to "the reference operator" also prevents the AI OS from being associated with the product rather than the protocol.

---

## Consequences

**Positive:**
- Legal name alignment: the commercially and legally registered entity matches the user-facing product
- Cleaner developer narrative: "Banza Protocol" as infrastructure, "the reference operator" as product built on it
- International clarity: BanzAI is unambiguous
- Reduces permanent dual-branding overhead

**Negative (managed):**
- Significant migration effort across three repositories, documentation, SVGs, and websites
- Existing documentation, READMEs, and ADRs will be temporarily inconsistent during migration
- SEO impact if/when banza.network transitions to banza.org (deferred decision)

**Neutral:**
- github.com/banza remains unchanged for now
- banza.network remains unchanged for now

---

## Related ADRs

- **ADR-016** (superseded): Arquitectura de Marca the reference operator/Banza — established the now-inverted naming
- **ADR-018**: Open Financial Kernel — protocol/ecosystem architecture (content unchanged, naming will update)
- **ADR-019**: Operator Separation — reference operator architecture (content unchanged, naming will update)
- **ADR-024**: Reference Operator — Banza/the reference operator relationship (content unchanged, naming will update)
