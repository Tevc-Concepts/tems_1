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
    
    # Update the Frappe template with new asset hashes
    echo "� Updating Frappe template..."
    ./update-template.sh
    
    echo ""
    echo "�📍 Output location:"
    echo "   ../../tems/public/frontend/driver-pwa/dist/"
    echo ""
    echo "🌐 Access URL (after cache clear):"
    echo "   http://tems.local:8000/driver/"
    echo ""
    echo "⚡ Next steps:"
    echo "   1. cd /workspace/development/frappe-bench"
    echo "   2. bench --site tems.local clear-cache"
    echo "   3. bench --site tems.local clear-website-cache"
    echo "   4. Visit http://tems.local:8000/driver/"
    echo ""
else
    echo ""
    echo "❌ Build failed. Check errors above."
    echo ""
    exit 1
fi
