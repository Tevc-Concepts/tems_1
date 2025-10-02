# TEMS Module Map

This map outlines dependencies and integration flows across TEMS modules on Frappe v15+. Each module should live under the `tems` app, extend ERPNext/HRMS where needed, and expose fixtures for roles/workspaces.

## Domains and Key Dependencies

- Governance
  - Depends on: Documents, Insights
  - Provides: Policy, Compliance Audit, SLA standards

- People (HRMS)
  - Depends on: HRMS Employee, Training
  - Provides: Driver Qualification, Training Records, Performance Reviews
  - Used by: Operations (assignment), Safety (eligibility), Finance (payroll links)

# TEMS Module Map — Inter-Domain Dependencies

This map reflects current implemented DocTypes and the 13 domains. Vehicle is the operational nucleus; Assets roll up to Vehicle.

```mermaid
flowchart LR
  subgraph HRMS/People
    Employee
    DriverQualification
    TrainingRecord
  end

  subgraph Fleet
    Vehicle
    Asset
    JourneyPlan
    RoutePlanning
    MaintenanceWorkOrder
    FuelLog
  end

  subgraph Operations
    DispatchSchedule
    ShiftPlan
    DutyAssignment
    OperationsEvent
    ControlException
    SOSEvent
  end

  subgraph Safety
    SafetyIncident
    SpotCheck
    IncidentParticipant
  end

  subgraph Trade
    TradeLane
    BorderCrossing
    CustomsClearance
  end

  subgraph Documents
    DocumentChecklist
    DocumentChecklistItem
  end

  subgraph Finance
    FleetCost
    AllocationRule
  end

  subgraph CRM
    FieldServiceRequest
    CustomerFeedback
  end

  subgraph SupplyChain
    SparePart
  end

  subgraph Informal
    InformalOperatorProfile
    OperatorMarket
    OperatorRouteAssociation
  end

  subgraph Climate
    EmissionsLog
  end

  subgraph Governance
    GovernancePolicy
    ComplianceObligation
    ApprovalMatrix
    GovernanceMeeting
  end

  Employee -->|assigned as| DutyAssignment
  Employee -->|driver| JourneyPlan
  DriverQualification -->|validates| JourneyPlan

  Asset -->|belongs to| Vehicle
  JourneyPlan -->|uses| Vehicle
  FuelLog -->|for| Vehicle
  MaintenanceWorkOrder -->|for| Asset
  MaintenanceWorkOrder -->|rolls up cost to| Vehicle

  DispatchSchedule --> DutyAssignment
  DutyAssignment --> OperationsEvent
  ControlException --> OperationsEvent
  SOSEvent --> OperationsEvent

  SafetyIncident -->|references| Vehicle
  IncidentParticipant -->|references| Employee

  TradeLane --> BorderCrossing
  BorderCrossing -->|links| JourneyPlan
  CustomsClearance -->|links| DeliveryNote

  DocumentChecklist -->|applies to| Vehicle

  FleetCost -->|for| Vehicle
  AllocationRule --> FleetCost

  FieldServiceRequest -->|assigned_to| Employee
  CustomerFeedback -->|journey_plan| JourneyPlan

  SparePart -->|Item link| MaintenanceWorkOrder

  InformalOperatorProfile --> OperatorRouteAssociation
  OperatorRouteAssociation --> RoutePlanning

  EmissionsLog -->|vehicle/journey| JourneyPlan

  GovernancePolicy -->|applies to| Vehicle
  ComplianceObligation -->|notifies| Employee
```

Notes
- Shapes are conceptual; refer to domain packages under `tems/tems_*` for exact DocType names and paths.
- All operations and costing ultimately reference Vehicle, with asset-level drill-down for traceability.
