---
title: BANZA Identity Purity Audit — BANZA-IDENTITY-PURITY-AUDIT-001
version: 1.0
date: 2026-05-30
status: COMPLETE
---

# BANZA Identity Purity Audit

Scope: All visible "Banzami" occurrences across banzami.org public surfaces.
Objective: Eliminate protocol contamination — cases where BANZA is explained through Banzami instead of Banzami being explained through BANZA.

---

## Classification Rules

| Class | Definition |
|---|---|
| **PROTOCOL_CONTAMINATION** | BANZA is being explained through Banzami; Banzami appears at protocol-level surfaces (hero, intros, architecture, reference pages) |
| **OPTIONAL_PRODUCT_REFERENCE** | Technically correct but unnecessary; Banzami appears where it could be omitted or deferred |
| **REQUIRED_PRODUCT_REFERENCE** | Banzami is the correct subject — product pages, SDK docs, merchant/consumer docs, legal entity, protected identifiers |
| **BROKEN** | Link or route is a 404 |
| **OUTDATED/DEFERRED** | Code identifier (not user-visible); tracked for Wave 4+ |
| **PROTECTED** | Must never change per ADR-025 domain exception |

---

## Audit Results

### HeroSection.tsx

| Location | Surface | Current text | Classification | Action |
|---|---|---|---|---|
| `HeroSection.tsx:57` | Hero subheadline | "Banzami é o produto de pagamentos de Angola, construído sobre o Banza — protocolo aberto de infraestrutura financeira." | **PROTOCOL_CONTAMINATION** | Replace with pure BANZA framing |

**Finding:** The primary hero text visible to every visitor on first load opens with "Banzami é..." — leading with the product name, explaining the protocol through the product. Banzami should not appear in the hero at all. The hero belongs to BANZA.

---

### apps/docs/app/page.tsx (Homepage)

| Location | Surface | Current text | Classification | Action |
|---|---|---|---|---|
| `page.tsx:20` | Metadata description | "...Banzami é o produto de pagamentos construído sobre o Banza — pagamentos wallet-to-wallet em Kwanza, QR-native, com Banzami SDKs..." | OPTIONAL_PRODUCT_REFERENCE | Keep — SEO: users search for Banzami |
| `page.tsx:141` | §6 Ecosystem section | "...Banzami SDKs, bancos e o core financeiro..." | REQUIRED_PRODUCT_REFERENCE | Keep — "Banzami SDK" is the product name |
| `page.tsx:155` | §7 QR Commerce section | "o Banzami QR serve todos os casos de uso..." | REQUIRED_PRODUCT_REFERENCE | Keep — "Banzami QR" is a product feature |
| `page.tsx:202` | §10 Developer section | "O Banzami é SDK-first." | OPTIONAL_PRODUCT_REFERENCE | Fix — SDK-first is a protocol-level principle, not product claim |
| `page.tsx:206` | §10 CTA button | `href="/banza-para-programadores"` | **BROKEN** | Fix → `/banzami-para-programadores` |
| `page.tsx:209` | §10 CTA button | `href="/o-motor-de-crescimento-do-banza"` | **BROKEN** | Fix → `/visao-geral-do-ecossistema` (route does not exist) |
| `page.tsx:263` | Source attribution | "Organização Banzami" | PROTECTED | Keep — legal entity name |

---

### apps/docs/app/layout.tsx (Global)

| Location | Surface | Current text | Classification | Action |
|---|---|---|---|---|
| `layout.tsx:21` | Global metadata description | "...Banzami é o produto de pagamentos construído sobre o Banza — wallet-to-wallet..." | OPTIONAL_PRODUCT_REFERENCE | Keep — SEO and global discoverability |
| `layout.tsx:24` | Keywords | `'Banzami'` | REQUIRED_PRODUCT_REFERENCE | Keep — SEO keyword |
| `layout.tsx:30–31` | Keywords | `'Banzami Business'`, `'Banzami SDK'` | REQUIRED_PRODUCT_REFERENCE | Keep — SEO product keywords |
| `layout.tsx:39` | OG description | "...Banzami é o produto de pagamentos construído sobre o Banza..." | OPTIONAL_PRODUCT_REFERENCE | Keep — SEO |
| `layout.tsx:56` | Authors | `'Organização Banzami'` | PROTECTED | Keep — legal entity |
| `layout.tsx:73,141` | Logo image src | `/images/banza/banzami-logo.png` | OUTDATED/DEFERRED | Wave 9 — file rename |
| `layout.tsx:82,83` | Navbar hrefs | `/banzami-para-programadores`, `/banzami-para-comerciantes` | REQUIRED_PRODUCT_REFERENCE | Keep — correct routes (fixed in Wave AA) |
| `layout.tsx:88,158` | BanzAI route | `/banzamia` | REQUIRED_PRODUCT_REFERENCE | Keep — BanzAI app route |
| `layout.tsx:152,153` | Footer hrefs | `/banzami-para-programadores`, `/banzami-para-comerciantes` | REQUIRED_PRODUCT_REFERENCE | Keep — correct routes (fixed in Wave AA) |

---

### apps/docs/app/[section]/page.tsx (Section Pages)

| Location | Surface | Current text | Classification | Action |
|---|---|---|---|---|
| `[section]/page.tsx:38` | Section metadata description | `"Banzami — §${section.number}: ${section.title}"` | **PROTOCOL_CONTAMINATION** | Fix → `"Banza — §${section.number}: ${section.title}"` |
| `[section]/page.tsx:40` | OG title | `"${section.title} · Banzami"` | **PROTOCOL_CONTAMINATION** | Fix → `"${section.title} · Banza"` |
| `[section]/page.tsx:41` | OG description | `"Referência oficial Banzami — secção ${section.number}: ${section.title}"` | **PROTOCOL_CONTAMINATION** | Fix → `"Referência oficial Banza — §${section.number}: ${section.title}"` |
| `[section]/page.tsx:50` | Code comment | `// How Banzami Works` | OUTDATED/DEFERRED | Wave 4 — code comment |
| `[section]/page.tsx:53,54,57,58` | Code comments | `// Banzami for Developers`, `// Banzami Flywheel`, etc. | OUTDATED/DEFERRED | Wave 4 — code comments |

**Finding:** All 17 section pages shared the same OG metadata template that branded the protocol reference as "Banzami reference". These pages cover BANZA protocol topics and must identify with Banza, not Banzami.

---

### apps/docs/app/roadmap/page.tsx

| Location | Surface | Current text | Classification | Action |
|---|---|---|---|---|
| `roadmap/page.tsx:103` | Breadcrumb | `<Link href="/banzamia">BanzAI</Link>` | REQUIRED_PRODUCT_REFERENCE | Keep — correct route and label |
| `roadmap/page.tsx:110` | Page intro text | "Protocol Operating System for the Banzami ecosystem." | **PROTOCOL_CONTAMINATION** | Fix → "for the Banza protocol." |
| `roadmap/page.tsx:154` | CTA button | `href="/banzamia"` | REQUIRED_PRODUCT_REFERENCE | Keep — correct route |

**Finding:** BanzAI is the Protocol Operating System for the **Banza** protocol. Calling it "for the Banzami ecosystem" inverts the hierarchy — it positions BanzAI as a Banzami product rather than a protocol-level system.

---

### apps/docs/app/sobre-banzamia/page.tsx

| Location | Surface | Current text | Classification | Action |
|---|---|---|---|---|
| `sobre-banzamia/page.tsx:12` | OG title | `'Sobre o BanzAI · Banzami'` | **PROTOCOL_CONTAMINATION** | Fix → `'Sobre o BanzAI · Banza'` |
| `sobre-banzamia/page.tsx:18` | Function name | `SobreBanzamiaPage()` | OUTDATED/DEFERRED | Wave 4 — code identifier |
| `sobre-banzamia/page.tsx:48,102` | Route hrefs | `/banzamia` | REQUIRED_PRODUCT_REFERENCE | Keep — BanzAI app route |

---

### apps/docs/app/validacao/page.tsx

| Location | Surface | Current text | Classification | Action |
|---|---|---|---|---|
| `validacao/page.tsx:35` | H1 heading | "Execução e Validação do Ecossistema Banzami" | **PROTOCOL_CONTAMINATION** | Fix → "Execução e Validação do Protocolo Banza" |
| `validacao/page.tsx:50` | Governance notice | "edição restrita à administração Banzami" | OPTIONAL_PRODUCT_REFERENCE | Keep — organizational reference, contextually accurate |
| `validacao/page.tsx:99` | Footer | "Organização Banzami" | PROTECTED | Keep — legal entity |

---

### apps/docs/app/operators/page.tsx

| Location | Surface | Current text | Classification | Action |
|---|---|---|---|---|
| `operators/page.tsx:93` | Protocol wire format | `/.well-known/banzami/operator.json` | PROTECTED | Never change — ADR-025 domain exception |

---

### apps/docs/components/HeroBanzamIAWidget.tsx

| Location | Surface | Current text | Classification | Action |
|---|---|---|---|---|
| Widget descriptor | Widget | "O Sistema Operativo do Protocolo Banza." | CORRECT | No action — already correct |
| H2 label | Widget | "Pergunte ao BanzAI" | CORRECT | No action |

---

### apps/docs/components/EcosystemMap.tsx

| Location | Surface | Current text | Classification | Action |
|---|---|---|---|---|
| `EcosystemMap.tsx:36` | Code comment | `/* Center node — Banzami Core */` | OUTDATED/DEFERRED | Wave 4 — code comment, not user-visible |

### apps/docs/components/MarkdownSection.tsx

| Location | Surface | Current text | Classification | Action |
|---|---|---|---|---|
| `MarkdownSection.tsx:53` | CSS class | `prose-banzami` | OUTDATED/DEFERRED | Wave 4 — code identifier, not user-visible |

---

## Summary Counts

| Classification | Count | Immediate action |
|---|---|---|
| PROTOCOL_CONTAMINATION | 7 | Fix immediately |
| OPTIONAL_PRODUCT_REFERENCE (fixed) | 2 | Fixed: hero subheadline context, "O Banzami é SDK-first" |
| OPTIONAL_PRODUCT_REFERENCE (kept) | 4 | Kept for SEO and organizational context |
| REQUIRED_PRODUCT_REFERENCE | 15 | No action |
| BROKEN | 2 | Fixed immediately |
| PROTECTED | 5 | Never change |
| OUTDATED/DEFERRED | 6 | Wave 4+ |

---

## Visitor Mental Model After Remediation

A visitor to banzami.org now encounters:

1. **Hero H1:** "Infraestrutura financeira programável." — BANZA signal
2. **Hero subheadline:** "Banza define como o dinheiro se move digitalmente em Angola — através de operadores certificados, regras verificáveis e infraestrutura aberta." — pure BANZA framing
3. **Sidebar:** "BANZA — Documentação do Protocolo" — BANZA signal
4. **Navbar:** "Banza" wordmark — BANZA signal
5. **BanzAI widget:** "O Sistema Operativo do Protocolo Banza." — correct positioning
6. **Feature sections:** Banzami appears in §6 (SDK), §7 (QR Commerce) as product features — contextually correct
7. **OG/SEO metadata:** includes Banzami for discoverability — correct
8. **Section page OGs:** "Banza — §N: Title" — BANZA signal on all 17 section pages

The hierarchy is self-evident from first contact: **BANZA = protocol → Banzami = product → BanzAI = protocol OS.**

---

*Audit completed: 2026-05-30.*
