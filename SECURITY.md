# Security Policy

## Reporting a vulnerability

If you discover a security vulnerability in Banzami, please report it responsibly.

**Do NOT open a public GitHub issue for security vulnerabilities.**

Instead, email: **security@banzami.org**

Include:
- A description of the vulnerability
- Steps to reproduce
- Potential impact assessment
- Any suggested fix (optional)

We will acknowledge your report within 48 hours and provide a timeline for a fix.

---

## Scope

This security policy covers:

- `core/` — Rust financial core crates (ledger, wallets, transactions, acquiring, etc.)
- `sdk/` — all official Banzami SDKs
- `contracts/` — protocol specifications and schemas
- `integrations/` — official integration plugins

## Out of scope

- The Banza commercial product (separate private repository)
- Third-party implementations built on Banzami
- Infrastructure or deployment issues (report to Banzami directly at security@banzami.org)

---

## Financial invariant vulnerabilities

Security issues in the financial core are our highest-priority category. This includes:

- Any code path that allows a ledger posting to be non-zero-sum
- Any code path that allows a wallet balance to go negative
- Any bypass of HMAC signature validation in the acquiring callback path
- Any way to credit a wallet without a corresponding debit
- Any way to process a duplicate callback as a unique event
- Any way to break idempotency guarantees

If you discover any of these, treat them as critical security issues and report via email, not a public issue.

---

## Forbidden disclosures

When interacting with this repository (issues, PRs, discussions), do not post:

- Private API keys or secrets
- Production database credentials
- Firebase or cloud service credentials
- Server IP addresses or private infrastructure details
- Operator-specific configurations that could reveal production system topology

---

## Webhook signature security

The `contracts/sdk-certification/` suite includes webhook signature vectors. If you discover that a Banzami SDK fails to correctly validate HMAC-SHA256 signatures:

1. Report it via email to security@banzami.org
2. Do not publish a proof-of-concept that could be used to forge legitimate webhooks
3. We will coordinate a fix and notify all known SDK implementors

---

## Security review for core financial logic

All pull requests that touch the following require explicit security review:

- `banzami-ledger/src/` — zero-sum enforcement
- `banzami-wallets/src/` — balance arithmetic and non-negative enforcement
- `banzami-acquiring/src/` — signature validation and callback processing
- `banzami-transactions/src/` — FSM transitions and atomicity

---

## Responsible disclosure

We follow a 90-day responsible disclosure timeline. We ask that you:

1. Give us reasonable time to fix the issue before public disclosure
2. Do not access, modify, or delete data belonging to others
3. Do not perform denial-of-service attacks

We will credit security researchers who responsibly disclose issues (unless you prefer to remain anonymous).
