#!/bin/bash
# Sync built PWA HTML files to www directory
# This ensures the www entry points have the correct hashed asset references

cd "$(dirname "$0")/.." || exit

echo "🔄 Syncing PWA HTML files from dist to www..."
echo ""

# Operations PWA
if [ -f "tems/public/frontend/operations-pwa/dist/index.html" ]; then
    cp tems/public/frontend/operations-pwa/dist/index.html tems/www/operations/index.html
    echo "✅ Operations HTML synced"
else
    echo "⚠️  Operations dist/index.html not found - build operations PWA first"
fi

# Safety PWA
if [ -f "tems/public/frontend/safety-pwa/dist/index.html" ]; then
    cp tems/public/frontend/safety-pwa/dist/index.html tems/www/safety/index.html
    echo "✅ Safety HTML synced"
else
    echo "⚠️  Safety dist/index.html not found - build safety PWA first"
fi

# Fleet PWA
if [ -f "tems/public/frontend/fleet-pwa/dist/index.html" ]; then
    cp tems/public/frontend/fleet-pwa/dist/index.html tems/www/fleet/index.html
    echo "✅ Fleet HTML synced"
else
    echo "⚠️  Fleet dist/index.html not found - build fleet PWA first"
fi

# Driver PWA
if [ -f "tems/public/frontend/driver-pwa/dist/index.html" ]; then
    cp tems/public/frontend/driver-pwa/dist/index.html tems/www/driver/index.html
    echo "✅ Driver HTML synced"
else
    echo "⚠️  Driver dist/index.html not found - build driver PWA first"
fi

echo ""
echo "🎉 PWA HTML sync complete!"
echo ""
echo "Next steps:"
echo "  1. Run 'bench restart' to reload changes"
echo "  2. Clear browser cache and test PWAs"
