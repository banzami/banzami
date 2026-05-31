"""BANZA exception hierarchy.

All exceptions raised by the SDK inherit from BanzaError, so callers
can either catch specific sub-classes or handle everything in one place.
"""

from __future__ import annotations


class BanzaError(Exception):
    """Base class for all BANZA SDK errors."""


class BanzaNetworkError(BanzaError):
    """Raised when a network-level failure occurs (connection refused, DNS, TLS)."""


class BanzaTimeoutError(BanzaNetworkError):
    """Raised when the HTTP request exceeds the configured timeout."""


class BanzaAPIError(BanzaError):
    """Raised when the API returns a structured error response (HTTP 4xx / 5xx)."""

    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        request_id: str | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code        = code
        self.message     = message
        self.request_id  = request_id

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"status_code={self.status_code}, "
            f"code={self.code!r}, "
            f"message={self.message!r})"
        )


class BanzaAuthenticationError(BanzaAPIError):
    """HTTP 401 — the API key is missing or invalid."""


class BanzaPermissionError(BanzaAPIError):
    """HTTP 403 — the API key lacks permission for this operation."""


class BanzaNotFoundError(BanzaAPIError):
    """HTTP 404 — the requested resource does not exist."""


class BanzaConflictError(BanzaAPIError):
    """HTTP 409 — a conflict with an existing resource (e.g. duplicate idempotency key)."""


class BanzaValidationError(BanzaAPIError):
    """HTTP 422 — the request body failed server-side validation."""


class BanzaRateLimitError(BanzaAPIError):
    """HTTP 429 — too many requests; the SDK will retry automatically."""


class BanzaInsufficientFundsError(BanzaAPIError):
    """Insufficient funds to complete the financial operation."""


class BanzaServerError(BanzaAPIError):
    """HTTP 5xx — a transient server-side error; the SDK will retry automatically."""


class BanzaWebhookSignatureError(BanzaError):
    """Raised when a webhook payload fails HMAC-SHA256 signature verification."""


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

_STATUS_MAP: dict[int, type[BanzaAPIError]] = {
    401: BanzaAuthenticationError,
    403: BanzaPermissionError,
    404: BanzaNotFoundError,
    409: BanzaConflictError,
    422: BanzaValidationError,
    429: BanzaRateLimitError,
}


def api_error_from_response(
    status_code: int,
    code: str,
    message: str,
    request_id: str | None = None,
) -> BanzaAPIError:
    """Return the most specific BanzaAPIError subclass for a given HTTP status."""
    if code == "INSUFFICIENT_FUNDS":
        return BanzaInsufficientFundsError(status_code, code, message, request_id)
    if status_code >= 500:
        return BanzaServerError(status_code, code, message, request_id)
    cls = _STATUS_MAP.get(status_code, BanzaAPIError)
    return cls(status_code, code, message, request_id)
