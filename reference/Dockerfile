# Banzami Reference Sandbox Operator
#
# Multi-stage build — compiles the sandbox operator from the monorepo root.
# The final image contains only the binary (no Rust toolchain).
#
# Build context must be the monorepo root so path deps resolve:
#   docker build -f reference/Dockerfile .
#
# This image is ONLY for local development. Do not deploy to production.

FROM rust:1.78-slim AS builder

WORKDIR /build

# Install system deps needed by some crates (openssl, pkg-config)
RUN apt-get update && apt-get install -y --no-install-recommends \
    pkg-config \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy core kernel crates (path dependencies)
COPY core/crates/ core/crates/
COPY core/Cargo.toml core/Cargo.toml
COPY core/Cargo.lock core/Cargo.lock

# Copy reference workspace
COPY reference/Cargo.toml reference/Cargo.toml
COPY reference/Cargo.lock reference/Cargo.lock
COPY reference/fake-acquirer/ reference/fake-acquirer/
COPY reference/local-notifications/ reference/local-notifications/
COPY reference/simulated-settlement/ reference/simulated-settlement/
COPY reference/sandbox-operator/ reference/sandbox-operator/

WORKDIR /build/reference

RUN cargo build --release --bin sandbox-operator

# -------------------------------------------------------------------------
# Runtime image
FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /build/reference/target/release/sandbox-operator /usr/local/bin/sandbox-operator

ENV PORT=3100
ENV RUST_LOG=sandbox_operator=info,banzami=info,info

EXPOSE 3100

ENTRYPOINT ["/usr/local/bin/sandbox-operator"]
