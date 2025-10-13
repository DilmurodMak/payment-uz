#!/bin/bash
# Quick setup script for Payment-UZ MCP Server

echo "🚀 Setting up Payment-UZ MCP Server..."
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Please install it first:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo "✅ Found uv"

# Create virtual environment using uv
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment with uv..."
    uv venv .venv
fi

# Install dependencies using uv
# Note: We activate the venv temporarily just for package installation
echo "📥 Installing dependencies with uv..."
source .venv/bin/activate
uv pip install -r requirements.txt
deactivate

# Copy .env.example if .env doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from example..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your payment provider credentials"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "⚠️  To activate the virtual environment in your current shell, run:"
echo "   source .venv/bin/activate"
echo ""
echo "📚 Next steps:"
echo "1. Activate the virtual environment (see command above)"
echo "2. Edit .env with your payment credentials"
echo "3. Add this server to your MCP client (Claude Desktop, Cursor, etc.)"
echo "4. Test it by asking: 'Generate a Payme payment link'"
echo ""
echo "📖 See README.md for configuration instructions"
echo ""
echo "🧪 To test the server (after activating venv), run:"
echo "   python server.py"
echo ""
