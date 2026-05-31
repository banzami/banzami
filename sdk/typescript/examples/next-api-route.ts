// Run: deploy as app/api/checkout/route.ts in a Next.js App Router project

import { NextRequest, NextResponse } from 'next/server';
import { BanzaClient }             from '@banza/sdk';

const banzaClient = new BanzaClient({
  baseUrl: process.env.BANZA_GATEWAY_URL!,
  apiKey:  process.env.BANZA_API_KEY!,
});

export async function POST(req: NextRequest): Promise<NextResponse> {
  const { amountMinor, description, orderId } = await req.json() as {
    amountMinor: number;
    description: string;
    orderId:     string;
  };

  const link = await banzaClient.createPaymentLink({
    merchantId:  process.env.BANZA_MERCHANT_ID!,
    walletId:    process.env.BANZA_WALLET_ID!,
    amountMinor,
    currency:    'AOA',
    description,
  });

  return NextResponse.json({
    checkoutUrl: `https://pay.banza.network/${link.slug}`,
    linkId:      link.id,
  });
}
