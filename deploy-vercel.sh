#!/bin/bash

echo "🚀 ConvertAnything - Vercel Deployment Script"
echo "=============================================="

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
fi

echo "📋 Pre-deployment checklist:"
echo "✅ vercel.json configured"
echo "✅ requirements.txt ready"
echo "✅ API endpoints created"
echo "✅ Frontend auto-detection enabled"

echo ""
echo "🔐 Environment Variables Required:"
echo "- OPENAI_API_KEY (for AI transcription)"
echo "- MAX_FILE_SIZE (optional, default: 10MB)"
echo ""

read -p "Do you have your OpenAI API key ready? (y/n): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Please get your OpenAI API key from: https://platform.openai.com/api-keys"
    echo "Then run this script again."
    exit 1
fi

echo "🚀 Starting Vercel deployment..."

# Deploy to Vercel
echo "Deploying with latest configuration..."
vercel --prod --force

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📝 Next steps:"
echo "1. Set your OPENAI_API_KEY in Vercel dashboard"
echo "2. Test the API endpoints"
echo "3. Update any hardcoded URLs in your frontend"
echo ""
echo "🔗 Useful commands:"
echo "  vercel logs --follow    # View live logs"
echo "  vercel domains          # Manage custom domains"
echo "  vercel env ls           # List environment variables"
echo ""
echo "🎉 Your ConvertAnything app is now live on Vercel!"
