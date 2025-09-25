# TEMS Entity Relationship Diagram (ERD)

This document maps the major modules/domains of the Transport Excellence Management System (TEMS) and their inter-relationships.  
The updated architecture puts **Operations** at the center as the execution hub, with other domains feeding into or drawing from it.

```mermaid
erDiagram

    %% Core Operations Hub
    OPERATIONS ||--o{ OPERATION_PLAN : manages
    OPERATIONS ||--o{ MOVEMENT_LOG : tracks
    OPERATIONS ||--o{ TRIP_ALLOCATION : allocates
    OPERATIONS ||--o{ COST_REVENUE_LEDGER : calculates

    %% HRMS / People
    EMPLOYEE ||--o{ DRIVER_QUALIFICATION : has
    EMPLOYEE ||--o{ TRAINING_RECORD : attends
    EMPLOYEE ||--o{ PERFORMANCE_REVIEW : reviewed_in
    HRMS ||--o{ EMPLOYEE : manages
    HRMS ||--o{ DRIVER_QUALIFICATION : validates
    OPERATIONS ||--o{ EMPLOYEE : assigns

    %% Fleet
    VEHICLE ||--o{ MAINTENANCE_WORK_ORDER : serviced_by
    VEHICLE ||--o{ EMISSION_LOG : emits
    FLEET ||--o{ VEHICLE : manages
    OPERATIONS ||--o{ VEHICLE : allocates

    %% Safety
    SAFETY ||--o{ JOURNEY_PLAN : prepares
    SAFETY ||--o{ INCIDENT_REPORT : records
    SAFETY ||--o{ RISK_ASSESSMENT : evaluates
    OPERATIONS ||--o{ JOURNEY_PLAN : executes

    %% Finance
    FINANCE ||--o{ JOURNEY_COSTING : captures
    FINANCE ||--o{ FX_RISK_LOG : manages
    OPERATIONS ||--o{ COST_REVENUE_LEDGER : integrates

    %% CRM
    CUSTOMER ||--o{ ORDER : places
    CRM ||--o{ CUSTOMER : manages
    CRM ||--o{ SLA_LOG : tracks
    OPERATIONS ||--o{ ORDER : fulfills

    %% Supply Chain
    SUPPLIER ||--o{ PROCUREMENT_ORDER : fulfills
    SUPPLYCHAIN ||--o{ INVENTORY_ITEM : manages
    OPERATIONS ||--o{ INVENTORY_ITEM : consumes

    %% Trade
    TRADE ||--o{ BORDER_CROSSING : requires
    TRADE ||--o{ FX_TRANSACTION : incurs
    OPERATIONS ||--o{ BORDER_CROSSING : executes

    %% Informal
    INFORMAL ||--o{ TRIP_MATCH : participates
    INFORMAL ||--o{ SAVINGS_GROUP : joins
    INFORMAL ||--o{ LOAN : accesses
    OPERATIONS ||--o{ TRIP_MATCH : integrates

    %% Climate
    CLIMATE ||--o{ CLIMATE_ALERT : issues
    CLIMATE ||--o{ RENEWABLE_ASSET : manages
    OPERATIONS ||--o{ CLIMATE_ALERT : adjusts

    %% Governance
    GOVERNANCE ||--o{ POLICY : defines
    GOVERNANCE ||--o{ COMPLIANCE_AUDIT : oversees
    OPERATIONS ||--o{ POLICY : enforces

    %% Documents
    DOCUMENTS ||--o{ COMPLIANCE_DOCUMENT : stores
    DOCUMENTS ||--o{ POLICY_DOCUMENT : holds
    OPERATIONS ||--o{ COMPLIANCE_DOCUMENT : references

    %% Insights
    INSIGHTS ||--o{ KPI_CONFIG : aggregates
    INSIGHTS ||--o{ DASHBOARD : visualizes
    INSIGHTS ||--o{ REPORT_SUBSCRIPTION : automates
    OPERATIONS ||--o{ KPI_CONFIG : feeds
