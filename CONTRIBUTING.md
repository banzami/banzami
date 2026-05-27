# Contributing to Banzami

Thank you for your interest in contributing to Banzami — open-source payment infrastructure for Angola.

## What you can contribute to

| Area | Examples |
|---|---|
| **SDKs** | Bug fixes, new language features, better error messages, test coverage |
| **Contracts** | OpenAPI corrections, webhook schema improvements, QR spec clarifications |
| **Documentation** | Translations, examples, guides, ADR discussions |
| **Integrations** | New framework plugins, commerce platform adapters |
| **SDK certification** | New test vectors, edge case coverage |

## What is out of scope here

- The Banza commercial product (apps, backend services, production infrastructure)
- Banza design system and branded UI components
- Production deployment and operational tooling

## How to contribute

### 1. Open an issue first

For anything beyond a trivial bug fix, open an issue to discuss the change before writing code. This prevents wasted effort and aligns with Banzami's protocol governance.

### 2. Fork and branch

```bash
git clone https://github.com/banzami/banzami.git
cd banzami
git checkout -b feature/your-change
```

### 3. Make your change

Follow the existing code style per language:
- TypeScript: ESLint + Prettier (`.eslintrc`, `.prettierrc`)
- Python: Ruff + mypy (`pyproject.toml`)
- PHP: PSR-12
- Go: `gofmt`
- Dart/Flutter: `dart format`

### 4. Test

Every SDK has a test suite. Run it before submitting:

```bash
# TypeScript
cd sdk/typescript && npm test

# Python
cd sdk/python && pytest

# Go
cd sdk/go && go test ./...
```

SDK changes must pass the certification suite:

```bash
# Webhook signature vectors
cd sdk-certification && python python/test_webhook_vectors.py
```

### 5. Submit a pull request

- Keep PRs focused — one change per PR
- Include a clear description of what changed and why
- Reference any related issues

## Protocol changes

Changes to `contracts/` (OpenAPI, webhooks, QR, events) require an Architecture Decision Record (ADR) in `docs/adr/`. Protocol changes affect all SDK implementations and must be discussed before merging.

## SDK certification

If you are implementing a new language SDK, run the certification suite against your implementation before claiming Banzami compatibility. All implementations must pass the signature vectors in `contracts/sdk-certification/`.

## Code of conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## License

By contributing, you agree that your contributions will be licensed under the [Apache 2.0 License](LICENSE).
