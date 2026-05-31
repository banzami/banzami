// Run: ts-node examples/payment-link.ts

import { BanzaClient } from '../src/client';

const client = new BanzaClient({
  gatewayUrl: process.env.BANZA_GATEWAY_URL ?? 'https://api.banza.network',
  apiKey:     process.env.BANZA_API_KEY!,
});

const link = await client.createPaymentLink({
  merchant_id:  process.env.BANZA_MERCHANT_ID!,
  wallet_id:    process.env.BANZA_WALLET_ID!,
  amount_minor: 15000,
  currency:     'AOA',
  description:  `Pedido #${Date.now()}`,
});

console.log('Checkout URL:', `https://pay.banza.network/${link.slug}`);
console.log('Link ID:', link.id);
console.log('Status:', link.status);
