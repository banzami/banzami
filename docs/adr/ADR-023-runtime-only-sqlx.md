# ADR-023 — Runtime-Only sqlx Queries in Public Crates

**Status:** Accepted  
**Date:** 2026-05-28  
**Author:** Banzami Organisation  
**Deciders:** Fidel Monteiro (Founder)  
**Supersedes:** None

---

## Context

sqlx provides two modes for database queries:

**Compile-time macros** (`sqlx::query!()`, `sqlx::query_as!()`): SQL is verified against the database schema at compile time. Requires either a live `DATABASE_URL` environment variable or a pre-generated `.sqlx/` query cache. Produces excellent type safety.

**Runtime queries** (`sqlx::query()`, `sqlx::query_as::<_, T>()`): SQL is parsed at runtime. No database required to build. Type mapping is done via `#[derive(sqlx::FromRow)]` struct field names.

The Banzami kernel was initially written with compile-time macros (inherited from the private Banza codebase). This meant that any developer who cloned the public repository could not run `cargo build` without a PostgreSQL database and the `DATABASE_URL` environment variable set.

This directly violated the contributor experience goal: `git clone → cargo build`.

## Decision

All repository implementations in public Banzami crates use **runtime sqlx queries only**.

Rules:
- No `sqlx::query!()` or `sqlx::query_as!()` macros in `core/crates/**`
- No `.sqlx/` query cache files in the repository
- All `SELECT` statements use explicit column lists (not `SELECT *`) except for simple identity lookups
- Row structs use `#[derive(sqlx::FromRow)]` with field names matching column aliases

The migration was applied in commit `3920912` to acquiring, compliance, reconciliation, settlement, and payouts repositories.

## Trade-offs accepted

**Lost:** Compile-time SQL verification against the live schema. A typo in a column name won't be caught until the query runs.

**Retained:** Compile-time type safety via `FromRow` derive. The struct field types must be compatible with the database column types, caught at runtime during the first query.

**Mitigated by:** Integration tests in the private Banza operator (which uses a live database) catch SQL errors before production deployment.

## Private Banza operator

The private Banza codebase may continue using compile-time sqlx macros (it has a live database available in CI). The kernel's decision to use runtime queries does not impose this choice on operators. Operators can use whatever sqlx mode suits their build environment.

## Consequences

**Positive:**
- `cargo build` works without a database for any contributor
- No `.sqlx/` cache files to maintain and keep in sync with schema migrations
- Contributors can run unit tests without any external infrastructure

**Negative:**
- SQL errors (misspelled columns, type mismatches) not caught until runtime
- No compile-time guarantee that the SQL is valid against the current schema
- `SELECT *` queries are discouraged (explicit column lists required) to avoid silent schema mismatch

## Alternatives considered

**Commit `.sqlx/` query cache:** Rejected. Requires regenerating the cache on every schema change, creating a maintenance burden and frequent merge conflicts.

**Feature flag to switch between modes:** Considered. Adds complexity without clear benefit — contributors always need the runtime mode.

**Abstract repository traits with no sqlx dependency:** Considered for long-term. A pure trait interface for repositories would remove any database dependency from the kernel. Deferred — current approach is pragmatic and good enough.
