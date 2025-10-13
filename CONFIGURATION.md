# Payment-UZ MCP Server - Configuration Guide

## 🔧 Setting Up with Different MCP Clients

### Claude Desktop

1. **Locate configuration file:**
   ```bash
   # macOS
   ~/Library/Application Support/Claude/claude_desktop_config.json
   
   # Windows
   %APPDATA%\Claude\claude_desktop_config.json
   
   # Linux
   ~/.config/Claude/claude_desktop_config.json
   ```

2. **Add server configuration:**
   ```json
   {
     "mcpServers": {
       "payment-uz": {
         "command": "python3",
         "args": [
           "/Users/YOUR_USERNAME/Desktop/Airbnb_Clone/Airbnb-Clone-Project/mcp-servers/payment-uz/server.py"
         ],
         "env": {
           "FASTMCP_LOG_LEVEL": "INFO"
         }
       }
     }
   }
   ```

3. **Restart Claude Desktop**

4. **Verify installation:**
   - Type: "List available MCP tools"
   - Should see payment-uz tools listed

### Cursor IDE

1. **Open Cursor settings** (Cmd/Ctrl + ,)

2. **Add to MCP configuration:**
   ```json
   {
     "mcp": {
       "servers": {
         "payment-uz": {
           "command": "python3",
           "args": ["./mcp-servers/payment-uz/server.py"]
         }
       }
     }
   }
   ```

3. **Reload Cursor**

### VS Code with Copilot

1. **Create `.vscode/mcp.json` in your workspace:**
   ```json
   {
     "servers": {
       "payment-uz": {
         "command": "python3",
         "args": ["./mcp-servers/payment-uz/server.py"]
       }
     }
   }
   ```

2. **Reload VS Code**

### Using MCP Inspector (For Testing)

```bash
# Install MCP Inspector
npm install -g @modelcontextprotocol/inspector

# Run inspector with your server
mcp-inspector python3 server.py
```

Opens a web interface at http://localhost:5173 to test tools interactively.

## 🔑 Environment Variables

### Required Variables

None! The server works without credentials for documentation and guides.

### Optional Variables (For Real API Calls)

If you want the server to make actual API calls (future feature):

```bash
# Payme
PAYME_MERCHANT_ID=your_merchant_id
PAYME_TEST_KEY=your_test_key
PAYME_SECRET_KEY=your_production_key

# Click
CLICK_SERVICE_ID=your_service_id
CLICK_MERCHANT_ID=your_merchant_id
CLICK_SECRET_KEY=your_secret_key

# Octo
OCTO_API_KEY=your_api_key
OCTO_SECRET_KEY=your_secret_key

# Environment
NODE_ENV=development  # or 'production'
```

## 🧪 Testing the Server

### Method 1: Direct Python Execution

```bash
cd mcp-servers/payment-uz
python3 server.py
```

You should see:
```
🚀 Starting Payment-UZ MCP Server...
📦 Exposing Uzbekistan payment systems (Payme, Click, Octo) as AI tools
🔧 Use with Claude Desktop, Cursor, or any MCP-compatible client
----------------------------------------------------------------------
```

### Method 2: With MCP Inspector

```bash
# Install inspector
npm install -g @modelcontextprotocol/inspector

# Run
npx @modelcontextprotocol/inspector python3 server.py
```

### Method 3: Through Claude Desktop

1. Add server configuration (see above)
2. Restart Claude
3. Ask: "What payment tools are available?"
4. Try: "Generate a Payme payment link for 50,000 UZS"

## 🐛 Troubleshooting

### Issue: "Command not found: python3"

**Solution:** Use `python` instead:
```json
{
  "command": "python",  // Changed from python3
  "args": ["..."]
}
```

### Issue: "Module 'fastmcp' not found"

**Solution:** Install dependencies:
```bash
cd mcp-servers/payment-uz
pip install -r requirements.txt
```

Or use absolute path to Python in virtual environment:
```json
{
  "command": "/full/path/to/venv/bin/python",
  "args": ["..."]
}
```

### Issue: Server not showing in Claude

**Solutions:**
1. Check configuration file syntax (must be valid JSON)
2. Use absolute paths, not relative paths
3. Restart Claude Desktop completely
4. Check Claude logs:
   ```bash
   # macOS
   ~/Library/Logs/Claude/
   ```

### Issue: "Permission denied" error

**Solution:** Make script executable:
```bash
chmod +x server.py
```

### Issue: Tools not working

**Checklist:**
- ✅ Server configured in MCP client
- ✅ Python dependencies installed
- ✅ Using Python 3.10+
- ✅ Client restarted after configuration
- ✅ No syntax errors in config JSON

## 📊 Verifying Installation

### Quick Test Commands

Ask your AI assistant these questions to verify:

1. **List Tools:**
   ```
   "What payment integration tools are available?"
   ```
   Should show 15+ tools.

2. **Generate Link:**
   ```
   "Generate a test Payme payment link for 10,000 UZS"
   ```
   Should return a valid URL.

3. **Get Guide:**
   ```
   "Show me the Payme integration guide"
   ```
   Should return comprehensive documentation.

4. **Compare Providers:**
   ```
   "Compare Payme, Click, and Octo"
   ```
   Should show comparison table.

## 🔄 Updating the Server

```bash
cd mcp-servers/payment-uz

# Pull latest changes
git pull

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart your MCP client
```

## 🚀 Advanced Configuration

### Custom Log Level

```json
{
  "command": "python3",
  "args": ["server.py"],
  "env": {
    "FASTMCP_LOG_LEVEL": "DEBUG"  // INFO, WARNING, ERROR
  }
}
```

### Run with specific Python version

```json
{
  "command": "/usr/local/bin/python3.11",
  "args": ["server.py"]
}
```

### Use virtual environment

```json
{
  "command": "./mcp-servers/payment-uz/venv/bin/python",
  "args": ["server.py"]
}
```

## 📖 Additional Resources

- **FastMCP Documentation:** https://gofastmcp.com/
- **MCP Protocol:** https://modelcontextprotocol.io/
- **Payme Docs:** https://developer.help.paycom.uz/
- **Click Docs:** https://docs.click.uz/
- **Octo Docs:** https://docs.octo.uz/

## 💬 Getting Help

1. **Check USAGE_EXAMPLES.md** - Real-world usage scenarios
2. **Ask your AI assistant** - It has access to all documentation
3. **Test with MCP Inspector** - Visual debugging tool
4. **Check server logs** - Enable DEBUG logging

---

**Need more help?** Open an issue on GitHub or ask your AI assistant! 🤖
