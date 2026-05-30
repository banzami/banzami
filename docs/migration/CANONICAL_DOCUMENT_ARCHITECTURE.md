---
name: canonical-document-architecture
description: Target canonical document structure for all three ecosystem repositories — produced by ECOSYSTEM-CANONICAL-DOCUMENT-ARCHITECTURE-001
metadata:
  type: project
---

# Canonical Document Architecture

**Mission:** ECOSYSTEM-CANONICAL-DOCUMENT-ARCHITECTURE-001  
**Date:** 2026-05-30  
**Status:** Authoritative

---

## Principle

Every document at the root of a repository must carry the explicit identity of its owner in its filename.

A developer who runs `ls` in any repository must immediately understand:
- **What** the document covers
- **Whose** domain it belongs to

No document title may create ambiguity. The file tree itself is architectural documentation.

---

## ~/banza — Protocol Repository

### Target Root Structure

```
~/banza
├── BANZA_REFERENCE.md          ← Canonical protocol reference (all rules, invariants, governance, certification, federation)
├── BANZA_MANIFESTO.md          ← Protocol founding philosophy and vision
├── BANZA_ARCHITECTURE.md       ← Protocol system architecture (promoted from docs/architecture/)
├── BANZA_GOVERNANCE.md         ← Protocol governance model (renamed from GOVERNANCE.md)
├── BANZA_CERTIFICATION.md      ← Certification levels L0–L4 (promoted from banzami/docs/certification.md)
├── BANZA_CONFORMANCE.md        ← Conformance suite and test vectors (promoted from docs/conformance.md)
├── BANZA_SECURITY.md           ← Protocol security policy (renamed from SECURITY.md)
├── BANZA_ROADMAP.md            ← Protocol roadmap (extracted from BANZA_REFERENCE.md §11)
├── CONTRIBUTING.md             ← How to contribute (GitHub-standard, kept)
├── CODE_OF_CONDUCT.md          ← Community conduct (GitHub-standard, kept)
├── LICENSE                     ← Apache 2.0 (legal-standard, kept)
├── README.md                   ← Repository entry point (GitHub-standard, kept)
├── CLAUDE.md                   ← Engineering constitution (project-specific, kept)
├── .gitignore
├── contracts/
├── conformance/
├── core/
├── docs/
├── infra/
├── reference/
├── sdk/
└── tools/
```

### BANZA Document Responsibilities

| Document | Answers | Must NOT contain |
|----------|---------|-----------------|
| `BANZA_REFERENCE.md` | What is the BANZA protocol? All rules, invariants, governance, certification, federation | Any Banzami product description, BanzAI features |
| `BANZA_MANIFESTO.md` | Why does BANZA exist? What problem does it solve? | Implementation details, product descriptions |
| `BANZA_ARCHITECTURE.md` | How is the BANZA protocol system structured? | Banzami-specific deployment topology |
| `BANZA_GOVERNANCE.md` | How are protocol decisions made? | Operator-specific governance |
| `BANZA_CERTIFICATION.md` | How does an operator achieve certification? L0–L4 requirements | Banzami-specific implementation |
| `BANZA_CONFORMANCE.md` | How does the conformance suite work? | Operator deployment details |
| `BANZA_SECURITY.md` | What is the protocol security policy? | Banzami product security |
| `BANZA_ROADMAP.md` | What is the protocol roadmap? | Banzami product roadmap |

---

## ~/banzai — Protocol OS Repository

### Target Root Structure

```
~/banzai
├── BANZAI_REFERENCE.md         ← Canonical Protocol OS reference (all capabilities, modules, truth model)
├── BANZAI_ARCHITECTURE.md      ← Protocol OS system architecture (extracted from BANZAI_REFERENCE.md §4)
├── BANZAI_CAPABILITIES.md      ← Six capabilities + 16 modules (extracted from BANZAI_REFERENCE.md §5–6)
├── BANZAI_GOVERNANCE.md        ← Protocol OS governance (renamed from GOVERNANCE.md)
├── BANZAI_SECURITY.md          ← Protocol OS security policy (renamed from SECURITY.md)
├── BANZAI_ROADMAP.md           ← Protocol OS roadmap (extracted from BANZAI_REFERENCE.md §11)
├── CONTRIBUTING.md             ← How to contribute (GitHub-standard, kept)
├── CODE_OF_CONDUCT.md          ← Community conduct (GitHub-standard, kept)
├── LICENSE                     ← Apache 2.0 (legal-standard, kept)
├── README.md                   ← Repository entry point (GitHub-standard, kept)
├── CLAUDE.md                   ← Engineering constitution (project-specific, kept)
├── .gitignore
├── apps/
├── contexts/
├── core/
├── docker/
├── docs/
├── infra/
├── node_modules/
├── prompts/
├── tsconfig.base.json
└── turbo.json
```

### BANZAI Document Responsibilities

| Document | Answers | Must NOT contain |
|----------|---------|-----------------|
| `BANZAI_REFERENCE.md` | What is BanzAI? All capabilities, truth model, security posture | Protocol rule definitions, Banzami product descriptions |
| `BANZAI_ARCHITECTURE.md` | How is BanzAI built? Stack, RAG, Protocol Graph, model routing | Protocol governance, operator deployment |
| `BANZAI_CAPABILITIES.md` | What can BanzAI do? Six capabilities, 16 modules | How to operate Banzami, protocol invariants |
| `BANZAI_GOVERNANCE.md` | How are BanzAI decisions made? Deterministic-first rule | Protocol ADR process |
| `BANZAI_SECURITY.md` | What is BanzAI's security posture? Read-only, citation-first | Banzami financial security |
| `BANZAI_ROADMAP.md` | What is BanzAI's roadmap? | Protocol roadmap, Banzami product roadmap |

---

## ~/banzami — Reference Operator Repository

### Target Root Structure

```
~/banzami
├── BANZAMI_REFERENCE.md        ← Canonical operator reference (wallets, merchant products, SDKs, architecture)
├── BANZAMI_ARCHITECTURE.md     ← Technical architecture of the reference implementation
├── BANZAMI_PRODUCTS.md         ← Product descriptions (Wallet, Business, QR, Checkout, Pay Links)
├── BANZAMI_GOVERNANCE.md       ← Operator governance (renamed from GOVERNANCE.md)
├── BANZAMI_OPERATIONS.md       ← Operational guide (services, monitoring, runbooks)
├── BANZAMI_DEPLOYMENT.md       ← Deployment guide (deploy.sh, services, environments)
├── BANZAMI_SECURITY.md         ← Operator security policy (renamed from SECURITY.md)
├── BANZAMI_ROADMAP.md          ← Operator product roadmap
├── CONTRIBUTING.md             ← How to contribute (GitHub-standard, kept)
├── CODE_OF_CONDUCT.md          ← Community conduct (GitHub-standard, kept)
├── LICENSE                     ← Apache 2.0 (legal-standard, kept)
├── README.md                   ← Repository entry point (GitHub-standard, kept)
├── CLAUDE.md                   ← Engineering constitution (project-specific, kept)
├── Makefile                    ← Build system (kept)
├── deploy.sh                   ← Deployment script (kept)
├── dev.sh                      ← Development script (kept)
├── .gitignore
├── apps/
├── core/
├── docs/
├── infra/
├── sdk/
├── services/
└── tools/
```

### BANZAMI Document Responsibilities

| Document | Answers | Must NOT contain |
|----------|---------|-----------------|
| `BANZAMI_REFERENCE.md` | What is Banzami? All products, architecture, SDKs, mission | Protocol governance, BanzAI capabilities |
| `BANZAMI_ARCHITECTURE.md` | How is Banzami built technically? Service topology, language boundaries | Protocol rule definitions |
| `BANZAMI_PRODUCTS.md` | What products does Banzami offer? Wallet, Business, QR, Checkout, Pay Links | How to implement the protocol |
| `BANZAMI_GOVERNANCE.md` | How are operator decisions made? Deployment governance, API versioning | Protocol ADR process |
| `BANZAMI_OPERATIONS.md` | How does the operator run? Services, monitoring, runbooks | Protocol governance |
| `BANZAMI_DEPLOYMENT.md` | How is the operator deployed? deploy.sh, services, environments | Protocol certification |
| `BANZAMI_SECURITY.md` | What is the operator's security policy? Payment flows, wallets, APIs | Protocol security |
| `BANZAMI_ROADMAP.md` | What is the operator's product roadmap? | Protocol roadmap |

---

## The 30-Second Test

Opening **any** of the three repositories, a new contributor must be able to answer:

```
~/banza  → BANZA = open financial infrastructure protocol
~/banzai → BanzAI = Protocol Operating System  
~/banzami → Banzami = reference operator implementation
```

**Without opening any file.**

The file tree achieves this when every document at the root:
1. Is prefixed with the owning entity's canonical name
2. Contains no content that belongs to another entity
3. Cross-references rather than duplicates content from other entities

---

## Document Identity Test

For any document `X_Y.md`, the identity test is:

```
1. Does the filename prefix (X) match the owning entity?
   - BANZA_ → protocol rules, invariants, governance, certification, federation
   - BANZAI_ → Protocol OS capabilities, architecture, cognitive layer
   - BANZAMI_ → operator products, deployment, operations

2. If entity X disappeared, would document Y still be relevant to the ecosystem?
   - YES → document may belong to a higher-level entity
   - NO → document belongs to X
```

---

*Produced by: ECOSYSTEM-CANONICAL-DOCUMENT-ARCHITECTURE-001*
