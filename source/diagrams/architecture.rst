.. _architecture:

System Architecture
===================

Our system follows a modular architecture to ensure scalability and ease of integration.

SDK Integration Flow (UML)
--------------------------

The following sequence diagram illustrates how the Client SDK interacts with the **BlueRound API** during a typical request.

.. mermaid::

   sequenceDiagram
      participant App as Client Application
      participant SDK as BlueRound SDK
      participant API as BlueRound API
      
      App->>SDK: call get_user(id)
      SDK->>SDK: Validate Local Token
      SDK->>API: GET /v1/users/{id}
      API-->>SDK: 200 OK (JSON)
      SDK-->>App: User Object
