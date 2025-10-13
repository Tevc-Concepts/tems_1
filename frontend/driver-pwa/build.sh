#!/bin/bash

echo "🚀 TEMS Driver PWA - Build Script"
echo "=================================="
echo ""

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
    echo ""
fi

# Run build
echo "🔨 Building PWA..."
npm run build

# Check if build was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Build successful!"
    echo ""
    echo "📍 Output location:"
    echo "   ../../tems/public/frontend/driver-pwa/dist/"
    echo ""
    echo "🌐 Access URL (after Frappe restart):"
    echo "   https://your-site.com/driver/"
    echo ""
    echo "⚡ Next steps:"
    echo "   1. cd /workspace/development/frappe-bench"
    echo "   2. bench restart"
    echo "   3. bench clear-cache"
    echo "   4. Visit https://your-site.com/driver/"
    echo ""
else
    echo ""
    echo "❌ Build failed. Check errors above."
    echo ""
    exit 1
fi
