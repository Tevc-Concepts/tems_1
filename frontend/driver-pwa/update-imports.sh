#!/bin/bash

# Script to update imports from local to shared in driver-pwa
# Run from: frontend/driver-pwa directory

echo "=== Updating Driver PWA Imports to Use Shared Code ==="
echo ""

# Function to update imports in a file
update_file() {
    local file="$1"
    echo "Updating: $file"
    
    # Replace auth store import
    sed -i "s|from '@/stores/auth'|from '@shared'|g" "$file"
    sed -i "s|from '../stores/auth'|from '@shared'|g" "$file"
    sed -i "s|from './stores/auth'|from '@shared'|g" "$file"
    sed -i "s|import { useAuthStore }|import { useAuth as useAuthStore }|g" "$file"
    
    # Replace offline store import
    sed -i "s|from '@/stores/offline'|from '@shared'|g" "$file"
    sed -i "s|from '../stores/offline'|from '@shared'|g" "$file"
    sed -i "s|from './stores/offline'|from '@shared'|g" "$file"
    
    # Replace composables
    sed -i "s|from '@/composables/useGeolocation'|from '@shared'|g" "$file"
    sed -i "s|from '@/composables/useCamera'|from '@shared'|g" "$file"
    sed -i "s|from '@/composables/useNotifications'|from '@shared'|g" "$file"
    sed -i "s|from '@/composables/useToast'|from '@shared'|g" "$file"
    sed -i "s|from '@/composables/useOfflineSync'|from '@shared'|g" "$file"
    
    # Replace utils
    sed -i "s|from '@/utils/frappeClient'|from '@shared'|g" "$file"
    sed -i "s|import frappeClient from '@/utils/frappeClient'|import { frappeClient } from '@shared'|g" "$file"
}

# Update all Vue files in src directory
find src -name "*.vue" -type f | while read file; do
    update_file "$file"
done

# Update all JS files in src directory
find src -name "*.js" -type f | while read file; do
    update_file "$file"
done

echo ""
echo "=== Import Updates Complete ==="
echo ""
echo "Files updated. Please review changes and test:"
echo "1. npm install (to link workspace dependencies)"
echo "2. npm run dev (to start development server)"
echo "3. Check browser console for errors"
