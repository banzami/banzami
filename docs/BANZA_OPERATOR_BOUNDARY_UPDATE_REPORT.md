# BANZA Operator Boundary Update Report

**Mission:** BANZAMI-INSTITUTIONAL-SEPARATION-001  
**Date:** 2026-05-30  
**Scope:** Updates to the BANZA protocol organization to reflect Banzami's institutional separation.

---

## What Changed

Banzami has been institutionally separated from the BANZA protocol organization.

The BANZA protocol organization (`github.com/banza-protocol`) now contains **only**:
- `banza` — open protocol (kernel, SDKs, contracts, certification)
- `banzai` — Protocol Operating System

Banzami has moved to its own GitHub organization:
- `github.com/banzami/banzami`

---

## Files Updated in This Repo

### Active documentation (not historical migration notes)

| File | Change |
|------|--------|
| `README.md` | Updated Banzami link → `github.com/banzami/banzami`; added institutional note |
| `core/Cargo.toml` | Updated repository field to new Banzami org URL |
| `core/README.md` | Updated Banzami git dependency examples |
| `docs/getting-started.md` | Updated clone URL for sandbox operator |
| `docs/adr/ADR-024-reference-operator.md` | Updated clone URL |
| `sdk/go/README.md` | Updated Banzami references |
| `BANZA_GOVERNANCE.md` | Added explicit Operator Independence section |

### Domain references

`banzami.org` → `banzami.com` across 54 active files including:
- `BANZA_GOVERNANCE.md`
- `BANZA_SECURITY.md`
- SDK files (`sdk/go/`, `sdk/typescript/`, `sdk/python/`, `sdk/php/`)
- Integration plugin files
- ADR documents
- API documentation

---

## Institutional Boundary Statement

The following statement is now in `BANZA_GOVERNANCE.md`:

> **Banzami is an independent commercial company.** BANZA is not owned by Banzami. BANZA is not governed by Banzami. Banzami does not control the certification framework. Banzami is not part of the BANZA protocol organization. Banzami may contribute to BANZA via the ADR process, like any other operator. The BANZA protocol continues to exist if Banzami ceases operations.

---

## What Was NOT Changed

- Historical migration docs in `docs/migration/` — preserved as audit record
- Historical audit docs in `docs/audit/` — preserved as audit record
- `github.com/banza-protocol/banza` — unchanged (this repo stays here)
- `github.com/banza-protocol/banzai` — unchanged (banzai stays here)

---

## CI Status

All CI checks pass. The README and governance docs are the only material changes — no compiled code was modified.

---

*Produced by: BANZAMI-INSTITUTIONAL-SEPARATION-001 — 2026-05-30*
