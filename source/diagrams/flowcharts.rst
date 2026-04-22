.. _flowcharts:

Business Process Flowcharts
===========================

We use flowcharts to map out complex logic within the SDK, particularly for authentication and error recovery.

Authentication Process (BPMN Style)
-----------------------------------

This flowchart describes the decision-making logic when a user attempts to access a protected resource.

.. mermaid::

   graph TD
      A[Start Request] --> B{Token Valid?}
      B -- Yes --> C[Access Resource]
      B -- No --> D{Refresh Token Exists?}
      D -- Yes --> E[Request New Access Token]
      D -- No --> F[Redirect to Login]
      E --> G{Success?}
      G -- Yes --> C
      G -- No --> F
      C --> H[End]

