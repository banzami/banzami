---
title: NARRATIVE_ALIGNMENT_SCORECARD
version: 1.0
date: 2026-05-30
status: AUDIT COMPLETE — no files modified
---

# Narrative Alignment Scorecard

**Scoring dimensions:**

| Dimension | Definition |
|---|---|
| **Identity Alignment** | Does the surface correctly identify BANZA as protocol, BanzAI as Protocol OS, Banzami as operator? |
| **Narrative Alignment** | Does the surface inherit from §§1–3? Does the structural argument (gap → model → solution) appear? |
| **Differentiation** | Does the surface distinguish BANZA from products, APIs, gateways, and closed operators? |
| **Protocol Focus** | Is the protocol layer the primary frame, not the product or the operator? |
| **BanzAI Positioning** | Is BanzAI positioned as Protocol OS, not as chatbot or Banzami product? |

**Score: 0–100 per dimension. Overall: mean of five dimensions.**

---

## Scorecard

### Homepage (`/`)

| Dimension | Score | Rationale |
|---|---|---|
| Identity Alignment | 72 | Hero and metadata name protocol correctly. Tagline renders BANZA/BanzAI/Banzami hierarchy. "Banzami SDK oficial" in developers section re-introduces operator-first frame. |
| Narrative Alignment | 38 | Problem section lists symptoms without naming structural cause. No §2 argument (why existing solutions don't work, what protocol vs. product means). No survivability argument. Five problems not identified as five symptoms of one cause. |
| Differentiation | 35 | No protocol/product distinction on the page. "Como funciona" leads with features (ledger, liquidação) — correct facts, wrong order. BANZA is never contrasted with closed-model alternatives. |
| Protocol Focus | 55 | Hero names the protocol correctly. But sections beneath the hero revert to product/feature framing (wallet-native philosophy, QR commerce, mobile experience). |
| BanzAI Positioning | 68 | BanzAI present as "sistema operativo nativo do protocolo" in metadata. Hero widget exists. But no prose explains why Protocol OS exists before the widget appears. |
| **Overall** | **54** | Strong identity signals in chrome (title, tagline, hero) but the body of the page reads as product marketing rather than protocol architecture. |

---

### Operators Page (`/operators`)

| Dimension | Score | Rationale |
|---|---|---|
| Identity Alignment | 60 | Correctly refers to "operadores que implementam o protocolo Banza." Does not claim Banzami owns the protocol. |
| Narrative Alignment | 12 | Jumps directly to the registry. No §2 argument (why the open model matters), no §3 argument (what certification means and why it's open). The WHY question is entirely absent. |
| Differentiation | 15 | No contrast between open certification and bilateral agreements. A reader who has never heard of M-Pesa vs. Pix distinction cannot understand why becoming a certified BANZA operator is structurally different from integrating a proprietary API. |
| Protocol Focus | 45 | Lists operators as an administrative fact. Treats certification as a status label, not as an architectural property of the open model. |
| BanzAI Positioning | 0 | BanzAI is not mentioned on the operators page. A certified operator would benefit from BanzAI for certification guidance — this connection is missing. |
| **Overall** | **26** | The weakest surface. A visitor who comes here to understand whether to become a certified operator leaves without an answer to the question they came with. |

---

### Reference Landing (`/reference`)

| Dimension | Score | Rationale |
|---|---|---|
| Identity Alignment | 95 | Tagline now correctly states "BANZA é o protocolo. BanzAI é o Sistema Operativo. Banzami é a implementação de referência." Metadata is correct. |
| Narrative Alignment | 90 | §§1–3 render in full — the structural argument is present, hardened, and correct. The canonical narrative is here. |
| Differentiation | 88 | §2 contains the M-Pesa/Pix contrast explicitly. §3 has the "O que o BANZA não é" table. |
| Protocol Focus | 92 | The reference document is the protocol reference. §§1–3 establish the protocol layer first. |
| BanzAI Positioning | 85 | §11 renders correctly in the full reference. The six capabilities are enumerated. |
| **Overall** | **90** | The reference page is the best-scoring surface — it directly renders the canonical source. Its only weaknesses are stale filename attribution and missing section intro for first-time visitors. |

---

### Dynamic Section Pages (`/[section]`)

| Dimension | Score | Rationale |
|---|---|---|
| Identity Alignment | 80 | Section content is canonical — inherited from BANZA_REFERENCE.md. Section titles and numbers are correct. |
| Narrative Alignment | 75 | Content is canonical. But six section-to-visual component mappings are wrong after the §§1–3 integration — wrong diagrams appear in wrong sections. |
| Differentiation | 78 | Inherited from canonical content. |
| Protocol Focus | 80 | Inherited from canonical content. |
| BanzAI Positioning | 70 | §11 section renders BanzAI content correctly. But the section visual for BanzAI (§11) has no visual component assigned. |
| **Overall** | **77** | Good overall because content is canonical. Dropped by the integration bugs in visual assignments. |

---

### BanzAI Live Interface (`/banzamia`)

| Dimension | Score | Rationale |
|---|---|---|
| Identity Alignment | 85 | Title and description are correct — "Protocol Operating System". |
| Narrative Alignment | 20 | No pre-interface narrative. A visitor lands and immediately sees a 16-module interface with no explanation of why it exists in relation to the BANZA protocol. |
| Differentiation | 25 | No text distinguishes BanzAI from a consumer chatbot before the interface loads. The canonical distinction — "not a chatbot, it's the Protocol OS" — is absent from the page itself. |
| Protocol Focus | 30 | The interface is technically about the protocol, but the page communicates nothing about protocol focus before the visitor must discover it through the interface. |
| BanzAI Positioning | 55 | Title is correct. But the page relies entirely on the interface itself to communicate BanzAI's identity — which is backwards. Identity should precede the interface. |
| **Overall** | **43** | Strong identity in metadata but near-zero narrative on the page. A visitor who lands here from a search engine has no context before the interface loads. |

---

### About BanzAI (`/sobre-banzamia`)

| Dimension | Score | Rationale |
|---|---|---|
| Identity Alignment | 45 | Title says "Sobre o BanzAI" — correct. But page renders §9 (Modelo de Certificação) due to integration bug. A visitor reads about certification, not BanzAI. |
| Narrative Alignment | 30 | Protocol OS context paragraph is strong. But the rendered section is wrong — the narrative content of §11 (BanzAI) is not being shown. |
| Differentiation | 35 | Protocol OS intro paragraph differentiates correctly. But the wrong section renders below it. |
| Protocol Focus | 40 | The intro paragraph is protocol-focused. The rendered content (§9 — certification model) is also protocol-focused but wrong context. |
| BanzAI Positioning | 30 | The intro paragraph positions BanzAI correctly. Everything below it is about certification, not BanzAI. |
| **Overall** | **36** | The integration bug dominates. This page is functionally broken — it shows certification content to visitors who came to learn about BanzAI. Fix required before narrative scoring is meaningful. |

---

### Roadmap (`/roadmap`)

| Dimension | Score | Rationale |
|---|---|---|
| Identity Alignment | 72 | "Protocol Operating System" badge is present. BanzAI correctly positioned as the Protocol OS. |
| Narrative Alignment | 22 | No §§1–3 narrative. Roadmap lists BanzAI features but never answers "what future does BANZA create?" — the protocol vision is absent. |
| Differentiation | 30 | No contrast between a protocol roadmap and a product roadmap. No federation milestone, no multi-operator milestone, no certification ecosystem milestone. |
| Protocol Focus | 28 | All 28 roadmap items are BanzAI tool capabilities. BANZA protocol milestones (RFC implementations, federation deployment, certification of additional operators) are absent. |
| BanzAI Positioning | 78 | BanzAI correctly framed as Protocol OS. The roadmap items accurately reflect BanzAI capabilities. |
| **Overall** | **46** | Strong on BanzAI identity, weak on BANZA protocol vision. A visitor who reads this roadmap knows what BanzAI will do, but not what BANZA will become. |

---

### Validation (`/validacao`)

| Dimension | Score | Rationale |
|---|---|---|
| Identity Alignment | 78 | "Protocolo Banza" correctly named in H1. Governance framing is correct. |
| Narrative Alignment | 42 | No §§1–3 narrative. No explanation of why an open protocol requires public validation. Technically correct but narratively sparse. |
| Differentiation | 55 | The validation system itself implies open protocol governance — but this is never stated. |
| Protocol Focus | 70 | Implementation matrix is organised by protocol features. |
| BanzAI Positioning | 20 | BanzAI is not mentioned. A user who wants to use BanzAI for certification guidance has no pointer from this page. |
| **Overall** | **53** | Technically solid, narratively thin. The validation system is one of the strongest protocol differentiation arguments (verifiable invariants, not contractual promises) but the page does not make this argument. |

---

### Footer

| Dimension | Score | Rationale |
|---|---|---|
| Identity Alignment | 82 | "Protocolo Aberto de Infraestrutura Financeira para Angola" — protocol-first. |
| Narrative Alignment | 40 | Footer links cover the ecosystem but provide no context. |
| Differentiation | 35 | No protocol differentiation in footer text. |
| Protocol Focus | 70 | Protocol framing in the tagline. |
| BanzAI Positioning | 55 | BanzAI link present in footer but listed without description. |
| **Overall** | **56** | Acceptable for a footer — identity is correct, narrative depth is appropriately limited. |

---

### Global Metadata / OG / SEO

| Dimension | Score | Rationale |
|---|---|---|
| Identity Alignment | 78 | Title and OG title are protocol-first. |
| Narrative Alignment | 45 | OG description covers protocol positioning but lacks the differentiation argument. |
| Differentiation | 40 | OG description does not contain the protocol/product distinction. |
| Protocol Focus | 72 | Primary description is protocol-focused. Keywords are dominated by operator-level terms. |
| BanzAI Positioning | 60 | BanzAI mentioned in site-level description. |
| **Overall** | **59** | Good primary metadata. Weakened by keyword strategy (Banzami Business, Banzami SDK) that doesn't reflect the protocol hierarchy. |

---

## Summary Matrix

| Surface | Identity | Narrative | Differentiation | Protocol | BanzAI | **Overall** |
|---|---|---|---|---|---|---|
| Homepage | 72 | 38 | 35 | 55 | 68 | **54** |
| Operators | 60 | 12 | 15 | 45 | 0 | **26** |
| Reference Landing | 95 | 90 | 88 | 92 | 85 | **90** |
| Dynamic Sections | 80 | 75 | 78 | 80 | 70 | **77** |
| BanzAI Interface | 85 | 20 | 25 | 30 | 55 | **43** |
| About BanzAI | 45 | 30 | 35 | 40 | 30 | **36** |
| Roadmap | 72 | 22 | 30 | 28 | 78 | **46** |
| Validation | 78 | 42 | 55 | 70 | 20 | **53** |
| Footer | 82 | 40 | 35 | 70 | 55 | **56** |
| Metadata / OG | 78 | 45 | 40 | 72 | 60 | **59** |

**Ecosystem average: 54/100**

---

## Target scores (post-propagation)

| Surface | Target Overall | Primary lever |
|---|---|---|
| Homepage | 82 | Narrative alignment — structural argument in problem section |
| Operators | 80 | All dimensions — complete rewrite of opening section |
| Reference Landing | 95 | Already best surface — minor attribution fix only |
| Dynamic Sections | 88 | Fix visual assignments + add §§1–3 visual components |
| BanzAI Interface | 78 | Add pre-interface protocol context block |
| About BanzAI | 85 | Fix integration bug, then narrative is mostly correct |
| Roadmap | 72 | Add BANZA protocol vision section before feature list |
| Validation | 72 | Add protocol-validation argument + BanzAI pointer |
| Footer | 62 | Add single-line protocol positioning tagline |
| Metadata / OG | 78 | Update keywords + OG descriptions for §§1–3 |

---

*Scorecard completed: 2026-05-30. No files modified.*
