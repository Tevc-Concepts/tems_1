# Operations Manager User Guide

**TEMS Platform - Operations Manager Role**  
**Version:** 1.0  
**Date:** October 15, 2025

---

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Dashboard Overview](#dashboard-overview)
4. [Core Tasks & Workflows](#core-tasks--workflows)
5. [Vehicle Management](#vehicle-management)
6. [Driver Management](#driver-management)
7. [Route Management](#route-management)
8. [Journey Planning](#journey-planning)
9. [Inspections & Checklists](#inspections--checklists)
10. [Reports & Analytics](#reports--analytics)
11. [Common Tasks Quick Reference](#common-tasks-quick-reference)
12. [Troubleshooting](#troubleshooting)
13. [FAQ](#faq)

---

## Introduction

### About Your Role

As an **Operations Manager** in the TEMS system, you are responsible for:

- **Planning & Scheduling:** Creating and managing journey plans for vehicles and drivers
- **Resource Management:** Overseeing vehicle and driver assignments
- **Route Optimization:** Planning efficient routes for transport operations
- **Compliance Monitoring:** Ensuring vehicles and drivers meet inspection requirements
- **Performance Tracking:** Monitoring operational metrics and KPIs
- **Coordination:** Working with Safety, Fleet, and Driver teams

### What You Can Do

✅ View operational dashboard with real-time metrics  
✅ Manage vehicles and driver assignments  
✅ Create and modify journey plans  
✅ Plan and optimize routes  
✅ Conduct pre-trip inspections  
✅ Review operational checklists  
✅ Generate operational reports  
✅ Monitor compliance status  

### What This Guide Covers

This guide will help you:
- Access and navigate the Operations PWA
- Perform your daily operational tasks
- Create journey plans and assign resources
- Conduct inspections and complete checklists
- Generate reports and monitor performance

---

## Getting Started

### Accessing the Operations PWA

**Step 1: Open Your Browser**
- Use Chrome, Edge, Firefox, or Safari
- Navigate to: `https://tems.yourdomain.com/assets/tems/frontend/operations-pwa/dist/index.html`

**Step 2: Login**
1. Enter your email address
2. Enter your password
3. Click "Login"

**Your Credentials:**
- **Email:** operations.manager@yourdomain.com (or as provided)
- **Password:** (Provided by system administrator)

**Step 3: First Login**
- You may be prompted to change your password
- Choose a strong password (minimum 8 characters, mix of letters, numbers, symbols)
- Enable Two-Factor Authentication if prompted (recommended)

### Navigation Overview

**Main Navigation:**
- **Dashboard** - Your home screen with key metrics
- **Vehicles** - Vehicle list and assignments
- **Drivers** - Driver roster and schedules
- **Routes** - Route library and planning
- **Journey Plans** - Active and planned journeys
- **Inspections** - Vehicle inspection records
- **Checklists** - Operational checklists
- **Reports** - Analytics and exports
- **Profile** - Your account settings

**Top Bar:**
- **Notifications** 🔔 - Alerts and updates
- **Search** 🔍 - Quick search across records
- **Help** ❓ - Access this guide
- **Profile Menu** 👤 - Settings and logout

---

## Dashboard Overview

### Understanding Your Dashboard

Your Operations Dashboard provides a real-time overview of key operational metrics:

#### Key Performance Indicators (KPIs)

**1. Active Journeys**
- Number of journeys currently in progress
- Click to see detailed list
- 🟢 Green: On schedule | 🟡 Yellow: Delayed | 🔴 Red: Critical

**2. Available Vehicles**
- Vehicles ready for assignment
- Click to view available vehicle list
- Filters: By type, location, capacity

**3. Active Drivers**
- Drivers currently on duty
- Click to see driver schedules
- Status: Available, On Journey, Off Duty

**4. Pending Inspections**
- Vehicles requiring inspection
- Click to view inspection queue
- ⚠️ Overdue items highlighted in red

**5. Today's Routes**
- Routes scheduled for today
- Click for route details
- Shows completion status

**6. Compliance Status**
- Overall compliance percentage
- Areas: Vehicle docs, driver licenses, inspections
- Click for detailed compliance report

#### Quick Actions Panel

**Common Tasks:**
- ➕ Create Journey Plan
- 🚗 Assign Vehicle
- 👤 Assign Driver
- 📋 Start Inspection
- 📍 View Routes
- 📊 Generate Report

#### Recent Activity

Shows your last 10 actions:
- Journey plans created/modified
- Inspections completed
- Reports generated
- Assignments made

#### Alerts & Notifications

Real-time alerts for:
- 🚨 Overdue inspections
- ⚠️ Journey delays
- ℹ️ Expiring driver licenses
- ✅ Completed journeys

---

## Core Tasks & Workflows

### Daily Morning Routine

**1. Review Dashboard (5 minutes)**
```
✓ Check active journeys count
✓ Verify available vehicles
✓ Review driver schedules
✓ Note any alerts
```

**2. Check Today's Plan (10 minutes)**
```
✓ Open "Journey Plans" → "Today"
✓ Verify all journeys have drivers assigned
✓ Confirm vehicles are assigned
✓ Check for any pending inspections
```

**3. Address Alerts (as needed)**
```
✓ Click notification bell
✓ Prioritize by urgency
✓ Take action on critical items
✓ Delegate to appropriate team
```

### Creating a Journey Plan

**When to create:** Before any scheduled transport operation

**Steps:**

**1. Start New Journey Plan**
- Click "➕ Create Journey Plan" on dashboard
- OR Navigate to "Journey Plans" → "New Journey Plan"

**2. Fill Basic Information**
- **Journey Name:** Descriptive name (e.g., "Lagos-Abuja Express - Morning")
- **Route:** Select from dropdown (or create new route)
- **Scheduled Date:** Select date
- **Departure Time:** Set time
- **Estimated Duration:** System calculates based on route

**3. Assign Vehicle**
- Click "Assign Vehicle"
- Filter available vehicles by:
  - Type (Bus, Truck, Van)
  - Capacity required
  - Location (nearest to departure point)
- Select vehicle from list
- System checks:
  - ✓ Valid insurance
  - ✓ Recent inspection
  - ✓ Maintenance up-to-date
- Click "Confirm Assignment"

**4. Assign Driver**
- Click "Assign Driver"
- Filter available drivers by:
  - License type
  - Route experience
  - Availability
- Select primary driver
- (Optional) Assign backup driver for long journeys
- System checks:
  - ✓ Valid license
  - ✓ Not exceeded duty hours
  - ✓ Medical clearance current
- Click "Confirm Assignment"

**5. Add Journey Details**
- **Passengers/Cargo:** Enter count or weight
- **Stops:** Add intermediate stops if any
- **Special Instructions:** Any special requirements
- **Emergency Contact:** Verify contact info
- **Risk Assessment:** System shows risk score based on:
  - Weather conditions
  - Route hazards
  - Vehicle condition
  - Driver experience

**6. Review & Submit**
- Review all details
- Check validation warnings
- Click "Save Draft" (to continue later)
- OR Click "Submit Journey Plan" (to activate)

**7. Pre-Trip Inspection**
- System prompts for pre-trip inspection
- Assign inspector OR conduct yourself
- Journey cannot start until inspection complete

**Result:** Journey Plan created and visible to Driver, Safety, and Fleet teams

---

## Vehicle Management

### Viewing Vehicle List

**Navigate:** Click "Vehicles" in main menu

**Vehicle List Shows:**
- Registration number
- Vehicle type
- Current status (Available, In Use, Maintenance, Out of Service)
- Current location
- Next scheduled maintenance
- Insurance expiry

**Filters:**
- Status (All, Available, In Use, etc.)
- Type (Bus, Truck, Van, etc.)
- Location
- Capacity range

**Sort by:**
- Registration number
- Status
- Next maintenance date
- Insurance expiry

### Viewing Vehicle Details

**Click any vehicle** to see full details:

**Overview Tab:**
- Registration details
- Make, model, year
- Capacity (passengers/cargo)
- Current odometer reading
- Fuel type
- Assigned driver (if any)

**Documents Tab:**
- Insurance certificate (status, expiry)
- Registration documents
- Roadworthiness certificate
- Permit documents
- Click any document to view/download

**History Tab:**
- Journey history
- Maintenance records
- Inspection reports
- Incident reports (if any)

**Performance Tab:**
- Total kilometers
- Fuel efficiency
- Utilization rate
- Downtime percentage

### Assigning Vehicles to Journeys

**Two methods:**

**Method 1: From Journey Plan**
1. Open journey plan
2. Click "Assign Vehicle"
3. Select from available list
4. Confirm

**Method 2: From Vehicle Page**
1. Open vehicle details
2. Click "Assign to Journey"
3. Select journey from list
4. Confirm

**System Validates:**
- Vehicle available for selected date/time
- No conflicting assignments
- Vehicle meets route requirements
- All documents current

### Checking Vehicle Availability

**Quick Check:**
1. Go to "Vehicles"
2. Filter by "Available"
3. Shows all vehicles ready for assignment

**Detailed Check:**
1. Open vehicle details
2. Click "Availability Calendar"
3. See schedule for next 30 days
4. Green = Available
5. Yellow = Scheduled
6. Red = Unavailable (maintenance/repairs)

---

## Driver Management

### Viewing Driver Roster

**Navigate:** Click "Drivers" in main menu

**Driver List Shows:**
- Name and photo
- Employee ID
- License type
- Current status (Available, On Journey, Off Duty, On Leave)
- Current location (if on journey)
- Next scheduled duty

**Filters:**
- Status
- License type
- Experience level
- Location

### Viewing Driver Profile

**Click any driver** to see full profile:

**Overview Tab:**
- Personal information
- Contact details
- Employment details
- License information
- Medical clearance status

**Qualifications Tab:**
- License type and number
- License expiry date
- Certifications
- Training completed
- Route authorizations

**Schedule Tab:**
- Current week schedule
- Today's assignments
- Upcoming journeys
- Time off requests

**Performance Tab:**
- Total journeys completed
- On-time percentage
- Incidents (if any)
- Customer ratings
- Fuel efficiency

### Assigning Drivers to Journeys

**From Journey Plan:**
1. Open journey plan
2. Click "Assign Driver"
3. System shows eligible drivers:
   - Has required license type
   - Available for selected date/time
   - Not exceeded duty hours
   - Medical clearance current
4. Select driver
5. (Optional) Add backup driver
6. Confirm

**System Checks:**
- ✓ No schedule conflicts
- ✓ Adequate rest between journeys
- ✓ Within maximum duty hours (per regulations)
- ✓ Qualified for route
- ✓ Medical clearance valid

### Checking Driver Availability

**Quick View:**
- Dashboard shows "Active Drivers" count
- Click to see who's available now

**Detailed View:**
1. Go to "Drivers"
2. Filter by "Available"
3. Click driver → "Schedule Tab"
4. See availability calendar

---

## Route Management

### Understanding Routes

**What is a Route?**
- Predefined path from origin to destination
- Includes waypoints, distance, estimated time
- Has risk assessment and special requirements
- Used as template for journey plans

**Route Types:**
- **Express Routes:** Direct, minimal stops
- **Local Routes:** Multiple stops
- **Special Routes:** Specific requirements (hazmat, oversized, etc.)

### Viewing Route Library

**Navigate:** Click "Routes" in main menu

**Route List Shows:**
- Route name
- Origin → Destination
- Distance (km)
- Estimated duration
- Risk level (Low, Medium, High)
- Frequency (how often used)

**Filters:**
- By origin city
- By destination city
- By risk level
- By route type

### Viewing Route Details

**Click any route** to see:

**Map View:**
- Visual route on map
- Waypoints marked
- Hazard zones highlighted
- Rest stops indicated

**Details Tab:**
- Distance breakdown
- Estimated time by segment
- Road types (highway, rural, urban)
- Toll points
- Border crossings (if any)

**Requirements Tab:**
- Vehicle types suitable
- License requirements
- Permits needed
- Special equipment

**Risk Assessment:**
- Weather considerations
- Road conditions
- Security concerns
- Historical incident data

### Using Routes in Journey Plans

**When creating journey plan:**
1. Select route from dropdown
2. System auto-fills:
   - Distance
   - Estimated duration
   - Waypoints
   - Special requirements
3. Adjust if needed
4. System suggests:
   - Suitable vehicles
   - Qualified drivers

---

## Journey Planning

### Journey Plan Lifecycle

**Stages:**
1. **Draft** - Being created, not yet submitted
2. **Planned** - Approved, scheduled for future
3. **Ready** - All assignments complete, pre-trip inspection done
4. **In Progress** - Journey underway
5. **Completed** - Journey finished successfully
6. **Cancelled** - Journey cancelled before start
7. **Incident** - Journey had issues, under review

### Managing Journey Plans

**View All Plans:**
- Navigate to "Journey Plans"
- Tabs: Today, This Week, All, Drafts, History

**Filter Plans:**
- By date range
- By status
- By route
- By vehicle
- By driver

**Search Plans:**
- By journey ID
- By destination
- By driver name
- By vehicle number

### Modifying a Journey Plan

**Before Journey Starts:**
1. Open journey plan
2. Click "Edit"
3. Modify details
4. If you change vehicle/driver:
   - System re-runs validation
   - May require new inspection
5. Save changes
6. System notifies affected parties

**While Journey In Progress:**
- Cannot edit core details
- Can add notes
- Can update status
- Can log incidents

**After Journey Complete:**
- Read-only
- Can add post-journey notes
- Can attach documentation

### Journey Plan Status Updates

**System Auto-Updates:**
- When driver starts journey (GPS signal)
- At each waypoint
- When journey completes

**Manual Updates:**
- Add notes or comments
- Report delays
- Log incidents
- Update estimated arrival

---

## Inspections & Checklists

### Pre-Trip Inspections

**Requirement:** Every vehicle must pass pre-trip inspection before journey

**Starting Inspection:**
1. Navigate to "Inspections" → "New Inspection"
2. Select vehicle
3. Select journey (if applicable)
4. System loads inspection checklist

**Inspection Categories:**

**1. Exterior (10 items)**
- Body condition (dents, scratches)
- Lights (headlights, taillights, indicators)
- Windows and mirrors
- Tires (condition, pressure, tread depth)
- License plates
- Fuel cap

**2. Interior (8 items)**
- Seats and seatbelts
- Dashboard instruments
- Steering and controls
- Emergency equipment (fire extinguisher, first aid)
- Cleanliness
- Interior lights

**3. Engine & Mechanics (12 items)**
- Engine oil level
- Coolant level
- Brake fluid
- Power steering fluid
- Battery condition
- Belts and hoses
- Brakes (test during short drive)
- Wipers and washer fluid

**4. Safety Equipment (6 items)**
- Fire extinguisher (present, valid, accessible)
- First aid kit (complete, not expired)
- Warning triangle
- Spare tire and jack
- Reflective vest
- Emergency contacts posted

**For Each Item:**
- ✅ Pass - Item is satisfactory
- ⚠️ Advisory - Item needs attention soon
- ❌ Fail - Item requires immediate repair

**Completing Inspection:**
1. Check all items
2. For any "Fail" items:
   - Add notes describing issue
   - Attach photos if possible
   - System notifies Fleet team
3. Overall result:
   - **Pass:** Journey can proceed
   - **Conditional Pass:** Journey can proceed, but repairs needed soon
   - **Fail:** Journey cannot proceed until repairs completed
4. Add inspector signature (digital)
5. Submit inspection

**After Submission:**
- Inspection linked to vehicle record
- If fail: Fleet team notified, vehicle marked "Out of Service"
- If pass: Journey plan status updated to "Ready"

### Operational Checklists

**Types of Checklists:**
- Pre-departure checklist (before journey starts)
- In-journey checklist (at waypoints)
- Post-journey checklist (after completion)

**Accessing Checklists:**
1. Navigate to "Checklists"
2. Filter by type
3. Select checklist

**Completing Checklist:**
1. Open checklist
2. Complete each item
3. Add notes if needed
4. Submit
5. Checklist attached to journey record

---

## Reports & Analytics

### Available Reports

**Operations Dashboard Reports:**
1. **Daily Operations Summary**
   - Journeys completed
   - On-time performance
   - Utilization rates

2. **Vehicle Utilization Report**
   - By vehicle
   - By vehicle type
   - Idle time analysis

3. **Driver Performance Report**
   - By driver
   - On-time percentage
   - Incidents

4. **Route Performance Report**
   - By route
   - Average time vs. estimated
   - Delays analysis

5. **Compliance Report**
   - Inspection completion rate
   - Document expiry status
   - Outstanding items

### Generating a Report

**Steps:**
1. Navigate to "Reports"
2. Select report type
3. Set parameters:
   - Date range
   - Filters (vehicle, driver, route, etc.)
   - Output format (PDF, Excel, CSV)
4. Click "Generate"
5. Report displays on screen
6. Download or print
7. Reports saved in "My Reports" for future reference

### Scheduling Recurring Reports

**For Regular Reports:**
1. Generate report once
2. Click "Schedule Report"
3. Set frequency:
   - Daily
   - Weekly (select day)
   - Monthly (select date)
4. Set recipients (email addresses)
5. Save schedule
6. Reports auto-generated and emailed

### Exporting Data

**Bulk Data Export:**
1. Navigate to section (e.g., "Journey Plans")
2. Apply filters
3. Click "Export"
4. Choose format (Excel, CSV)
5. File downloads
6. Use for external analysis

---

## Common Tasks Quick Reference

### Create Journey Plan (Quick)
```
1. Dashboard → "➕ Create Journey Plan"
2. Fill: Name, Route, Date, Time
3. Assign Vehicle → Select → Confirm
4. Assign Driver → Select → Confirm
5. Review → Submit
6. Conduct/Assign Pre-Trip Inspection
```

### Check Vehicle Availability
```
1. Vehicles → Filter "Available"
2. OR click vehicle → "Availability Calendar"
```

### Check Driver Schedule
```
1. Drivers → Click driver name
2. "Schedule Tab" → View calendar
```

### Conduct Pre-Trip Inspection
```
1. Inspections → "New Inspection"
2. Select vehicle
3. Complete checklist items
4. Add notes/photos for any issues
5. Submit
```

### Generate Daily Summary Report
```
1. Reports → "Daily Operations Summary"
2. Select date
3. Generate → Download
```

### Modify Journey Plan (Before Start)
```
1. Journey Plans → Find plan
2. Click "Edit"
3. Make changes
4. Save
5. Re-submit if needed
```

### View Journey Status (In Progress)
```
1. Dashboard → "Active Journeys" count
2. Click to see list
3. Click journey for live tracking
```

### Report Journey Delay
```
1. Journey Plans → Open journey
2. "Update Status" → "Delayed"
3. Add reason and new ETA
4. System notifies stakeholders
```

---

## Troubleshooting

### Login Issues

**Problem:** Cannot login  
**Solutions:**
- Verify username/email is correct
- Check password (case-sensitive)
- Try "Forgot Password" link
- Clear browser cache and cookies
- Try different browser
- Contact system admin if still unable

**Problem:** Password expired  
**Solutions:**
- Use "Forgot Password" to reset
- Contact system admin for temporary password

### Dashboard Not Loading

**Problem:** Dashboard blank or loading forever  
**Solutions:**
- Check internet connection
- Refresh page (F5 or Ctrl+R)
- Clear browser cache
- Try different browser
- Check if system maintenance is scheduled

### Cannot Create Journey Plan

**Problem:** "Submit" button disabled  
**Check:**
- All required fields filled?
- Vehicle assigned and valid?
- Driver assigned and qualified?
- No validation errors shown?
- Pre-trip inspection completed?

**Problem:** No vehicles available  
**Solutions:**
- Check filters (may be filtering out available vehicles)
- Check selected date/time (vehicles may be booked)
- View vehicle calendar for availability
- Contact Fleet team if all vehicles in maintenance

### Inspection Issues

**Problem:** Cannot submit inspection  
**Check:**
- All items checked?
- Notes added for failed items?
- Photos attached where required?
- Digital signature added?

**Problem:** Vehicle failed inspection but journey is urgent  
**Action:**
- Cannot override safety
- Contact Fleet team for emergency repair
- Assign different vehicle
- Reschedule journey if necessary

### Report Not Generating

**Problem:** Report generation fails  
**Solutions:**
- Check date range (too large may timeout)
- Try smaller date range
- Try different output format
- Clear browser cache
- Contact system admin if persists

---

## FAQ

**Q: How far in advance should I create journey plans?**  
A: Recommended 24-48 hours in advance to allow time for vehicle inspection, driver preparation, and any issues to be resolved.

**Q: Can I assign the same driver to multiple journeys in one day?**  
A: Yes, but system enforces duty hour regulations. Driver cannot exceed maximum duty hours per day as per transport regulations.

**Q: What if a vehicle breaks down during a journey?**  
A: Driver reports via Driver PWA → Operations receives alert → Coordinate with Fleet team for rescue/repair → Assign replacement vehicle if available → Update journey plan status.

**Q: Can I create a journey plan without a route?**  
A: Yes, but you must manually enter origin, destination, and estimated duration. Using predefined routes is recommended for accuracy and compliance.

**Q: How do I know if a driver is qualified for a specific route?**  
A: When assigning driver, system shows only qualified drivers based on license type and route requirements. If a driver is not in the list, they are not qualified.

**Q: What happens if I forget to conduct pre-trip inspection?**  
A: Journey cannot start. Driver will see "Inspection Required" in their app and cannot begin journey until inspection is complete and passed.

**Q: Can I cancel a journey after it has started?**  
A: You can mark it for cancellation, but you must coordinate with the driver. Use "Update Status" → "Cancel Journey" → Add reason → Driver will receive notification and must confirm.

**Q: How do I handle emergency situations?**  
A: Use emergency contact system in journey plan → Notify relevant teams (Safety, Fleet) → Follow emergency procedures → Document all actions → File incident report.

**Q: Can I see historical data for performance analysis?**  
A: Yes, navigate to Reports → Select report type → Set date range to historical period → Generate report with trends and analytics.

**Q: What if I make a mistake in a journey plan?**  
A: Before journey starts: Edit and save changes. After journey starts: Add notes explaining what happened, but cannot modify core details. After completion: Plans are locked, but you can add post-journey notes.

---

## Contact & Support

**For Technical Issues:**
- Email: support@yourdomain.com
- Phone: +234-XXX-XXX-XXXX
- Help Desk: Available 24/7

**For Training:**
- Email: training@yourdomain.com
- Schedule 1-on-1 session
- Group training available

**For Feedback:**
- Use "Feedback" button in app
- Email: feedback@yourdomain.com

---

**Document Version:** 1.0  
**Last Updated:** October 15, 2025  
**Next Review:** Post-UAT feedback  
**Maintained By:** TEMS Training Team
