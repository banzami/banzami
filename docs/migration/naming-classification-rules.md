# Naming Inversion — Occurrence Classification Rules

**ADR:** ADR-025 — Ecosystem Naming Inversion  
**Version:** 1.0  
**Date:** 2026-05-29

---

## Purpose

Before renaming any occurrence of "Banzami", "Banza", or "BanzamIA", every occurrence must be assigned a **class**. The class determines what the occurrence means semantically and therefore which new name replaces it — or whether it must not be renamed at all.

A global search-and-replace will produce incorrect results because the same string can have different meanings in different contexts. Classify first. Rename second.

---

## Classes

### PROTOCOL

**Definition:** The occurrence refers to the open financial infrastructure protocol, the kernel codebase, the ecosystem of operators, or the specification (RFCs, ADRs, invariants).

**Rename rule:** `Banzami` → `Banza`

**Examples:**
- "The Banzami Protocol defines settlement invariants"
- "The Banzami Kernel enforces double-entry ledger rules"
- "Operators certified on the Banzami ecosystem"

**Do NOT apply PROTOCOL class to:**
- Product feature names (those are class PRODUCT)
- The legal entity name in formal documents (those are class ORG)

---

### PRODUCT

**Definition:** The occurrence refers to the consumer/merchant-facing payment application, its features, or the reference operator experience.

**Rename rule:** `Banza` → `Banzami`

**Examples:**
- "Open the Banza app"
- "Banza Wallet balance"
- "Banza QR payment"
- "Banza Business dashboard"
- "Pay with Banza"

---

### AI_OS

**Definition:** The occurrence refers to the Protocol Operating System (the BanzamIA / BanzAI product).

**Rename rule:** `BanzamIA` → `BanzAI`

**Examples:**
- "BanzamIA is the Protocol Operating System"
- "Ask BanzamIA about certification"
- "BanzamIA Chat component"
- "banzamia-client library"

---

### ORG

**Definition:** The occurrence refers to the legal organization, company registration, or formal entity name.

**Rename rule:** Context-dependent. The legal entity is registered as "Banzami". After inversion, the company building the protocol may be referred to as "Banza Protocol Organization" or simply retain the legal name "Banzami" in legal documents. Apply with care and confirm with the founder before renaming ORG occurrences.

**Examples:**
- "Banzami Lda" (legal form — retain as-is)
- "Organização Banzami" in ADR headers
- "Founded by Banzami team"

---

### DOMAIN

**Definition:** The occurrence is or contains a domain name.

**Rename rule:** DO NOT RENAME. `banzami.org` is protected. Domain migration requires a separate decision and DNS transition plan.

**Examples:**
- `banzami.org`
- `https://banzami.org/banzamia`
- Any URL containing `banzami.org`

---

### EMAIL

**Definition:** The occurrence is or contains an email address using a protected domain.

**Rename rule:** DO NOT RENAME. `contact@banzami.org` is protected.

**Examples:**
- `contact@banzami.org`
- Any address `@banzami.org`

---

### REPO

**Definition:** The occurrence refers to a repository name or GitHub path.

**Rename rule:** DO NOT RENAME without a separate repository-rename ADR. Repository renames break clone URLs and CI/CD pipelines. Document the planned new name in the migration map but do not act on it yet.

**Examples:**
- `github.com/banzami/banzami` (kernel repo)
- `github.com/banzami/banzamia` (AI OS repo)
- `github.com/banzami/banza` (operator repo)

---

### PACKAGE

**Definition:** The occurrence is a package name, crate name, npm package, or similar published identifier.

**Rename rule:** DO NOT RENAME without a separate package-rename decision. Published packages have consumers. Renaming without a deprecation/redirect strategy breaks existing installations.

**Examples:**
- `banza-sdk` (npm)
- `banza-typescript-sdk`
- `banza_core` (Rust crate)
- `banzamia-client`

---

### ENV_VAR

**Definition:** The occurrence is an environment variable name used in `.env` files, Docker Compose, or CI/CD configuration.

**Rename rule:** Rename only in coordination with all deployment environments. Must update all `.env` files, Docker Compose files, CI/CD secrets, and server configurations simultaneously. High coordination cost — defer to a dedicated migration step.

**Examples:**
- `BANZAMIA_API_URL`
- `BANZA_DB_URL`
- `BANZAMI_SECRET`

---

### CODE_SYMBOL

**Definition:** The occurrence is a function name, class name, interface name, variable name, or other code identifier inside source files.

**Rename rule:** Rename in the same wave as the product/AI_OS rename, using IDE rename refactoring tools to catch all call sites. Must update imports, exports, and tests.

**Examples:**
- `BanzamIAApp` component
- `BanzamIASidebar` component
- `BanzamIAChat` component
- `chatStream` (neutral — no rename needed)
- `isLiveMode` (neutral — no rename needed)

---

### DATABASE

**Definition:** The occurrence appears in a database schema, migration file, table name, column name, or stored procedure.

**Rename rule:** DO NOT RENAME without a database migration. Renaming database objects requires `ALTER TABLE` / `ALTER COLUMN` migrations and coordination with all services that reference those names. Defer to a dedicated migration step.

**Examples:**
- Table names containing `banza` or `banzami`
- Column comments referencing brand names

---

### API_ROUTE

**Definition:** The occurrence is part of a public API route path.

**Rename rule:** DO NOT RENAME without versioning. Changing a public API route is a breaking change for SDK consumers. Must version the API (v2 route) and deprecate the old route with a sunset period.

**Examples:**
- `/api/banzamia/...`
- `/v1/banza/...`

---

### PUBLIC_COPY

**Definition:** The occurrence appears in user-visible text: website pages, marketing copy, app UI strings, error messages, metadata descriptions, or OpenGraph tags.

**Rename rule:** Rename in Wave 2 (website) or alongside the corresponding product/AI_OS rename. Each surface should be updated in one coordinated commit, not piecemeal.

**Examples:**
- Page titles: "BanzamIA — Protocol Operating System"
- Meta descriptions mentioning Banzami or Banza as product
- Welcome screen text
- Sidebar labels

---

### SVG_TEXT

**Definition:** The occurrence appears inside an SVG file as text content.

**Rename rule:** Rename when renaming PUBLIC_COPY for that surface. SVGs must be regenerated or edited carefully — text in SVGs is often positioned precisely and may require visual verification after rename.

**Examples:**
- Architecture diagram labels
- Tagline text in SVG files: "Ferramentas determinam a verdade · A IA explica a verdade."
- Module name text in `banzamia-product-architecture.svg`

---

### TEST_FIXTURE

**Definition:** The occurrence appears in a test file, fixture, seed data, or test helper.

**Rename rule:** Rename together with the code symbols they reference. Test fixtures should always match the production symbols they test.

**Examples:**
- Mock data with `operatorId: "banza-test-001"`
- Test descriptions: `describe("BanzamIA chat", ...)`

---

## Decision Table

| Occurrence is... | Class | Rename? | To what? |
|-----------------|-------|---------|----------|
| Protocol / ecosystem / kernel | PROTOCOL | Yes | Banza |
| Product feature / consumer UX | PRODUCT | Yes | Banzami |
| AI Protocol OS | AI_OS | Yes | BanzAI |
| Legal entity / company name | ORG | Confirm with founder | — |
| Domain name | DOMAIN | No | Protected |
| Email address | EMAIL | No | Protected |
| Repository path | REPO | No (deferred) | Separate ADR |
| Published package | PACKAGE | No (deferred) | Separate ADR |
| Environment variable | ENV_VAR | No (deferred) | Coordinated step |
| Code symbol | CODE_SYMBOL | Yes, with refactor tools | Matches product/AI_OS |
| Database object | DATABASE | No (deferred) | Separate migration |
| API route | API_ROUTE | No (deferred) | Versioned change |
| User-visible text | PUBLIC_COPY | Yes, Wave 2+ | Matches semantic class |
| SVG text | SVG_TEXT | Yes, with PUBLIC_COPY | Matches semantic class |
| Test file | TEST_FIXTURE | Yes, with code symbols | Matches what is tested |
