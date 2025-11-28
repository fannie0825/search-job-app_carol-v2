#!/bin/bash
# macOS Setup Script for CareerLens API Keys

echo "🍎 CareerLens API Key Setup for macOS"
echo "======================================"
echo ""

# Check if .env exists
if [ -f ".env" ]; then
    echo "⚠️  .env file already exists!"
    read -p "Do you want to overwrite it? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Cancelled."
        exit 1
    fi
fi

# Copy from example
if [ -f ".env.example" ]; then
    cp .env.example .env
    echo "✅ Created .env file from .env.example"
else
    echo "❌ .env.example not found!"
    exit 1
fi

echo ""
echo "📝 Next steps:"
echo "1. Open .env file:"
echo "   code .env"
echo "   OR"
echo "   open -a TextEdit .env"
echo ""
echo "2. Add your API keys from Streamlit secrets.toml"
echo "3. Save the file"
echo "4. Restart your React app: npm start"
echo ""
echo "💡 To verify: npm run check-env"
