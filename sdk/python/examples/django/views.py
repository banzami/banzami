"""Django views example — integrating BANZA into a Django project.

In your Django settings add:
    BANZA_API_KEY      = "bz_live_..."
    BANZA_WEBHOOK_SECRET = "whsec_..."

In urls.py:
    path("webhooks/banzami/", views.banza_webhook),
    path("checkout/qr/", views.create_qr_checkout),
"""

from __future__ import annotations

import asyncio
import json
import os

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from banza import BanzaClient, BanzaWebhookSignatureError
from banza.utils.money import to_minor


def _get_client() -> BanzaClient:
    return BanzaClient(
        api_key=getattr(settings, "BANZA_API_KEY", os.environ["BANZA_API_KEY"]),
        webhook_secret=getattr(settings, "BANZA_WEBHOOK_SECRET", None),
    )


# ---------------------------------------------------------------------------
# QR checkout
# ---------------------------------------------------------------------------

@require_POST
def create_qr_checkout(request):
    """POST {"amount_kz": 5000} → {"qr_id": ..., "payload": ...}"""
    from datetime import datetime, timedelta, timezone

    body = json.loads(request.body)
    amount_kz = float(body["amount_kz"])
    owner_id  = body.get("owner_id") or os.environ["BANZA_WALLET_ID"]

    async def _create():
        async with _get_client() as client:
            return await client.qr_payments.create_dynamic(
                owner_id=owner_id,
                amount=to_minor(amount_kz, "AOA"),
                expires_at=datetime.now(tz=timezone.utc) + timedelta(minutes=15),
            )

    qr = asyncio.run(_create())
    return JsonResponse({
        "qr_id":   qr.qr_code.id,
        "payload": qr.payload,
        "status":  qr.qr_code.status,
    })


# ---------------------------------------------------------------------------
# Webhook
# ---------------------------------------------------------------------------

@csrf_exempt
@require_POST
def banza_webhook(request):
    """Receive and verify BANZA webhook events."""
    signature = request.headers.get("Banza-Signature", "")
    raw       = request.body

    webhook_secret = getattr(settings, "BANZA_WEBHOOK_SECRET", os.environ.get("BANZA_WEBHOOK_SECRET", ""))
    client = _get_client()

    try:
        event = client.webhooks.construct_event(raw, signature, webhook_secret=webhook_secret)
    except BanzaWebhookSignatureError:
        return JsonResponse({"error": "invalid signature"}, status=400)
    except ValueError as exc:
        return JsonResponse({"error": str(exc)}, status=400)

    if event.type == "transaction.completed":
        _handle_transaction_completed(event.payload)
    elif event.type == "payout.completed":
        _handle_payout_completed(event.payload)

    return JsonResponse({"received": True})


def _handle_transaction_completed(payload: dict) -> None:
    print(f"[banzami] Transaction completed: {payload.get('transaction_id')}")


def _handle_payout_completed(payload: dict) -> None:
    print(f"[banzami] Payout completed: {payload.get('payout_id')}")
