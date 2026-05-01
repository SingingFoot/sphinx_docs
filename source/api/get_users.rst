.. _api-get-users:

Users
=====

The Users API lets you list all users in your organization and retrieve
individual user profiles. All endpoints require a valid Bearer token with
at minimum the ``users:read`` scope (see :doc:`oauth`).

----

.. contents:: On This Page
   :depth: 2
   :local:
   :backlinks: none

----

User Object
-----------

Every endpoint that returns user data uses the same **User object** schema:

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Field
     - Type
     - Description
   * - ``id``
     - ``string``
     - Unique resource identifier, prefixed ``usr_``.
   * - ``name``
     - ``string``
     - Full display name.
   * - ``email``
     - ``string``
     - Primary email address (unique per organization).
   * - ``role``
     - ``string``
     - One of ``admin``, ``member``, or ``viewer``.
   * - ``status``
     - ``string``
     - One of ``active``, ``inactive``, or ``pending_invite``.
   * - ``created_at``
     - ``string (ISO 8601)``
     - Timestamp when the user record was created.
   * - ``updated_at``
     - ``string (ISO 8601)``
     - Timestamp of the most recent modification.

----

List Users
----------

.. http:get:: /users

   Returns a paginated list of all users in the authenticated organization,
   ordered by ``created_at`` descending (newest first).

   :reqheader Authorization: ``Bearer <access_token>`` — required.
   :reqheader Accept: ``application/json`` — recommended.

   :query limit: Maximum number of results to return. Default ``20``, max ``100``.
   :query offset: Number of results to skip for pagination. Default ``0``.
   :query status: Filter by user status. One of ``active``, ``inactive``, ``pending_invite``.
   :query role: Filter by role. One of ``admin``, ``member``, ``viewer``.
   :query q: Partial-match search across ``name`` and ``email`` fields.

   :resheader Content-Type: ``application/json``
   :resheader X-Request-ID: Echo of the request ID (if supplied).

   :status 200: Success — paginated array of User objects returned.
   :status 400: Invalid query parameter value.
   :status 401: Missing or expired Bearer token.
   :status 403: Token lacks the ``users:read`` scope.
   :status 429: Rate limit exceeded — see ``Retry-After`` header.

**Example request:**

.. code-block:: bash
   :caption: List the first 5 active users

   curl -X GET "https://api.blueround.com/v1/users?limit=5&status=active" \
        -H "Authorization: Bearer YOUR_TOKEN" \
        -H "Accept: application/json"

**Example response** (``200 OK``):

.. code-block:: json
   :caption: GET /v1/users — response body

   {
     "data": [
       {
         "id":         "usr_98765",
         "name":       "Oleg Shinkarenko",
         "email":      "oleg@example.com",
         "role":       "admin",
         "status":     "active",
         "created_at": "2025-11-15T08:30:00Z",
         "updated_at": "2026-04-01T14:22:00Z"
       },
       {
         "id":         "usr_12340",
         "name":       "Alice Müller",
         "email":      "alice@example.com",
         "role":       "member",
         "status":     "active",
         "created_at": "2026-01-03T10:00:00Z",
         "updated_at": "2026-01-03T10:00:00Z"
       }
     ],
     "meta": {
       "total":      1250,
       "limit":      5,
       "offset":     0,
       "request_id": "req_a1b2c3d4"
     }
   }

.. tip::
   Use the ``q`` parameter for lightweight search:
   ``GET /users?q=alice`` returns all users whose name or email contains
   *alice* (case-insensitive).

----

Retrieve a Single User
----------------------

.. http:get:: /users/(string:user_id)

   Retrieve a single user record by its unique identifier.

   :param user_id: The ``usr_``-prefixed user ID (e.g., ``usr_98765``).

   :reqheader Authorization: ``Bearer <access_token>`` — required.
   :reqheader Accept: ``application/json`` — recommended.

   :resheader Content-Type: ``application/json``

   :status 200: Success — single User object returned.
   :status 401: Missing or expired Bearer token.
   :status 403: Token lacks the ``users:read`` scope.
   :status 404: No user with the given ``user_id`` exists in your organization.
   :status 429: Rate limit exceeded.

**Example request:**

.. code-block:: bash
   :caption: Retrieve user usr_98765

   curl -X GET "https://api.blueround.com/v1/users/usr_98765" \
        -H "Authorization: Bearer YOUR_TOKEN" \
        -H "Accept: application/json"

**Example response** (``200 OK``):

.. code-block:: json
   :caption: GET /v1/users/{user_id} — response body

   {
     "data": {
       "id":         "usr_98765",
       "name":       "Oleg Shinkarenko",
       "email":      "oleg@example.com",
       "role":       "admin",
       "status":     "active",
       "created_at": "2025-11-15T08:30:00Z",
       "updated_at": "2026-04-01T14:22:00Z"
     },
     "meta": {
       "request_id": "req_b5c6d7e8"
     }
   }

**Error response** (``404 Not Found``):

.. code-block:: json

   {
     "error": {
       "code":    "RESOURCE_NOT_FOUND",
       "message": "User usr_00000 does not exist.",
       "docs":    "https://docs.blueround.com/api/errors#RESOURCE_NOT_FOUND"
     }
   }

----

Pagination
----------

List endpoints use **offset-based pagination**. The ``meta`` block in
every list response tells you the full result set size so you can
calculate total pages:

.. code-block:: python
   :caption: Python — fetch all users with automatic pagination

   import requests

   BASE = "https://api.blueround.com/v1"
   HEADERS = {"Authorization": "Bearer YOUR_TOKEN"}
   LIMIT = 100

   users, offset = [], 0
   while True:
       resp = requests.get(
           f"{BASE}/users",
           headers=HEADERS,
           params={"limit": LIMIT, "offset": offset},
       ).json()
       users.extend(resp["data"])
       if offset + LIMIT >= resp["meta"]["total"]:
           break
       offset += LIMIT

   print(f"Fetched {len(users)} users in total.")

.. note::
   The maximum ``limit`` per request is **100**. For organizations with
   thousands of users, fetching the full list in parallel using ``offset``
   slices is significantly faster than sequential requests.

.. seealso::

   * :doc:`about` — Pagination details, rate limits, and request format.
   * :doc:`errors` — Full list of error codes returned by this endpoint.
   * :doc:`oauth` — How to obtain and refresh access tokens.
