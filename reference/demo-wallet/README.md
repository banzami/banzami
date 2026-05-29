# Demo Wallet

A minimal browser-based wallet UI for experimenting with the Banza sandbox.

## Usage

1. Start the sandbox operator (port 3100):
   ```bash
   cd reference && cargo run --bin sandbox-operator
   # or
   cd reference && docker compose up
   ```

2. Open `index.html` in your browser:
   ```bash
   open reference/demo-wallet/index.html
   ```

No build step. No framework. Pure HTML + vanilla JavaScript.

## What it shows

- Balances for the three seed wallets (Merchant A, Merchant B, Consumer)
- Create new in-memory wallets
- Send transfers between wallets
- Transfer history (newest first)
- Sandbox health indicator

## What it is not

This is a developer tool, not a consumer product. It has no authentication,
no real payment processing, and no connection to any bank or payment rail.

State resets when the sandbox operator restarts.
