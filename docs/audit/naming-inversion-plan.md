# Naming Inversion Plan — BANZA-NAMING-INVERSION

**Version:** 1.0  
**Date:** 2026-05-29  
**ADR:** ADR-025 — Ecosystem Naming Inversion  
**Status:** Planning complete — migration not yet started

---

## Summary

The legally approved company name is **Banza**. The current architecture (ADR-016) assigns "Banza" to the protocol/infrastructure layer and "Banzami" to the user-facing product — the opposite of what the legal registration requires.

ADR-025 formally inverts the naming:

| Role | Before | After |
|------|--------|-------|
| Protocol / ecosystem / kernel | Banza | **Banzami** |
| Product / reference operator | Banzami | **Banza** |
| Protocol Operating System | BanzAI | **BanzAI** |

---

## Migration Documents

All migration planning documents live in `docs/migration/`:

| File | Purpose |
|------|---------|
| `naming-inversion-map.md` | Full table of legacy → new name mappings with migration notes |
| `naming-classification-rules.md` | Occurrence class definitions and rename decision table |
| `DO-NOT-GLOBAL-REPLACE.md` | Warning against batch search-and-replace; explains why it fails |

---

## What Has Been Done

- [x] ADR-025 written and accepted (`docs/adr/ADR-025-ecosystem-naming-inversion.md`)
- [x] Migration map created (`docs/migration/naming-inversion-map.md`)
- [x] Classification rules created (`docs/migration/naming-classification-rules.md`)
- [x] Global-replace warning created (`docs/migration/DO-NOT-GLOBAL-REPLACE.md`)
- [x] ADR-016 marked as superseded by ADR-025

## What Has NOT Been Done Yet

- [ ] Wave 1: Documentation rename (ADRs, READMEs, BANZAMI_REFERENCE.md)
- [ ] Wave 2: Website copy rename (banzami.org pages, metadata, SVG text)
- [ ] Wave 3: AI OS rename (BanzAI → BanzAI, components, routes, identifiers)
- [ ] Wave 4: Repository renames (requires separate ADR)
- [ ] Wave 5: Package/crate renames (requires separate ADR and deprecation plan)
- [ ] Wave 6: Domain/email migration (requires separate ADR and DNS plan)

---

## Protected Names (never rename without separate ADR)

- `banzami.org` — domain
- `contact@banzami.org` — email
- `github.com/banzami` — GitHub organization

---

## SDK Open Decision

The SDK name is unresolved. "Banzami SDK" (built on the Banzami protocol) is the natural fit after inversion, but the packages are currently published as `banza-*`. A separate decision is required before renaming any SDK packages.
