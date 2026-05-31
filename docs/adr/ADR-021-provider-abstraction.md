# ADR-021 — Provider Abstraction Model

**Status:** Accepted  
**Date:** 2026-05-28  
**Author:** the reference operator Organisation  
**Deciders:** Fidel Monteiro (Founder)  
**Supersedes:** None  
**See also:** ADR-019

---

## Context

The Banza kernel must integrate with external systems: payment rails, notification services, risk engines, identity providers, routing databases. These integrations are operator-specific — each operator uses different services and has different credentials.

The original architecture coupled provider implementations directly into the kernel crates (e.g., `EMISProvider`, `SimulatedProvider` as enum variants). This created:

- Private provider code mixed with public kernel code
- Impossible to extract kernel without extracting operator business logic
- Contributors cannot run the system without private credentials
- No way to swap providers without modifying kernel code

## Decision

Every external integration point is expressed as a **Rust trait** in the kernel. Operators implement these traits for their specific providers. The kernel engine is generic over the provider trait.

The canonical pattern:

```rust
// In banza-acquiring (kernel):
pub trait AcquirerProvider: Send + Sync {
    fn provider_name(&self) -> &'static str;
    async fn initiate_payment(&self, req: InitiatePaymentRequest) 
        -> Result<ExternalPaymentRef, AcquirerError>;
    async fn validate_callback(&self, raw_body: &[u8], signature: &str)
        -> Result<PaymentConfirmation, AcquirerError>;
}

// In banza-acquiring (kernel):
pub struct PostgresAcquiringEngine<P: AcquirerProvider> {
    provider: P,
    repo: PostgresAcquiringRepository,
}

// In operator (private):
impl AcquirerProvider for EMISProvider { ... }
impl AcquirerProvider for SimulatedProvider { ... }
```

### Provider trait inventory

| Trait | Crate | Purpose |
|---|---|---|
| `AcquirerProvider` | `banza-acquiring` | Payment rail integration |
| `RoutingProvider` | `banza-routing` | Payment rail selection |
| `NotificationProvider` | *(reference/local-notifications)* | Push/event delivery |
| `RiskProvider` | `banza-risk` | Transaction risk assessment |
| `SettlementProvider` | `banza-settlement` | Settlement execution |

### Reference implementations

For each provider trait, the `reference/sandbox-operator/` provides a simulated implementation that:
- Works without external infrastructure
- Generates deterministic responses
- Is suitable for local development and testing
- Is clearly labelled as non-production

## Consequences

**Positive:**
- Kernel crates compile with zero knowledge of any specific provider
- Operators can swap providers without modifying kernel code
- Reference implementations allow contributors to run the system locally
- Provider implementations can be tested independently

**Negative:**
- More upfront design work to define stable trait interfaces
- Generic engines (`PostgresAcquiringEngine<P>`) have more complex type signatures
- Trait objects require `dyn` or monomorphization decision per use case

## Alternatives considered

**Enum dispatch (EMISProvider | SimulatedProvider):** Rejected. Encodes specific providers in the kernel; cannot be extended without modifying the kernel.

**Configuration-based provider selection (strings):** Rejected for type safety. String dispatch loses compile-time verification.

**Dynamic trait objects everywhere (`Box<dyn AcquirerProvider>`):** Evaluated. Acceptable for some use cases (API servers); monomorphization preferred for performance-critical paths.
