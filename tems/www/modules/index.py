"""
Python controller for module pages
Dynamically generates module detail pages based on configuration
"""

import frappe
from frappe import _

# Module configurations
MODULES_CONFIG = {
    "governance": {
        "title": "Leadership & Governance",
        "description": "Strategic planning, KPIs, policy management, and executive dashboards for transport excellence",
        "icon": "🛡️",
        "color": "#a855f7",
        "gradient": "linear-gradient(135deg, #a855f7 0%, #7c3aed 100%)",
        "stats": [
            {"value": "100%", "label": "Policy Compliance"},
            {"value": "Real-time", "label": "KPI Tracking"},
            {"value": "360°", "label": "Governance View"},
            {"value": "Automated", "label": "Compliance Audits"}
        ],
        "features": [
            {"icon": "🎯", "title": "Strategic Planning", "description": "Define vision, mission, and strategic goals with cascading KPIs across the organization"},
            {"icon": "📋", "title": "Policy Management", "description": "Create, publish, and track policy acknowledgment and compliance across all staff"},
            {"icon": "✅", "title": "Compliance Audits", "description": "Schedule and conduct regular compliance audits with automated workflows and notifications"},
            {"icon": "📊", "title": "Executive Dashboards", "description": "Real-time visibility into organizational performance with customizable executive dashboards"},
            {"icon": "🔍", "title": "Spot Checks", "description": "Conduct random spot checks to ensure adherence to policies and procedures"},
            {"icon": "⚖️", "title": "Regulatory Compliance", "description": "Track regulatory requirements and ensure timely compliance across operations"}
        ],
        "benefits": [
            "Ensure 100% policy compliance across the organization",
            "Real-time visibility into strategic goal achievement",
            "Automated compliance tracking and reporting",
            "Reduced regulatory risk and penalties",
            "Data-driven executive decision making",
            "Standardized governance processes"
        ],
        "use_cases": [
            {
                "title": "🏢 Multi-Branch Transport Company",
                "description": "A transport company with 15 branches uses TEMS Governance to ensure consistent policy implementation. The system tracks policy acknowledgment across 500+ staff, automates compliance audits, and provides executives with real-time visibility into KPI achievement across all locations."
            },
            {
                "title": "🚌 Public Transport Authority",
                "description": "A government transport authority manages regulatory compliance for 200+ licensed operators. TEMS helps them track operator compliance, schedule regular audits, and generate regulatory reports automatically."
            }
        ]
    },
    "operations": {
        "title": "Operations Management",
        "description": "Real-time dispatch, route optimization, and operational excellence for efficient transport operations",
        "icon": "🚚",
        "color": "#3b82f6",
        "gradient": "linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)",
        "stats": [
            {"value": "20%", "label": "Route Optimization"},
            {"value": "Real-time", "label": "GPS Tracking"},
            {"value": "95%", "label": "On-Time Performance"},
            {"value": "24/7", "label": "Operations Control"}
        ],
        "features": [
            {"icon": "📍", "title": "Trip Management", "description": "Plan, schedule, and track all trips with real-time status updates and GPS integration"},
            {"icon": "🗺️", "title": "Route Optimization", "description": "AI-powered route optimization to minimize distance, fuel consumption, and travel time"},
            {"icon": "📱", "title": "Real-time Tracking", "description": "Live GPS tracking of all vehicles with geofencing and automated alerts"},
            {"icon": "🎯", "title": "Dispatch Control", "description": "Centralized dispatch console for managing vehicle and driver assignments"},
            {"icon": "⚠️", "title": "SOS Management", "description": "Emergency response system with instant alerts and incident tracking"},
            {"icon": "📊", "title": "Performance Analytics", "description": "Comprehensive operational metrics and KPI dashboards"}
        ],
        "benefits": [
            "Reduce fuel costs through optimized routing",
            "Improve on-time performance by 30%+",
            "Real-time visibility into all operations",
            "Faster emergency response times",
            "Reduced operational costs",
            "Enhanced customer satisfaction"
        ],
        "use_cases": [
            {
                "title": "📦 E-commerce Delivery",
                "description": "A last-mile delivery company handles 1000+ deliveries daily. TEMS Operations optimizes routes in real-time, tracks each vehicle's progress, and provides customers with accurate delivery ETAs. This has reduced delivery times by 25% and fuel costs by 15%."
            },
            {
                "title": "🚌 Inter-city Bus Service",
                "description": "A bus operator runs 50+ daily routes across 10 cities. TEMS provides real-time tracking, automated delays notifications to passengers, and helps dispatchers manage vehicle breakdowns or route changes efficiently."
            }
        ]
    },
    "safety": {
        "title": "Safety & Risk Management",
        "description": "Comprehensive incident management, risk assessments, and compliance monitoring for safer operations",
        "icon": "⚠️",
        "color": "#ef4444",
        "gradient": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)",
        "stats": [
            {"value": "60%", "label": "Incident Reduction"},
            {"value": "Real-time", "label": "Risk Alerts"},
            {"value": "100%", "label": "Incident Tracking"},
            {"value": "Proactive", "label": "Risk Management"}
        ],
        "features": [
            {"icon": "📝", "title": "Incident Reporting", "description": "Digital incident reporting with photo attachments, witness statements, and automated workflows"},
            {"icon": "🔍", "title": "Risk Assessments", "description": "Conduct and track risk assessments for routes, drivers, and vehicles"},
            {"icon": "✅", "title": "Safety Audits", "description": "Schedule and perform regular safety audits with checklists and findings tracking"},
            {"icon": "👨‍✈️", "title": "Driver Competence", "description": "Track driver qualifications, licenses, medical fitness, and training requirements"},
            {"icon": "🛣️", "title": "Journey Planning", "description": "Pre-trip safety planning with risk assessment and route hazard identification"},
            {"icon": "📊", "title": "Safety Analytics", "description": "Analyze incident trends, identify high-risk areas, and measure safety KPIs"}
        ],
        "benefits": [
            "Reduce accidents and incidents by up to 60%",
            "Ensure driver competence and compliance",
            "Proactive risk identification and mitigation",
            "Comprehensive incident investigation trails",
            "Regulatory compliance and audit readiness",
            "Lower insurance premiums"
        ],
        "use_cases": [
            {
                "title": "🚛 Long-Haul Freight",
                "description": "A freight company operates 24/7 across hazardous routes. TEMS Safety tracks driver fatigue, conducts pre-trip risk assessments, and records all incidents. Since implementation, they've reduced accidents by 55% and improved their safety rating."
            },
            {
                "title": "🚌 School Transport",
                "description": "A school bus operator prioritizes child safety. TEMS ensures all drivers have valid licenses and clearances, tracks vehicle safety inspections, and maintains detailed incident records for compliance."
            }
        ]
    },
    "finance": {
        "title": "Finance & Profitability",
        "description": "Comprehensive cost tracking, revenue management, and profitability analysis for transport operations",
        "icon": "💰",
        "color": "#f59e0b",
        "gradient": "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)",
        "stats": [
            {"value": "25%", "label": "Cost Reduction"},
            {"value": "Real-time", "label": "P&L Tracking"},
            {"value": "100%", "label": "Cost Visibility"},
            {"value": "Automated", "label": "Revenue Recognition"}
        ],
        "features": [
            {"icon": "📒", "title": "Cost & Revenue Ledger", "description": "Track all costs and revenues at vehicle, trip, and route levels"},
            {"icon": "📈", "title": "Profitability Analysis", "description": "Calculate profitability by vehicle, route, customer, and service type"},
            {"icon": "🧮", "title": "Journey Costing", "description": "Allocate costs accurately to each journey including fuel, tolls, and driver wages"},
            {"icon": "💳", "title": "Payment Management", "description": "Manage invoicing, payments, and receivables with integration to accounting systems"},
            {"icon": "📊", "title": "Financial Reports", "description": "Comprehensive financial reports including P&L, cash flow, and cost analysis"},
            {"icon": "🎯", "title": "Budget Management", "description": "Set budgets, track variances, and receive alerts for budget overruns"}
        ],
        "benefits": [
            "Reduce operational costs by 25%+",
            "Accurate profitability tracking per vehicle",
            "Identify and eliminate unprofitable routes",
            "Improved cash flow management",
            "Data-driven pricing decisions",
            "Financial transparency and control"
        ],
        "use_cases": [
            {
                "title": "🚚 Fleet Operator",
                "description": "A fleet operator with 100+ vehicles struggled with profitability visibility. TEMS Finance tracks costs and revenues per vehicle, revealing that 15 vehicles were unprofitable. After optimization, overall profitability improved by 18%."
            },
            {
                "title": "🚌 Tour Bus Company",
                "description": "A tour operator needs to price routes accurately. TEMS provides detailed cost breakdowns including fuel, maintenance, and driver costs, enabling them to set profitable rates while remaining competitive."
            }
        ]
    },
    "cargo": {
        "title": "Cargo Logistics",
        "description": "Comprehensive freight management, consignment tracking, and load optimization",
        "icon": "📦",
        "color": "#f97316",
        "gradient": "linear-gradient(135deg, #f97316 0%, #ea580c 100%)",
        "stats": [
            {"value": "95%", "label": "Load Optimization"},
            {"value": "Real-time", "label": "Cargo Tracking"},
            {"value": "30%", "label": "Capacity Increase"},
            {"value": "100%", "label": "POD Management"}
        ],
        "features": [
            {"icon": "📦", "title": "Consignment Management", "description": "End-to-end consignment tracking from pickup to delivery with status updates"},
            {"icon": "⚖️", "title": "Load Optimization", "description": "Maximize vehicle capacity utilization with intelligent load planning"},
            {"icon": "📄", "title": "Documentation", "description": "Digital waybills, PODs, and customs documentation"},
            {"icon": "📍", "title": "Tracking & Alerts", "description": "Real-time consignment tracking with customer notifications"},
            {"icon": "💰", "title": "Freight Pricing", "description": "Dynamic freight pricing based on weight, distance, and service level"},
            {"icon": "📊", "title": "Cargo Analytics", "description": "Analyze cargo volumes, routes, and customer profitability"}
        ],
        "benefits": [
            "Increase load capacity utilization by 30%",
            "Real-time cargo visibility for customers",
            "Reduce paperwork with digital documentation",
            "Faster delivery confirmation with e-POD",
            "Optimize routes based on cargo requirements",
            "Improved customer satisfaction"
        ],
        "use_cases": [
            {
                "title": "🚛 Cross-Border Freight",
                "description": "A freight forwarder handles cargo across 5 countries. TEMS Cargo tracks consignments across borders, manages customs documentation, and provides customers with real-time tracking portals."
            },
            {
                "title": "📦 Last-Mile Delivery",
                "description": "An e-commerce logistics provider handles 2000+ parcels daily. TEMS optimizes vehicle loads, provides customers with delivery notifications, and captures digital PODs."
            }
        ]
    },
    "passenger": {
        "title": "Passenger Transport",
        "description": "Comprehensive booking, seat management, and passenger service management",
        "icon": "👥",
        "color": "#6366f1",
        "gradient": "linear-gradient(135deg, #6366f1 0%, #4f46e5 100%)",
        "stats": [
            {"value": "100%", "label": "Seat Utilization"},
            {"value": "Real-time", "label": "Booking System"},
            {"value": "35%", "label": "Revenue Increase"},
            {"value": "Digital", "label": "Ticketing"}
        ],
        "features": [
            {"icon": "🎫", "title": "Booking Management", "description": "Online and offline booking with seat selection and payment integration"},
            {"icon": "💺", "title": "Seat Allocation", "description": "Real-time seat availability and dynamic seat assignment"},
            {"icon": "📱", "title": "Digital Ticketing", "description": "E-tickets, QR codes, and mobile ticket validation"},
            {"icon": "👥", "title": "Passenger Manifest", "description": "Complete passenger records for compliance and safety"},
            {"icon": "💳", "title": "Pricing & Promotions", "description": "Dynamic pricing, discounts, and promotional campaigns"},
            {"icon": "📊", "title": "Passenger Analytics", "description": "Analyze booking patterns, load factors, and customer preferences"}
        ],
        "benefits": [
            "Increase seat utilization to 100%",
            "Reduce no-shows with digital ticketing",
            "Real-time booking and payment processing",
            "Enhanced passenger experience",
            "Dynamic pricing to maximize revenue",
            "Compliance with passenger manifest requirements"
        ],
        "use_cases": [
            {
                "title": "🚌 Inter-city Bus Service",
                "description": "A bus company operates 50+ daily routes. TEMS Passenger provides online booking, e-ticketing, and real-time seat availability. This increased online bookings by 70% and overall load factor by 25%."
            },
            {
                "title": "🚖 Ride-Sharing Service",
                "description": "A ride-sharing platform manages bookings for shared taxis. TEMS optimizes seat allocation, manages payments, and ensures passenger safety with digital records."
            }
        ]
    },
    "tyre": {
        "title": "Tyre Management",
        "description": "Comprehensive tyre lifecycle tracking, predictive maintenance, and cost optimization",
        "icon": "⚙️",
        "color": "#6b7280",
        "gradient": "linear-gradient(135deg, #6b7280 0%, #4b5563 100%)",
        "stats": [
            {"value": "40%", "label": "Tyre Life Extension"},
            {"value": "Real-time", "label": "Pressure Monitoring"},
            {"value": "25%", "label": "Cost Reduction"},
            {"value": "Predictive", "label": "Replacement Alerts"}
        ],
        "features": [
            {"icon": "🔄", "title": "Lifecycle Tracking", "description": "Track each tyre from purchase through disposal including installations and rotations"},
            {"icon": "📊", "title": "Pressure Monitoring", "description": "Real-time tyre pressure and temperature monitoring with alerts"},
            {"icon": "💰", "title": "Cost Analysis", "description": "Calculate cost-per-kilometer and identify optimization opportunities"},
            {"icon": "📅", "title": "Rotation Scheduling", "description": "Automated rotation reminders to maximize tyre life"},
            {"icon": "🔮", "title": "Predictive Maintenance", "description": "AI predictions for tyre replacement timing based on wear patterns"},
            {"icon": "📈", "title": "Tyre Analytics", "description": "Analyze tyre performance, vendor quality, and fleet trends"}
        ],
        "benefits": [
            "Extend tyre life by up to 40%",
            "Reduce fuel consumption with proper inflation",
            "Prevent blowouts with predictive alerts",
            "Optimize tyre purchasing decisions",
            "Track warranty claims efficiently",
            "Lower total cost of ownership"
        ],
        "use_cases": [
            {
                "title": "🚛 Long-Haul Fleet",
                "description": "A trucking company with 200 vehicles spends $2M annually on tyres. TEMS Tyre Management tracks each tyre's lifecycle, schedules rotations, and predicts replacements. This extended tyre life by 35% and reduced costs by $500K annually."
            },
            {
                "title": "🚌 City Bus Fleet",
                "description": "A municipal bus fleet faces high tyre wear on urban routes. TEMS monitors tyre pressure in real-time, preventing under-inflation which was causing 60% of premature failures."
            }
        ]
    },
    "ai": {
        "title": "AI & Insights",
        "description": "Machine learning predictions, anomaly detection, and advanced analytics",
        "icon": "🤖",
        "color": "#ec4899",
        "gradient": "linear-gradient(135deg, #eebed6 0%, #db2777 100%)",
        "stats": [
            {"value": "70%", "label": "Prediction Accuracy"},
            {"value": "Real-time", "label": "Anomaly Detection"},
            {"value": "50%", "label": "Breakdown Prevention"},
            {"value": "AI-Powered", "label": "Insights"}
        ],
        "features": [
            {"icon": "🔧", "title": "Predictive Maintenance", "description": "ML models predict component failures before they occur"},
            {"icon": "📈", "title": "Demand Forecasting", "description": "Predict booking demand and optimize fleet deployment"},
            {"icon": "🔍", "title": "Anomaly Detection", "description": "Automatically identify unusual patterns and potential issues"},
            {"icon": "🎯", "title": "Smart Alerts", "description": "Context-aware alerts that reduce false positives by 80%"},
            {"icon": "💡", "title": "Optimization Recommendations", "description": "AI-powered suggestions for route, fuel, and cost optimization"},
            {"icon": "📊", "title": "Advanced Analytics", "description": "Deep insights into operations, costs, and performance"}
        ],
        "benefits": [
            "Prevent 50%+ of unexpected breakdowns",
            "Optimize maintenance timing and costs",
            "Identify inefficiencies automatically",
            "Reduce false alerts significantly",
            "Data-driven strategic decisions",
            "Continuous performance improvement"
        ],
        "use_cases": [
            {
                "title": "🚛 Predictive Fleet Maintenance",
                "description": "A logistics company uses TEMS AI to predict engine failures. The system analyzes sensor data from 300 vehicles and alerts mechanics 2-3 weeks before failures occur, reducing unplanned downtime by 65%."
            },
            {
                "title": "🚌 Demand Forecasting",
                "description": "A bus operator uses AI to forecast passenger demand across routes. This enables dynamic fleet allocation, reducing empty runs by 40% and improving revenue by 20%."
            }
        ]
    },
    "people": {
        "title": "People & HR Management",
        "description": "Comprehensive recruitment, training, competency management, and performance tracking",
        "icon": "👔",
        "color": "#14b8a6",
        "gradient": "linear-gradient(135deg, #14b8a6 0%, #0d9488 100%)",
        "stats": [
            {"value": "50%", "label": "Faster Hiring"},
            {"value": "100%", "label": "Competency Tracking"},
            {"value": "40%", "label": "Training Efficiency"},
            {"value": "Real-time", "label": "Performance Data"}
        ],
        "features": [
            {"icon": "📝", "title": "Recruitment", "description": "Streamlined recruitment with applicant tracking and onboarding workflows"},
            {"icon": "📚", "title": "Training Management", "description": "Schedule, track, and evaluate training programs and certifications"},
            {"icon": "🎯", "title": "Competency Matrix", "description": "Define and track required competencies for each role"},
            {"icon": "📊", "title": "Performance Reviews", "description": "Structured performance evaluations with goal tracking"},
            {"icon": "📄", "title": "Document Management", "description": "Store and track licenses, certifications, and employee documents"},
            {"icon": "⏰", "title": "Attendance & Leave", "description": "Integrated time tracking and leave management"}
        ],
        "benefits": [
            "Reduce hiring time by 50%",
            "Ensure 100% compliance with certifications",
            "Track employee competencies systematically",
            "Improve performance management",
            "Reduce training costs",
            "Better workforce planning"
        ],
        "use_cases": [
            {
                "title": "🚌 Driver Recruitment",
                "description": "A transport company hires 50+ drivers annually. TEMS People streamlines recruitment, verifies licenses and clearances, and ensures all drivers complete required training before deployment."
            },
            {
                "title": "👷 Multi-Role Organization",
                "description": "A logistics company has drivers, mechanics, and administrators. TEMS tracks competencies for each role, schedules training renewals, and alerts HR when certifications expire."
            }
        ]
    },
    "trade": {
        "title": "Cross-Border Trade",
        "description": "Border crossing management, customs clearance, and trade compliance",
        "icon": "🌍",
        "color": "#3b82f6",
        "gradient": "linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)",
        "stats": [
            {"value": "40%", "label": "Faster Clearance"},
            {"value": "100%", "label": "Document Tracking"},
            {"value": "Real-time", "label": "Border Status"},
            {"value": "Digital", "label": "Documentation"}
        ],
        "features": [
            {"icon": "🛂", "title": "Border Crossings", "description": "Track vehicles, drivers, and cargo at border posts with status updates"},
            {"icon": "📄", "title": "Customs Documentation", "description": "Digital management of customs declarations, permits, and certificates"},
            {"icon": "🗺️", "title": "Trade Lanes", "description": "Define and manage trade corridors with border post requirements"},
            {"icon": "✅", "title": "Compliance Tracking", "description": "Ensure compliance with trade regulations across countries"},
            {"icon": "⏱️", "title": "Dwell Time Tracking", "description": "Monitor and optimize border crossing times"},
            {"icon": "📊", "title": "Trade Analytics", "description": "Analyze trade volumes, clearance times, and bottlenecks"}
        ],
        "benefits": [
            "Reduce border crossing times by 40%",
            "Digital customs documentation",
            "Compliance with trade regulations",
            "Real-time border post visibility",
            "Reduced paperwork and delays",
            "Improved cross-border efficiency"
        ],
        "use_cases": [
            {
                "title": "🚛 Regional Freight",
                "description": "A freight company operates across 6 African countries. TEMS Trade tracks vehicles at each border post, manages customs documentation digitally, and reduced average border crossing time from 8 hours to 4.5 hours."
            },
            {
                "title": "🌍 Import/Export Business",
                "description": "An importer manages shipments through multiple ports. TEMS tracks documentation, compliance requirements, and coordinates with customs agents automatically."
            }
        ]
    },
    "climate": {
        "title": "Climate & Sustainability",
        "description": "Emissions tracking, carbon footprint analysis, and eco-routing for sustainable transport",
        "icon": "🌱",
        "color": "#22c55e",
        "gradient": "linear-gradient(135deg, #22c55e 0%, #16a34a 100%)",
        "stats": [
            {"value": "30%", "label": "Emissions Reduction"},
            {"value": "Real-time", "label": "Carbon Tracking"},
            {"value": "100%", "label": "Route Optimization"},
            {"value": "Automated", "label": "ESG Reporting"}
        ],
        "features": [
            {"icon": "📊", "title": "Emissions Tracking", "description": "Calculate and track CO2 emissions per vehicle, trip, and route"},
            {"icon": "🌍", "title": "Carbon Footprint", "description": "Comprehensive carbon footprint analysis across operations"},
            {"icon": "🗺️", "title": "Eco-routing", "description": "Route optimization prioritizing fuel efficiency and emissions reduction"},
            {"icon": "☁️", "title": "Climate Alerts", "description": "Weather-based alerts for route planning and safety"},
            {"icon": "📈", "title": "ESG Reporting", "description": "Automated environmental, social, and governance reporting"},
            {"icon": "🎯", "title": "Sustainability Goals", "description": "Set and track carbon reduction targets"}
        ],
        "benefits": [
            "Reduce carbon emissions by 30%+",
            "Meet ESG reporting requirements",
            "Optimize routes for fuel efficiency",
            "Demonstrate environmental commitment",
            "Reduce fuel costs simultaneously",
            "Comply with emission regulations"
        ],
        "use_cases": [
            {
                "title": "🚛 Green Logistics",
                "description": "A logistics company committed to carbon neutrality by 2030. TEMS Climate tracks emissions per shipment, recommends eco-routes, and provides carbon reports to customers. They've reduced emissions by 28% in 2 years."
            },
            {
                "title": "🚌 Sustainable Public Transport",
                "description": "A city bus operator reports ESG metrics to government. TEMS automates carbon footprint calculation, tracks progress towards emission targets, and generates compliance reports."
            }
        ]
    },
    "supply_chain": {
        "title": "Supply Chain Management",
        "description": "Procurement, inventory management, and supplier performance optimization",
        "icon": "📊",
        "color": "#a855f7",
        "gradient": "linear-gradient(135deg, #a855f7 0%, #7c3aed 100%)",
        "stats": [
            {"value": "35%", "label": "Cost Savings"},
            {"value": "Real-time", "label": "Inventory Tracking"},
            {"value": "90%", "label": "Stock Availability"},
            {"value": "Automated", "label": "Procurement"}
        ],
        "features": [
            {"icon": "🛒", "title": "Procurement", "description": "Streamlined procurement with RFQs, POs, and vendor management"},
            {"icon": "📦", "title": "Inventory Management", "description": "Track spare parts, consumables, and materials across locations"},
            {"icon": "⭐", "title": "Supplier Ratings", "description": "Evaluate supplier performance on quality, delivery, and cost"},
            {"icon": "🚚", "title": "Logistics", "description": "Coordinate inbound and outbound logistics efficiently"},
            {"icon": "🔔", "title": "Stock Alerts", "description": "Automated low-stock alerts and reorder point management"},
            {"icon": "📊", "title": "Supply Chain Analytics", "description": "Analyze spend, lead times, and supplier performance"}
        ],
        "benefits": [
            "Reduce procurement costs by 35%",
            "Maintain optimal stock levels",
            "Reduce stockouts and downtime",
            "Improve supplier performance",
            "Streamline procurement processes",
            "Better spend visibility and control"
        ],
        "use_cases": [
            {
                "title": "🔧 Spare Parts Management",
                "description": "A fleet operator manages 500+ SKUs across 10 workshops. TEMS Supply Chain tracks inventory in real-time, alerts when critical parts are low, and automates reordering. This reduced stockouts by 80% and excess inventory by 40%."
            },
            {
                "title": "⛽ Fuel Procurement",
                "description": "A transport company spends $5M annually on fuel. TEMS tracks fuel purchases across suppliers, analyzes pricing trends, and consolidated purchasing led to 12% cost savings."
            }
        ]
    }
}


def get_context(context):
    """Get context for module detail page"""
    # Allow guest access
    frappe.flags.ignore_permissions = True
    
    # Get module ID from path
    module_id = frappe.form_dict.get("module") or context.get("module")
    
    if not module_id or module_id not in MODULES_CONFIG:
        frappe.throw(_("Module not found"), frappe.DoesNotExistError)
    
    module_data = MODULES_CONFIG[module_id]
    
    context.update({
        "module_id": module_id,
        "module": module_data,
        "no_cache": 1,  # Don't cache for now
        "show_sidebar": False,
        "title": f"{module_data['title']} - TEMS"
    })
    
    return context
