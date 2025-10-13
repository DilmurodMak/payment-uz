# Payment-UZ MCP Server - Usage Examples

This document shows real-world examples of using the Payment-UZ MCP server through AI assistants.

## 🎯 Basic Usage Patterns

### 1. Generate Payment Links

#### Payme Payment Link
```
👤 You: I need to create a Payme payment link for booking #123, amount is 250,000 UZS, 
        return URL should be https://myapp.com/payment/callback

🤖 AI: I'll generate that Payme checkout URL for you.
```

The AI will use `payme_generate_checkout_url` and return:
```json
{
  "success": true,
  "payment_url": "https://checkout.test.paycom.uz/ENCODED_PARAMS_HERE",
  "environment": "test",
  "amount_uzs": 250000,
  "amount_tiyin": 25000000,
  "order_id": "booking_123"
}
```

#### Click Invoice
```
👤 You: Generate a Click payment invoice for 150,000 UZS, transaction ID: order_456

🤖 AI: [Uses click_generate_invoice_url tool]
```

### 2. Webhook Verification

#### Verify Payme Webhook
```
👤 You: I received a webhook with this authorization header:
        "Basic bWVyY2hhbnRfaWQ6c2VjcmV0X2tleQ=="
        Can you verify if it's valid?

🤖 AI: Let me verify that Payme webhook authentication for you.
```

#### Verify Click Signature
```
👤 You: I need to verify this Click webhook signature:
        - click_trans_id: 12345
        - service_id: 67890
        - amount: 50000
        - action: 1
        - sign_time: 2025-10-11 10:30:00
        - received signature: abc123def456

🤖 AI: [Uses click_verify_webhook_signature to validate]
```

### 3. Get Integration Help

```
👤 You: I'm integrating Payme for the first time. What do I need to know?

🤖 AI: [Uses payme_get_integration_guide]
      Here's everything you need for Payme integration:
      
      Payme uses JSON-RPC 2.0 protocol. You need to implement 6 methods:
      1. CheckPerformTransaction - validates before payment
      2. CreateTransaction - creates the transaction
      ...
```

## 🏗️ Advanced Use Cases

### Comparing Payment Providers

```
👤 You: I'm building a hotel booking platform. Which payment provider should I use?

🤖 AI: [Uses compare_payment_providers]
      Based on your booking platform needs, here's my recommendation:
      
      1. **Payme** (Priority: HIGH)
         - Most trusted by Uzbek users
         - Essential for B2B bookings
         - 40% market share
         
      2. **Click** (Priority: HIGH)
         - Easy integration (1-3 days)
         - Popular for e-commerce
         - 35% market share
         
      3. **Octo** (Priority: MEDIUM)
         - Modern features
         - Good for tech-savvy users
         - Growing market share
      
      💡 Recommendation: Start with Payme + Click to cover 75% of users.
```

### Security Best Practices

```
👤 You: What security measures should I implement for payment webhooks?

🤖 AI: [Uses payment_security_best_practices]
      Here are critical security measures for payment webhooks:
      
      🔒 Webhook Security:
      - Always verify signatures (Payme: Basic Auth, Click: MD5, Octo: SHA-256)
      - Use HTTPS only
      - Implement rate limiting
      - Log all webhook requests
      - Whitelist payment provider IPs
      
      🗄️ Data Protection:
      - Never store card numbers
      - Encrypt sensitive transaction data
      - Follow PCI DSS compliance
      ...
```

### Code Generation

```
👤 You: Generate a complete Node.js Express webhook handler for Payme with TypeScript

🤖 AI: [Uses generate_payment_integration prompt]
```

Returns full production-ready code:
```typescript
import express from 'express';
import crypto from 'crypto';

interface PaymeWebhookRequest {
  method: string;
  params: {
    account: { order_id: string };
    amount: number;
    id?: string;
    time?: number;
  };
  id: number;
}

// Payme webhook handler
router.post('/api/payme/webhook', async (req, res) => {
  try {
    // Verify authorization
    const auth = req.headers.authorization;
    if (!verifyPaymeAuth(auth)) {
      return res.json({
        error: { code: -32504, message: "Invalid authorization" },
        id: req.body.id
      });
    }
    
    // Handle methods
    const { method, params, id } = req.body;
    switch (method) {
      case 'CheckPerformTransaction':
        // Implementation...
        break;
      // ... other methods
    }
  } catch (error) {
    // Error handling
  }
});
```

## 🎓 Learning Scenarios

### Scenario 1: First-Time Integration

```
👤 You: I've never integrated payments before. Walk me through Payme step by step.

🤖 AI: I'll guide you through Payme integration step by step.
      
      📋 **Step 1: Get Credentials**
      - Sign up at test.paycom.uz
      - Get your merchant_id and secret_key
      
      📋 **Step 2: Understand the Flow**
      [Uses payme_get_integration_guide]
      Payme uses a 6-method JSON-RPC flow:
      1. User clicks "Pay with Payme"
      2. You generate checkout URL
      3. User completes payment on Payme
      4. Payme calls your webhook...
      
      📋 **Step 3: Implementation**
      Let me generate the code for you...
```

### Scenario 2: Debugging Webhook Issues

```
👤 You: My Payme webhook keeps returning -32504 error. What's wrong?

🤖 AI: Error -32504 means "Invalid authorization". Let me help debug:
      
      [Uses payme_verify_webhook_auth]
      
      ❌ Common causes:
      1. Wrong merchant key in .env
      2. Not using correct Base64 encoding
      3. Authorization header format incorrect
      
      ✅ Correct format:
      Authorization: Basic base64(merchant_id:merchant_key)
      
      Try using the verify tool to test your header...
```

### Scenario 3: Production Migration

```
👤 You: I'm ready to move from Payme sandbox to production. What changes do I need?

🤖 AI: Here's your production migration checklist:
      
      🔧 **Configuration Changes**
      1. Update PAYME_SECRET_KEY from test key to production key
      2. Change checkout URL:
         - Test: https://checkout.test.paycom.uz
         - Prod: https://checkout.paycom.uz
      3. Update merchant_id (if different)
      
      🔒 **Security Checklist**
      - ✅ HTTPS enabled on webhook endpoint
      - ✅ Webhook signature verification implemented
      - ✅ Rate limiting configured
      - ✅ Error logging enabled
      
      🧪 **Testing**
      - Test small payment first (1000 UZS)
      - Verify webhook delivery
      - Check transaction in Payme dashboard
      
      Would you like me to review your production code?
```

## 🔄 Real-World Integration Examples

### E-commerce Checkout Flow

```
👤 You: I'm building a checkout page. Show me how to integrate all three providers.

🤖 AI: I'll create a multi-provider checkout integration for you.

      **Frontend HTML**
      ```html
      <div class="payment-options">
        <button onclick="payWithPayme()">Pay with Payme</button>
        <button onclick="payWithClick()">Pay with Click</button>
        <button onclick="payWithOcto()">Pay with Octo</button>
      </div>
      ```
      
      **Backend API**
      [Generates complete Express.js API with all three integrations]
```

### Booking Platform Integration

```
👤 You: For my booking platform, when should I allow payment?

🤖 AI: For booking platforms, follow this payment flow:
      
      📅 **Booking States**
      1. pending → No payment yet
      2. selected (host approved) → Enable payment
      3. paid → Payment completed
      4. approved → Booking confirmed
      
      💡 **Best Practice**
      Only generate payment links when booking is "selected" by host.
      This prevents users from paying for unconfirmed bookings.
      
      [Uses your GetSpace implementation as reference]
      
      Here's the recommended flow...
```

## 💻 Code Generation Examples

### Generate Full Integration

```
👤 You: Generate a complete Python FastAPI integration for all three providers

🤖 AI: [Uses generate_payment_integration]
      I'll create a production-ready FastAPI integration...
```

### Generate Database Schema

```
👤 You: What database schema do I need for payment transactions?

🤖 AI: Here's a robust transaction schema for all three providers:
      
      ```sql
      CREATE TABLE transactions (
        id SERIAL PRIMARY KEY,
        provider VARCHAR(10) NOT NULL, -- 'payme', 'click', 'octo'
        provider_transaction_id VARCHAR(255) UNIQUE,
        booking_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        amount DECIMAL(10,2) NOT NULL,
        currency VARCHAR(3) DEFAULT 'UZS',
        state INTEGER NOT NULL, -- 1: pending, 2: paid, -1: cancelled
        provider_data JSONB,
        create_date TIMESTAMP DEFAULT NOW(),
        perform_date TIMESTAMP,
        cancel_date TIMESTAMP,
        INDEX idx_provider_txn (provider, provider_transaction_id),
        INDEX idx_booking (booking_id)
      );
      ```
```

## 🎯 Quick Commands

Here are some quick commands to try:

```
"Generate a Payme payment link for 100,000 UZS"

"Compare Payme, Click, and Octo"

"Show me Payme test credentials"

"Verify this Click signature: [data]"

"What's the difference between Payme and Octo?"

"Generate Node.js webhook handler for Click"

"Security best practices for payment webhooks"

"How do I handle payment timeouts?"

"Show Octo integration guide"

"Generate TypeScript types for Payme webhook"
```

## 🚀 Pro Tips

1. **Always verify signatures** - Never trust webhooks without verification
2. **Use test credentials first** - All providers have sandbox environments
3. **Log everything** - Detailed logs are crucial for debugging
4. **Implement idempotency** - Prevent duplicate payments
5. **Set timeouts** - Don't let pending payments linger forever
6. **Handle all states** - Payments can be pending, paid, cancelled, or failed

---

**Need more help?** Just ask your AI assistant - it has access to all these tools! 🤖
