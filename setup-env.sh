#!/bin/bash

echo "🚀 MLAgent Docker Setup - Environment Configuration"
echo "=================================================="

# Check if .env already exists
if [ -f ".env" ]; then
    echo "⚠️  .env file already exists!"
    echo "Do you want to overwrite it? (y/N)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo "Cancelled. Existing .env file preserved."
        exit 0
    fi
fi

# Copy the example file
cp .env.example .env
echo "✅ Created .env file from .env.example"

echo ""
echo "🔑 REQUIRED: You must fill in these values in .env file:"
echo "=============================================="
echo "1. DB_PASS - Set a strong PostgreSQL password"
echo "2. SECRET_KEY - Generate with: openssl rand -hex 32"
echo "3. ANTHROPIC_API_KEY - Your Anthropic API key"
echo ""

# Generate a secret key
if command -v openssl &> /dev/null; then
    SECRET_KEY=$(openssl rand -hex 32)
    echo "🎲 Generated SECRET_KEY for you: $SECRET_KEY"
    # Replace the placeholder in .env
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s/your_secret_key_here_generate_with_openssl_rand_hex_32/$SECRET_KEY/" .env
    else
        # Linux
        sed -i "s/your_secret_key_here_generate_with_openssl_rand_hex_32/$SECRET_KEY/" .env
    fi
    echo "✅ Automatically set SECRET_KEY in .env file"
else
    echo "⚠️  openssl not found. Please manually generate SECRET_KEY"
fi

echo ""
echo "📝 Next steps:"
echo "============="
echo "1. Edit .env file and set DB_PASS to a strong password"
echo "2. Edit .env file and set ANTHROPIC_API_KEY to your API key"
echo "3. Run: docker-compose up -d"
echo ""
echo "🔗 Access your application at:"
echo "   Frontend: http://localhost:3000"
echo "   API Gateway: http://localhost:8000"