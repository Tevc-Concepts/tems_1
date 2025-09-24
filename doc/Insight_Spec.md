Transport Excellence Management System (TEMS)
Enhanced Product Requirements Document v2.0
Data Triangulation & Profitability Analytics Focus
Document Version: 2.0
Date: 2024
Target Platform: Frappe Framework / ERPNext
Focus: Comprehensive Profitability Analysis & Data Triangulation
1. Executive Summary & Enhanced Vision
The Transport Excellence Management System (TEMS) v2.0 represents a paradigm shift towards complete financial transparency and data-driven profitability optimization. Building upon the foundational requirements, this enhanced PRD focuses specifically on implementing comprehensive data triangulation architecture that enables granular profitability analysis across all business dimensions.

Core Enhancement Objectives:
360-Degree Profitability Visibility: Real-time profitability analysis at asset, trip, business unit, customer, and enterprise levels
Complete Data Triangulation: Every transaction, cost, and revenue point tracked and attributed across multiple dimensions
Advanced Analytics Framework: Frappe Insights integration with drill-down capabilities for deep operational insights
Real-Time Cost Allocation: Dynamic cost attribution and revenue recognition systems
2. Data Triangulation Architecture
2.1 Core Data Model Framework
The enhanced TEMS implements a multi-dimensional data model that captures every financial and operational transaction with complete attribution across all profitability dimensions. This architecture ensures that every cost can be traced to its source and every revenue stream can be analyzed across multiple business perspectives.

2.1.1 Primary Data Entities
Entity	Frappe DocType	Key Fields	Profitability Attribution
Transaction Core	TEMS_Transaction	transaction_id, timestamp, amount, type, status	Base for all financial calculations
Cost Attribution	TEMS_Cost_Attribution	cost_center, asset_id, trip_id, customer_id, bu_id	Multi-dimensional cost allocation
Revenue Attribution	TEMS_Revenue_Attribution	revenue_stream, customer_id, service_type, margin	Revenue source tracking
Asset Performance	TEMS_Asset_Performance	asset_id, utilization, maintenance_cost, revenue	Individual asset ROI calculation
Trip Economics	TEMS_Trip_Economics	trip_id, route_id, total_cost, revenue, margin	Per-journey profitability
2.1.2 Frappe Framework Implementation Specifications
# TEMS Transaction Core DocType Definition class TEMSTransaction(Document): def validate(self): self.calculate_profit_attribution() self.update_related_profitibility_metrics() def calculate_profit_attribution(self): # Multi-dimensional cost allocation logic for dimension in ['asset', 'trip', 'customer', 'business_unit']: self.allocate_cost_to_dimension(dimension) def on_submit(self): self.update_real_time_dashboards() self.trigger_profitability_recalculation()
Implementation Note: All DocTypes must implement the profit attribution validation hook to ensure real-time profitability calculation updates across all dimensions.
2.2 Data Collection & Validation Framework
2.2.1 Real-Time Data Capture Points
Asset Level: Fuel consumption, maintenance costs, depreciation, utilization hours, revenue generation
Trip Level: Route costs, driver wages, fuel consumption, toll fees, customer payments, cargo-specific charges
Customer Level: Service fees, payment terms, credit costs, relationship maintenance costs, lifetime value
Business Unit Level: Operational overhead, staff costs, facility expenses, equipment allocation, revenue contribution
Enterprise Level: Administrative costs, strategic investments, regulatory compliance costs, overall profitability
2.2.2 Data Validation & Quality Assurance
# Data Validation Framework @frappe.whitelist() def validate_profitability_data(doc, method): """ Comprehensive data validation for profitability calculations """ # Validate cost attribution completeness total_allocated = sum([ doc.asset_allocated_cost or 0, doc.trip_allocated_cost or 0, doc.overhead_allocated_cost or 0 ]) if abs(total_allocated - doc.total_cost) > 0.01: frappe.throw("Cost allocation mismatch detected") # Validate revenue recognition validate_revenue_recognition(doc) update_profitability_metrics(doc)
3. Comprehensive Profitability Analysis Modules
3.1 Asset Profitability Analysis
3.1.1 Individual Asset ROI Calculation
Each asset (vehicle, equipment, facility) maintains a comprehensive profitability profile that tracks all associated costs and revenues in real-time. The system calculates multiple profitability metrics including ROI, net present value, and total cost of ownership.

Metric	Calculation Method	Frappe Field	Update Frequency
Asset ROI	(Revenue - Total Costs) / Initial Investment	asset_roi	Real-time
Daily Profitability	Daily Revenue - Daily Operating Costs	daily_profit	Daily
Utilization Rate	Active Hours / Available Hours	utilization_rate	Hourly
Revenue per KM	Total Revenue / Total Distance	revenue_per_km	Per Trip
Maintenance ROI	Avoided Breakdown Costs / Maintenance Investment	maintenance_roi	Monthly
3.1.2 Asset Cost Attribution Framework
# Asset Profitability Calculation Engine class AssetProfitabilityCalculator: def __init__(self, asset_id): self.asset = frappe.get_doc("Asset", asset_id) self.costs = self.collect_all_costs() self.revenues = self.collect_all_revenues() def calculate_comprehensive_roi(self): """Calculate multi-dimensional ROI""" return { 'financial_roi': self.calculate_financial_roi(), 'operational_roi': self.calculate_operational_roi(), 'environmental_roi': self.calculate_environmental_roi(), 'total_roi': self.calculate_total_roi() } def collect_all_costs(self): """Comprehensive cost collection""" return { 'direct_costs': self.get_direct_operating_costs(), 'indirect_costs': self.get_allocated_overhead_costs(), 'maintenance_costs': self.get_maintenance_costs(), 'depreciation': self.get_depreciation_costs(), 'financing_costs': self.get_financing_costs() }
3.2 Trip/Route Profitability Analysis
3.2.1 Per-Journey Economics
Every trip generates a comprehensive profitability report that includes direct costs, allocated overhead, revenue attribution, and margin analysis. This enables route optimization and pricing strategy development.

Trip Profitability Components:
Direct Costs: Fuel, tolls, driver wages, vehicle wear
Allocated Overhead: Insurance, licensing, administrative costs
Opportunity Costs: Alternative route revenues, asset utilization
Revenue Streams: Base freight, fuel surcharges, accessorial charges
Risk Adjustments: Security costs, weather delays, border delays
3.2.2 Route Profitability Optimization
Analysis Dimension	Key Metrics	Optimization Target	Implementation Method
Distance Efficiency	Revenue per KM, Cost per KM	Maximize revenue density	Route optimization algorithms
Time Efficiency	Revenue per hour, Turnaround time	Minimize idle time	Dynamic scheduling
Load Optimization	Load factor, Weight utilization	Maximize payload revenue	Load planning algorithms
Risk-Adjusted Returns	Risk-adjusted margin, Insurance costs	Optimize risk/return ratio	Predictive risk modeling
3.3 Business Unit Profitability Analysis
3.3.1 Departmental P&L Attribution
Each business unit maintains a complete profit and loss statement with sophisticated cost allocation methodologies that ensure accurate profitability measurement across different operational divisions.

# Business Unit Profitability Framework class BusinessUnitProfitability: def __init__(self, business_unit_id): self.bu = frappe.get_doc("Business Unit", business_unit_id) self.cost_centers = self.get_related_cost_centers() def generate_bu_pnl(self, period): """Generate comprehensive P&L for business unit""" return { 'revenue': { 'direct_revenue': self.calculate_direct_revenue(period), 'allocated_revenue': self.calculate_allocated_revenue(period), 'total_revenue': 0 # Calculated }, 'costs': { 'direct_costs': self.calculate_direct_costs(period), 'allocated_overhead': self.calculate_allocated_overhead(period), 'depreciation': self.calculate_depreciation(period), 'total_costs': 0 # Calculated }, 'profitability': { 'gross_profit': 0, # Revenue - Direct Costs 'operating_profit': 0, # Gross Profit - Overhead 'net_profit': 0, # Operating Profit - Depreciation 'profit_margin': 0 # Net Profit / Revenue } }
3.4 Customer Profitability Analysis
3.4.1 Client-Specific Margin Analysis
Comprehensive customer profitability analysis that considers all aspects of the customer relationship including service costs, payment terms, credit risk, and lifetime value calculations.

Customer Profitability Factor	Measurement Method	Impact on Margins	Optimization Strategy
Service Delivery Costs	Activity-based costing per customer	Direct margin impact	Service standardization
Payment Terms Impact	Cash flow timing analysis	Financing cost allocation	Payment term optimization
Credit Risk Costs	Expected credit loss calculation	Risk-adjusted margin	Credit policy refinement
Relationship Maintenance	Sales and support cost allocation	Overhead allocation impact	Relationship efficiency
Volume Discounts	Volume-based margin analysis	Scale economy benefits	Pricing tier optimization
3.5 Enterprise-Wide Profitability Analysis
3.5.1 Consolidated Profitability Dashboard
The enterprise-level profitability analysis aggregates all lower-level profitability data to provide comprehensive business performance insights with drill-down capabilities to investigate profitability drivers and detractors.

4. Frappe Insights Integration & Advanced Analytics
4.1 Dashboard Architecture
4.1.1 Multi-Level Dashboard Hierarchy
Dashboard Levels:
Executive Dashboard: High-level KPIs and trend analysis
Operational Dashboard: Detailed operational metrics with real-time updates
Asset Dashboard: Individual asset performance and utilization
Financial Dashboard: Comprehensive profitability analysis
Customer Dashboard: Customer-specific performance metrics
4.1.2 Frappe Insights Configuration
# Frappe Insights Dashboard Configuration { "dashboard_name": "TEMS_Profitability_Master", "charts": [ { "chart_name": "Asset_Profitability_Overview", "chart_type": "bar", "data_source": "TEMS Asset Profitability", "x_axis": "asset_name", "y_axis": "roi_percentage", "filters": [ {"field": "is_active", "operator": "=", "value": 1}, {"field": "creation", "operator": ">=", "value": "2024-01-01"} ], "drill_down": { "target_dashboard": "Asset_Detail_Dashboard", "parameter": "asset_id" } }, { "chart_name": "Trip_Profitability_Trends", "chart_type": "line", "data_source": "TEMS Trip Economics", "x_axis": "trip_date", "y_axis": "profit_margin", "time_series": true, "drill_down": { "target_dashboard": "Trip_Detail_Analysis", "parameter": "trip_id" } } ], "filters": [ {"field": "company", "type": "select"}, {"field": "date_range", "type": "daterange"}, {"field": "business_unit", "type": "multiselect"} ] }
4.2 Advanced Analytics Capabilities
4.2.1 Predictive Profitability Modeling
Asset Performance Prediction: ML models to predict future asset profitability based on utilization patterns, maintenance history, and market conditions
Route Profitability Forecasting: Predictive analytics for route profitability considering seasonal variations, fuel price fluctuations, and demand patterns
Customer Lifetime Value: Advanced CLV calculations incorporating churn probability, growth potential, and service cost evolution
Market Opportunity Analysis: Identification of profitable expansion opportunities based on current performance data
4.2.2 Real-Time Profitability Alerts
# Real-Time Alert Configuration def setup_profitability_alerts(): """Configure automated profitability alerts""" alert_configs = [ { 'alert_name': 'Low_Asset_ROI', 'condition': 'asset_roi < 15%', 'frequency': 'daily', 'recipients': ['fleet_manager', 'finance_director'], 'action': 'trigger_asset_review_workflow' }, { 'alert_name': 'Negative_Trip_Margin', 'condition': 'trip_margin < 0', 'frequency': 'immediate', 'recipients': ['operations_manager', 'trip_coordinator'], 'action': 'escalate_pricing_review' }, { 'alert_name': 'Customer_Profitability_Decline', 'condition': 'customer_margin_trend < -5%', 'frequency': 'weekly', 'recipients': ['sales_manager', 'account_manager'], 'action': 'initiate_customer_review' } ] for config in alert_configs: create_custom_alert(config)
5. Real-Time Cost Allocation & Revenue Attribution
5.1 Dynamic Cost Allocation Engine
5.1.1 Multi-Dimensional Cost Allocation
The system implements sophisticated cost allocation methodologies that distribute costs across multiple dimensions simultaneously, ensuring accurate profitability calculation at all organizational levels.

Cost Category	Allocation Method	Allocation Basis	Update Frequency
Direct Operating Costs	Direct Attribution	Actual consumption/usage	Real-time
Vehicle Maintenance	Activity-Based Costing	Usage hours, mileage, service type	Per maintenance event
Administrative Overhead	Revenue-Based Allocation	Proportional to revenue generation	Monthly
Facility Costs	Space/Time Allocation	Floor space usage, time occupation	Monthly
Insurance Costs	Risk-Based Allocation	Asset value, risk profile, usage	Policy period
5.1.2 Cost Allocation Implementation
# Advanced Cost Allocation Engine class TEMSCostAllocationEngine: def __init__(self): self.allocation_rules = self.load_allocation_rules() self.cost_pools = self.initialize_cost_pools() def allocate_costs_real_time(self, transaction): """Real-time cost allocation across all dimensions""" # Primary allocation to direct cost objects direct_allocations = self.calculate_direct_allocations(transaction) # Secondary allocation for overhead costs overhead_allocations = self.calculate_overhead_allocations(transaction) # Tertiary allocation for shared services shared_service_allocations = self.calculate_shared_service_allocations(transaction) # Update all profitability dimensions self.update_asset_profitability(direct_allocations) self.update_trip_profitability(direct_allocations) self.update_customer_profitability(direct_allocations) self.update_business_unit_profitability(overhead_allocations) return { 'direct': direct_allocations, 'overhead': overhead_allocations, 'shared_services': shared_service_allocations } def calculate_activity_based_costs(self, cost_pool, cost_drivers): """Activity-based costing implementation""" cost_per_driver = cost_pool / sum(cost_drivers.values()) allocations = {} for object_id, driver_quantity in cost_drivers.items(): allocations[object_id] = cost_per_driver * driver_quantity return allocations
5.2 Revenue Attribution Framework
5.2.1 Multi-Source Revenue Recognition
The revenue attribution system captures and allocates revenue from multiple sources across all profitability dimensions, ensuring accurate margin calculation and performance measurement.

Revenue Attribution Sources:
Base Transportation Fees: Core service delivery charges
Fuel Surcharges: Dynamic fuel cost recovery
Accessorial Services: Loading, unloading, waiting time, special handling
Premium Services: Express delivery, security escort, climate control
Volume Incentives: Customer loyalty programs and volume discounts
Cross-Border Fees: Documentation, customs clearance, regulatory compliance
6. Implementation Roadmap & Technical Specifications
6.1 Frappe/ERPNext Customization Framework
6.1.1 Core DocType Extensions
ERPNext DocType	TEMS Extensions	New Fields	Custom Scripts
Asset	TEMS Asset Profitability	roi_percentage, utilization_rate, profit_contribution	Real-time ROI calculation
Sales Invoice	TEMS Revenue Attribution	trip_reference, asset_allocation, margin_analysis	Multi-dimensional revenue split
Purchase Invoice	TEMS Cost Attribution	cost_allocation_matrix, profitability_impact	Dynamic cost allocation
Project	TEMS Trip Management	route_profitability, resource_utilization	Trip economics calculation
6.1.2 Custom App Structure
# TEMS App Structure tems/ ├── tems/ │ ├── __init__.py │ ├── hooks.py │ ├── profitability_engine/ │ │ ├── __init__.py │ │ ├── asset_profitability.py │ │ ├── trip_profitability.py │ │ ├── customer_profitability.py │ │ ├── business_unit_profitability.py │ │ └── cost_allocation_engine.py │ ├── analytics/ │ │ ├── __init__.py │ │ ├── dashboard_controller.py │ │ ├── insights_integration.py │ │ └── predictive_models.py │ ├── doctypes/ │ │ ├── tems_transaction/ │ │ ├── tems_asset_profitability/ │ │ ├── tems_trip_economics/ │ │ └── tems_profitability_dashboard/ │ └── reports/ │ ├── asset_profitability_report/ │ ├── trip_profitability_analysis/ │ └── consolidated_profitability/ ├── setup.py └── requirements.txt
6.2 Database Schema Enhancements
6.2.1 Profitability Data Tables
-- Asset Profitability Tracking Table CREATE TABLE `tabTEMS Asset Profitability` ( `name` VARCHAR(140) NOT NULL, `asset_id` VARCHAR(140) NOT NULL, `calculation_date` DATE NOT NULL, `total_revenue` DECIMAL(18,2) DEFAULT 0, `direct_costs` DECIMAL(18,2) DEFAULT 0, `allocated_overhead` DECIMAL(18,2) DEFAULT 0, `depreciation` DECIMAL(18,2) DEFAULT 0, `net_profit` DECIMAL(18,2) DEFAULT 0, `roi_percentage` DECIMAL(8,4) DEFAULT 0, `utilization_rate` DECIMAL(8,4) DEFAULT 0, `profit_per_km` DECIMAL(10,4) DEFAULT 0, `profit_per_hour` DECIMAL(10,4) DEFAULT 0, `ytd_profit` DECIMAL(18,2) DEFAULT 0, `ytd_roi` DECIMAL(8,4) DEFAULT 0, PRIMARY KEY (`name`), INDEX `idx_asset_date` (`asset_id`, `calculation_date`) ); -- Trip Economics Tracking Table CREATE TABLE `tabTEMS Trip Economics` ( `name` VARCHAR(140) NOT NULL, `trip_id` VARCHAR(140) NOT NULL, `route_id` VARCHAR(140), `customer_id` VARCHAR(140), `asset_id` VARCHAR(140), `business_unit` VARCHAR(140), `trip_date` DATE NOT NULL, `total_distance` DECIMAL(10,2) DEFAULT 0, `total_duration` DECIMAL(8,2) DEFAULT 0, `fuel_cost` DECIMAL(12,2) DEFAULT 0, `driver_cost` DECIMAL(12,2) DEFAULT 0, `maintenance_allocation` DECIMAL(12,2) DEFAULT 0, `overhead_allocation` DECIMAL(12,2) DEFAULT 0, `total_cost` DECIMAL(15,2) DEFAULT 0, `base_revenue` DECIMAL(15,2) DEFAULT 0, `surcharge_revenue` DECIMAL(12,2) DEFAULT 0, `accessorial_revenue` DECIMAL(12,2) DEFAULT 0, `total_revenue` DECIMAL(15,2) DEFAULT 0, `gross_profit` DECIMAL(15,2) DEFAULT 0, `profit_margin` DECIMAL(8,4) DEFAULT 0, `revenue_per_km` DECIMAL(10,4) DEFAULT 0, `cost_per_km` DECIMAL(10,4) DEFAULT 0, PRIMARY KEY (`name`), INDEX `idx_trip_date` (`trip_date`), INDEX `idx_route_date` (`route_id`, `trip_date`), INDEX `idx_customer_date` (`customer_id`, `trip_date`) );
6.3 Integration Specifications
6.3.1 External System Integrations
Telematics Systems: Real-time vehicle data for accurate cost allocation
Fuel Management Systems: Precise fuel consumption and cost tracking
Mobile Money Platforms: Payment processing and revenue recognition
Government Regulatory Systems: Compliance cost tracking and reporting
Weather Services: Route optimization and risk-adjusted profitability
Banking Systems: Cash flow management and financing cost allocation
7. Performance & Scalability Requirements
7.1 System Performance Specifications
Performance Metric	Target	Measurement Method	Optimization Strategy
Dashboard Load Time	< 3 seconds	User experience monitoring	Data pre-aggregation, caching
Real-time Calculation	< 500ms	Transaction processing time	Optimized algorithms, indexing
Report Generation	< 10 seconds	Report export time	Background processing, pagination
Data Synchronization	< 5 minutes	Offline-online sync time	Incremental sync, compression
Concurrent Users	500+ users	Load testing results	Horizontal scaling, load balancing
7.2 Data Architecture Scalability
# Data Archiving and Performance Optimization class TEMSDataArchival: def __init__(self): self.retention_policies = { 'real_time_data': 90, # days 'monthly_aggregates': 1825, # 5 years 'yearly_summaries': 3650, # 10 years } def archive_old_data(self): """Automated data archiving for performance optimization""" # Archive detailed transaction data archive_query = """ INSERT INTO `tabTEMS Transaction Archive` SELECT * FROM `tabTEMS Transaction` WHERE creation < DATE_SUB(NOW(), INTERVAL 90 DAY) """ # Create monthly aggregates before archiving self.create_monthly_aggregates() # Archive old detailed records frappe.db.sql(archive_query) # Delete archived records from main table delete_query = """ DELETE FROM `tabTEMS Transaction` WHERE creation < DATE_SUB(NOW(), INTERVAL 90 DAY) """ frappe.db.sql(delete_query) def create_monthly_aggregates(self): """Create monthly aggregate tables for historical analysis""" pass
8. Testing & Validation Framework
8.1 Profitability Calculation Validation
8.1.1 Test Scenarios
Asset Profitability Validation: Verify ROI calculations across different asset types and utilization patterns
Trip Profitability Accuracy: Validate cost allocation and revenue attribution for complex multi-stop trips
Customer Profitability Consistency: Ensure consistent margin calculations across different service types and payment terms
Data Triangulation Integrity: Verify that sum of individual profitabilities equals total business profitability
Real-time Update Accuracy: Confirm that profitability metrics update correctly with new transactions
8.1.2 Automated Testing Framework
# Automated Profitability Testing class TEMSProfitabilityTests(unittest.TestCase): def setUp(self): self.test_data = self.create_test_scenario() def test_asset_roi_calculation(self): """Test asset ROI calculation accuracy""" asset = self.test_data['assets'][0] expected_roi = self.calculate_expected_roi(asset) actual_roi = calculate_asset_roi(asset.name) self.assertAlmostEqual( expected_roi, actual_roi, places=4, msg="Asset ROI calculation mismatch" ) def test_profitability_triangulation(self): """Test data triangulation integrity""" total_business_profit = get_total_business_profit() sum_of_parts = ( sum_asset_profits() + sum_unallocated_overhead() ) self.assertAlmostEqual( total_business_profit, sum_of_parts, places=2, msg="Profitability triangulation failed" ) def test_real_time_updates(self): """Test real-time profitability updates""" initial_profit = get_asset_profit('ASSET-001') # Create new transaction create_test_transaction('ASSET-001', amount=1000) updated_profit = get_asset_profit('ASSET-001') self.assertNotEqual( initial_profit, updated_profit, msg="Real-time update failed" )
9. Success Metrics & KPIs
9.1 Implementation Success Metrics
Success Metric	Target Value	Measurement Period	Success Criteria
Data Accuracy	99.5%	Continuous	Profitability calculations within 0.5% margin of error
User Adoption	85%	6 months post-deployment	85% of target users actively using profitability features
Decision Impact	25%	12 months	25% improvement in profitable decision-making
Cost Reduction	15%	12 months	15% reduction in unprofitable operations
Revenue Optimization	20%	12 months	20% improvement in revenue per asset utilization
9.2 Business Impact Measurement
Expected Business Outcomes:
Enhanced Profitability Visibility: Complete transparency into profit drivers and detractors across all business dimensions
Optimized Resource Allocation: Data-driven decisions on asset deployment, route selection, and customer prioritization
Improved Pricing Strategies: Accurate cost understanding enabling competitive yet profitable pricing
Risk-Adjusted Decision Making: Comprehensive risk and profitability analysis for strategic decisions
Operational Excellence: Continuous improvement driven by detailed performance analytics
10. Conclusion & Next Steps
This enhanced PRD provides a comprehensive framework for implementing sophisticated profitability analysis and data triangulation capabilities within the TEMS platform using Frappe/ERPNext. The detailed specifications ensure that every aspect of the business can be analyzed for profitability, enabling data-driven decision making and continuous operational improvement.

The implementation roadmap prioritizes the core data architecture and profitability calculation engines, ensuring that accurate and real-time profitability analysis is available across all business dimensions from day one of deployment.

Implementation Priority: Begin with core data model implementation and cost allocation engine, followed by dashboard development and advanced analytics integration. This approach ensures solid foundational capabilities before adding sophisticated visualization and predictive features.
Document Version: 2.0 - Enhanced Profitability Focus
Last Updated: 2024
Next Review: Quarterly updates based on implementation progress
