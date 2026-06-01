# BANZA Infrastructure Alignment Report

**Document ID:** BANZA-INFRA-ALIGNMENT-001  
**Date:** 2026-06-01  
**Authority:** BANZA-WEBSITE-AND-INFRASTRUCTURE-ALIGNMENT-001  
**Scope:** BANZA repo · BanzAI repo · VM 217.160.9.248 · Website

---

## Summary

The infrastructure has significant legacy architecture from before ADR-025 (ecosystem naming inversion) and the BANZA/BanzAI separation. The core financial services (postgres, core-api, gateway, frontends) are running correctly as operator product infrastructure. The BANZA protocol website and BanzAI API layer have architecture violations that must be resolved before public launch.

**8 contradictions identified.** 2 are critical (block launch). 4 are high. 2 are medium.

---

## Phase 1 — Architecture Validation Results

### Ecosystem hierarchy verified

```
BANZA (open protocol kernel) ← ~/banza
  ↓
BanzAI (Protocol OS) ← ~/banzai
  ↓
Operators (reference implementation) ← ~/banza (apps/operator)
```

This dependency direction is correctly implemented in the repositories. The protocol (`~/banza`) does not depend on BanzAI or any operator. BanzAI (`~/banzai`) depends on BANZA for its knowledge corpus. The operator services depend on both.

### Architecture contradictions found

---

### CONTRADICTION-001 — docs-frontend metadata names the reference operator

**Location:** `/srv/banzami/src/apps/docs/app/layout.tsx`  
**Severity:** CRITICAL (blocks launch)  
**Type:** Operator brand in protocol website

```typescript
// CURRENT (wrong)
metadata.description = "...BanzAI é o sistema operativo nativo do protocolo. 
                         Banzami é o operador de referência — wallets, QR e SDKs em Kwanza."
metadata.keywords = ['Banza', 'Banzami', 'protocolo financeiro Angola', ...]
```

The public BANZA protocol website must never name a specific operator in site metadata. The protocol exists independently of any operator.

**Required correction:** Remove all operator brand references from metadata. Replace with:
```typescript
metadata.description = "BANZA is Angola's open payment protocol — public rules, open certification, 
                         verifiable invariants, and federation."
metadata.keywords = ['BANZA', 'open payment protocol', 'Angola', 'financial infrastructure', 
                     'BanzAI', 'certified operators', 'federation', 'QR payments']
```

---

### CONTRADICTION-002 — docs-frontend static generation broken

**Location:** `/srv/banzami/src/apps/docs/app/[section]/page.tsx`  
**Severity:** CRITICAL (blocks launch)  
**Type:** Stale build — BANZA_REFERENCE.md was restructured but website not rebuilt

```
Error: Internal: NoFallbackError
```

`getAllSectionSlugs()` reads slugs from the current BANZA_REFERENCE.md. The document was restructured from Portuguese sections to 12 English sections. The deployed image was built against the old section structure. `dynamicParams = false` means unknown slugs return 404. The entire `[section]` route is broken.

**Required correction:** Rebuild the docs-frontend image against the updated BANZA_REFERENCE.md (12 English sections). The `getAllSectionSlugs()` function must return the new section slugs.

---

### CONTRADICTION-003 — BanzAI API uses pre-ADR-025 env var naming

**Location:** `/srv/banzamia/src/docker/docker-compose.yml`  
**Severity:** HIGH  
**Type:** Naming violation — pre-ADR-025 residue

```yaml
# CURRENT (wrong)
BANZAMIA_MODE: "live-api-no-model"
BANZAMIA_ALLOWED_ORIGINS: "https://banzami.org"
BANZAMIA_QDRANT_URL: ...
BANZAMIA_QWEN_URL: ...
```

ADR-025 established that the Protocol OS is called "BanzAI", not "BanzamIA". All environment variables, config, and documentation must use `BANZAI_*` prefix, not `BANZAMIA_*`.

**Required correction:** Update env var names to `BANZAI_*` throughout the BanzAI deployment. The BANZAI_REFERENCE.md (now complete) documents the canonical env vars.

---

### CONTRADICTION-004 — BanzAI API references specific operator URL

**Location:** `/srv/banzamia/src/docker/docker-compose.yml`  
**Severity:** HIGH  
**Type:** Operator dependency in BanzAI

```yaml
# CURRENT (wrong)
BANZAMIA_REFERENCE_OPERATOR_URL: "${BANZAMIA_REFERENCE_OPERATOR_URL:-}"
```

BanzAI must never reference a specific operator by name or URL as a dependency. BanzAI is operator-neutral (ADR-025). This env var implies BanzAI has a privileged connection to a specific operator.

**Required correction:** Remove `BANZAMIA_REFERENCE_OPERATOR_URL`. If operator health-check integration is needed, use a generic `BANZAI_OPERATOR_API_URL` that any operator can configure.

---

### CONTRADICTION-005 — BanzAI API port 4001 exposed without nginx

**Location:** VM iptables / docker-compose  
**Severity:** HIGH  
**Type:** Security + architecture gap

Port 4001 (`banzamia-api-1`) is bound to `0.0.0.0:4001`, bypassing ufw. BanzAI's API is accessible directly from the internet without nginx termination, authentication, or rate limiting. Additionally, there is no `/banzai/api/` route in the nginx config — BanzAI is not integrated into the BANZA website backend.

**Required correction:**
1. Remove port binding from banzamia docker-compose: `# ports:  # - "4001:4001"` → connect via Docker network
2. Add BanzAI to `banzami_net` Docker network
3. Add nginx upstream route under `banzami.org`:
```nginx
location /banzai/api/ {
    proxy_pass http://banzamia-api:4001/;
    proxy_http_version 1.1;
    ...
}
```

---

### CONTRADICTION-006 — Website serves Portuguese content

**Location:** `/srv/banzami/src/apps/docs/` — layout.tsx, page.tsx, components  
**Severity:** HIGH  
**Type:** Language / internationalization

Multiple UI elements, problem descriptions, use case cards, and section titles are hardcoded in Portuguese. The BANZA_REFERENCE.md content is now English, but the React component UI text (problem cards, use case cards, nav labels) remains Portuguese.

Affected files:
- `app/page.tsx` — problem cards, use case cards (Portuguese)
- `app/layout.tsx` — metadata (Portuguese)
- `app/sobre-o-banzai/page.tsx` — entire page is Portuguese slug
- `app/validacao/page.tsx` — "validation" route in Portuguese

**Required correction:** Translate hardcoded UI text to English. Rename Portuguese slug routes (`sobre-o-banzai` → `about`, `validacao` → `validation`).

---

### CONTRADICTION-007 — Two separate docker-compose files for related services

**Location:** `/srv/banzami/docker-compose.yml` + `/srv/banzamia/src/docker/docker-compose.yml`  
**Severity:** MEDIUM  
**Type:** Operational complexity

The BanzAI API runs in a completely separate compose project (`banzamia` network) from the main deployment (`banzami_net` network). This means:
- BanzAI cannot use the internal Docker network to reach operator services
- No shared network between BanzAI and nginx
- Two separate `docker compose up` commands required for full deployment

**Required correction:** Either consolidate into one docker-compose, or explicitly document the network bridge (the current workaround is port 4001 external binding, which creates CONTRADICTION-005).

---

### CONTRADICTION-008 — Source code deployed on production VM

**Location:** `/srv/banzami/src/` + `/srv/banzamia/src/`  
**Severity:** MEDIUM  
**Type:** Security / operational hygiene

Full source code repositories are checked out on the production VM. This means:
- `.env` files, secrets, and credentials may be in source tree
- Accidental `git pull` could deploy untested code
- Disk usage is significantly increased (contributing to 80% disk usage)

**Required correction:** Remove source code from VM. Deploy from Docker images built in CI/CD pipeline only. Keep only `docker-compose.yml` and secrets on the VM.

---

## Phase 6 — BanzAI Integration Verification

### Required content for `/banzai` page

The `/banzai` page at `banzami.org/banzai` must contain all of the following (from BANZAI_REFERENCE.md):

| Content | Source | Status |
|---------|--------|--------|
| What is BanzAI | §1 | Available in BANZAI_REFERENCE.md |
| Authority boundary table | §1 | Available in BANZAI_REFERENCE.md |
| Why BanzAI exists | §2 | Available in BANZAI_REFERENCE.md |
| Six operational verbs (corrected) | §4 | Available — "Evaluate" not "Certify" |
| Knowledge Engine | §5 | Available in BANZAI_REFERENCE.md |
| Evaluation Engine | §6 | Available in BANZAI_REFERENCE.md |
| Certification Support | §7 | Available in BANZAI_REFERENCE.md |
| Federation Intelligence | §8 | Available in BANZAI_REFERENCE.md |
| Validation Studio | §10 | Available in BANZAI_REFERENCE.md |
| Mandatory statement | — | "BANZA defines. BANZA certifies. BanzAI evaluates. Operators implement." |

**Mandatory statement position:** The authority boundary must appear prominently — first section, before any capability description.

### BanzAI integration architecture (correct model)

```
banzami.org/banzai          → docs-frontend (renders BANZAI_REFERENCE.md)
banzami.org/banzai/api/*    → nginx → banzamia-api (Docker internal network)
```

BanzAI does NOT get its own domain. BanzAI is a section of the BANZA website.

---

## Phase 8 — Repository Architecture Violations

### BANZA repo (`~/banza`)

| Location | Issue | Severity |
|----------|-------|----------|
| `BANZAI_REFERENCE.md` (prior version — already fixed) | Had "certifica" as operational verb | FIXED |
| `docs/reference/BANZAI_REFERENCE_WEBSITE_MAPPING.md` | References "banzai.network" as a separate site | LOW — needs clarification note |
| `docs/reference/BANZAI_REFERENCE_RESTRUCTURE_PLAN.md` | References "banzai.network" as a separate site | LOW — needs clarification note |

**Note on "banzai.network" references:** Prior reference documents in `docs/reference/` mention `banzai.network` as a potential URL. This is inconsistent with the architectural decision that BanzAI has no separate public website. These references should be annotated as forward-looking notes, not approved architectures.

### BanzAI repo (`~/banzai`)

| Location | Issue | Severity |
|----------|-------|----------|
| `apps/api/src/providers/vllm.ts` | Internal env var naming uses `BANZAI_QWEN_URL` | OK — correct naming |
| `apps/api/src/providers/factory.ts` | Uses `BANZAI_*` env vars | OK — correct naming |
| Docker compose | Uses `BANZAMIA_*` env vars (old naming) | CONTRADICTION-003 |

---

## Alignment Score

| Category | Issues | Resolved | Score |
|----------|--------|----------|-------|
| Repository structure | 1 | 0 | 7/10 |
| Environment naming | 3 | 0 | 5/10 |
| Website content | 4 | 2 (ref docs done) | 6/10 |
| BanzAI integration | 3 | 1 (BANZAI_REFERENCE.md done) | 6/10 |
| Security | 2 | 0 | 5/10 |
| **Overall** | **13** | **3** | **5.8/10** |

**After resolving all 8 contradictions: estimated 9.5/10**
