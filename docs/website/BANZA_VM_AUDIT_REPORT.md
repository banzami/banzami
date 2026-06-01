# BANZA VM Audit Report

**Document ID:** BANZA-VM-AUDIT-001  
**Date:** 2026-06-01  
**Authority:** BANZA-WEBSITE-AND-INFRASTRUCTURE-ALIGNMENT-001  
**Target:** 217.160.9.248

---

## VM Specifications

| Property | Value |
|----------|-------|
| IP | 217.160.9.248 |
| OS | Ubuntu 24.04 LTS (kernel 6.8.0-117) |
| CPU | 4 vCPU |
| RAM | 3.8 GB (1.9 GB used, no swap) |
| Disk | 116 GB (92 GB used — **80% full**) |
| Uptime | 13 days |
| Load | 0.14 (healthy) |

### Critical: No swap configured

With no swap, an OOM event will kill processes immediately. Given 80% disk and 51% memory usage with no headroom, this is a risk for new service additions.

---

## Running Services Inventory

### Docker Containers

| Container | Image | Status | Port | Classification |
|-----------|-------|--------|------|---------------|
| `banzami-nginx-1` | nginx:1.27-alpine | **Up 13d** | 80, 443 | **KEEP — UPDATE** |
| `banzami-postgres-1` | postgres:16-alpine | **Up 13d** | 5432 (internal) | **KEEP** |
| `banzami-redis-1` | redis:7-alpine | **Up 13d** | 6379 (internal) | **KEEP** |
| `banzami-core-api-1` | banzami/core-api:latest | **Up 9d** | 8081 (internal) | **KEEP** |
| `banzami-api-gateway-1` | banzami/api-gateway:latest | **Up 6d** | 8080 (internal) | **KEEP** |
| `banzami-admin-api-1` | banzami/admin-api:latest | **Up 9d** | 8082 (internal) | **KEEP** |
| `banzami-public-api-1` | banzami/public-api:latest | **Up 5d** | 8083 (internal) | **KEEP** |
| `banzami-pay-frontend-1` | banzami/pay-frontend:latest | **Up 8d** | 3002 (internal) | **KEEP** |
| `banzami-core-api-staging-1` | banzami/core-api:latest | **Up 5d** | 8081 (internal) | **KEEP** |
| `banzami-public-api-staging-1` | 077ead1f52ff | **Up 5d** | 8083 (internal) | **UPDATE** (pinned to image hash) |
| `banzami-docs-frontend-1` | banzami/docs-frontend:latest | **Up 41h** | 3005 (internal) | **UPDATE** (erroring, Portuguese, operator branding) |
| `banzamia-api-1` | banzami/banzamia-api:latest | **Up 3d** | **4001 (external)** | **UPDATE** (naming, env vars, nginx integration) |
| `banzami-admin-frontend-1` | banzami/admin-frontend:latest | Up 13d **UNHEALTHY** | 3002 (internal) | **INVESTIGATE + FIX** |
| `banzami-dashboard-frontend-1` | banzami/dashboard-frontend:latest | Up 8d **UNHEALTHY** | 3001 (internal) | **INVESTIGATE + FIX** |
| `banzami-checkout-frontend-1` | banzami/checkout-frontend:latest | Up 13d **UNHEALTHY** | 3003 (internal) | **INVESTIGATE + FIX** |

### Container Classification Details

**`banzami-docs-frontend-1` — UPDATE (HIGH PRIORITY)**
- Currently serves `banzami.org` — the BANZA protocol website
- Next.js `NoFallbackError`: static generation is broken
- Root cause: `getAllSectionSlugs()` references old Portuguese section slugs from the pre-consolidation BANZA_REFERENCE.md; the rebuilt English sections use different slugs
- Fix: rebuild the docs-frontend image against the updated BANZA_REFERENCE.md
- Also: metadata contains "Banzami é o operador de referência" — must be removed
- Action: trigger redeploy from updated source

**`banzamia-api-1` — UPDATE (MEDIUM PRIORITY)**
- This is the BanzAI Protocol OS API
- Environment variable naming uses `BANZAMIA_*` prefix — pre-ADR-025 naming
- `BANZAMIA_ALLOWED_ORIGINS=https://banzami.org` — correct but old env var name
- Container is in a **separate docker-compose** at `/srv/banzamia/` — not in main `banzami/docker-compose.yml`
- Port 4001 is externally exposed (Docker bypasses ufw — **security concern**)
- No nginx route — not accessible from `banzami.org/banzai/api/`
- Actions: (1) add nginx route, (2) update env var names to `BANZAI_*`, (3) consolidate compose files or document separation

**`banzami-public-api-staging-1` — UPDATE**
- Pinned to image hash `077ead1f52ff` — not a named tag
- Should reference `banzami/public-api:latest` for consistency
- Update docker-compose to use tagged image

**Unhealthy containers (`admin-frontend`, `dashboard-frontend`, `checkout-frontend`):**
- All three show Next.js runtime errors in logs
- High failing streak counts (49k–78k failures = running unhealthy for extended period)
- These are operator product UIs — they serve the reference operator's merchant/admin surfaces
- All unhealthy but still serving requests (Next.js apps don't necessarily die on healthcheck failure)
- Root cause investigation needed — likely environment variable or API connectivity issue
- **These are operator product concerns, not BANZA protocol concerns**

---

## Nginx Configuration Audit

| Virtual Host | Routes to | Status | Classification |
|-------------|-----------|--------|---------------|
| `banzami.org`, `www.banzami.org` | `docs-frontend:3005` | **Broken (NoFallbackError)** | **UPDATE** |
| `api.banzami.org` | `api-gateway:8080` + `admin-api:8082/admin/` | Healthy | KEEP |
| `consumer.banzami.org` | `public-api:8083` | Healthy | KEEP |
| `admin.banzami.org` | `admin-frontend:3002` + `admin-api:8082/api/` | Running | KEEP |
| `business.banzami.org` | `dashboard-frontend:3001` | Running | KEEP |
| `pay.banzami.org` | `pay-frontend:3002` | Healthy | KEEP |
| `staging.banzami.org` | `public-api-staging:8083` | Healthy | KEEP |

**Missing nginx route:** No route for BanzAI API (`banzamia-api-1:4001`). Must add:
```nginx
location /banzai/api/ {
    proxy_pass http://banzamia-api:4001/;
    ...
}
```
under the `banzami.org` server block.

**SSL Configuration:**
- Certificate: `/etc/nginx/certs/banzami.pem` (Cloudflare origin CA cert)
- Valid: May 17 2026 → **Aug 15 2026** (75 days remaining)
- Certbot: installed (`/etc/cron.d/certbot` exists)
- Cloudflare origin CA cert: does NOT auto-renew with certbot — manual renewal required before Aug 15
- **Action: Verify Cloudflare origin cert renewal process; confirm certbot cron target**

---

## Storage Audit

| Path | Size | Classification |
|------|------|---------------|
| `/srv/banzami/` | ~15GB est. | KEEP (production deployment) |
| `/srv/banzami/data/postgres/` | Primary financial DB | KEEP |
| `/srv/banzami/data/redis/` | Cache/session data | KEEP |
| `/srv/banzami/nginx/` | Nginx config + certs | KEEP |
| `/srv/banzami/src/` | Full source code | **MIGRATE** (should not be on prod VM) |
| `/srv/banzamia/` | BanzAI deployment | KEEP + UPDATE |
| `/srv/banzamia/src/` | BanzAI source code | **MIGRATE** (should not be on prod VM) |
| `/var/lib/containerd/` | Container layers (~60GB) | REVIEW (Docker image cache) |

**Disk pressure (80% = 92GB/116GB):**
- Largest consumer is Docker overlay layers (container images)
- `/srv/banzami/src/` and `/srv/banzamia/src/` contain full source code clones — not appropriate for a production VM
- Removing unused Docker images could free significant space
- Run `docker system prune` to reclaim overlay storage

**Backup status — CRITICAL:**
- Only 2 SQL backup files: `backup_20260516_213832.sql` (0 bytes — EMPTY) and `backup_20260516_213841.sql` (80KB)
- Last backup: May 16 2026 (16 days ago)
- No automated backup schedule confirmed
- 0-byte backup file indicates a backup failure event
- **Action: Restore automated backup process immediately. Current data at risk.**

---

## Security Audit

| Item | Status | Risk | Action |
|------|--------|------|--------|
| Firewall (ufw) | Active: 22/80/443 only | LOW | KEEP |
| Port 4001 (BanzAI API) | Docker bypasses ufw → **externally reachable** | **HIGH** | Add nginx proxy, remove direct exposure |
| SSL protocols | TLSv1.2 + TLSv1.3 | LOW | KEEP |
| Cloudflare origin cert | Expires Aug 15 2026 | MEDIUM | Plan renewal |
| Source code on VM | `/srv/banzami/src/`, `/srv/banzamia/src/` | MEDIUM | Migrate off VM |
| No swap | OOM risk | MEDIUM | Configure swap |
| Stale backups | 16 days, one 0-byte | CRITICAL | Restore backups |
| Redis password | Configured | LOW | KEEP |
| Postgres password | Configured via env | LOW | KEEP |

**Port 4001 exposure detail:**
Docker adds iptables rules that bypass ufw. The `banzamia-api-1` container binds to `0.0.0.0:4001` and is reachable from the internet despite ufw not allowing port 4001. Fix: remove the ports mapping from the banzamia docker-compose and add a proper nginx proxy route.

---

## Monitoring and Operations

| Item | Status |
|------|--------|
| Cron jobs | certbot, e2scrub_all, sysstat — all standard OS crons |
| Custom backup cron | NOT FOUND — backups were manual or from deleted cron |
| Application monitoring | No dedicated monitoring container |
| Log rotation | Docker handles container log rotation |
| Health checks | Configured on all containers (3 currently failing) |

---

## Classification Summary

| Classification | Containers/Services | Action |
|---------------|---------------------|--------|
| **KEEP** | postgres, redis, core-api, api-gateway, admin-api, public-api, pay-frontend, core-api-staging, nginx | No change required |
| **UPDATE** | docs-frontend, banzamia-api, public-api-staging | Priority updates before website launch |
| **INVESTIGATE + FIX** | admin-frontend, dashboard-frontend, checkout-frontend | Operator product issue — investigate separately |
| **MIGRATE** | /srv/banzami/src/, /srv/banzamia/src/ | Source code should not be on production VM |
| **REMOVE** | Stale Docker images/layers | Run docker system prune after audit |
