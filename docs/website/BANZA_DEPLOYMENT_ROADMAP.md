# BANZA Deployment Roadmap

**Document ID:** BANZA-DEPLOYMENT-ROADMAP-001  
**Date:** 2026-06-01  
**Authority:** BANZA-WEBSITE-AND-INFRASTRUCTURE-ALIGNMENT-001  
**Target:** 217.160.9.248 · banzami.org (temporary) → banza.network (production)

---

## Deployment Sequence Overview

| Wave | Name | Goal | Duration | Blocks |
|------|------|------|----------|--------|
| **Wave 1** | Infrastructure Cleanup | Secure, clean, and aligned VM | 1–2 days | Wave 2 |
| **Wave 2** | Website Deployment | BANZA protocol website live at banzami.org | 1 day | Wave 3 |
| **Wave 3** | Documentation Publication | Developer and protocol docs live | 1 week | Wave 4 |
| **Wave 4** | Developer Portal | Conformance runner, SDK docs, API reference | 1–2 weeks | Wave 5 |
| **Wave 5** | Operator Onboarding | Certification application, quickstart live | Requires M2 | Wave 6 |
| **Wave 6** | Production Trust (M2) | Root key ceremony, live Key Manifest + BRL | OPS-001 | banza.network |

---

## Wave 1 — Infrastructure Cleanup

**Goal:** VM is secure, clean, and fully aligned with the frozen architecture.  
**Duration:** 1–2 days  
**All tasks unblocked.**

### W1-1: Fix backup process (CRITICAL — do first)

```bash
# Immediate manual backup
docker exec banzami-postgres-1 pg_dump -U banzami banzami \
  > /srv/banzami/backup_$(date +%Y%m%d_%H%M%S).sql

docker exec banzami-postgres-1 pg_dump -U banzami banzami_staging \
  > /srv/banzami/backup_staging_$(date +%Y%m%d_%H%M%S).sql

# Automated backup cron (every 6 hours)
cat > /etc/cron.d/banzami-backup << 'EOF'
0 */6 * * * root docker exec banzami-postgres-1 pg_dump -U banzami banzami \
  > /srv/banzami/data/backups/banzami_$(date +\%Y\%m\%d_\%H\%M\%S).sql 2>&1
EOF
mkdir -p /srv/banzami/data/backups
```

### W1-2: Add swap (15 min)

```bash
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab
```

### W1-3: Remove port 4001 external binding

In `/srv/banzamia/src/docker/docker-compose.yml`:
```yaml
# Remove the ports mapping entirely
# ports:
#   - "4001:4001"
```

Connect banzamia to banzami_net instead:
```yaml
networks:
  - banzami_net  # or define external network reference

networks:
  banzami_net:
    external: true
    name: banzami_banzami_net
```

Restart: `cd /srv/banzamia && docker compose up -d`

### W1-4: Update env var naming (BANZAMIA → BANZAI)

In `/srv/banzamia/src/docker/docker-compose.yml`:
```yaml
# Replace all BANZAMIA_* with BANZAI_*
BANZAI_MODE:             "${BANZAI_MODE:-live-api-no-model}"
BANZAI_ALLOWED_ORIGINS:  "${BANZAI_ALLOWED_ORIGINS:-https://banzami.org}"
BANZAI_QDRANT_URL:       "${BANZAI_QDRANT_URL:-}"
BANZAI_QWEN_URL:         "${BANZAI_QWEN_URL:-}"
BANZAI_QWEN_CODER_URL:   "${BANZAI_QWEN_CODER_URL:-}"
BANZAI_DEEPSEEK_URL:     "${BANZAI_DEEPSEEK_URL:-}"
# Remove:
# BANZAMIA_REFERENCE_OPERATOR_URL (operator-specific — violates neutrality)
```

### W1-5: Reclaim disk space

```bash
# Remove unused Docker images and stopped containers
docker system prune -f

# Remove duplicate/old backup files
rm /srv/banzami/backup_20260516_213832.sql  # 0-byte failed backup
# Review /srv/banzami/docker-compose.yml.bak files
```

### W1-6: Investigate unhealthy frontend containers

```bash
# Check what health test is failing
docker inspect banzami-admin-frontend-1 | grep -A10 '"Healthcheck"'
docker exec banzami-admin-frontend-1 node --version
docker logs banzami-admin-frontend-1 --tail 50
```

These are operator product services — fix is the operator team's responsibility. Document status.

---

## Wave 2 — Website Deployment

**Goal:** BANZA protocol website live at banzami.org with correct identity and content.  
**Duration:** 1 day  
**Requires:** Wave 1 complete (W1-2 and W1-3 at minimum)

### W2-1: Fix docs-frontend metadata (30 min)

File: `/srv/banzami/src/apps/docs/app/layout.tsx`

```typescript
export const metadata: Metadata = {
  title: {
    default: 'BANZA — Open Financial Infrastructure Protocol',
    template: '%s · BANZA',
  },
  description:
    'BANZA is Angola\'s open financial infrastructure protocol — public rules, open certification, ' +
    'verifiable invariants, and federation. BanzAI is the Protocol Operating System.',
  keywords: [
    'BANZA', 'open payment protocol', 'Angola', 'financial infrastructure',
    'BanzAI', 'protocol operating system', 'certified operators', 'federation',
    'QR payments', 'instant payments', 'open source fintech',
  ],
}
```

### W2-2: Translate Portuguese UI text (1–2 hours)

File: `/srv/banzami/src/apps/docs/app/page.tsx`

Replace Portuguese problem cards, use case cards, and navigation labels with English equivalents sourced from BANZA_REFERENCE.md §1–2.

Route cleanup:
- `app/sobre-o-banzai/` → `app/about/` (or remove if content is now in `/protocol`)
- `app/validacao/` → `app/validation/` (or remove if content is now in `/certification`)

### W2-3: Rebuild docs-frontend image (30 min)

```bash
cd /srv/banzami/src
docker build -f apps/docs/Dockerfile -t banzami/docs-frontend:latest .
```

Or trigger CI/CD rebuild if pipeline is configured.

### W2-4: Deploy updated docs-frontend (10 min)

```bash
cd /srv/banzami
docker compose up -d docs-frontend
# Verify
curl -s https://banzami.org/ | grep -i "BANZA"
curl -s https://banzami.org/protocol | head -5
curl -s https://banzami.org/banzai | head -5
```

### W2-5: Add nginx route for BanzAI API (30 min)

In `/srv/banzami/nginx/conf.d/banzami.conf`, add to the `banzami.org` server block:

```nginx
location /banzai/api/ {
    proxy_pass         http://banzamia-api:4001/;
    proxy_http_version 1.1;
    proxy_set_header   Host              $host;
    proxy_set_header   X-Real-IP         $http_cf_connecting_ip;
    proxy_set_header   X-Forwarded-For   $http_cf_connecting_ip;
    proxy_set_header   X-Forwarded-Proto $scheme;
    proxy_read_timeout 30s;
    
    # Security: only allow BanzAI endpoints
    # POST /ask, /research, /certify, /validate, /trace, /simulate, /federation
    # GET /rag/stats, /health
}
```

```bash
docker compose exec nginx nginx -s reload
curl -s https://banzami.org/banzai/api/health
```

### W2-6: Smoke test (30 min)

```bash
# All sections must return 200
for section in protocol certification federation trust operators developers governance roadmap faq; do
  status=$(curl -s -o /dev/null -w "%{http_code}" https://banzami.org/$section)
  echo "$section: $status"
done

# BanzAI section
curl -s -o /dev/null -w "%{http_code}" https://banzami.org/banzai
curl -s https://banzami.org/banzai/api/health | jq .

# No operator brand in metadata
curl -s https://banzami.org/ | grep -i "Banzami" | grep -v "api.banzami.org"
# Should return empty (no operator brand in protocol site content)
```

---

## Wave 3 — Documentation Publication

**Goal:** Full protocol documentation accessible online.  
**Duration:** 1 week

### W3-1: GOV-001/002/003 — RFC status updates

Update RFC-0001, RFC-0002, RFC-0005 status from `Draft` to `Implemented` in `docs/rfc/`.

### W3-2: DOC-003 — BANZA_CERTIFICATION.md L4 caveat

Mark L4 as v1.1 scope in `BANZA_CERTIFICATION.md`.

### W3-3: PROTO-001 — RFC files with ADR-026 references

Update RFC files to cross-reference ADR-026 federation trust model.

### W3-4: BANZA_ROADMAP.md update

Update with federation complete status and current M1–M6 milestone tracking.

### W3-5: /docs page deployment

Ensure `/docs` route renders the full protocol reference with all sections navigable.

---

## Wave 4 — Developer Portal

**Goal:** Developers can explore contracts, run conformance, and get started.  
**Duration:** 1–2 weeks

### W4-1: Conformance runner documentation

Add `tools/banza-conformance/` usage documentation to the website developers section.

### W4-2: SDK documentation pages

Create dedicated pages for each SDK (TypeScript, Python, Go, PHP, Flutter) with installation and quickstart.

### W4-3: API reference (OpenAPI explorer)

Add interactive OpenAPI explorer for protocol contracts.

### W4-4: `contracts/federation/key-manifest.json`

Create the key manifest contract file (PROTO-003) — placeholder until M2 ceremony.

---

## Wave 5 — Operator Onboarding

**Goal:** First operators can start their certification journey.  
**Duration:** Requires M2 completion  
**Blocked by:** M2 (Root key ceremony — OPS-001)

### W5-1: FEDERATION_OPERATOR_QUICKSTART.md with live endpoints

After M2, update quickstart with production Key Manifest and BRL URLs.

### W5-2: Certificate issuance runbook (DOC-004)

Step-by-step guide for issuing operator certificates.

### W5-3: BRL operations runbook (DOC-005)

BRL update procedures, rotation schedule, emergency revocation.

### W5-4: Operator registry

First certified operators listed at `/operators`.

### W5-5: Trust section live URLs

Update `/trust` page with production endpoints:
- `banza.network/.well-known/banza/key-manifest.json`
- `banza.network/federation/revocation-list.json`

---

## Wave 6 — Production Trust Publication (M2)

**Goal:** Root key ceremony complete, Key Manifest and BRL live, production trust infrastructure active.  
**Duration:** Scheduled (OPS-001 pending physical logistics)  
**Hard blockers:** OPS-001-G2 (Witness), OPS-001-G3 (USB drives), OPS-001-G4 (air-gapped machine)

After Wave 6 completes:
- SDK v1.0 release with Key Manifest pinned
- banza.network domain transition
- First operator certification possible
- M3 (First Operator Certified) unblocked
- banzami.org → banza.network redirect configured

---

## Domain Transition (banzami.org → banza.network)

| Step | Action |
|------|--------|
| 1 | Deploy BANZA website at banza.network with all Wave 1–5 content |
| 2 | Configure nginx to serve both domains in parallel for 30 days |
| 3 | Add canonical `<link rel="canonical">` pointing to banza.network |
| 4 | Set up 301 redirects from banzami.org → banza.network |
| 5 | Update all hardcoded banzami.org references in docs |
| 6 | Communicate domain change to operators |
| 7 | Keep banzami.org operator subdomains running until operator migrates |

---

## SSL Certificate Renewal Plan

Current certificate expires: **Aug 15 2026** (75 days)

| Action | When |
|--------|------|
| Verify certbot cron target (does it renew Cloudflare origin cert?) | Immediately |
| If certbot manages non-Cloudflare cert: confirm auto-renewal test | Within 1 week |
| If Cloudflare origin cert: manual renewal process via Cloudflare dashboard | By July 15 (30 days before expiry) |
| Document renewal procedure in ops runbook | Wave 1 |

---

## Summary Timeline

```
2026-06-01 (TODAY)
│
├── Wave 1 (1–2 days)
│   ├── W1-1: Restore backups                     ← IMMEDIATE
│   ├── W1-2: Add swap
│   ├── W1-3: Fix port 4001 exposure
│   ├── W1-4: Update BANZAMIA_ → BANZAI_ env vars
│   └── W1-5: Reclaim disk space
│
├── Wave 2 (1 day)
│   ├── W2-1: Fix metadata (remove operator brand)
│   ├── W2-2: Translate Portuguese UI
│   ├── W2-3/4: Rebuild + deploy docs-frontend
│   ├── W2-5: Add nginx /banzai/api/ route
│   └── W2-6: Smoke test
│       → banzami.org is live ✓
│
├── Wave 3 (1 week)
│   └── GOV-001/002/003, DOC-003, PROTO-001, BANZA_ROADMAP.md
│
├── Wave 4 (1–2 weeks)
│   └── Conformance runner, SDK docs, API reference, contracts/
│
├── Wave 5 (post M2)
│   └── Quickstart with live endpoints, operator registry, runbooks
│
└── Wave 6 (OPS-001 ceremony)
    └── M2 complete → Trust live → banza.network transition → M3 unblocked
```
