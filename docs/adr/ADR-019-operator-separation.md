# ADR-019 — Kernel/Operator Separation

**Status:** Accepted  
**Date:** 2026-05-28  
**Author:** the reference operator Organisation  
**Deciders:** Fidel Monteiro (Founder)  
**Supersedes:** None  
**See also:** ADR-018, ADR-021

---

## Context

After the kernel extraction (ADR-018), the boundary between "kernel responsibility" and "operator responsibility" must be made explicit and durable. Without a formal boundary, operators would inevitably depend on undocumented kernel internals, and the kernel would accumulate operator-specific assumptions.

The risk is subtle coupling: a kernel function that hardcodes a country-specific behaviour, an engine that assumes a specific provider, or a configuration value that only makes sense for one operator.

## Decision

The kernel/operator split is governed by one rule:

> **The kernel defines interfaces and invariants. Operators implement providers.**

Concretely:

| Kernel responsibility | Operator responsibility |
|---|---|
| `AcquirerProvider` trait | `EMISProvider`, `MulticaixaProvider` |
| `RoutingEngine` + `RoutingRule` struct | Operator-specific routing table |
| `NotificationProvider` trait | Firebase FCM implementation |
| `RiskProvider` trait | Operator risk scoring heuristics |
| Ledger zero-sum invariant | Bank integration |
| Transaction state machine | Compliance rules |
| QR payload format | Custom QR branding |

**Forbidden in the kernel:**
- Hardcoded provider names (EMIS, Multicaixa, specific banks)
- Country-specific or currency-specific behaviour
- Any code that imports operator-specific types
- Business rules that differ by operator

**Required in the kernel:**
- Every operator integration point is expressed as a trait
- Traits are documented with invariants the operator must uphold
- Reference implementations exist in `reference/sandbox-operator/`

## Consequences

**Positive:**
- Multiple operators can build on the same kernel without forking
- Kernel evolves independently of operator business logic
- Contributors can understand the kernel without understanding any operator
- Operator migrations (e.g., changing payment rails) don't require kernel changes

**Negative:**
- More interface design discipline required upfront
- Some features that "just work" for the reference operator must be expressed as provider traits
- Reference implementations add maintenance overhead

## Alternatives considered

**Monolithic codebase with feature flags:** Rejected. Feature flags encode operator-specific decisions in the kernel and grow unbounded.

**One kernel per operator (forks):** Rejected. Defeats the purpose of an open kernel; diverges immediately.

**Configuration files for operator behaviour:** Rejected for business logic. Config files can express values (TTLs, limits) but not behaviour (routing strategy, risk logic).
