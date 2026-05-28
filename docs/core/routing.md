# banzami-routing — Payment Rail Routing

The routing crate selects which payment rail to use for a given payment, based on operator-defined rules.

---

## What it is

`banzami-routing` provides a simple, configurable rule engine that maps (currency, amount, metadata) to a payment rail. Operators define their routing rules; the engine evaluates them.

There are no hardcoded rails, no hardcoded currencies, no geographic assumptions in the core crate.

---

## Routing rules

A routing rule maps a condition to a payment rail:

```rust
pub struct RoutingRule {
    pub currency: Currency,
    pub rail:     PaymentRail,
    pub priority: u32,
}
```

Rules are evaluated in descending priority order. The first matching rule wins.

---

## PaymentRail

`PaymentRail` is a string-based identifier:

```rust
pub struct PaymentRail(String);

impl PaymentRail {
    pub fn new(name: impl Into<String>) -> Self { ... }
    pub fn as_str(&self) -> &str { ... }
}
```

Operators define their own rail names. Example values: `"MULTICAIXA_EXPRESS"`, `"SEPA_CREDIT"`, `"ACH"`, `"SIMULATED"`. The engine does not interpret the value — it only selects it and passes it to downstream components.

---

## Operator configuration

Operators create their routing engine with their own rules:

```rust
let engine = StaticRoutingEngine::new(vec![
    RoutingRule {
        currency: Currency::AOA,
        rail:     PaymentRail::new("MULTICAIXA_EXPRESS"),
        priority: 100,
    },
    RoutingRule {
        currency: Currency::USD,
        rail:     PaymentRail::new("ACH"),
        priority: 100,
    },
]);
```

The `with_example_rules()` constructor provides an illustrative multi-currency example. **Do not use it in production** — define your own rules matching the rails you have access to.

---

## No implicit fallback

If no rule matches a payment, the engine returns an error. It does not silently route to a default provider. This is intentional: silent fallback would hide misconfiguration. Operators must ensure their rule set covers all currencies they accept.

---

## Environment isolation

The routing engine itself is environment-agnostic. Environment isolation (sandbox vs production) is the operator's responsibility at the provider level, not the routing level. Operators should use separate routing configurations per environment if needed.

---

## Invariants

- No hardcoded rails or currencies (fully operator-defined)
- No implicit fallback — missing match is an error
- Rules are pure and deterministic — same input always produces same output
