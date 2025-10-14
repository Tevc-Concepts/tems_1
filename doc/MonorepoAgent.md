
markdown# TEMS PWA Monorepo Refactoring - Complete Architecture Setup

## Context
I have a Frappe/ERPNext V15+ application called TEMS (Transportation Enterprise Management System) with an existing `driver-pwa` implementation. I need to refactor this into a scalable monorepo structure that supports 4 role-based PWAs (Driver, Operations, Safety, Fleet Management) while maintaining full integration with Frappe backend without affecting Frappe Desk functionality.

## Current Structure
```
frappe-bench/
└── apps/
    └── tems/
        ├── tems/
        │   ├── tems_{domain}/        # 13 modules (fleet, safety, operations, etc.)
        │   ├── public/
        │   ├── www/
        │   └── api/
        └── frontend/
            └── driver-pwa/           # Existing Vue 3 + Vite PWA
                ├── src/
                ├── package.json
                ├── vite.config.js
                └── node_modules/
```

## Required Architecture
Transform to workspace-based monorepo:
```
frappe-bench/
└── apps/
    └── tems/
        ├── tems/
        │   ├── tems_{domain}/
        │   ├── public/              # Build outputs go here
        │   │   ├── driver/
        │   │   ├── operations/
        │   │   ├── safety/
        │   │   └── fleet/
        │   ├── www/                 # Frappe web routes
        │   │   ├── driver/
        │   │   ├── operations/
        │   │   ├── safety/
        │   │   └── fleet/
        │   └── api/pwa/            # Centralized PWA APIs
        │       ├── driver.py
        │       ├── operations.py
        │       ├── safety.py
        │       └── fleet.py
        └── frontend/
            ├── package.json         # Root workspace config
            ├── node_modules/        # Shared dependencies
            ├── tailwind.config.js   # Shared Tailwind
            ├── tsconfig.json        # Shared TypeScript
            ├── .eslintrc.js         # Shared linting
            ├── shared/              # Shared code
            │   ├── components/
            │   │   ├── layout/
            │   │   ├── common/
            │   │   └── forms/
            │   ├── composables/
            │   │   ├── useAuth.ts
            │   │   ├── useGeolocation.ts
            │   │   ├── useCamera.ts
            │   │   ├── useOfflineSync.ts
            │   │   └── useNotification.ts
            │   ├── stores/
            │   │   ├── auth.ts
            │   │   ├── offline.ts
            │   │   └── base.ts
            │   ├── utils/
            │   │   ├── frappeClient.ts
            │   │   ├── helpers.ts
            │   │   ├── constants.ts
            │   │   └── types.ts
            │   └── styles/
            │       └── main.css
            ├── driver-pwa/
            │   ├── src/
            │   ├── package.json
            │   ├── vite.config.ts
            │   └── tsconfig.json
            ├── operations-pwa/
            │   ├── src/
            │   ├── package.json
            │   ├── vite.config.ts
            │   └── tsconfig.json
            ├── safety-pwa/
            │   ├── src/
            │   ├── package.json
            │   ├── vite.config.ts
            │   └── tsconfig.json
            └── fleet-pwa/
                ├── src/
                ├── package.json
                ├── vite.config.ts
                └── tsconfig.json
```

## Technology Stack
- **Frontend**: Vue 3 (Composition API + `<script setup>`)
- **Build Tool**: Vite 5+
- **Language**: TypeScript (strict mode)
- **State Management**: Pinia 2+
- **Routing**: Vue Router 4+
- **UI Framework**: Tailwind CSS 3+ with custom design system
- **PWA**: vite-plugin-pwa with Workbox
- **Offline Storage**: localForage + IndexedDB
- **HTTP Client**: Axios with Frappe integration
- **Icons**: lucide-vue-next
- **Date Handling**: date-fns
- **Utilities**: @vueuse/core
- **Code Quality**: ESLint + Prettier
- **Monorepo**: npm workspaces (native)

## PWA Requirements

### 1. Driver PWA
- Trip management (Journey Plan DocType)
- Real-time navigation
- Vehicle inspection (Spot Check DocType)
- Fuel logging (Fuel Log DocType)
- Incident reporting (Safety Incident DocType)
- Offline-first with sync queue
- Camera integration for inspections
- Geolocation tracking

### 2. Operations PWA
- Real-time fleet tracking
- Dispatch management (Dispatch Schedule DocType)
- Trip planning and allocation (Operation Plan DocType)
- Movement logging (Movement Log DocType)
- Control exception handling
- Analytics dashboard
- Route optimization

### 3. Safety PWA
- Compliance tracking (Compliance Audit DocType)
- Incident management (Safety Incident DocType)
- Risk assessments (Risk Assessment DocType)
- Vehicle spot checks
- Safety training records
- Audit checklists

### 4. Fleet PWA
- Maintenance scheduling (Maintenance Work Order DocType)
- Asset utilization tracking
- Fuel consumption analytics
- Vehicle lifecycle management
- Spare parts inventory
- Cost tracking (Fleet Costs DocType)

## Frappe Integration Requirements

### Authentication
- Support both session-based and JWT token authentication
- Implement token refresh mechanism
- Role-based access control using Frappe permissions
- Offline authentication with cached credentials

### API Integration
- Use Frappe REST API (`/api/resource/{DocType}`)
- Implement Frappe RPC calls (`/api/method/{method}`)
- File upload integration with Frappe File DocType
- Real-time updates via Frappe Socket.io (if available)

### DocTypes (Key ones provided in context)
Reference the attached `doctype_reference.md` for complete field structures.

### Offline Strategy
- Cache GET requests with IndexedDB
- Queue POST/PUT/DELETE operations when offline
- Sync queue when connection restored
- Conflict resolution for concurrent edits
- Background sync with Service Worker

## Refactoring Tasks

### Phase 1: Core Infrastructure Setup
1. Create root `package.json` with npm workspaces configuration
2. Set up shared TypeScript configuration with path aliases
3. Configure shared Tailwind CSS with custom design tokens
4. Set up ESLint + Prettier with Vue/TypeScript rules
5. Create shared Vite config base with common plugins
6. Implement git hooks (husky + lint-staged)

### Phase 2: Shared Module Architecture
1. Create type-safe Frappe API client with:
   - Automatic retry logic
   - Request/response interceptors
   - Error handling and logging
   - Offline detection
   - Token management
2. Implement base Pinia stores with:
   - Generic CRUD operations
   - Offline sync capabilities
   - Optimistic updates
   - State persistence
3. Create core composables:
   - `useAuth` - Authentication & authorization
   - `useOfflineSync` - Sync queue management
   - `useGeolocation` - GPS tracking
   - `useCamera` - Photo capture
   - `useNotification` - Push notifications & toasts
   - `useFormValidation` - Form validation utilities
4. Build shared UI component library:
   - Layout components (AppHeader, AppSidebar, AppBottomNav)
   - Common components (Button, Input, Select, Modal, Toast)
   - Data display (Table, Card, Badge, StatusIndicator)
   - Form components with validation
   - Loading states and skeletons
5. Create utility functions:
   - Date/time formatters
   - Number formatters
   - Validation helpers
   - Error handlers
   - Storage helpers

### Phase 3: PWA-Specific Setup
For each PWA (driver, operations, safety, fleet):
1. Create workspace with minimal `package.json`
2. Configure Vite with:
   - Proper build output path (`tems/public/{pwa-name}`)
   - PWA plugin with role-specific manifest
   - Dev server proxy to Frappe backend
   - Path aliases to shared code
3. Implement role-specific routing
4. Create PWA-specific components and views
5. Configure Service Worker with appropriate caching strategies

### Phase 4: Frappe Backend Integration
1. Update `tems/hooks.py` to add web routes for all PWAs
2. Create `tems/www/{pwa-name}/index.html` entry points
3. Implement centralized PWA API endpoints in `tems/api/pwa/`
4. Add permissions and role checks
5. Implement file upload handling
6. Set up real-time event handlers (if needed)

### Phase 5: Build & Deployment
1. Create build scripts for:
   - Development (all PWAs with hot reload)
   - Production (optimized builds)
   - Individual PWA builds
2. Configure Docker integration:
   - Multi-stage build
   - Proper caching layers
   - Development vs production modes
3. Set up CI/CD scripts for automated builds
4. Create deployment documentation

## Key Requirements & Constraints

### Code Quality
- Use TypeScript strict mode throughout
- Implement comprehensive error handling
- Add JSDoc comments for public APIs
- Follow Vue 3 Composition API best practices
- Use `<script setup>` syntax
- Implement proper TypeScript types for all Frappe DocTypes

### Performance
- Implement code splitting per PWA
- Lazy load routes and components
- Optimize bundle sizes (< 200KB initial load per PWA)
- Use virtual scrolling for large lists
- Implement proper memoization

### Offline-First
- All read operations must work offline
- Write operations queue when offline
- Implement conflict resolution
- Show clear offline indicators
- Handle partial connectivity scenarios

### Security
- Never store passwords in localStorage
- Implement proper XSS prevention
- Sanitize all user inputs
- Use CSP headers
- Implement rate limiting on API calls

### UX/UI
- Mobile-first responsive design
- Modern, professional UI with proper contrast
- Smooth transitions and animations
- Loading states for all async operations
- Error states with recovery options
- Empty states with helpful guidance
- Consistent spacing and typography
- Accessible (WCAG 2.1 AA compliance)

### Frappe Integration
- Do NOT modify Frappe core files
- Do NOT interfere with Frappe Desk
- Use Frappe's permission system
- Follow Frappe naming conventions
- Respect Frappe's DocType structure
- Use Frappe's file attachment system

## Development Workflow

### Scripts Required
```json
{
  "dev:all": "Run all PWAs concurrently",
  "dev:driver": "Run driver PWA only",
  "dev:operations": "Run operations PWA only",
  "dev:safety": "Run safety PWA only",
  "dev:fleet": "Run fleet PWA only",
  "build:all": "Build all PWAs for production",
  "build:driver": "Build driver PWA only",
  "build:operations": "Build operations PWA only",
  "build:safety": "Build safety PWA only",
  "build:fleet": "Build fleet PWA only",
  "type-check": "Run TypeScript type checking",
  "lint": "Run ESLint",
  "lint:fix": "Fix ESLint errors",
  "format": "Run Prettier",
  "test": "Run unit tests (future)",
  "clean": "Clean all build outputs and node_modules"
}
```

### Git Structure
```
.gitignore should include:
- node_modules/
- */dist/
- *.local
- .env.local
- tems/public/driver/
- tems/public/operations/
- tems/public/safety/
- tems/public/fleet/
```

## Migration Plan for Existing driver-pwa

1. Backup current driver-pwa implementation
2. Extract reusable components to shared/
3. Extract stores to shared/stores/
4. Extract composables to shared/composables/
5. Extract utilities to shared/utils/
6. Refactor driver-pwa to use shared code with @shared alias
7. Update imports throughout driver-pwa
8. Test driver-pwa functionality after refactor
9. Ensure build output still goes to correct location

## Testing & Validation

After refactoring, validate:
1. All PWAs build successfully without errors
2. No circular dependencies in shared code
3. TypeScript compiles without errors
4. Each PWA runs independently
5. Shared components work across all PWAs
6. Frappe API integration works correctly
7. Offline functionality works as expected
8. Build outputs are in correct Frappe directories
9. Frappe Desk is unaffected and still works
10. File sizes are optimized (< 200KB initial)

## Expected Deliverables

1. Complete monorepo structure with all configuration files
2. Shared component library with examples
3. Core composables with TypeScript types
4. Base Pinia stores with offline sync
5. Type-safe Frappe API client
6. Updated build and dev scripts
7. Comprehensive README.md with:
   - Setup instructions
   - Development workflow
   - Build process
   - Deployment guide
   - Architecture documentation
8. Migration guide for existing driver-pwa
9. Example implementations for each PWA type

## Design System Specifications

### Colors
```typescript
const colors = {
  primary: {
    50: '#f0f9ff',
    100: '#e0f2fe',
    500: '#0ea5e9',
    600: '#0284c7',
    700: '#0369a1',
  },
  success: '#10b981',
  warning: '#f59e0b',
  danger: '#ef4444',
  gray: {
    50: '#f9fafb',
    100: '#f3f4f6',
    500: '#6b7280',
    900: '#111827',
  }
}
```

### Typography
- Font Family: System font stack
- Base Size: 16px
- Scale: 1.25 (Major Third)

### Spacing
- Base: 4px (0.25rem)
- Scale: 4, 8, 12, 16, 24, 32, 48, 64

### Shadows
```css
--shadow-soft: 0 2px 15px -3px rgba(0, 0, 0, 0.07), 0 10px 20px -2px rgba(0, 0, 0, 0.04);
--shadow-card: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
```

## Questions to Address During Implementation

1. Should we use Turborepo/Nx for better caching, or stick with npm workspaces?
2. Do we need a shared component preview/documentation tool (Storybook)?
3. Should we implement E2E testing (Playwright/Cypress) from the start?
4. Do we need separate staging/production environment configs?
5. Should we implement feature flags for gradual rollout?
6. Do we need internationalization (i18n) support?
7. Should we implement analytics/telemetry?

## Success Criteria

✅ Clean separation of concerns (shared vs PWA-specific)
✅ No code duplication across PWAs
✅ Type-safe Frappe integration
✅ Offline-first functionality working
✅ Build size optimized (< 200KB per PWA)
✅ Fast development experience (< 3s HMR)
✅ Frappe Desk completely unaffected
✅ All PWAs deployable independently
✅ Easy to add new PWAs in future
✅ Clear documentation for team onboarding

## Timeline
Target: Complete refactoring in 3-5 working days

---

Please implement this refactoring with:
- Clean, production-ready code
- Comprehensive TypeScript types
- Proper error handling
- Detailed comments for complex logic
- Following Vue 3 and Vite best practices
- Ensuring scalability for future PWAs

Ask clarifying questions if any requirements are unclear.

🎯 Additional Context Files to Provide
Create these files to give the AI agent complete context:
1. current-structure.txt
txt[Paste your current driver-pwa file tree output from:
tree -L 4 -I 'node_modules|dist|.git' frontend/driver-pwa/
]
2. frappe-context.md
markdown# Frappe Environment Context

## Versions
- Frappe: V15.83.0
- ERPNext: V15.80.0
- Node.js: 18.x
- Python: 3.11

## Docker Setup
- Using frappe_docker
- Development in VSCode devcontainer
- Production: Frappe Cloud or VPS

## Frappe Backend URL
- Development: http://localhost:8000
- API Endpoint: http://localhost:8000/api/resource/{DocType}

## Current Desk URLs (Must not affect)
- http://localhost:8000/app (Frappe Desk)
- http://localhost:8000/desk (Legacy)
3. existing-driver-pwa-features.md
markdown# Current Driver PWA Features

## Implemented
- [ ] Login/Authentication
- [ ] Dashboard with trip overview
- [ ] Trip list view
- [ ] Trip details
- [ ] Basic offline storage
- [ ] ...

## Partially Implemented
- [ ] ...

## Not Yet Implemented
- [ ] ...