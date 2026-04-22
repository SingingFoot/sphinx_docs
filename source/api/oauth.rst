OAuth2 Authentication
=====================

Our API uses **OAuth 2.0** for secure authorization. Every request must include an ``Authorization`` header with a valid Bearer token.

.. centered:: **Authorization: Bearer <your_access_token>**

Registration
------------

Before using OAuth, you must register your application in the **Developer Dashboard** to obtain your:

* ``client_id``
* ``client_secret``

Grant Types
-----------

We support the following OAuth2 grant types:

1. **Authorization Code Grant**: Recommended for web and mobile apps.
2. **Client Credentials Grant**: Recommended for machine-to-machine communication.

.. warning::
   Your ``client_secret`` is private. Never share it or include it in client-side code (like JavaScript or mobile apps).

Token Expiration
----------------

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - Token Type
     - TTL (Time To Live)
   * - Access Token
     - 3600 seconds (1 hour)
   * - Refresh Token
     - 30 days
