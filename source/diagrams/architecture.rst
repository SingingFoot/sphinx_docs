.. _architecture:

System Architecture
===================

This page documents the BlueRound platform architecture: component responsibilities,
communication patterns, deployment topology, and request-level data flows.
All diagrams are maintained as plain-text Mermaid source and live alongside the
documentation they describe.

----

.. contents:: On This Page
   :depth: 2
   :local:
   :backlinks: none

----

Component Overview
------------------

The platform is divided into five logical layers. Each layer has a single
well-defined responsibility and communicates only with adjacent layers.

.. list-table:: Platform components
   :header-rows: 1
   :widths: 22 18 60

   * - Component
     - Layer
     - Responsibility
   * - **Client Application**
     - Presentation
     - Web, mobile, or CLI interface operated by the end user.
   * - **RedCore SDK**
     - Integration
     - Language-specific wrapper; handles auth, retries, and pagination.
   * - **API Gateway**
     - Edge
     - TLS termination, rate limiting, request routing, and logging.
   * - **Auth Service**
     - Security
     - OAuth 2.0 token issuance, validation, and revocation.
   * - **BlueRound API**
     - Application
     - Business logic for user management, catalog, and workflows.
   * - **Data Store**
     - Persistence
     - PostgreSQL (relational data) + Redis (token cache & rate counters).
   * - **CDN / Object Store**
     - Delivery
     - Static assets, documentation builds, and file uploads (S3-compatible).

High-Level Architecture
-----------------------

.. mermaid::

   flowchart TD
     subgraph Clients["Client Layer"]
       WebApp["Web App\n(Browser)"]
       MobileApp["Mobile App\n(iOS / Android)"]
       CLI["CLI / Script\n(RedCore SDK)"]
     end

     subgraph Edge["Edge Layer"]
       GW["API Gateway\n(Rate Limit · TLS · Routing)"]
       CDN["CDN\n(Static Assets)"]
     end

     subgraph Services["Application Layer"]
       AuthSvc["Auth Service\n(OAuth 2.0)"]
       API["BlueRound API\n(REST)"]
       WorkerQ["Background Worker\n(Async Jobs)"]
     end

     subgraph Persistence["Data Layer"]
       PG[("PostgreSQL\n(Primary Store)")]
       Redis[("Redis\n(Cache · Sessions)")]
       S3[("Object Store\n(Files · Docs)")]
     end

     WebApp & MobileApp & CLI -->|HTTPS| GW
     GW -->|Static| CDN
     GW -->|/oauth/*| AuthSvc
     GW -->|/v1/*| API
     AuthSvc --> Redis
     API --> PG
     API --> Redis
     API -->|Enqueue| WorkerQ
     WorkerQ --> PG
     WorkerQ --> S3
     API --> S3

SDK Integration Sequence
------------------------

A typical SDK call for ``GET /users/{id}`` — showing token validation,
the happy path, and automatic token refresh.

.. mermaid::

   sequenceDiagram
     participant App  as Client Application
     participant SDK  as RedCore SDK
     participant Cache as Token Cache (Redis)
     participant Auth  as Auth Service
     participant API   as BlueRound API

     App->>SDK: client.users.get("usr_98765")
     SDK->>Cache: Is access_token still valid?
     alt Token valid
       Cache-->>SDK: ✓ valid, TTL remaining
     else Token expired
       Cache-->>SDK: ✗ expired
       SDK->>Auth: POST /oauth/token (refresh_token)
       Auth-->>SDK: new access_token + refresh_token
       SDK->>Cache: Store new tokens
     end
     SDK->>API: GET /v1/users/usr_98765\nAuthorization: Bearer <token>
     API->>API: Authorize scope (users:read)
     API-->>SDK: 200 OK — User JSON
     SDK-->>App: User object (typed)

Error Recovery Sequence
-----------------------

How the SDK handles transient 5xx errors with exponential back-off,
and what happens when all retries are exhausted.

.. mermaid::

   sequenceDiagram
     participant App  as Client Application
     participant SDK  as RedCore SDK
     participant API  as BlueRound API

     App->>SDK: client.users.list()
     SDK->>API: GET /v1/users  (attempt 1)
     API-->>SDK: 503 Service Unavailable
     SDK->>SDK: Wait 1 s (back-off attempt 1)
     SDK->>API: GET /v1/users  (attempt 2)
     API-->>SDK: 500 Internal Server Error
     SDK->>SDK: Wait 2 s (back-off attempt 2)
     SDK->>API: GET /v1/users  (attempt 3)
     API-->>SDK: 200 OK
     SDK-->>App: User list

     Note over App,SDK: If attempt 3 also fails…
     SDK-->>App: raise RedcoreAPIError(status=500)

OAuth 2.0 Token Lifecycle
--------------------------

State machine showing every possible transition for an access/refresh
token pair from issuance to final revocation or expiry.

.. mermaid::

   stateDiagram-v2
     [*] --> Issued: POST /oauth/token
     Issued --> Active: Stored by client
     Active --> Expired: TTL (3 600 s) elapsed
     Active --> Revoked: POST /oauth/revoke
     Expired --> Active: Refreshed via refresh_token
     Expired --> Invalid: Refresh token also expired (>30 days)
     Revoked --> [*]
     Invalid --> [*]: Re-authentication required

Deployment Architecture
-----------------------

Production topology across two availability zones with an active-active
API cluster and a primary + read-replica database pair.

.. mermaid::

   flowchart LR
     subgraph AZ1["Availability Zone A"]
       LB1["Load Balancer"]
       API1["API Node 1"]
       API2["API Node 2"]
       PG_Primary[("PostgreSQL\nPrimary")]
     end

     subgraph AZ2["Availability Zone B"]
       LB2["Load Balancer"]
       API3["API Node 3"]
       API4["API Node 4"]
       PG_Replica[("PostgreSQL\nReplica")]
     end

     subgraph Global["Global / Shared"]
       GW_GLB["Global Load Balancer\n(Anycast)"]
       RedisCluster[("Redis Cluster\n(3-node)")]
       S3_Bucket[("Object Store\n(multi-region)")]
     end

     Internet(("Internet")) --> GW_GLB
     GW_GLB --> LB1 & LB2
     LB1 --> API1 & API2
     LB2 --> API3 & API4
     API1 & API2 & API3 & API4 --> RedisCluster
     API1 & API2 --> PG_Primary
     API3 & API4 --> PG_Replica
     PG_Primary -.->|replication| PG_Replica
     API1 & API2 & API3 & API4 --> S3_Bucket

.. list-table:: Infrastructure sizing (production defaults)
   :header-rows: 1
   :widths: 30 25 45

   * - Component
     - Instance type
     - Notes
   * - API Nodes (×4)
     - 4 vCPU / 8 GB RAM
     - Auto-scales to ×8 under sustained load.
   * - PostgreSQL Primary
     - 8 vCPU / 32 GB RAM
     - Point-in-time recovery enabled, 30-day retention.
   * - PostgreSQL Replica
     - 4 vCPU / 16 GB RAM
     - Read traffic + reporting queries.
   * - Redis Cluster (×3)
     - 2 vCPU / 4 GB RAM
     - Cluster mode; AOF persistence enabled.
   * - Object Store
     - N/A (managed)
     - 99.999 999 999 % (11-nines) durability guarantee.

Data Flow: User Creation
------------------------

End-to-end data flow for ``POST /users``, from SDK call to invitation
email delivery, including async background job processing.

.. mermaid::

   flowchart TD
     A["SDK: client.users.create(email, name, role)"]
     B["API Gateway\nRate-limit check · Auth scope check"]
     C["BlueRound API\nValidate payload · Check for duplicates"]
     D{{"Duplicate\nemail?"}}
     E["Write user record → PostgreSQL"]
     F["Enqueue invitation job → Worker Queue"]
     G["Return 201 Created + User JSON"]
     H["Background Worker\nRender email template"]
     I["Email Provider\nSend invitation"]
     J["Update user.status → pending_invite"]

     A --> B --> C --> D
     D -- Yes --> ERR["Return 409 DUPLICATE_RESOURCE"]
     D -- No --> E --> F --> G
     F --> H --> I --> J

.. seealso::

   * :doc:`flowcharts` — Decision flowcharts for auth, retry, and CI/CD pipelines.
   * :doc:`/api/about` — API versioning, base URLs, and rate limits.
   * :doc:`/sdk/getting_started` — SDK initialization and first API call.
