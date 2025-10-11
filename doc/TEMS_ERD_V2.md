# TEMS Entity Relationship Diagram (ERD)
## Multimodal Architecture — Cargo and Passenger Integration

The Transport Excellence Management System (TEMS) supports both **Cargo logistics** and **Passenger transportation** within the same platform, using a unified operational, financial, and fleet structure.  
This diagram and accompanying notes define entity relationships and flow of data across modules.

---

```mermaid
erDiagram

    %% ─────────────────────────────
    %% CORE ENTITIES
    %% ─────────────────────────────
    VEHICLE {
        string vehicle_id
        string vehicle_type  "Cargo | Passenger"
        string registration_no
        string status
    }

    ASSET {
        string asset_id
        string asset_type "Trailer | Tire | Engine | Equipment"
        string vehicle_id
        float cost
        date purchase_date
    }

    %% ─────────────────────────────
    %% PEOPLE / HRMS
    %% ─────────────────────────────
    EMPLOYEE {
        string employee_id
        string name
        string role
        string license_no
        date valid_till
    }

    DRIVER_QUALIFICATION {
        string qualification_id
        string employee_id
        string vehicle_category
        string certification_status
    }

    %% ─────────────────────────────
    %% OPERATIONS CORE
    %% ─────────────────────────────
    OPERATION_PLAN {
        string operation_id
        string vehicle_id
        string operation_mode "Cargo | Passenger"
        string route
        date start_date
        date end_date
    }

    MOVEMENT_LOG {
        string movement_id
        string operation_id
        string vehicle_id
        string status "Check-In | Transit | Delivered | Diversion"
        datetime timestamp
    }

    COST_REVENUE_LEDGER {
        string ledger_id
        string vehicle_id
        float cost
        float revenue
        string source_type "Cargo | Passenger"
    }

    %% ─────────────────────────────
    %% CARGO MODULE
    %% ─────────────────────────────
    CARGO_CONSIGNMENT {
        string consignment_id
        string customer_id
        string origin
        string destination
        float cargo_weight
        float cargo_value
        string vehicle_id
    }

    CARGO_MANIFEST {
        string manifest_id
        string operation_id
        string vehicle_id
    }

    CARGO_WAYBILL {
        string waybill_id
        string consignment_id
        string manifest_id
    }

    %% ─────────────────────────────
    %% PASSENGER MODULE
    %% ─────────────────────────────
    PASSENGER_TRIP {
        string trip_id
        string route
        datetime departure_time
        string vehicle_id
        int seat_capacity
    }

    PASSENGER_BOOKING {
        string booking_id
        string trip_id
        string passenger_name
        int seat_no
        float fare
    }

    PASSENGER_MANIFEST {
        string manifest_id
        string trip_id
        string vehicle_id
    }

    %% ─────────────────────────────
    %% SAFETY, FINANCE, HRMS, SUPPLY CHAIN
    %% ─────────────────────────────
    INCIDENT_REPORT {
        string incident_id
        string operation_id
        string vehicle_id
        string severity
    }

    RISK_ASSESSMENT {
        string risk_id
        string vehicle_id
        string score
    }

    JOURNEY_COSTING {
        string cost_id
        string vehicle_id
        float total_cost
    }

    SUPPLIER {
        string supplier_id
        string name
    }

    PROCUREMENT_ORDER {
        string order_id
        string supplier_id
        string asset_id
        float amount
    }

    %% ─────────────────────────────
    %% RELATIONSHIPS
    %% ─────────────────────────────

    ASSET }o--|| VEHICLE : "attached_to"
    EMPLOYEE ||--o{ DRIVER_QUALIFICATION : "holds"
    VEHICLE ||--o{ OPERATION_PLAN : "assigned_to"
    OPERATION_PLAN ||--o{ MOVEMENT_LOG : "generates"
    VEHICLE ||--o{ COST_REVENUE_LEDGER : "has"
    VEHICLE ||--o{ RISK_ASSESSMENT : "evaluated_by"
    OPERATION_PLAN ||--o{ INCIDENT_REPORT : "reports"
    VEHICLE ||--o{ JOURNEY_COSTING : "tracked_in"

    %% Cargo Branch
    OPERATION_PLAN ||--o{ CARGO_CONSIGNMENT : "includes"
    CARGO_CONSIGNMENT ||--o{ CARGO_MANIFEST : "grouped_in"
    CARGO_MANIFEST ||--o{ CARGO_WAYBILL : "documented_by"

    %% Passenger Branch
    OPERATION_PLAN ||--o{ PASSENGER_TRIP : "includes"
    PASSENGER_TRIP ||--o{ PASSENGER_BOOKING : "books"
    PASSENGER_TRIP ||--o{ PASSENGER_MANIFEST : "lists"

    %% Procurement & Assets
    SUPPLIER ||--o{ PROCUREMENT_ORDER : "fulfills"
    PROCUREMENT_ORDER ||--o{ ASSET : "creates"

