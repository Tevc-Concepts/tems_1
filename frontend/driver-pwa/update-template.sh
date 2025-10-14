#!/bin/bash
# Post-build script to update custom TEMS template with new asset hashes

echo "🔄 Updating custom TEMS driver template..."

BUILD_HTML="../../tems/public/frontend/driver-pwa/dist/index.html"
TEMPLATE_HTML="../../tems/www/driver/index.html"

# Check if build output exists
if [ ! -f "$BUILD_HTML" ]; then
    echo "❌ Build output not found: $BUILD_HTML"
    exit 1
fi

# Extract asset paths from build output
CSS_FILE=$(grep -oP '(?<=href="/assets/tems/frontend/driver-pwa/dist/assets/)[^"]*\.css' "$BUILD_HTML")
JS_FILE=$(grep -oP '(?<=src="/assets/tems/frontend/driver-pwa/dist/assets/)[^"]*\.js' "$BUILD_HTML" | head -1)

if [ -z "$CSS_FILE" ] || [ -z "$JS_FILE" ]; then
    echo "❌ Could not extract asset filenames from build output"
    exit 1
fi

echo "  📄 CSS: $CSS_FILE"
echo "  📄 JS: $JS_FILE"

# Create custom TEMS template (no Frappe template inheritance)
cat > "$TEMPLATE_HTML" << 'TEMPLATE_START'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="theme-color" content="#36454f">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="mobile-web-app-capable" content="yes">
    
    <title>TEMS Driver Portal</title>
    
    <!-- TEMS Brand Favicon -->
    <link rel="icon" type="image/svg+xml" href="/assets/tems/frontend/driver-pwa/dist/vite.svg">
    <link rel="apple-touch-icon" sizes="192x192" href="/assets/tems/frontend/driver-pwa/dist/pwa-192x192.png">
    
    <!-- TEMS Global Theme -->
    <link rel="stylesheet" href="/assets/tems/css/tems_theme.css">
    
    <!-- Driver PWA Styles -->
TEMPLATE_START

echo "    <link rel=\"stylesheet\" href=\"/assets/tems/frontend/driver-pwa/dist/assets/$CSS_FILE\">" >> "$TEMPLATE_HTML"

cat >> "$TEMPLATE_HTML" << 'TEMPLATE_MIDDLE'
    
    <!-- PWA Manifest -->
    <link rel="manifest" href="/assets/tems/frontend/driver-pwa/dist/manifest.webmanifest">
    
    <style>
        /* TEMS Portal Base Styles */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        html, body {
            width: 100%;
            height: 100%;
            overflow: hidden;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #e0e2db;
            color: #36454f;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }
        
        #app {
            width: 100%;
            height: 100%;
            position: relative;
        }
        
        /* Loading Screen */
        .tems-loading {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, #36454f 0%, #2b373f 50%, #20292f 100%);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 9999;
            transition: opacity 0.5s ease, visibility 0.5s ease;
        }
        
        .tems-loading.hidden {
            opacity: 0;
            visibility: hidden;
        }
        
        .tems-logo {
            width: 120px;
            height: 120px;
            margin-bottom: 2rem;
            animation: pulse 2s ease-in-out infinite;
        }
        
        .tems-loader {
            width: 60px;
            height: 60px;
            border: 4px solid rgba(57, 255, 20, 0.2);
            border-top-color: #39ff14;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            box-shadow: 0 0 20px rgba(57, 255, 20, 0.4);
        }
        
        .tems-loading-text {
            color: #39ff14;
            font-size: 1.2rem;
            font-weight: 700;
            margin-top: 1.5rem;
            text-shadow: 0 0 10px rgba(57, 255, 20, 0.6);
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        @keyframes pulse {
            0%, 100% { 
                transform: scale(1);
                opacity: 1;
            }
            50% { 
                transform: scale(1.05);
                opacity: 0.8;
            }
        }
        
        /* No Script Fallback */
        .no-js-message {
            display: none;
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: white;
            padding: 2rem;
            border-radius: 1rem;
            box-shadow: 0 20px 40px rgba(54, 69, 79, 0.3);
            text-align: center;
            max-width: 90%;
            width: 400px;
        }
        
        .no-js-message h2 {
            color: #36454f;
            margin-bottom: 1rem;
        }
        
        .no-js-message p {
            color: #758188;
        }
    </style>
</head>
<body class="tems-theme tems-portal">
    <!-- Loading Screen -->
    <div id="tems-loading" class="tems-loading">
        <svg class="tems-logo" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
            <!-- TEMS Circuit Map Pin Icon -->
            <defs>
                <linearGradient id="neonGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#39ff14;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#2ecc10;stop-opacity:1" />
                </linearGradient>
                <filter id="glow">
                    <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
                    <feMerge>
                        <feMergeNode in="coloredBlur"/>
                        <feMergeNode in="SourceGraphic"/>
                    </feMerge>
                </filter>
            </defs>
            <path d="M100 20 C75 20 55 40 55 65 C55 90 100 130 100 130 C100 130 145 90 145 65 C145 40 125 20 100 20 Z" 
                  fill="none" stroke="url(#neonGradient)" stroke-width="4" filter="url(#glow)"/>
            <circle cx="100" cy="65" r="25" fill="none" stroke="url(#neonGradient)" stroke-width="3" filter="url(#glow)"/>
            <path d="M85 65 L100 50 L115 65 M100 50 L100 80 M85 80 L115 80" 
                  stroke="url(#neonGradient)" stroke-width="2" fill="none" stroke-linecap="round" filter="url(#glow)"/>
        </svg>
        <div class="tems-loader"></div>
        <div class="tems-loading-text">Loading TEMS Driver Portal...</div>
    </div>
    
    <!-- Main App Container -->
    <div id="app"></div>
    
    <!-- No JavaScript Fallback -->
    <noscript>
        <div class="no-js-message" style="display: block;">
            <h2>⚠️ JavaScript Required</h2>
            <p>TEMS Driver Portal requires JavaScript to run. Please enable JavaScript in your browser settings and reload the page.</p>
        </div>
    </noscript>
    
    <!-- Driver PWA Application -->
TEMPLATE_MIDDLE

echo "    <script type=\"module\" src=\"/assets/tems/frontend/driver-pwa/dist/assets/$JS_FILE\"></script>" >> "$TEMPLATE_HTML"

cat >> "$TEMPLATE_HTML" << 'TEMPLATE_END'
    
    <!-- Service Worker Registration -->
    <script src="/assets/tems/frontend/driver-pwa/dist/registerSW.js"></script>
    
    <!-- Hide Loading Screen After App Loads -->
    <script>
        window.addEventListener('load', function() {
            setTimeout(function() {
                const loader = document.getElementById('tems-loading');
                if (loader) {
                    loader.classList.add('hidden');
                    setTimeout(function() {
                        loader.style.display = 'none';
                    }, 500);
                }
            }, 1000);
        });
        
        // Fallback: Hide loader after 5 seconds regardless
        setTimeout(function() {
            const loader = document.getElementById('tems-loading');
            if (loader && !loader.classList.contains('hidden')) {
                loader.classList.add('hidden');
            }
        }, 5000);
    </script>
</body>
</html>
TEMPLATE_END

echo "✅ Custom TEMS template updated successfully!"
echo ""
echo "🎨 Features:"
echo "   ✓ Custom TEMS branding (no Frappe template dependency)"
echo "   ✓ Neon green (#39ff14) loading animation"
echo "   ✓ Charcoal gray (#36454f) theme-color for mobile"
echo "   ✓ Circuit-style TEMS logo animation"
echo "   ✓ Progressive loading screen"
echo ""
echo "📍 Next steps:"
echo "  1. cd /workspace/development/frappe-bench"
echo "  2. bench --site tems.local clear-cache"
echo "  3. bench --site tems.local clear-website-cache"
echo "  4. Access: http://tems.local:8000/driver"
