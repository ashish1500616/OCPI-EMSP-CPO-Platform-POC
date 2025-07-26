# Architecture Documentation

This section provides a comprehensive visual overview of the system architecture, workflows, and data models.

## System Context Diagram

This diagram illustrates the EMSP platform's position within its operational ecosystem. It highlights the key external systems the platform interacts with, providing a high-level overview of its boundaries and dependencies.

```mermaid
graph TD
    subgraph EMSP Platform
        A[FastAPI Application]
    end

    subgraph External Systems
        B(CPO Platforms)
        C(Charging Stations)
        D(Mobile App)
        E(Payment Gateway)
    end

    A -- OCPI 2.2.1 --> B
    B -- OCPI 2.2.1 --> A
    A -- User Interaction --> D
    D -- User Interaction --> A
    A -- Billing --> E
    CPO_Platforms -- OCPP --> C
    B -- OCPI Data --> D

    style A fill:#f9f,stroke:#333,stroke-width:2px
```

## Component Architecture Diagram

This diagram provides a detailed view of the internal components of the EMSP platform. It shows how the FastAPI application is structured and how the different layers interact.

```mermaid
graph TD
    subgraph "FastAPI Application"
        direction LR
        A[API Endpoints] --> B{OCPI Router}
        B --> C[OCPI Modules]
        C --> D{CRUD Interface}
        C --> E{Authentication}
        D --> F[Data Persistence]
        E --> F
    end

    subgraph "OCPI Modules (extrawest_ocpi)"
        direction TB
        C1[Locations]
        C2[Sessions]
        C3[CDRs]
        C4[Tariffs]
        C5[Commands]
        C6[Tokens]
        C7[...]
    end

    subgraph "Data Layer"
        direction TB
        F --> G[(Database)]
        F --> H[(Mock Storage)]
    end

    C --> C1
    C --> C2
    C --> C3
    C --> C4
    C --> C5
    C --> C6
    C --> C7

    style A fill:#ccf,stroke:#333,stroke-width:2px
    style B fill:#f9f,stroke:#333,stroke-width:2px
    style C fill:#fcf,stroke:#333,stroke-width:2px
    style D fill:#cfc,stroke:#333,stroke-width:2px
    style E fill:#cfc,stroke:#333,stroke-width:2px
    style F fill:#ffc,stroke:#333,stroke-width:2px
```

## Deployment Diagram

This diagram shows a potential deployment strategy for the EMSP platform in a production environment. It illustrates how the application components are distributed across the infrastructure.

```mermaid
graph TD
    subgraph "User's Device"
        A[Mobile App / Browser]
    end

    subgraph "Cloud Infrastructure (e.g., AWS, Azure, GCP)"
        B(Internet) --> C{Load Balancer / Reverse Proxy}
        C --> D["Web Server (Docker Container)"]
        D -- "DB Connection" --> E["Database Server (PostgreSQL)"]
    end

    subgraph "Web Server Node"
        direction LR
        D --> F[FastAPI App]
        F --> G[Uvicorn]
    end

    A -- HTTPS --> B
```

## Sequence Diagram: EMSP-CPO Authentication and Token Exchange

This diagram shows the sequence of interactions for the initial handshake and authentication between the EMSP and a CPO platform, as defined by the OCPI 2.2.1 credentials module.

```mermaid
sequenceDiagram
    participant EMSP
    participant CPO

    EMSP->>CPO: POST /ocpi/2.2.1/credentials
    note right of EMSP: EMSP sends its token (Token A) and endpoint information.
    CPO-->>EMSP: 200 OK (with CPO's token and endpoint info)
    note left of CPO: CPO responds with its token (Token C) and endpoint details.

    EMSP->>CPO: GET /ocpi/2.2.1/locations
    note right of EMSP: EMSP uses CPO's token (Token C) for authentication.
    CPO-->>EMSP: 200 OK (with location data)

    CPO->>EMSP: POST /ocpi/emsp/2.2.1/commands/START_SESSION
    note left of CPO: CPO uses EMSP's token (Token A) for authentication.
    EMSP-->>CPO: 200 OK (command response)
```

## Sequence Diagram: Location and Tariff Data Synchronization

This diagram illustrates how the EMSP synchronizes charging location and tariff data with a CPO platform. This is a fundamental process for ensuring that the EMSP has accurate information to display to its users.

```mermaid
sequenceDiagram
    participant EMSP
    participant CPO

    EMSP->>CPO: GET /ocpi/2.2.1/locations
    note right of EMSP: Request a list of all charging locations.
    CPO-->>EMSP: 200 OK (with a list of locations)

    EMSP->>CPO: GET /ocpi/2.2.1/locations/{location_id}
    note right of EMSP: Request details for a specific location.
    CPO-->>EMSP: 200 OK (with location details)

    EMSP->>CPO: GET /ocpi/2.2.1/tariffs
    note right of EMSP: Request a list of all available tariffs.
    CPO-->>EMSP: 200 OK (with a list of tariffs)

    loop Data Update (Push Model)
        CPO->>EMSP: PUT /ocpi/emsp/2.2.1/locations/{location_id}/{evse_uid}
        note left of CPO: CPO pushes an update for a specific EVSE.
        EMSP-->>CPO: 200 OK
    end
```

## Sequence Diagram: Charging Session Lifecycle

This diagram shows the complete lifecycle of a charging session, from initiation by the user to completion. It illustrates the roles of the User, EMSP, CPO, and the physical Charging Station.

```mermaid
sequenceDiagram
    participant User
    participant EMSP
    participant CPO
    participant ChargingStation

    User->>EMSP: Start Charging Request (via Mobile App)
    EMSP->>CPO: POST /ocpi/2.2.1/commands/START_SESSION
    note right of EMSP: EMSP sends a command to the CPO to start the session.
    CPO->>ChargingStation: Start Charging Command (OCPP)
    ChargingStation-->>CPO: Command Accepted
    CPO-->>EMSP: 200 OK (Command Response: ACCEPTED)

    loop Session Updates
        CPO->>EMSP: PUT /ocpi/emsp/2.2.1/sessions/{session_id}
        note left of CPO: CPO pushes session updates (e.g., energy consumed).
        EMSP-->>CPO: 200 OK
    end

    User->>EMSP: Stop Charging Request (via Mobile App)
    EMSP->>CPO: POST /ocpi/2.2.1/commands/STOP_SESSION
    note right of EMSP: EMSP sends a command to the CPO to stop the session.
    CPO->>ChargingStation: Stop Charging Command (OCPP)
    ChargingStation-->>CPO: Command Accepted
    CPO-->>EMSP: 200 OK (Command Response: ACCEPTED)

    CPO->>EMSP: PUT /ocpi/emsp/2.2.1/sessions/{session_id}
    note left of CPO: CPO pushes the final session update with status COMPLETED.
    EMSP-->>CPO: 200 OK
```

## Sequence Diagram: CDR Processing and Billing

This diagram illustrates the process of handling Charge Detail Records (CDRs) and billing the user for a completed charging session.

```mermaid
sequenceDiagram
    participant CPO
    participant EMSP
    participant BillingSystem
    participant User

    CPO->>EMSP: POST /ocpi/emsp/2.2.1/cdrs
    note left of CPO: CPO sends the Charge Detail Record (CDR) after the session.
    EMSP-->>CPO: 200 OK

    EMSP->>BillingSystem: Process CDR for Invoicing
    note right of EMSP: EMSP forwards the CDR to the internal or external billing system.
    BillingSystem-->>EMSP: CDR Processed

    BillingSystem->>User: Issue Invoice
    note right of BillingSystem: The user is billed for the charging session.
```

## Activity Diagram: Session Authorization

This diagram shows the business process for authorizing a charging session when a user presents their credentials (e.g., an RFID card) at a charging station.

```mermaid
graph TD
    A[Start] --> B{User presents RFID token or uses Mobile App};
    B --> C{CPO receives authorization request};
    C --> D[CPO sends Token Authorization Request To EMSP]
    D --> E{EMSP receives request};
    E --> F{Is token valid?};
    F -- Yes --> G{Is user account active and in good standing?};
    F -- No --> H[Respond with AUTH_BLOCKED];
    G -- Yes --> I[Respond with AUTH_ALLOWED];
    G -- No --> J[Respond with AUTH_BLOCKED];
    I --> K{CPO starts charging session};
    H --> L[End];
    J --> L;
    K --> L;

    style A fill:#cfc,stroke:#333,stroke-width:2px
    style L fill:#fcc,stroke:#333,stroke-width:2px
```

## Activity Diagram: Payment Processing

This diagram outlines the process of handling payments after a charging session is complete and a CDR has been received.

```mermaid
graph TD
    A[Start] --> B{CDR is received from CPO};
    B --> C{EMSP validates CDR};
    C --> D{Calculate final cost based on CDR and tariffs};
    D --> E{EMSP sends payment request to Payment Gateway};
    E --> F{Payment Gateway processes payment};
    F -- Success --> G{Payment Gateway sends confirmation to EMSP};
    F -- Failure --> H{Handle payment failure};
    G --> I{EMSP updates user's billing status};
    I --> J[End];
    H --> K{Notify user of payment issue};
    K --> J;

    style A fill:#cfc,stroke:#333,stroke-width:2px
    style J fill:#fcc,stroke:#333,stroke-width:2px
```

## Entity Relationship Diagram (ERD)

This diagram shows the database schema and the relationships between the main OCPI entities.

```mermaid
erDiagram
    LOCATION ||--o{ EVSE : contains
    EVSE ||--|{ CONNECTOR : contains
    SESSION ||--|| CDR : results_in
    SESSION }o--|| TOKEN : authenticated_by
    SESSION }o--|| LOCATION : occurs_at
    TARIFF ||--o{ SESSION : applies_to

    LOCATION {
        string id
        string name
        string address
        string city
        string country
    }

    EVSE {
        string uid
        string status
    }

    CONNECTOR {
        string id
        string standard
        string format
        string power_type
    }

    SESSION {
        string id
        datetime start_date_time
        datetime end_date_time
        float kwh
        string auth_method
    }

    CDR {
        string id
        datetime start_date_time
        datetime end_date_time
        float total_energy
        float total_time
        float total_cost
    }

    TOKEN {
        string uid
        string type
        string auth_id
        bool valid
    }

    TARIFF {
        string id
        string currency
        string type
    }
```

## API Interaction Diagram

This diagram shows the relationships between the main OCPI REST endpoints and how they are used for communication between the EMSP and CPO platforms.

```mermaid
graph TD
    subgraph "EMSP (Receiver)"
        A["/locations"]
        B["/sessions"]
        C["/cdrs"]
        D["/tariffs"]
    end

    subgraph "EMSP (Sender)"
        E["/commands"]
        F["/tokens"]
    end

    subgraph "CPO"
        G[CPO Platform]
    end

    G -- "GET, PUT, PATCH, DELETE" --> A
    G -- "GET, PUT, PATCH, DELETE" --> B
    G -- "GET, POST" --> C
    G -- "GET, PUT, PATCH, DELETE" --> D
    A -- " " --> G
    B -- " " --> G
    C -- " " --> G
    D -- " " --> G

    G -- "POST" --> E
    G -- "GET, PUT, PATCH, DELETE" --> F
    E -- " " --> G
    F -- " " --> G
```

## State Transition Diagram: Charging Session States

This diagram illustrates the lifecycle of a charging session through its various states, as defined by the OCPI protocol.

```mermaid
stateDiagram-v2
    [*] --> PENDING
    PENDING --> ACTIVE: START_SESSION command
    ACTIVE --> COMPLETED: STOP_SESSION command
    ACTIVE --> INVALID: Session fails
    PENDING --> INVALID: Authorization fails
    COMPLETED --> [*]
    INVALID --> [*]
```

## State Transition Diagram: Connector Statuses

This diagram shows the various states that a charging connector can be in, and the events that cause it to transition from one state to another.

```mermaid
stateDiagram-v2
    [*] --> AVAILABLE
    AVAILABLE --> PREPARING: User connects EV
    PREPARING --> CHARGING: Charging starts
    CHARGING --> SUSPENDED_EVSE: EVSE pauses charging
    CHARGING --> SUSPENDED_EV: EV pauses charging
    SUSPENDED_EVSE --> CHARGING: Charging resumes
    SUSPENDED_EV --> CHARging: Charging resumes
    CHARGING --> FINISHING: Charging complete
    FINISHING --> AVAILABLE: User unplugs EV
    AVAILABLE --> UNAVAILABLE: Maintenance
    UNAVAILABLE --> AVAILABLE: Maintenance complete
    AVAILABLE --> FAULTED: Connector error
    FAULTED --> AVAILABLE: Error resolved
