# Payment-UZ MCP Server 🇺🇿💳

A **FastMCP server** that exposes Uzbekistan's payment systems (Payme, Click, Octo) as AI-accessible tools. Built for developers to easily integrate payment providers through AI assistants like Claude, ChatGPT, and Cursor.

[![MCP](https://img.shields.io/badge/MCP-Compatible-blue)](https://modelcontextprotocol.io)
[![Python](https://img.shields.io/badge/Python-3.10+-green.svg)](https://www.python.org/)
[![FastMCP](https://img.shields.io/badge/FastMCP-2.11+-orange)](https://gofastmcp.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 What is This?

**Payment-UZ MCP** is a Model Context Protocol server that turns complex payment integrations into simple AI conversations. Instead of reading documentation and writing code manually, just ask your AI assistant:

> "Generate a Payme payment link for 50,000 UZS"
> 
> "How do I verify a Click webhook signature?"
> 
> "Compare Payme, Click, and Octo for my e-commerce site"

The AI uses this MCP server to provide accurate, production-ready payment integration guidance and code.

## ✨ Features

### 🔧 **Payment Provider Tools**

#### Payme Integration
- ✅ Generate checkout URLs
- ✅ Verify webhook authentication
- ✅ Complete integration guide with JSON-RPC 2.0
- ✅ Transaction state management
- ✅ Error code reference

#### Click Integration  
- ✅ Generate invoice URLs
- ✅ Verify MD5 webhook signatures
- ✅ Two-phase payment flow (prepare + complete)
- ✅ Merchant API documentation
- ✅ Error handling guide

#### Octo Integration
- ✅ Create payment transactions
- ✅ Verify SHA-256 webhook signatures
- ✅ Modern REST API integration
- ✅ Card tokenization support
- ✅ Refund handling

### 📊 **Comparison & Analysis**
- Compare all three providers side-by-side
- Security best practices
- Market share and recommendations
- Integration complexity analysis

### 🛡️ **Security Tools**
- Signature verification for all providers
- Webhook authentication validation
- PCI compliance guidelines
- Fraud prevention strategies

### 💻 **Code Generation**
- Production-ready code examples
- Multi-language support (Node.js, Python, PHP)
- Framework-specific implementations
- Database schemas and migration scripts

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- pip or uv package manager
- An MCP-compatible AI client (Claude Desktop, Cursor, etc.)

### Installation

```bash
# Clone or download this server
cd mcp-servers/payment-uz

# Install dependencies
pip install -r requirements.txt

# Or use uv for faster installation
uv pip install -r requirements.txt
```

### Usage with Claude Desktop

1. Open Claude Desktop configuration:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. Add the server configuration:

```json
{
  "mcpServers": {
    "payment-uz": {
      "command": "python",
      "args": [
        "/FULL/PATH/TO/mcp-servers/payment-uz/server.py"
      ]
    }
  }
}
```

3. Restart Claude Desktop

4. Start asking payment integration questions!

### Usage with Cursor / VS Code

Add to your MCP configuration:

```json
{
  "mcpServers": {
    "payment-uz": {
      "command": "python",
      "args": ["./mcp-servers/payment-uz/server.py"]
    }
  }
}
```

## 📖 Available Tools

### Payme Tools
- `payme_generate_checkout_url` - Generate payment URLs
- `payme_verify_webhook_auth` - Verify Basic Auth headers
- `payme_get_integration_guide` - Complete integration documentation

### Click Tools
- `click_generate_invoice_url` - Create payment invoices
- `click_verify_webhook_signature` - Verify MD5 signatures
- `click_get_integration_guide` - Two-phase payment guide

### Octo Tools
- `octo_create_payment` - Initialize payment transactions
- `octo_verify_webhook_signature` - Verify SHA-256 signatures
- `octo_get_integration_guide` - Modern REST API guide

### General Tools
- `compare_payment_providers` - Provider comparison matrix
- `payment_security_best_practices` - Security guidelines

### Resources
- `payment-uz://status` - Real-time provider status

### Prompts
- `generate_payment_integration` - Generate integration code

## 💡 Example Conversations

### Generate a Payme Payment Link

**You:** Generate a Payme checkout URL for a booking worth 150,000 UZS

**AI (using MCP):**
```json
{
  "success": true,
  "payment_url": "https://checkout.test.paycom.uz/...",
  "amount_uzs": 150000,
  "amount_tiyin": 15000000,
  "environment": "test"
}
```

### Compare Payment Providers

**You:** Which payment provider should I integrate first for my booking platform?

**AI (using MCP):** Based on the comparison, I recommend:
1. **Payme** - Essential for enterprise/B2B bookings (highest trust)
2. **Click** - Easy integration, covers most consumer payments
3. **Octo** - For modern features like recurring payments

### Verify Webhook Security

**You:** How do I verify a Click webhook signature?

**AI (using MCP):** Use the `click_verify_webhook_signature` tool with MD5 hash verification...

## 🏗️ Architecture

```
Payment-UZ MCP Server
├── FastMCP Framework
├── Tools (15+ payment tools)
├── Resources (Status monitoring)
├── Prompts (Code generation)
└── Security (Signature verification)
```

## 🔐 Security Features

- ✅ **Signature Verification** - All providers supported
- ✅ **Webhook Authentication** - Basic Auth and token validation
- ✅ **Best Practices Guide** - PCI DSS compliance tips
- ✅ **Fraud Prevention** - Detection strategies included
- ✅ **Secure by Default** - Production-ready code examples

## 🌍 Uzbekistan Payment Ecosystem

### Market Coverage

| Provider | Market Share | Best For |
|----------|-------------|----------|
| **Payme** | ~40% | Enterprise, Government |
| **Click** | ~35% | E-commerce, SMB |
| **Octo** | ~15% | SaaS, Modern Apps |

### Why This Matters

Uzbekistan has a unique payment landscape with these three dominant providers. Unlike global markets where Stripe/PayPal dominate, Uzbek developers **must** integrate local providers. This MCP server makes that integration **10x easier**.

## 🛠️ Development

### Project Structure

```
payment-uz/
├── server.py              # Main MCP server
├── requirements.txt       # Python dependencies
├── pyproject.toml        # Package configuration
├── README.md             # This file
└── examples/             # Usage examples (coming soon)
```

### Running Tests

```bash
# Test the server locally
python server.py

# In another terminal, test with MCP Inspector
npx @modelcontextprotocol/inspector python server.py
```

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

MIT License - feel free to use in your projects!

## 🙏 Acknowledgments

- Built on [FastMCP](https://gofastmcp.com/) by @jlowin
- Inspired by the [Model Context Protocol](https://modelcontextprotocol.io/)
- Payment integration based on [GetSpace](https://github.com/DilmurodMak/booking_web_app) production implementation

## 📧 Contact

- **Author:** GetSpace Team
- **Repository:** [github.com/DilmurodMak/payment-uz-mcp](https://github.com/DilmurodMak/payment-uz-mcp)
- **Issues:** [Report bugs or request features](https://github.com/DilmurodMak/payment-uz-mcp/issues)

## 🚀 What's Next?

- [ ] Add real-time payment status checking via API
- [ ] Support for recurring payments
- [ ] Multi-language code generation (Go, Java, C#)
- [ ] Interactive payment flow visualizations
- [ ] Webhook testing utilities
- [ ] Payment reconciliation tools

---

**Made with ❤️ for the Uzbekistan developer community**

*Stop reading payment docs. Start asking AI.* 🤖
