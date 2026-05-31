"""BANZA Python SDK.

Quick start:

    from banza import BanzaClient

    async with BanzaClient(api_key="bz_live_...") as client:
        tx = await client.transactions.create(amount=50000, currency="AOA")
        print(tx.id)
"""

from .client import BanzaClient, BanzaHooks
from .config import BanzaConfig, LIVE_URL, SANDBOX_URL
from .exceptions import (
    BanzaAPIError,
    BanzaError,
    BanzaAuthenticationError,
    BanzaConflictError,
    BanzaInsufficientFundsError,
    BanzaNotFoundError,
    BanzaPermissionError,
    BanzaRateLimitError,
    BanzaServerError,
    BanzaTimeoutError,
    BanzaValidationError,
    BanzaNetworkError,
    BanzaWebhookSignatureError,
)
from .models import (
    ApiKey,
    Dispute,
    DisputeStatus,
    Merchant,
    NewApiKey,
    Payout,
    PayoutStatus,
    PaymentLink,
    PaymentLinkStatus,
    PaymentRequest,
    PaymentRequestStatus,
    QrCode,
    QrPayment,
    Refund,
    RefundStatus,
    Transaction,
    TransactionStatus,
    Transfer,
    TransferStatus,
    Wallet,
    WalletBalance,
    WebhookEndpoint,
    WebhookEvent,
    WebhookEventType,
)
from .pagination import Page, auto_paginate
from .signature import generate_test_signature
from .utils import format_minor, new_idempotency_key, to_minor

__version__ = "0.1.0"

__all__ = [
    # Primary entry point
    "BanzaClient",
    "BanzaClient",
    "BanzaConfig",
    "BanzaHooks",
    # Exceptions
    "BanzaError",
    "BanzaAPIError",
    "BanzaAuthenticationError",
    "BanzaPermissionError",
    "BanzaNotFoundError",
    "BanzaConflictError",
    "BanzaValidationError",
    "BanzaRateLimitError",
    "BanzaInsufficientFundsError",
    "BanzaServerError",
    "BanzaNetworkError",
    "BanzaTimeoutError",
    "BanzaWebhookSignatureError",
    # Models
    "Transaction",
    "TransactionStatus",
    "QrCode",
    "QrPayment",
    "Transfer",
    "TransferStatus",
    "Payout",
    "PayoutStatus",
    "Wallet",
    "WalletBalance",
    "Merchant",
    "ApiKey",
    "NewApiKey",
    "PaymentLink",
    "PaymentLinkStatus",
    "Refund",
    "RefundStatus",
    "Dispute",
    "DisputeStatus",
    "PaymentRequest",
    "PaymentRequestStatus",
    "WebhookEndpoint",
    "WebhookEvent",
    "WebhookEventType",
    # Test helpers
    "generate_test_signature",
    # Pagination
    "Page",
    "auto_paginate",
    # Money utilities
    "format_minor",
    "to_minor",
    "new_idempotency_key",
]
