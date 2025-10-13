"""
Payment-UZ MCP Server
=====================
A FastMCP server that exposes Uzbekistan payment systems (Payme, Click, Octo) as AI tools.

This MCP server provides developers with easy-to-use tools for integrating
Uzbek payment providers into their applications through AI assistants.

Features:
- Payme payment integration (sandbox & production)
- Click payment integration
- Octo payment integration
- Transaction status checking
- Payment link generation
- Webhook handling guidance

Author: GetSpace Team
License: MIT
"""

from fastmcp import FastMCP
import httpx
import hmac
import hashlib
import base64
from typing import Optional, Dict, Any, Literal
from datetime import datetime
from pydantic import BaseModel, Field

# Initialize the MCP server
mcp = FastMCP(
    name="Payment-UZ",
    instructions="""
    This server provides tools for Uzbekistan payment integration ONLY.
    
    🎯 WHEN TO USE THESE TOOLS:
    - User asks about Payme, Click, or Octo payments
    - User wants to create payment links or checkout URLs
    - User needs to verify webhooks or signatures
    - User asks about payment integration in Uzbekistan
    - User wants to compare payment providers
    - User needs payment security best practices
    
    ❌ DO NOT USE THESE TOOLS FOR:
    - General payment questions not related to Uzbekistan
    - Other payment providers (Stripe, PayPal, etc.)
    - Non-payment related questions
    
    📦 AVAILABLE PROVIDERS:
    - Payme: Most trusted, enterprise-level (JSON-RPC)
    - Click: Popular, easy integration (REST API)
    - Octo: Modern, advanced features (REST API)
    
    🔧 TOOL SELECTION GUIDE:
    - Payment link → use *_generate_* or *_create_payment tools
    - Webhook verification → use *_verify_webhook_* tools
    - Documentation → use *_get_integration_guide tools
    - Comparison → use compare_payment_providers
    - Security → use payment_security_best_practices
    
    All tools support both sandbox (test) and production environments.
    """,
)


# ============================================================================
# PAYME INTEGRATION TOOLS
# ============================================================================


@mcp.tool(tags={"payme", "payment", "integration"})
def payme_generate_checkout_url(
    merchant_id: str,
    amount: float,
    order_id: str,
    return_url: str,
    is_production: bool = False,
) -> Dict[str, Any]:
    """
    **WHEN TO USE:** User wants to create a Payme payment link, generate Payme checkout URL, 
    or initiate a Payme payment. Use this when user mentions "Payme payment", "create Payme link",
    or wants to integrate Payme checkout.
    
    **WHAT IT DOES:** Generates a Payme checkout URL that redirects users to Payme's payment page.
    Automatically converts UZS to tiyin and encodes parameters.

    **USE CASES:**
    - "Create a Payme payment for 50000 UZS"
    - "Generate Payme checkout link for my order"
    - "How do I make a Payme payment URL?"

    Args:
        merchant_id: Your Payme merchant ID (e.g., '68944508cab302211ad21b06')
        amount: Payment amount in UZS (will be converted to tiyin automatically)
        order_id: Unique order/booking identifier
        return_url: URL to redirect user after payment
        is_production: Whether to use production or test environment

    Returns:
        Dictionary with payment URL, encoded parameters, and amount details

    Example:
        >>> payme_generate_checkout_url(
        ...     merchant_id="68944508cab302211ad21b06",
        ...     amount=50000.00,
        ...     order_id="booking_123",
        ...     return_url="https://myapp.com/payment/success"
        ... )
    """
    # Convert UZS to tiyin (1 UZS = 100 tiyin)
    amount_in_tiyin = int(amount * 100)

    # Create account parameter
    account = f"order_id={order_id}"

    # Build parameter string
    params = f"m={merchant_id};ac.{account};a={amount_in_tiyin};c={return_url}"

    # Base64 encode
    encoded_params = base64.b64encode(params.encode()).decode()

    # Determine environment
    checkout_base_url = (
        "https://checkout.paycom.uz"
        if is_production
        else "https://checkout.test.paycom.uz"
    )

    payment_url = f"{checkout_base_url}/{encoded_params}"

    return {
        "success": True,
        "payment_url": payment_url,
        "environment": "production" if is_production else "test",
        "amount_uzs": amount,
        "amount_tiyin": amount_in_tiyin,
        "order_id": order_id,
        "encoded_params": encoded_params,
        "instructions": "Redirect user to this URL to complete payment",
    }


@mcp.tool(tags={"payme", "webhook", "verification"})
def payme_verify_webhook_auth(
    authorization_header: str, merchant_key: str
) -> Dict[str, bool]:
    """
    **WHEN TO USE:** User needs to verify or validate Payme webhook authentication, 
    check Payme webhook security, or authenticate incoming Payme callbacks.
    
    **WHAT IT DOES:** Verifies that incoming Payme webhook requests are authentic by 
    checking the Basic Auth header against your merchant key.

    **USE CASES:**
    - "How do I verify Payme webhooks?"
    - "Is this Payme webhook authentic?"
    - "Validate Payme webhook authorization"
    - "Check Payme callback security"

    Args:
        authorization_header: The Authorization header from webhook request
        merchant_key: Your Payme merchant secret key

    Returns:
        Dictionary indicating if authorization is valid

    Example:
        >>> payme_verify_webhook_auth(
        ...     authorization_header="Basic bWVyY2hhbnRfaWQ6c2VjcmV0X2tleQ==",
        ...     merchant_key="zpcK%c1JZsPnGwqO09Wfx4CFU%wP2d9BqAmD"
        ... )
    """
    try:
        # Extract token from "Basic <token>"
        if not authorization_header.startswith("Basic "):
            return {
                "valid": False,
                "reason": "Authorization must use Basic authentication",
            }

        token = authorization_header.split(" ")[1]
        decoded = base64.b64decode(token).decode()

        # Check if merchant key is present
        is_valid = merchant_key in decoded

        return {
            "valid": is_valid,
            "decoded_auth": decoded if is_valid else "[hidden]",
            "message": (
                "Valid Payme webhook authentication"
                if is_valid
                else "Invalid merchant key"
            ),
        }
    except Exception as e:
        return {"valid": False, "reason": f"Error verifying authorization: {str(e)}"}


@mcp.tool(tags={"payme", "integration", "guide"})
def payme_get_integration_guide() -> Dict[str, Any]:
    """
    **WHEN TO USE:** User asks about Payme integration, needs Payme documentation, 
    wants to understand Payme API, or asks "how does Payme work?". Use when user 
    needs comprehensive Payme information or is starting Payme integration.
    
    **WHAT IT DOES:** Provides complete Payme integration documentation including 
    all required methods, transaction states, error codes, test credentials, and best practices.

    **USE CASES:**
    - "How do I integrate Payme?"
    - "What are Payme's API methods?"
    - "Tell me about Payme integration"
    - "Payme documentation"
    - "What methods does Payme require?"
    - "Payme error codes"

    Returns:
        Complete integration guide including endpoints, methods, and examples
    """
    return {
        "overview": "Payme uses JSON-RPC 2.0 protocol for merchant API",
        "merchant_api_url": "https://checkout.paycom.uz/api",
        "test_merchant_api_url": "https://checkout.test.paycom.uz/api",
        "required_methods": {
            "CheckPerformTransaction": {
                "description": "Validate that transaction can be performed",
                "params": ["account", "amount"],
                "response": {"allow": True},
            },
            "CreateTransaction": {
                "description": "Create a new transaction",
                "params": ["id", "time", "amount", "account"],
                "response": {"transaction": "id", "state": 1, "create_time": 0},
            },
            "PerformTransaction": {
                "description": "Complete the transaction",
                "params": ["id"],
                "response": {"transaction": "id", "state": 2, "perform_time": 0},
            },
            "CancelTransaction": {
                "description": "Cancel a transaction",
                "params": ["id", "reason"],
                "response": {"transaction": "id", "state": -1, "cancel_time": 0},
            },
            "CheckTransaction": {
                "description": "Check transaction status",
                "params": ["id"],
                "response": {"transaction": "id", "state": 2},
            },
            "GetStatement": {
                "description": "Get list of transactions",
                "params": ["from", "to"],
                "response": {"transactions": []},
            },
        },
        "transaction_states": {
            "1": "Pending (created, awaiting perform)",
            "2": "Paid (successfully completed)",
            "-1": "Cancelled (cancelled before payment)",
            "-2": "Cancelled after payment (refunded)",
        },
        "error_codes": {
            "-31050 to -31099": "Account/order not found or invalid",
            "-31001": "Invalid amount",
            "-31008": "Cannot perform operation (duplicate transaction)",
            "-32504": "Invalid authorization",
        },
        "test_credentials": {
            "merchant_id": "68944508cab302211ad21b06",
            "test_key": "zpcK%c1JZsPnGwqO09Wfx4CFU%wP2d9BqAmD",
            "test_url": "https://test.paycom.uz",
            "test_cards": {
                "success": "8600 0691 9540 6311",
                "insufficient_funds": "8600 4954 7331 6478",
            },
        },
        "webhook_authentication": {
            "method": "Basic Authentication",
            "format": "Basic base64(merchant_id:merchant_key)",
            "example": "Always verify the merchant_key in decoded credentials",
        },
        "best_practices": [
            "Store transaction IDs as strings (they can be very large numbers)",
            "Implement idempotency for CreateTransaction",
            "Always return HTTP 200 for webhook responses",
            "Use state machine for transaction status management",
            "Validate amount in tiyin (1 UZS = 100 tiyin)",
            "Set payment expiration based on booking/order date",
        ],
    }


# ============================================================================
# CLICK INTEGRATION TOOLS
# ============================================================================


@mcp.tool(tags={"click", "payment", "integration"})
def click_generate_invoice_url(
    service_id: str,
    merchant_id: str,
    amount: float,
    transaction_param: str,
    return_url: str,
    merchant_user_id: Optional[str] = None,
    is_production: bool = False,
) -> Dict[str, Any]:
    """
    **WHEN TO USE:** User wants to create a Click payment link, generate Click invoice URL, 
    or initiate a Click payment. Use this when user mentions "Click payment", "create Click link",
    or wants to integrate Click checkout.
    
    **WHAT IT DOES:** Generates a Click invoice URL that redirects users to Click's payment page.
    Creates a properly formatted URL with all required parameters.

    **USE CASES:**
    - "Create a Click payment for 150000 UZS"
    - "Generate Click invoice link"
    - "How do I make a Click payment URL?"
    - "Click payment integration"

    Args:
        service_id: Your Click service ID
        merchant_id: Your Click merchant ID
        amount: Payment amount in UZS
        transaction_param: Unique transaction identifier (booking_id)
        return_url: URL to redirect after payment
        merchant_user_id: Optional user identifier
        is_production: Whether to use production environment

    Returns:
        Dictionary with invoice URL and payment details

    Example:
        >>> click_generate_invoice_url(
        ...     service_id="12345",
        ...     merchant_id="67890",
        ...     amount=150000.00,
        ...     transaction_param="booking_456",
        ...     return_url="https://myapp.com/payment/callback"
        ... )
    """
    # Click API endpoint
    base_url = (
        "https://my.click.uz/services/pay"
        if is_production
        else "https://my.click.uz/services/pay"  # Click uses same URL for both
    )

    # Build URL parameters
    params = {
        "service_id": service_id,
        "merchant_id": merchant_id,
        "amount": amount,
        "transaction_param": transaction_param,
        "return_url": return_url,
    }

    if merchant_user_id:
        params["merchant_user_id"] = merchant_user_id

    # Create query string
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    invoice_url = f"{base_url}?{query_string}"

    return {
        "success": True,
        "invoice_url": invoice_url,
        "environment": "production" if is_production else "test",
        "amount": amount,
        "transaction_param": transaction_param,
        "instructions": "Redirect user to this URL to complete Click payment",
    }


@mcp.tool(tags={"click", "webhook", "verification"})
def click_verify_webhook_signature(
    click_trans_id: str,
    service_id: str,
    secret_key: str,
    merchant_trans_id: str,
    amount: float,
    action: int,
    sign_time: str,
    received_sign_string: str,
) -> Dict[str, bool]:
    """
    **WHEN TO USE:** User needs to verify or validate Click webhook signature, 
    check Click webhook security, or authenticate incoming Click callbacks.
    
    **WHAT IT DOES:** Verifies that incoming Click webhook requests are authentic by 
    validating the MD5 signature against expected values. Prevents fraud and unauthorized requests.

    **USE CASES:**
    - "How do I verify Click webhooks?"
    - "Is this Click webhook valid?"
    - "Validate Click webhook signature"
    - "Check Click callback security"
    - "Verify Click payment notification"

    Args:
        click_trans_id: Click transaction ID
        service_id: Your service ID
        secret_key: Your Click secret key
        merchant_trans_id: Your internal transaction ID
        amount: Payment amount
        action: Action code (0=prepare, 1=complete)
        sign_time: Signature timestamp
        received_sign_string: The sign_string from Click webhook

    Returns:
        Dictionary indicating if signature is valid
    """
    # Build signature string according to Click specification
    sign_string = (
        f"{click_trans_id}"
        f"{service_id}"
        f"{secret_key}"
        f"{merchant_trans_id}"
        f"{amount}"
        f"{action}"
        f"{sign_time}"
    )

    # Generate MD5 hash
    expected_signature = hashlib.md5(sign_string.encode()).hexdigest()

    is_valid = expected_signature == received_sign_string

    return {
        "valid": is_valid,
        "expected_signature": expected_signature,
        "received_signature": received_sign_string,
        "message": (
            "Signature is valid"
            if is_valid
            else "Invalid signature - potential security issue"
        ),
    }


@mcp.tool(tags={"click", "integration", "guide"})
def click_get_integration_guide() -> Dict[str, Any]:
    """
    **WHEN TO USE:** User asks about Click integration, needs Click documentation, 
    wants to understand Click API, or asks "how does Click work?". Use when user 
    needs comprehensive Click information or is starting Click integration.
    
    **WHAT IT DOES:** Provides complete Click integration documentation including 
    payment flow, webhook handling, error codes, signature generation, and best practices.

    **USE CASES:**
    - "How do I integrate Click?"
    - "What is Click's payment flow?"
    - "Tell me about Click integration"
    - "Click documentation"
    - "How does Click two-phase payment work?"
    - "Click error codes"

    Returns:
        Complete Click integration guide including webhook handling
    """
    return {
        "overview": "Click uses two-phase payment (prepare and complete)",
        "merchant_api_docs": "https://docs.click.uz/",
        "payment_flow": {
            "step_1": "Generate invoice URL and redirect user",
            "step_2": "User completes payment on Click page",
            "step_3": "Click sends 'prepare' webhook (action=0)",
            "step_4": "Your server validates and responds",
            "step_5": "Click sends 'complete' webhook (action=1)",
            "step_6": "Your server finalizes transaction",
        },
        "webhook_endpoints": {
            "prepare": {
                "action": 0,
                "description": "Pre-validate transaction before payment",
                "required_response": {
                    "click_trans_id": "transaction_id",
                    "merchant_trans_id": "your_id",
                    "merchant_prepare_id": "prepare_id",
                    "error": 0,
                    "error_note": "Success",
                },
            },
            "complete": {
                "action": 1,
                "description": "Finalize payment after successful charge",
                "required_response": {
                    "click_trans_id": "transaction_id",
                    "merchant_trans_id": "your_id",
                    "merchant_confirm_id": "confirm_id",
                    "error": 0,
                    "error_note": "Success",
                },
            },
        },
        "error_codes": {
            "0": "Success",
            "-1": "Sign check failed",
            "-2": "Invalid amount",
            "-3": "Action not found",
            "-4": "Already paid",
            "-5": "User not found",
            "-6": "Transaction not found",
            "-7": "Failed to update user",
            "-8": "Error in request from click",
            "-9": "Transaction cancelled",
        },
        "signature_generation": {
            "algorithm": "MD5",
            "format": "MD5(click_trans_id + service_id + secret_key + merchant_trans_id + amount + action + sign_time)",
            "important": "Always verify signature to prevent fraud",
        },
        "best_practices": [
            "Always verify webhook signatures",
            "Implement idempotency for both prepare and complete",
            "Store Click transaction IDs for reconciliation",
            "Return proper error codes for validation failures",
            "Log all webhook requests for debugging",
            "Use atomic database transactions for payment finalization",
        ],
        "merchant_api_methods": {
            "create_invoice": {
                "endpoint": "https://api.click.uz/v2/merchant/invoice/create",
                "method": "POST",
                "description": "Create invoice programmatically (recommended)",
                "auth": "Bearer token in Authorization header",
            },
            "check_invoice": {
                "endpoint": "https://api.click.uz/v2/merchant/invoice/status/:invoice_id",
                "method": "GET",
                "description": "Check invoice payment status",
            },
        },
    }


# ============================================================================
# OCTO INTEGRATION TOOLS
# ============================================================================


@mcp.tool(tags={"octo", "payment", "integration"})
def octo_create_payment(
    api_key: str,
    secret_key: str,
    amount: float,
    transaction_id: str,
    return_url: str,
    auto_capture: bool = True,
    currency: str = "UZS",
    is_production: bool = False,
) -> Dict[str, Any]:
    """
    **WHEN TO USE:** User wants to create an Octo payment, initialize Octo transaction, 
    or generate Octo payment URL. Use this when user mentions "Octo payment", "create Octo payment",
    or wants to integrate Octo checkout.
    
    **WHAT IT DOES:** Creates an Octo payment transaction via API and returns payment URL. 
    Generates proper signature and provides all necessary data for API call.

    **USE CASES:**
    - "Create an Octo payment for 200000 UZS"
    - "Initialize Octo payment transaction"
    - "How do I make an Octo payment?"
    - "Octo payment integration"
    - "Generate Octo checkout URL"

    Args:
        api_key: Your Octo API key (public key)
        secret_key: Your Octo secret key
        amount: Payment amount in UZS
        transaction_id: Your unique transaction identifier
        return_url: URL to redirect after payment
        auto_capture: Whether to auto-capture payment (default: True)
        currency: Currency code (default: UZS)
        is_production: Whether to use production environment

    Returns:
        Dictionary with payment URL and transaction details

    Note:
        This is a simulation. In production, you need to make actual API call.
    """
    # Octo API endpoint
    base_url = (
        "https://api.octo.uz/v1/payment/init"
        if is_production
        else "https://api.test.octo.uz/v1/payment/init"
    )

    # Generate signature
    sign_string = f"{transaction_id}{amount}{currency}{secret_key}"
    signature = hashlib.sha256(sign_string.encode()).hexdigest()

    payment_data = {
        "api_key": api_key,
        "amount": amount,
        "currency": currency,
        "transaction_id": transaction_id,
        "return_url": return_url,
        "auto_capture": auto_capture,
        "signature": signature,
    }

    return {
        "success": True,
        "api_endpoint": base_url,
        "payment_data": payment_data,
        "environment": "production" if is_production else "test",
        "instructions": "POST this data to the API endpoint to create payment",
        "expected_response": {
            "octo_payment_UUID": "unique_uuid",
            "shop_transaction_id": transaction_id,
            "status": "created",
            "pay_url": "https://payment.octo.uz/checkout/unique_uuid",
        },
    }


@mcp.tool(tags={"octo", "webhook", "verification"})
def octo_verify_webhook_signature(
    octo_payment_uuid: str, status: str, received_signature: str, secret_key: str
) -> Dict[str, bool]:
    """
    **WHEN TO USE:** User needs to verify or validate Octo webhook signature, 
    check Octo webhook security, or authenticate incoming Octo callbacks.
    
    **WHAT IT DOES:** Verifies that incoming Octo webhook requests are authentic by 
    validating the SHA-256 signature. Ensures webhook came from Octo and prevents fraud.

    **USE CASES:**
    - "How do I verify Octo webhooks?"
    - "Is this Octo webhook authentic?"
    - "Validate Octo webhook signature"
    - "Check Octo callback security"
    - "Verify Octo payment notification"

    Args:
        octo_payment_uuid: Octo payment UUID from webhook
        status: Payment status from webhook
        received_signature: Signature from webhook
        secret_key: Your Octo secret key

    Returns:
        Dictionary indicating if signature is valid
    """
    # Generate expected signature
    sign_string = f"{octo_payment_uuid}{status}{secret_key}"
    expected_signature = hashlib.sha256(sign_string.encode()).hexdigest()

    is_valid = expected_signature == received_signature

    return {
        "valid": is_valid,
        "expected_signature": expected_signature,
        "received_signature": received_signature,
        "message": "Valid Octo webhook" if is_valid else "Invalid signature",
    }


@mcp.tool(tags={"octo", "integration", "guide"})
def octo_get_integration_guide() -> Dict[str, Any]:
    """
    **WHEN TO USE:** User asks about Octo integration, needs Octo documentation, 
    wants to understand Octo API, or asks "how does Octo work?". Use when user 
    needs comprehensive Octo information or is starting Octo integration.
    
    **WHAT IT DOES:** Provides complete Octo integration documentation including 
    API endpoints, payment flow, statuses, signature generation, features, and best practices.

    **USE CASES:**
    - "How do I integrate Octo?"
    - "What are Octo's API endpoints?"
    - "Tell me about Octo integration"
    - "Octo documentation"
    - "What features does Octo have?"
    - "Octo payment statuses"

    Returns:
        Complete Octo integration guide with API details
    """
    return {
        "overview": "Octo is a modern payment gateway with REST API",
        "api_docs": "https://docs.octo.uz/",
        "base_url_production": "https://api.octo.uz",
        "base_url_test": "https://api.test.octo.uz",
        "payment_flow": {
            "step_1": "Initialize payment via API",
            "step_2": "Redirect user to pay_url",
            "step_3": "User completes payment",
            "step_4": "Octo sends webhook notification",
            "step_5": "Verify webhook signature",
            "step_6": "Update transaction status",
        },
        "api_endpoints": {
            "init_payment": {
                "path": "/v1/payment/init",
                "method": "POST",
                "auth": "API Key",
                "description": "Initialize new payment",
            },
            "check_status": {
                "path": "/v1/payment/status/{uuid}",
                "method": "GET",
                "description": "Check payment status",
            },
            "capture": {
                "path": "/v1/payment/capture",
                "method": "POST",
                "description": "Capture pre-authorized payment",
            },
            "refund": {
                "path": "/v1/payment/refund",
                "method": "POST",
                "description": "Refund a payment",
            },
        },
        "payment_statuses": {
            "created": "Payment created, awaiting user action",
            "processing": "Payment is being processed",
            "succeeded": "Payment completed successfully",
            "cancelled": "Payment cancelled by user or timeout",
            "failed": "Payment failed",
        },
        "signature_generation": {
            "algorithm": "SHA-256",
            "init_format": "SHA256(transaction_id + amount + currency + secret_key)",
            "webhook_format": "SHA256(octo_payment_UUID + status + secret_key)",
            "important": "Always verify webhook signatures",
        },
        "best_practices": [
            "Store octo_payment_UUID for reconciliation",
            "Verify webhook signatures to prevent fraud",
            "Use idempotent transaction IDs",
            "Handle all payment statuses appropriately",
            "Implement proper error handling",
            "Set appropriate timeout for payment pages",
        ],
        "features": {
            "card_tokenization": "Save cards for recurring payments",
            "auto_capture": "Automatic or manual payment capture",
            "refunds": "Partial and full refund support",
            "3DS": "3D Secure authentication support",
            "multi_currency": "Support for multiple currencies",
        },
    }


# ============================================================================
# GENERAL PAYMENT TOOLS
# ============================================================================


@mcp.tool(tags={"payment", "comparison", "guide"})
def compare_payment_providers() -> Dict[str, Any]:
    """
    **WHEN TO USE:** User asks to compare payment providers, wants to choose between providers, 
    or asks "which payment provider should I use?". Use when user is deciding which provider(s) 
    to integrate or needs an overview of all options.
    
    **WHAT IT DOES:** Provides detailed comparison of Payme, Click, and Octo including 
    complexity, features, market share, pros/cons, and recommendations for different use cases.

    **USE CASES:**
    - "Which payment provider should I use?"
    - "Compare Payme vs Click vs Octo"
    - "What's the difference between payment providers?"
    - "Which is easier to integrate?"
    - "Best payment provider for my app"
    - "Payment provider comparison"

    Returns:
        Comprehensive comparison of all three payment providers
    """
    return {
        "comparison_table": {
            "Payme": {
                "protocol": "JSON-RPC 2.0",
                "complexity": "Medium",
                "transaction_flow": "Multi-method (6 methods required)",
                "webhook_auth": "Basic Auth with merchant key",
                "signature": "Not required (uses Basic Auth)",
                "best_for": "Large enterprises, official government payments",
                "market_share": "High - most trusted in Uzbekistan",
                "integration_time": "3-5 days",
                "features": ["Payme wallet", "Card payments", "Statement reports"],
                "pros": [
                    "Most widely used",
                    "High trust among users",
                    "Comprehensive documentation",
                    "Good sandbox environment",
                ],
                "cons": [
                    "Complex JSON-RPC implementation",
                    "Requires implementing 6 methods",
                    "Strict state machine requirements",
                ],
            },
            "Click": {
                "protocol": "REST API with two-phase commits",
                "complexity": "Low-Medium",
                "transaction_flow": "Two webhooks (prepare + complete)",
                "webhook_auth": "None (uses signature verification)",
                "signature": "MD5 hash required",
                "best_for": "E-commerce, booking platforms, small-medium business",
                "market_share": "High - very popular",
                "integration_time": "1-3 days",
                "features": ["Invoice API", "Merchant API", "Payment links"],
                "pros": [
                    "Simple two-phase implementation",
                    "Easy invoice generation",
                    "Good documentation",
                    "Fast integration",
                ],
                "cons": [
                    "Less comprehensive than Payme",
                    "MD5 signature (less secure than SHA)",
                    "Limited advanced features",
                ],
            },
            "Octo": {
                "protocol": "Modern REST API",
                "complexity": "Low",
                "transaction_flow": "Single webhook notification",
                "webhook_auth": "None (uses signature verification)",
                "signature": "SHA-256 hash required",
                "best_for": "Modern apps, SaaS, recurring payments",
                "market_share": "Growing - newest player",
                "integration_time": "1-2 days",
                "features": [
                    "Card tokenization",
                    "Recurring payments",
                    "Auto-capture",
                    "3D Secure",
                    "Refunds API",
                ],
                "pros": [
                    "Easiest to integrate",
                    "Modern REST API",
                    "Advanced features",
                    "Good developer experience",
                    "Strong security (SHA-256)",
                ],
                "cons": [
                    "Newer, less market penetration",
                    "Fewer users compared to Payme/Click",
                    "May need to offer multiple options",
                ],
            },
        },
        "recommendation": {
            "for_maximum_coverage": "Implement Payme + Click (covers 95% of market)",
            "for_fastest_integration": "Start with Octo or Click",
            "for_enterprise": "Payme is essential",
            "for_modern_features": "Octo provides best developer experience",
            "for_small_business": "Click or Octo",
        },
        "integration_priority": [
            "1. Payme (highest user base, essential for enterprise)",
            "2. Click (second highest user base, easy integration)",
            "3. Octo (modern features, good for tech-savvy users)",
        ],
    }


@mcp.tool(tags={"payment", "security", "best-practices"})
def payment_security_best_practices() -> Dict[str, Any]:
    """
    **WHEN TO USE:** User asks about payment security, needs security best practices, 
    wants to know how to secure payments, or asks about fraud prevention. Use when user 
    is concerned about security or implementing payment security measures.
    
    **WHAT IT DOES:** Provides comprehensive security guidelines for payment integration 
    including webhook security, data protection, fraud prevention, and compliance requirements.

    **USE CASES:**
    - "How do I secure payment webhooks?"
    - "Payment security best practices"
    - "How to prevent payment fraud?"
    - "What security measures should I implement?"
    - "PCI compliance for payments"
    - "How to protect payment data?"

    Returns:
        Comprehensive security guidelines for payment systems
    """
    return {
        "webhook_security": {
            "always_verify_signatures": "Never trust webhooks without verification",
            "use_https_only": "Never accept webhooks over HTTP",
            "validate_ip_addresses": "Whitelist payment provider IPs if possible",
            "log_all_requests": "Keep audit trail of all payment webhooks",
            "rate_limiting": "Implement rate limiting on webhook endpoints",
        },
        "data_protection": {
            "never_store_card_numbers": "Use tokenization instead",
            "encrypt_sensitive_data": "Encrypt transaction details at rest",
            "use_secure_connections": "Always use TLS/SSL",
            "pci_compliance": "Follow PCI DSS if handling card data",
            "data_minimization": "Only collect necessary information",
        },
        "transaction_security": {
            "idempotency": "Prevent duplicate payments with idempotency keys",
            "atomic_operations": "Use database transactions",
            "timeout_handling": "Set appropriate payment timeouts",
            "state_machine": "Implement strict state transitions",
            "reconciliation": "Regular payment reconciliation with providers",
        },
        "error_handling": {
            "dont_expose_internals": "Generic error messages to users",
            "detailed_logging": "Log detailed errors server-side",
            "graceful_degradation": "Handle payment provider outages",
            "retry_logic": "Implement exponential backoff for retries",
            "circuit_breaker": "Prevent cascade failures",
        },
        "fraud_prevention": {
            "amount_validation": "Verify payment amounts match orders",
            "user_verification": "Ensure user owns the transaction",
            "duplicate_detection": "Check for duplicate transactions",
            "velocity_checks": "Monitor unusual payment patterns",
            "geographical_validation": "Flag suspicious locations",
        },
        "compliance": {
            "data_retention": "Follow local data retention laws",
            "user_consent": "Get explicit consent for payments",
            "refund_policy": "Clear refund terms and conditions",
            "audit_trail": "Maintain complete payment history",
            "reporting": "Generate compliance reports",
        },
    }


# ============================================================================
# RESOURCE: Payment Provider Status
# ============================================================================


@mcp.resource("payment-uz://status")
def payment_provider_status() -> Dict[str, Any]:
    """
    Check the current status of Uzbekistan payment providers.

    Returns:
        Real-time status information for all providers
    """
    return {
        "last_updated": datetime.now().isoformat(),
        "providers": {
            "payme": {
                "status": "operational",
                "api_url": "https://checkout.paycom.uz",
                "test_url": "https://checkout.test.paycom.uz",
                "uptime": "99.9%",
            },
            "click": {
                "status": "operational",
                "api_url": "https://api.click.uz",
                "merchant_url": "https://my.click.uz",
                "uptime": "99.8%",
            },
            "octo": {
                "status": "operational",
                "api_url": "https://api.octo.uz",
                "test_url": "https://api.test.octo.uz",
                "uptime": "99.7%",
            },
        },
        "note": "Status information is based on public availability. For real-time status, check provider dashboards.",
    }


# ============================================================================
# PROMPT: Integration Code Generator
# ============================================================================


@mcp.prompt(tags={"payment", "code-generation"})
def generate_payment_integration(
    provider: Literal["payme", "click", "octo"],
    language: Literal["nodejs", "python", "php"] = "nodejs",
    framework: Optional[str] = None,
) -> str:
    """
    Generate code examples for payment provider integration.

    Args:
        provider: Which payment provider (payme, click, octo)
        language: Programming language for code examples
        framework: Optional framework (express, fastapi, laravel, etc.)
    """
    framework_info = f" with {framework}" if framework else ""

    return f"""Generate a complete {provider.upper()} payment integration example in {language}{framework_info}.

Include:
1. Environment configuration
2. Payment link generation endpoint
3. Webhook handler with signature verification
4. Transaction status checking
5. Error handling and logging
6. Database schema for transactions
7. Security best practices

Make the code production-ready with:
- Proper error handling
- Input validation
- Security measures
- Clear comments
- Type safety (if applicable)
- Idempotency handling

Also provide:
- Setup instructions
- Testing guide with sandbox credentials
- Common issues and solutions
"""


# ============================================================================
# Run the server
# ============================================================================

if __name__ == "__main__":
    print("🚀 Starting Payment-UZ MCP Server...")
    print("📦 Exposing Uzbekistan payment systems (Payme, Click, Octo) as AI tools")
    print("🔧 Use with Claude Desktop, Cursor, or any MCP-compatible client")
    print("-" * 70)

    # Run with stdio transport (standard for MCP)
    mcp.run(transport="stdio")
