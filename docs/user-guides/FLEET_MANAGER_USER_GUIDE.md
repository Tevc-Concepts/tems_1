# Fleet Manager User Guide

**TEMS Platform - Fleet Manager Role**  
**Version:** 1.0  
**Date:** October 15, 2025

---

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Dashboard Overview](#dashboard-overview)
4. [Vehicle Management](#vehicle-management)
5. [Maintenance Management](#maintenance-management)
6. [Work Orders](#work-orders)
7. [Fuel Management](#fuel-management)
8. [Asset Tracking](#asset-tracking)
9. [Fleet Reports & Analytics](#fleet-reports--analytics)
10. [Common Tasks Quick Reference](#common-tasks-quick-reference)
11. [Troubleshooting](#troubleshooting)
12. [FAQ](#faq)

---

## Introduction

### About Your Role

As a **Fleet Manager** in the TEMS system, you are responsible for:

- **Vehicle Lifecycle Management:** From acquisition to disposal
- **Maintenance Planning:** Preventive and corrective maintenance scheduling
- **Cost Control:** Managing fleet operational costs
- **Performance Monitoring:** Tracking vehicle performance and utilization
- **Compliance:** Ensuring vehicles meet regulatory requirements
- **Asset Optimization:** Maximizing vehicle availability and lifespan
- **Vendor Management:** Coordinating with service providers

### What You Can Do

✅ View fleet dashboard with vehicle status and metrics  
✅ Manage vehicle records and documentation  
✅ Schedule and track maintenance activities  
✅ Create and manage work orders  
✅ Monitor fuel consumption and costs  
✅ Track vehicle performance and utilization  
✅ Generate fleet reports and analytics  
✅ Manage service providers and vendors  

---

## Getting Started

### Accessing the Fleet PWA

**URL:** `https://tems.yourdomain.com/fleet`

**Your Credentials:**
- **Email:** fleet.manager@yourdomain.com (or as provided)
- **Password:** (Provided by system administrator)

### Navigation Overview

**Main Navigation:**
- **Dashboard** - Fleet metrics and KPIs
- **Vehicles** - Vehicle inventory and details
- **Maintenance** - Maintenance schedule and history
- **Work Orders** - Service requests and repairs
- **Fuel** - Fuel consumption and costs
- **Assets** - Fleet asset management
- **Reports** - Fleet analytics and exports

---

## Dashboard Overview

### Key Fleet Indicators

**1. Total Fleet Size**
- Total number of vehicles
- Breakdown by type (Bus, Truck, Van, etc.)
- Click to view inventory

**2. Vehicle Availability**
- Vehicles currently available for operation
- Percentage of fleet operational
- Click to see available vehicles

**3. In Maintenance**
- Vehicles currently under maintenance
- Expected return to service dates
- Click for maintenance details

**4. Overdue Maintenance**
- Vehicles past scheduled maintenance date
- Prioritized by days overdue
- ⚠️ Immediate attention required

**5. Fuel Costs (This Month)**
- Total fuel expenditure
- Cost per kilometer
- Comparison to previous month
- Trend graph

**6. Fleet Utilization**
- Average utilization percentage
- Idle vehicles highlighted
- Click for utilization report

**7. Maintenance Costs (This Month)**
- Total maintenance expenditure
- By vehicle or by type
- Cost trends

### Quick Actions

- 🚗 Add New Vehicle
- 🔧 Schedule Maintenance
- 📋 Create Work Order
- ⛽ Record Fuel Entry
- 📊 Generate Fleet Report
- 🔍 Search Vehicle

### Alerts & Notifications

- 🚨 Vehicles overdue for maintenance
- ⚠️ Vehicles approaching maintenance due date
- ℹ️ Work orders pending approval
- ⛽ Unusual fuel consumption detected
- 📄 Documents expiring within 30 days

---

## Vehicle Management

### Vehicle Inventory

**Viewing All Vehicles:**
1. Navigate to "Vehicles"
2. See list of all fleet vehicles
3. Columns show:
   - Registration number
   - Make/Model/Year
   - Type
   - Status
   - Location
   - Next maintenance due
   - Insurance expiry

**Filters:**
- Status (All, Available, In Use, Maintenance, Out of Service)
- Type (Bus, Truck, Van, Car, etc.)
- Location
- Age
- Mileage range
- Maintenance status

**Sorting:**
- Registration number
- Acquisition date
- Mileage
- Next maintenance due
- Insurance expiry

### Vehicle Details

**Click any vehicle** to view complete profile:

**Overview Tab:**
- Registration details
- Make, model, year
- VIN (Vehicle Identification Number)
- Engine number
- Color
- Capacity (passengers/cargo weight)
- Acquisition date
- Purchase price
- Current book value
- Current location
- Assigned driver (if any)
- Status

**Specifications Tab:**
- Engine type and size
- Fuel type
- Transmission
- Dimensions (length, width, height)
- Weight (tare, gross)
- Tire specifications
- Features and accessories

**Documents Tab:**
- Registration certificate
  - Document number
  - Issue date
  - Expiry date
  - Status (Valid/Expired/Expiring Soon)
  - Download/View
- Insurance certificate
  - Policy number
  - Provider
  - Coverage type
  - Premium amount
  - Expiry date
  - Download/View
- Roadworthiness certificate
  - Certificate number
  - Test date
  - Expiry date
  - Download/View
- Permits and licenses
  - Permit type
  - Authority
  - Expiry date
  - Download/View

**Maintenance Tab:**
- Maintenance schedule
- Maintenance history
- Service records
- Repairs completed
- Parts replaced
- Costs incurred
- Timeline view

**Performance Tab:**
- Total kilometers driven
- Average kilometers per day
- Fuel consumption
  - Liters consumed
  - Km per liter
  - Cost per km
- Utilization rate
  - Percentage of time in use
  - Idle days
- Breakdown history
- Downtime analysis

**Costs Tab:**
- Total cost of ownership
- Breakdown by category:
  - Purchase/depreciation
  - Fuel
  - Maintenance
  - Insurance
  - Registration
  - Other
- Monthly cost trend
- Cost per kilometer

**History Tab:**
- Journey history
- Assignment history
- Incident reports
- Inspection reports
- Modifications/upgrades
- Timeline of all activities

### Adding a New Vehicle

**Steps:**
1. Navigate to "Vehicles" → "Add New Vehicle"
2. Fill "Basic Information":
   - Registration number (required)
   - VIN (required)
   - Make (required)
   - Model (required)
   - Year (required)
   - Color
   - Type (required)
   - Subtype
3. Fill "Acquisition Details":
   - Acquisition date
   - Purchase price
   - Vendor/dealer
   - Condition (New/Used)
   - Initial mileage
4. Fill "Specifications":
   - Engine details
   - Fuel type
   - Transmission
   - Capacity
   - Dimensions
   - Weight
5. Upload "Documents":
   - Registration certificate
   - Insurance
   - Roadworthiness (if applicable)
   - Purchase invoice
6. Set "Maintenance Schedule":
   - First service due
   - Service interval (km or months)
   - Service type
7. Assign "Initial Location"
8. Review and Submit

**Result:** Vehicle added to fleet inventory, ID generated, accessible to all teams

### Updating Vehicle Information

**To Update:**
1. Open vehicle details
2. Click "Edit" button
3. Modify fields as needed
4. Save changes
5. System logs modification history

**Document Updates:**
1. Open vehicle → "Documents" tab
2. Click document to update
3. Upload new document
4. Update expiry date
5. Save
6. Old document archived, new document active

### Decommissioning a Vehicle

**When to Decommission:**
- End of useful life
- Excessive repair costs
- Safety concerns
- Fleet downsizing

**Process:**
1. Open vehicle details
2. Click "Decommission"
3. Fill decommission form:
   - Reason
   - Final mileage
   - Disposal method (Sale, Scrap, Donation)
   - Disposal date
   - Amount received (if sold)
4. Upload final documents:
   - Transfer of ownership (if sold)
   - Scrapping certificate (if scrapped)
5. Submit
6. Vehicle moved to "Decommissioned" status
7. Historical records retained

---

## Maintenance Management

### Types of Maintenance

**1. Preventive Maintenance**
- Scheduled based on time or mileage
- Regular services to prevent breakdowns
- Examples:
  - Oil change every 5,000 km
  - Tire rotation every 10,000 km
  - Major service every 40,000 km

**2. Corrective Maintenance**
- Repairs due to breakdowns or failures
- Unscheduled
- Examples:
  - Engine repairs
  - Transmission repairs
  - Electrical system repairs

**3. Predictive Maintenance**
- Based on vehicle condition monitoring
- Prevents anticipated failures
- Examples:
  - Replace worn brake pads
  - Replace aging battery
  - Replace leaking seals

**4. Condition-Based Maintenance**
- Triggered by inspection findings
- Examples:
  - Replace cracked windshield
  - Repair body damage
  - Fix identified leaks

### Maintenance Schedule

**Viewing Schedule:**
1. Navigate to "Maintenance" → "Schedule"
2. View options:
   - Calendar view (by month)
   - List view (all upcoming)
   - Vehicle view (by vehicle)
3. Color coding:
   - 🟢 Green: Completed
   - 🟡 Yellow: Due soon (within 7 days)
   - 🔴 Red: Overdue
   - ⚪ Gray: Scheduled (future)

**Filtering:**
- By vehicle
- By maintenance type
- By date range
- By status

**Scheduling Maintenance:**
1. Click "Schedule Maintenance"
2. Select vehicle
3. Select maintenance type:
   - Oil change
   - Tire service
   - Brake service
   - Major service
   - Inspection
   - Custom (specify)
4. Set due date:
   - Specific date
   - OR mileage-based (e.g., at 50,000 km)
5. Select service provider:
   - Internal workshop
   - External vendor (select from list)
6. Estimated cost
7. Estimated duration (days)
8. Notes
9. Submit

**Auto-Scheduling:**
- System auto-creates recurring maintenance based on:
  - Vehicle manufacturer recommendations
  - Regulatory requirements
  - Custom intervals set per vehicle
- Notifications sent 30 days before due date
- Reminders at 7 days before

### Conducting Maintenance

**When Maintenance is Due:**
1. System notifies Fleet Manager
2. Open maintenance record
3. Click "Start Maintenance"
4. Vehicle status changed to "In Maintenance"
5. Operations team notified (vehicle unavailable)

**During Maintenance:**
1. Create work order (see Work Orders section)
2. Assign to technician
3. Track progress
4. Update status
5. Record parts used
6. Record labor hours
7. Record costs

**Completing Maintenance:**
1. Open maintenance record
2. Click "Complete Maintenance"
3. Fill completion details:
   - Completion date
   - Final mileage
   - Work performed
   - Parts replaced
   - Total cost (auto-calculated from work order)
   - Next service due (auto-calculated)
4. Upload documentation:
   - Service report
   - Invoices
   - Warranty documents (if applicable)
5. Inspection passed?
   - Yes: Vehicle returned to service
   - No: Additional work needed
6. Submit
7. Vehicle status changed to "Available"
8. Operations team notified

### Maintenance History

**Viewing History:**
1. Open vehicle details
2. Click "Maintenance" tab
3. See all past maintenance:
   - Date
   - Type
   - Mileage at service
   - Cost
   - Duration
   - Provider
   - Status
4. Click any record for full details
5. Export history to Excel/PDF

**Analyzing Patterns:**
- Frequent repairs indicate problem areas
- Cost trends show if vehicle becoming expensive
- Downtime analysis shows reliability
- Use for decision-making (repair vs. replace)

---

## Work Orders

### What is a Work Order?

A work order is a detailed instruction for maintenance or repair work:
- Created for each maintenance task
- Tracks work performed
- Records parts and labor
- Calculates costs
- Links to vehicle maintenance history

### Creating a Work Order

**Starting New Work Order:**
1. Navigate to "Work Orders" → "New Work Order"
2. OR from maintenance record, click "Create Work Order"

**Work Order Details:**

**1. Basic Information**
- WO number (auto-generated)
- Vehicle (select from dropdown)
- Type:
  - Preventive Maintenance
  - Corrective Maintenance
  - Inspection
  - Repair
  - Other
- Priority:
  - 🔴 Urgent (vehicle breakdown, safety issue)
  - 🟡 High (affects operations)
  - 🟢 Normal (routine maintenance)
  - ⚪ Low (non-critical)
- Requested date
- Target completion date

**2. Work Description**
- Problem description
- Work to be performed
- Special instructions
- Safety precautions

**3. Assignment**
- Assign to:
  - Internal technician
  - External service provider
- Workshop/location
- Estimated hours

**4. Parts Required**
- Add parts needed:
  - Part name/number
  - Quantity
  - Unit cost
  - Supplier
  - In stock? (system checks inventory)
- Total parts cost (auto-calculated)

**5. Labor**
- Estimated labor hours
- Labor rate
- Total labor cost (auto-calculated)

**6. Additional Costs**
- Transportation
- External services
- Other expenses

**7. Total Estimated Cost**
- Auto-calculated from parts + labor + additional

**8. Approvals**
- If cost > threshold, requires approval
- System routes to appropriate approver

**9. Submit Work Order**
- Review all details
- Submit
- WO status: "Pending" or "Approved"

### Work Order Workflow

**Statuses:**
1. **Draft** - Being created
2. **Pending Approval** - Awaiting cost approval
3. **Approved** - Ready to execute
4. **In Progress** - Work underway
5. **On Hold** - Waiting for parts/info
6. **Completed** - Work finished
7. **Closed** - Reviewed and closed
8. **Cancelled** - Work order cancelled

**Updating Work Order:**
1. Open work order
2. Click "Update Status"
3. Select new status
4. Add notes explaining status change
5. If completing:
   - Record actual parts used
   - Record actual labor hours
   - Upload invoices/receipts
   - Final inspection passed?
6. Save

**Closing Work Order:**
1. Work must be in "Completed" status
2. Review all details accurate
3. Verify costs recorded
4. Attach final documentation
5. Click "Close Work Order"
6. WO closed, costs added to vehicle record
7. Maintenance record updated

### Managing Open Work Orders

**Viewing Open WOs:**
1. Navigate to "Work Orders" → "Open"
2. See all work orders in progress
3. Filter by:
   - Priority
   - Status
   - Vehicle
   - Date
   - Assigned to

**Prioritizing Work:**
- Sort by priority
- Focus on urgent items first
- Coordinate with Operations for vehicle availability
- Track completion timeline

**Escalating Delays:**
- If work order delayed beyond target date
- Add notes explaining delay
- Update estimated completion
- Notify Operations if impacts schedule
- Consider alternative solutions

---

## Fuel Management

### Recording Fuel Entries

**When Vehicle Refuels:**
1. Navigate to "Fuel" → "New Entry"
2. Fill details:
   - Vehicle (select)
   - Date and time
   - Odometer reading (required)
   - Liters filled
   - Cost per liter
   - Total cost (auto-calculated)
   - Fuel station
   - Payment method
   - Invoice/receipt number
3. Upload receipt photo (optional)
4. Submit

**Auto-Calculations:**
- System calculates:
  - Kilometers since last fill
  - Fuel consumption (km/liter)
  - Cost per kilometer
  - Variance from vehicle average
  - Alerts if unusual consumption

### Monitoring Fuel Consumption

**Vehicle Fuel Efficiency:**
1. Open vehicle details
2. Click "Performance" tab
3. View fuel metrics:
   - Average km/liter
   - Fuel cost per km
   - Monthly fuel consumption
   - Trend graph
   - Comparison to similar vehicles

**Fleet Fuel Overview:**
1. Navigate to "Fuel" → "Overview"
2. See fleet-wide metrics:
   - Total fuel consumed (this month)
   - Total fuel cost (this month)
   - Average km/liter (fleet)
   - Top 5 most efficient vehicles
   - Top 5 least efficient vehicles
   - Fuel cost trends

**Identifying Issues:**
- System alerts if:
  - Fuel efficiency drops >10% from average
  - Unusually high fuel consumption
  - Frequent refueling (possible leak)
- Investigate and take corrective action:
  - Check for leaks
  - Review driving behavior
  - Schedule maintenance
  - Check tire pressure

### Fuel Cost Control

**Analyzing Costs:**
1. Navigate to "Fuel" → "Reports"
2. Generate fuel cost report:
   - By vehicle
   - By month
   - By fuel type
3. Identify cost drivers:
   - Which vehicles are most expensive?
   - Fuel price trends
   - Consumption patterns

**Optimization Strategies:**
- Use more fuel-efficient vehicles for long routes
- Maintain proper tire pressure (improves efficiency)
- Regular maintenance (optimizes engine performance)
- Driver training on fuel-efficient driving
- Monitor for fuel theft or misuse

---

## Asset Tracking

### Vehicle Location Tracking

**Real-Time Location:**
1. Navigate to "Assets" → "Live Tracking"
2. See map with all vehicles
3. Color coding:
   - 🟢 Moving
   - 🔵 Parked
   - 🟡 Idle (engine on, not moving)
   - 🔴 Offline (no GPS signal)
4. Click vehicle marker for details:
   - Current location address
   - Speed
   - Direction
   - Engine status
   - Driver
   - Journey (if on journey)

**Location History:**
1. Click vehicle
2. Select date range
3. View route history on map
4. Playback journey
5. Export location log

### Asset Utilization

**Utilization Metrics:**
1. Navigate to "Assets" → "Utilization"
2. See metrics per vehicle:
   - Days in use vs. available days
   - Total hours operated
   - Idle hours
   - Maintenance downtime
   - Utilization percentage
3. Target: >75% utilization

**Optimizing Utilization:**
- Identify underutilized vehicles:
  - <50% utilization → Investigate why
  - Consider redeploying to busier routes
  - Consider selling/leasing if persistent
- Identify overutilized vehicles:
  - >90% utilization → Risk of excessive wear
  - Consider adding vehicles to fleet
  - Plan maintenance windows

### Vehicle Assignments

**Current Assignments:**
1. Navigate to "Assets" → "Assignments"
2. See which vehicles are assigned to:
   - Specific drivers
   - Specific routes
   - Specific departments
3. Assignment types:
   - Permanent (vehicle always with same driver)
   - Temporary (for specific journey/period)
   - Pool (shared among multiple drivers)

**Managing Assignments:**
1. Click vehicle
2. View current assignment
3. Change assignment:
   - Unassign from current
   - Assign to new driver/route
   - Set assignment type
   - Set effective date
4. Save
5. Driver notified of new assignment

---

## Fleet Reports & Analytics

### Available Reports

**1. Fleet Inventory Report**
- Complete list of all vehicles
- Details per vehicle
- Filter and export options

**2. Maintenance Summary Report**
- Maintenance performed
- Costs by vehicle/type
- Overdue maintenance items
- Scheduled upcoming maintenance

**3. Vehicle Availability Report**
- Available vs. unavailable vehicles
- Reasons for unavailability
- Impact on operations

**4. Cost Analysis Report**
- Total cost of ownership by vehicle
- Cost breakdown by category
- Cost per kilometer
- Budget vs. actual
- Cost trends

**5. Fuel Consumption Report**
- Fuel used by vehicle/fleet
- Fuel efficiency metrics
- Fuel costs
- Comparison periods

**6. Utilization Report**
- Utilization by vehicle
- Idle time analysis
- Revenue per vehicle
- ROI calculations

**7. Performance Dashboard**
- KPIs for fleet performance
- Benchmarks and targets
- Trend analysis
- Predictive insights

### Generating Reports

**Steps:**
1. Navigate to "Reports"
2. Select report type
3. Set parameters:
   - Date range
   - Vehicles (all or specific)
   - Filters
4. Preview report
5. Download format:
   - PDF (for presentation)
   - Excel (for analysis)
   - CSV (for data export)
6. Schedule recurring reports (optional)

### Dashboard Analytics

**Key Metrics Tracked:**
- Fleet size trend
- Average vehicle age
- Maintenance cost per km
- Fuel cost per km
- Utilization rate
- Availability percentage
- Breakdown frequency
- Cost per vehicle

**Trends & Insights:**
- Month-over-month comparisons
- Year-over-year growth
- Seasonal patterns
- Predictive maintenance needs
- Replacement recommendations

---

## Common Tasks Quick Reference

### Add New Vehicle
```
1. Vehicles → "Add New Vehicle"
2. Fill: Registration, Make, Model, Year, Type
3. Upload: Documents
4. Set: Maintenance schedule
5. Submit
```

### Schedule Maintenance
```
1. Maintenance → "Schedule Maintenance"
2. Select: Vehicle and Type
3. Set: Due date or mileage
4. Assign: Service provider
5. Submit
```

### Create Work Order
```
1. Work Orders → "New Work Order"
2. Select: Vehicle, Type, Priority
3. Describe: Work needed
4. Add: Parts and labor
5. Submit for approval
```

### Record Fuel Entry
```
1. Fuel → "New Entry"
2. Select: Vehicle
3. Enter: Liters, Cost, Odometer
4. Upload: Receipt
5. Submit
```

### Check Vehicle Status
```
1. Dashboard → Vehicle Status section
2. OR Vehicles → Search vehicle
3. View current status and location
```

### Generate Fleet Report
```
1. Reports → Select report type
2. Set: Date range and filters
3. Generate → Download
```

---

## Troubleshooting

**Q: Vehicle not appearing in available list**  
A: Check vehicle status - may be In Maintenance, Out of Service, or already assigned

**Q: Cannot schedule maintenance**  
A: Verify vehicle exists, date is future date, service provider is active

**Q: Work order won't submit**  
A: Check all required fields filled, parts availability confirmed, approval obtained if needed

**Q: Fuel consumption seems incorrect**  
A: Verify odometer readings entered correctly, check for missed fuel entries, review for data entry errors

**Q: Reports not generating**  
A: Check date range not too large, filters not too restrictive, try different output format

---

## FAQ

**Q: How often should preventive maintenance be scheduled?**  
A: Follow manufacturer recommendations or regulatory requirements, typically every 5,000-10,000 km for minor service, 40,000-50,000 km for major service.

**Q: When should a vehicle be replaced?**  
A: When repair costs exceed 50% of vehicle value, or when reliability becomes issue affecting operations, or at end of depreciation life (typically 5-8 years).

**Q: How do I know if a vehicle is cost-effective?**  
A: Check cost per kilometer - if significantly higher than fleet average or exceeds revenue generated, may need attention.

**Q: Can I assign one vehicle to multiple drivers?**  
A: Yes, use "Pool" assignment type. Vehicle available to all assigned drivers on first-come basis.

**Q: What if maintenance costs exceed estimate in work order?**  
A: Additional approval may be required. Update work order with revised costs and reason, submit for re-approval.

**Q: How do I track warranty claims?**  
A: Record warranty info in vehicle documents, note warranty repairs in work orders, track warranty expiry dates.

---

**Document Version:** 1.0  
**Last Updated:** October 15, 2025  
**Maintained By:** TEMS Training Team
