.. _api-errors:

Errors & Status Codes
=====================

The BlueRound API uses standard **HTTP status codes** to signal the outcome
of every request. Whenever a request fails, the response body contains a
structured ``error`` object that gives you a machine-readable code, a
human-readable message, and a link to this page for further guidance.

----

.. contents:: On This Page
   :depth: 2
   :local:
   :backlinks: none

----

Error Response Format
---------------------

All error responses follow the same envelope schema:

.. code-block:: json
   :caption: Standard error envelope

   {
     "error": {
       "code":    "RESOURCE_NOT_FOUND",
       "message": "User usr_00000 does not exist.",
       "docs":    "https://docs.blueround.com/api/errors#RESOURCE_NOT_FOUND",
       "details": []
     }
   }

.. list-table:: Error object fields
   :header-rows: 1
   :widths: 25 20 55

   * - Field
     - Type
     - Description
   * - ``code``
     - ``string``
     - Machine-readable error identifier. Use this in code, not ``message``.
   * - ``message``
     - ``string``
     - Human-readable explanation. Subject to change — do not parse.
   * - ``docs``
     - ``string``
     - Permalink to the relevant section of this page.
   * - ``details``
     - ``array``
     - Present on ``VALIDATION_ERROR`` only. Each item names a failing field.

For validation errors, ``details`` provides per-field information:

.. code-block:: json
   :caption: Validation error with field-level details

   {
     "error": {
       "code":    "VALIDATION_ERROR",
       "message": "The request body contains invalid fields.",
       "docs":    "https://docs.blueround.com/api/errors#VALIDATION_ERROR",
       "details": [
         { "field": "email",  "issue": "Must be a valid email address." },
         { "field": "role",   "issue": "Must be one of: admin, member, viewer." }
       ]
     }
   }

HTTP Status Code Reference
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 12 30 58

   * - Code
     - Meaning
     - When it occurs
   * - ``200``
     - OK
     - Request succeeded. Response body contains ``data``.
   * - ``201``
     - Created
     - Resource created successfully. ``Location`` header points to the new resource.
   * - ``204``
     - No Content
     - Request succeeded with no response body (e.g., token revocation).
   * - ``400``
     - Bad Request
     - Malformed JSON, invalid query parameter, or failed validation.
   * - ``401``
     - Unauthorized
     - Missing, expired, or malformed Bearer token.
   * - ``403``
     - Forbidden
     - Valid token but insufficient scope for this operation.
   * - ``404``
     - Not Found
     - Resource does not exist or is not visible to this token.
   * - ``409``
     - Conflict
     - Duplicate resource (e.g., email already registered).
   * - ``422``
     - Unprocessable Entity
     - Syntactically valid request, but semantically invalid (business rule violation).
   * - ``429``
     - Too Many Requests
     - Rate limit exceeded. Retry after ``Retry-After`` seconds.
   * - ``500``
     - Internal Server Error
     - Unexpected server-side failure. Retry with exponential back-off.
   * - ``503``
     - Service Unavailable
     - Temporary outage or maintenance. Check `status.blueround.com <https://status.blueround.com>`_.

Error Code Catalogue
--------------------

.. _VALIDATION_ERROR:

``VALIDATION_ERROR`` (400)
~~~~~~~~~~~~~~~~~~~~~~~~~~

One or more request fields failed validation. Inspect the ``details`` array
for per-field information and correct the request before retrying.

.. _INVALID_TOKEN:

``INVALID_TOKEN`` (401)
~~~~~~~~~~~~~~~~~~~~~~~

The supplied Bearer token is malformed or does not exist.
Obtain a fresh token via :doc:`oauth` and retry.

.. _TOKEN_EXPIRED:

``TOKEN_EXPIRED`` (401)
~~~~~~~~~~~~~~~~~~~~~~~

The access token has passed its ``expires_in`` limit (3 600 seconds).
Use the refresh token grant to obtain a new access token without
re-authenticating the user.

.. code-block:: bash
   :caption: Refresh an expired access token

   curl -X POST "https://auth.blueround.com/oauth/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "grant_type=refresh_token" \
     -d "refresh_token=def50200a9f3..." \
     -d "client_id=YOUR_CLIENT_ID" \
     -d "client_secret=YOUR_CLIENT_SECRET"

.. _INSUFFICIENT_SCOPE:

``INSUFFICIENT_SCOPE`` (403)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The token is valid but does not carry the scope required by this endpoint.
Request a new token that includes the missing scope (e.g., ``users:write``).

.. list-table:: Scope requirements by endpoint
   :header-rows: 1
   :widths: 50 50

   * - Endpoint
     - Required scope
   * - ``GET /users``
     - ``users:read``
   * - ``GET /users/{id}``
     - ``users:read``
   * - ``POST /users``
     - ``users:write``
   * - ``PATCH /users/{id}``
     - ``users:write``
   * - ``DELETE /users/{id}``
     - ``users:write``

.. _RESOURCE_NOT_FOUND:

``RESOURCE_NOT_FOUND`` (404)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The requested resource ID does not exist within your organization or is
not accessible to the authenticated token. Verify the ID and that the
resource belongs to your account.

.. _DUPLICATE_RESOURCE:

``DUPLICATE_RESOURCE`` (409)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A resource with a unique attribute (e.g., email address) already exists.
Retrieve the existing resource instead of creating a new one, or use a
different unique value.

.. _RATE_LIMIT_EXCEEDED:

``RATE_LIMIT_EXCEEDED`` (429)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Your application has exceeded its allowed request rate. Inspect the
``Retry-After`` response header and pause requests for that many seconds
before retrying.

.. code-block:: python
   :caption: Python — respecting Retry-After on 429 responses

   import time
   import requests

   def get_with_retry(url, headers, max_retries=5):
       for attempt in range(max_retries):
           resp = requests.get(url, headers=headers)
           if resp.status_code == 429:
               wait = int(resp.headers.get("Retry-After", 5))
               print(f"Rate limited. Retrying in {wait}s…")
               time.sleep(wait)
               continue
           resp.raise_for_status()
           return resp.json()
       raise RuntimeError("Max retries exceeded.")

.. _INTERNAL_ERROR:

``INTERNAL_ERROR`` (500)
~~~~~~~~~~~~~~~~~~~~~~~~~

An unexpected error occurred on the BlueRound servers. These are rare and
typically transient. Retry using **exponential back-off**:

.. list-table:: Recommended back-off schedule
   :header-rows: 1
   :widths: 20 40 40

   * - Attempt
     - Wait before retry
     - Notes
   * - 1st retry
     - 1 second
     - After the initial failure.
   * - 2nd retry
     - 2 seconds
     - —
   * - 3rd retry
     - 4 seconds
     - —
   * - 4th retry
     - 8 seconds
     - —
   * - Give up
     - —
     - Log the ``X-Request-ID`` and open a support ticket.

.. important::
   Always log the ``X-Request-ID`` response header when a ``500`` error
   occurs. Include it in your support ticket so the BlueRound team can
   locate the server-side trace instantly.

Debugging Tips
--------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Symptom
     - Likely cause and fix
   * - ``401`` on every request
     - Token missing from header, or ``Authorization: Bearer`` typo.
       Print the raw header your code sends.
   * - ``401`` after working for 1 hour
     - Access token expired. Implement automatic refresh — see
       :ref:`TOKEN_EXPIRED`.
   * - ``403`` with valid token
     - Token scope is too narrow. Re-request with the required scope listed
       in :ref:`INSUFFICIENT_SCOPE`.
   * - ``404`` for a resource you created
     - Check you are using the correct environment (production vs. staging).
       Staging data resets nightly.
   * - Intermittent ``500``
     - Retry with back-off. If persistent, check `status.blueround.com
       <https://status.blueround.com>`_ for an active incident.

.. seealso::

   * :doc:`about` — Rate limit headers and base URLs.
   * :doc:`oauth` — Token acquisition, refresh, and revocation.
   * :doc:`get_users` — Status codes specific to the Users endpoints.
