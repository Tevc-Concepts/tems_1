/**
 * TEMS Landing Page JavaScript
 * Handles PWA installation, dynamic content loading, and animations
 */

(function() {
    'use strict';

    // Module data for dynamic rendering
    const modules = [
        {
            id: 'governance',
            title: 'Leadership & Governance',
            description: 'Strategic planning, KPIs, policy management, and executive dashboards',
            icon: '🛡️',
            color: 'purple',
            route: '/modules/governance',
            features: [
                'Vision & Mission Tracking',
                'Strategic Goals & KPIs',
                'Policy Management',
                'Compliance Audits'
            ]
        },
        {
            id: 'operations',
            title: 'Operations Management',
            description: 'Real-time dispatch, route optimization, and operational excellence',
            icon: '🚚',
            color: 'blue',
            route: '/modules/operations',
            features: [
                'Trip Management',
                'Route Optimization',
                'Real-time Tracking',
                'Dispatch Control'
            ]
        },
        {
            id: 'fleet',
            title: 'Fleet Management',
            description: 'Asset lifecycle, maintenance scheduling, and utilization tracking',
            icon: '🔧',
            color: 'green',
            route: '/modules/fleet',
            features: [
                'Asset Management',
                'Maintenance Scheduling',
                'Utilization Tracking',
                'Work Order Management'
            ]
        },
        {
            id: 'safety',
            title: 'Safety & Risk',
            description: 'Incident management, risk assessments, and compliance monitoring',
            icon: '⚠️',
            color: 'red',
            route: '/modules/safety',
            features: [
                'Incident Reporting',
                'Risk Assessments',
                'Safety Audits',
                'Driver Competence'
            ]
        },
        {
            id: 'finance',
            title: 'Finance & Profitability',
            description: 'Cost tracking, revenue management, and profitability analysis',
            icon: '💰',
            color: 'yellow',
            route: '/modules/finance',
            features: [
                'Cost & Revenue Ledger',
                'Profitability Analysis',
                'Journey Costing',
                'Financial Reports'
            ]
        },
        {
            id: 'cargo',
            title: 'Cargo Logistics',
            description: 'Freight management, consignment tracking, and load optimization',
            icon: '📦',
            color: 'orange',
            route: '/modules/cargo',
            features: [
                'Consignment Tracking',
                'Load Optimization',
                'Freight Management',
                'Documentation'
            ]
        },
        {
            id: 'passenger',
            title: 'Passenger Transport',
            description: 'Booking systems, seat management, and passenger services',
            icon: '👥',
            color: 'indigo',
            route: '/modules/passenger',
            features: [
                'Booking Management',
                'Seat Allocation',
                'Ticketing',
                'Passenger Manifest'
            ]
        },
        {
            id: 'tyre',
            title: 'Tyre Management',
            description: 'Tyre lifecycle tracking, predictive maintenance, and cost analysis',
            icon: '⚙️',
            color: 'gray',
            route: '/modules/tyre',
            features: [
                'Lifecycle Tracking',
                'Pressure Monitoring',
                'Cost Analysis',
                'Rotation Scheduling'
            ]
        },
        {
            id: 'ai',
            title: 'AI & Insights',
            description: 'Machine learning predictions, anomaly detection, and analytics',
            icon: '🤖',
            color: 'pink',
            route: '/modules/ai',
            features: [
                'Predictive Maintenance',
                'Demand Forecasting',
                'Anomaly Detection',
                'Smart Alerts'
            ]
        },
        {
            id: 'people',
            title: 'People & HR',
            description: 'Recruitment, training, competency management, and performance tracking',
            icon: '👔',
            color: 'teal',
            route: '/modules/people',
            features: [
                'Recruitment',
                'Training Records',
                'Competency Matrix',
                'Performance Reviews'
            ]
        },
        {
            id: 'trade',
            title: 'Cross-Border Trade',
            description: 'Border crossing management, customs clearance, and compliance',
            icon: '🌍',
            color: 'blue',
            route: '/modules/trade',
            features: [
                'Border Crossings',
                'Customs Clearance',
                'Trade Lanes',
                'Documentation'
            ]
        },
        {
            id: 'climate',
            title: 'Climate & Sustainability',
            description: 'Emissions tracking, carbon footprint analysis, and eco-routing',
            icon: '🌱',
            color: 'green',
            route: '/modules/climate',
            features: [
                'Emissions Tracking',
                'Carbon Footprint',
                'Eco-routing',
                'Climate Alerts'
            ]
        },
        {
            id: 'supply-chain',
            title: 'Supply Chain',
            description: 'Procurement, inventory management, and supplier performance',
            icon: '📊',
            color: 'purple',
            route: '/modules/supply-chain',
            features: [
                'Procurement',
                'Inventory Management',
                'Supplier Ratings',
                'Logistics'
            ]
        }
    ];

    // PWA Installation handling
    let deferredPrompt;

    window.addEventListener('beforeinstallprompt', (e) => {
        // Prevent the mini-infobar from appearing on mobile
        e.preventDefault();
        // Store the event for later use
        deferredPrompt = e;
        // Show install button
        showInstallButton();
    });

    function showInstallButton() {
        const installButton = document.getElementById('install-button');
        if (installButton) {
            installButton.style.display = 'inline-flex';
            installButton.addEventListener('click', installPWA);
        }
    }

    async function installPWA() {
        if (!deferredPrompt) {
            return;
        }

        // Show the install prompt
        deferredPrompt.prompt();

        // Wait for the user to respond to the prompt
        const { outcome } = await deferredPrompt.userChoice;

        if (outcome === 'accepted') {
            console.log('User accepted the install prompt');
            showInstalledMessage();
        } else {
            console.log('User dismissed the install prompt');
        }

        // Clear the deferredPrompt
        deferredPrompt = null;
    }

    function showInstalledMessage() {
        const installButton = document.getElementById('install-button');
        const installedMessage = document.getElementById('installed-message');
        
        if (installButton) {
            installButton.style.display = 'none';
        }
        if (installedMessage) {
            installedMessage.style.display = 'block';
        }
    }

    // Check if already installed
    window.addEventListener('appinstalled', () => {
        console.log('TEMS PWA was installed');
        showInstalledMessage();
    });

    // Fetch and update metrics
    async function fetchMetrics() {
        try {
            const response = await fetch('/api/method/tems.tems.www.index.get_live_metrics');
            const data = await response.json();
            
            if (data.message) {
                updateMetrics(data.message);
            }
        } catch (error) {
            console.error('Error fetching metrics:', error);
            // Set default values
            updateMetrics({
                active_vehicles: 0,
                ongoing_trips: 0,
                active_consignments: 0,
                passengers_today: 0,
                safety_incidents: 0,
                fleet_utilization: 0,
                on_time_rate: 0,
                avg_response_time: 0
            });
        }
    }

    function updateMetrics(metrics) {
        // Update main metrics
        const vehiclesEl = document.getElementById('metric-vehicles');
        const tripsEl = document.getElementById('metric-trips');
        const consignmentsEl = document.getElementById('metric-consignments');
        const passengersEl = document.getElementById('metric-passengers');

        if (vehiclesEl) animateValue(vehiclesEl, 0, metrics.active_vehicles, 1500);
        if (tripsEl) animateValue(tripsEl, 0, metrics.ongoing_trips, 1500);
        if (consignmentsEl) animateValue(consignmentsEl, 0, metrics.active_consignments, 1500);
        if (passengersEl) animateValue(passengersEl, 0, metrics.passengers_today, 1500);

        // Update additional stats
        const incidentsEl = document.getElementById('stat-incidents');
        const responseEl = document.getElementById('stat-response');
        const utilizationEl = document.getElementById('stat-utilization');
        const ontimeEl = document.getElementById('stat-ontime');

        if (incidentsEl) incidentsEl.textContent = metrics.safety_incidents;
        if (responseEl) responseEl.textContent = `${metrics.avg_response_time}min`;
        if (utilizationEl) utilizationEl.textContent = `${metrics.fleet_utilization}%`;
        if (ontimeEl) ontimeEl.textContent = `${metrics.on_time_rate}%`;
    }

    function animateValue(element, start, end, duration) {
        const range = end - start;
        const increment = range / (duration / 16); // 60fps
        let current = start;

        const timer = setInterval(() => {
            current += increment;
            if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
                current = end;
                clearInterval(timer);
            }
            element.textContent = Math.round(current);
        }, 16);
    }

    // Render modules
    function renderModules() {
        const modulesGrid = document.getElementById('modules-grid');
        if (!modulesGrid) return;

        modulesGrid.innerHTML = modules.map(module => `
            <div class="module-card ${module.color}" onclick="window.location.href='${module.route}'">
                <div class="module-icon">${module.icon}</div>
                <h3 class="module-title">${module.title}</h3>
                <p class="module-description">${module.description}</p>
                <ul class="module-features">
                    ${module.features.map(feature => `<li>${feature}</li>`).join('')}
                </ul>
            </div>
        `).join('');
    }

    // Smooth scroll
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Intersection Observer for animations
    function setupScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, observerOptions);

        // Observe module cards
        document.querySelectorAll('.module-card').forEach(card => {
            observer.observe(card);
        });

        // Observe metric cards
        document.querySelectorAll('.metric-card').forEach(card => {
            observer.observe(card);
        });
    }

    // Initialize on DOM ready
    function init() {
        renderModules();
        fetchMetrics();
        setupScrollAnimations();

        // Refresh metrics every 30 seconds
        setInterval(fetchMetrics, 30000);

        // Check if running as standalone PWA
        if (window.matchMedia('(display-mode: standalone)').matches || 
            window.navigator.standalone === true) {
            console.log('Running as installed PWA');
            showInstalledMessage();
        }
    }

    // Run init when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Service Worker registration
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('/assets/tems/sw.js')
                .then(registration => {
                    console.log('Service Worker registered:', registration);
                })
                .catch(error => {
                    console.log('Service Worker registration failed:', error);
                });
        });
    }
})();
