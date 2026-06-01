# BANZA Deployment Readiness Report

**Document ID:** BANZA-DEPLOYMENT-READINESS-001  
**Date:** 2026-06-01  
**Authority:** BANZA-WEBSITE-AND-INFRASTRUCTURE-ALIGNMENT-001  
**Question:** Can the BANZA website be deployed today on 217.160.9.248 using banzami.org?

---

## Phase 11 — Final Verdict

### Can BANZA be publicly deployed on 217.160.9.248 using banzami.org while remaining fully aligned with the frozen BANZA architecture?

**YES — with a mandatory pre-deployment sequence of 5 steps.**

The infrastructure is ready. The VM is running. SSL is valid. Nginx is configured. The deployment path exists. Two critical blockers must be resolved before the website launches. Three additional steps are required for full alignment.

---

## Blockers

### BLOCKER-1 — docs-frontend is broken (CRITICAL)

**What:** The BANZA public website at `banzami.org` currently returns `NoFallbackError` from Next.js on all content pages. The static generation fails because `getAllSectionSlugs()` references old Portuguese section slugs, but BANZA_REFERENCE.md was restructured to 12 English sections.

**Impact:** The BANZA website is not publicly accessible. All content pages return errors.

**Fix:** Rebuild the docs-frontend Docker image against the updated BANZA_REFERENCE.md. Push the new image to the registry. Redeploy with `docker compose pull && docker compose up -d docs-frontend`.

**Effort:** 1–2 hours (build + push + deploy)

**Unblocked?** YES — no external dependencies.

---

### BLOCKER-2 — docs-frontend metadata names the reference operator (CRITICAL)

**What:** Site `<title>`, `<meta description>`, and `<meta keywords>` contain the operator name and "Banzami é o operador de referência". The BANZA protocol website must not name any specific operator.

**Impact:** Every page on `banzami.org` presents the operator brand as part of the BANZA protocol identity. This violates ADR-025 and the operator neutrality principle.

**Fix:** Update `apps/docs/app/layout.tsx` to use protocol-neutral metadata before the image rebuild.

**Effort:** 30 minutes.

**Unblocked?** YES — no external dependencies.

---

## Pre-Deployment Sequence (5 steps, all unblocked)

### Step 1 — Fix docs-frontend metadata (30 min)

In `/srv/banzami/src/apps/docs/app/layout.tsx`:

```typescript
// Replace
title: 'Banza — Protocolo de Infraestrutura Financeira Programável'
description: '... Banzami é o operador de referência ...'
keywords: ['Banzami', ...]

// With
title: 'BANZA — Open Payment Protocol'
description: 'BANZA is Angola\'s open financial infrastructure protocol. Public rules, open certification, verifiable invariants, and federation. BanzAI is the Protocol Operating System.'
keywords: ['BANZA', 'open payment protocol', 'Angola', 'financial infrastructure', 
           'BanzAI', 'certified operators', 'QR payments', 'federation']
```

### Step 2 — Fix Portuguese UI text (1–2 hours)

Update hardcoded Portuguese strings in:
- `app/page.tsx` — problem cards, use case cards
- `app/layout.tsx` — metadata (done in Step 1)
- Route `sobre-o-banzai` → `about`
- Route `validacao` → `validation`

The content sections (from BANZA_REFERENCE.md) are already in English. Only hardcoded UI text requires translation.

### Step 3 — Rebuild and deploy docs-frontend (1 hour)

```bash
cd /srv/banzami/src/apps/docs
docker build -t banzami/docs-frontend:latest .
docker push banzami/docs-frontend:latest  # or load directly on VM
cd /srv/banzami
docker compose pull docs-frontend
docker compose up -d docs-frontend
```

Verify: `curl https://banzami.org/` returns 200 with correct content.

### Step 4 — Add nginx route for BanzAI API (30 min)

Add to `/srv/banzami/nginx/conf.d/banzami.conf` under the `banzami.org` server block:

```nginx
location /banzai/api/ {
    proxy_pass         http://172.17.0.2:4001/;
    proxy_http_version 1.1;
    proxy_set_header   Host              $host;
    proxy_set_header   X-Real-IP         $http_cf_connecting_ip;
    proxy_set_header   X-Forwarded-For   $http_cf_connecting_ip;
    proxy_set_header   X-Forwarded-Proto $scheme;
    proxy_read_timeout 30s;
}
```

*Note: Once banzamia-api is moved to `banzami_net` (CONTRADICTION-007 fix), use `http://banzamia-api:4001/` instead of the IP.*

Reload nginx: `docker compose exec nginx nginx -s reload`

### Step 5 — Restore database backups (CRITICAL — must be done before or concurrent with launch)

The existing backup from May 16 is 16 days stale. One backup is 0 bytes (failed).

```bash
# Create immediate backup
docker exec banzami-postgres-1 pg_dump -U banzami banzami > /srv/banzami/backup_$(date +%Y%m%d_%H%M%S).sql

# Add to crontab
echo "0 */6 * * * docker exec banzami-postgres-1 pg_dump -U banzami banzami > /srv/banzami/backup_\$(date +%Y\%m\%d_\%H\%M\%S).sql" >> /etc/cron.d/banzami-backup
```

---

## Post-Launch Alignment Work (not blockers, but required before public announcement)

| Item | Priority | Effort |
|------|----------|--------|
| Fix CONTRADICTION-003: `BANZAMIA_*` → `BANZAI_*` env vars | HIGH | 30 min |
| Fix CONTRADICTION-004: Remove `BANZAMIA_REFERENCE_OPERATOR_URL` | HIGH | 15 min |
| Fix CONTRADICTION-005: Remove port 4001 external binding | HIGH | 30 min |
| Fix CONTRADICTION-007: Consolidate docker-compose network | MEDIUM | 1 hour |
| Fix CONTRADICTION-008: Remove source code from VM | MEDIUM | 30 min |
| Add swap to VM | MEDIUM | 15 min |
| Set up automated disk space monitoring | MEDIUM | 30 min |

---

## Build Process Audit

| Step | Status | Notes |
|------|--------|-------|
| Source code present on VM | YES (`/srv/banzami/src/`) | Can build locally on VM |
| Docker daemon | Running | `docker compose` available |
| Image registry | Configured (`banzami/*`) | Push requires registry credentials |
| SSL | Valid until Aug 15 2026 | Cloudflare origin cert — plan renewal |
| Nginx | Running, configured | Reload required for new routes |
| Database | Healthy | postgres:16-alpine |
| Redis | Healthy | redis:7-alpine |

---

## What Is NOT Required for Initial Launch

The following items are important but NOT required for the initial BANZA website to go live:

- Root key ceremony (M2) — Trust section will note "ceremony scheduled"
- Live BanzAI AI mode (vLLM/Qwen) — BanzAI API works in mock mode
- Production Qdrant deployment — BanzAI works with static knowledge
- Operator registry URL — can be "coming soon"
- Visual assets (diagrams) — React components exist; full visuals can be shipped iteratively
- Portuguese translation — English is the primary language; Portuguese is a later addition
- banza.network domain — banzami.org is the current production domain

---

## Deployment Readiness Score

| Area | Score (0–10) | Status |
|------|:---:|--------|
| Infrastructure | 9 | VM running, nginx configured, SSL valid |
| Content | 8 | BANZA_REFERENCE.md complete, English |
| Build process | 7 | Source available, Docker configured |
| Security | 6 | Port 4001 exposure, missing swap |
| Monitoring | 4 | No dedicated monitoring, broken backups |
| BanzAI integration | 5 | Running but not nginx-integrated |
| **Overall** | **6.5** | **Ready with 5 pre-deployment steps** |
