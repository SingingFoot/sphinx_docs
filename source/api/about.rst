.. _api-about:

About the BlueRound API
=======================

The **BlueRound API** is a RESTful HTTP interface for managing users, handling
OAuth 2.0 authentication, and automating documentation workflows.
All resources are served over HTTPS and represented as JSON.

.. note::
   Current stable version: ``v1.2.0`` — see :ref:`api-versioning` for the
   upgrade policy and deprecation timeline.

----

.. contents:: On This Page
   :depth: 2
   :local:
   :backlinks: none

----

.. _api-versioning:

API Versioning
--------------

BlueRound uses **semantic versioning**. The version is embedded in every
base URL (e.g., ``/v1/``). Breaking changes are introduced only in a new
major version prefix; minor and patch releases are always backward-compatible.

.. list-table:: Version status
   :header-rows: 1
   :widths: 15 20 65

   * - Version
     - Status
     - Notes
   * - ``v1``
     - ✅ Stable
     - Current production version. All new features are added here.
   * - ``v2``
     - 🚧 Preview
     - Opt-in beta. Breaking changes possible. Contact support to join.
   * - ``v0``
     - ❌ Deprecated
     - Sunset date: **2026-09-01**. Migrate to ``v1`` before that date.

.. deprecated:: 0.9
   ``/v0/`` endpoints are deprecated and will be removed on 2026-09-01.
   All ``v0`` paths have direct equivalents in ``v1``.

Base URLs
---------

All API requests **must** be made over HTTPS. Plain HTTP requests are
rejected with ``301 Moved Permanently``.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Environment
     - Base URL
   * - **Production**
     - ``https://api.blueround.com/v1``
   * - **Staging**
     - ``https://api.blueround.dev/v1``
   * - **Local mock**
     - ``http://localhost:4010/v1`` (run ``npx @stoplight/prism-cli mock openapi.yaml``)

.. tip::
   Use the **staging** environment for integration testing. It mirrors
   production data structures but operates on an isolated dataset that
   resets nightly at 02:00 UTC.

Authentication
--------------

Every request must include a valid Bearer token in the ``Authorization`` header:

.. code-block:: http

   GET /v1/users HTTP/1.1
   Host: api.blueround.com
   Authorization: Bearer <your_access_token>
   Accept: application/json

Tokens are obtained via the OAuth 2.0 flow described in :doc:`oauth`.
Access tokens expire after **3 600 seconds** (1 hour). Use the refresh
token endpoint to obtain a new one without re-authenticating.

.. seealso::

   :doc:`oauth` — Full OAuth 2.0 token lifecycle, scopes, and revocation.

Request Format
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Header
     - Required value
   * - ``Content-Type``
     - ``application/json`` for ``POST``, ``PUT``, and ``PATCH`` requests.
   * - ``Accept``
     - ``application/json`` (optional but recommended).
   * - ``Authorization``
     - ``Bearer <access_token>`` — required on all endpoints.
   * - ``X-Request-ID``
     - Optional UUID. Echoed back in the response; useful for tracing.

All request bodies must be valid JSON. Dates and timestamps follow
**ISO 8601** (e.g., ``2026-04-30T09:00:00Z``). Numeric IDs are strings
prefixed by resource type (e.g., ``usr_98765``).

Response Format
---------------

Every response body is a JSON object. Success responses wrap the primary
payload in a ``data`` key. Error responses use the ``error`` key:

.. code-block:: javascript

   {
     "data": { /* primary payload */ },
     "meta": {
       "request_id": "req_a1b2c3",
       "version":    "1.2.0"
     }
   }

.. code-block:: json

   {
     "error": {
       "code":    "RESOURCE_NOT_FOUND",
       "message": "User usr_00000 does not exist.",
       "docs":    "https://docs.blueround.com/api/errors#RESOURCE_NOT_FOUND"
     }
   }

See :doc:`errors` for the complete list of error codes and handling guidance.

Pagination
----------

List endpoints return paginated results using **cursor-based pagination**.
Pass ``limit`` and ``offset`` query parameters to control page size and
starting position.

.. code-block:: http

   GET /v1/users?limit=25&offset=50 HTTP/1.1

The response ``meta`` object includes ``total``, ``limit``, and ``offset``
fields so clients can calculate whether further pages exist:

.. code-block:: javascript

   {
     "data": [ /* array of resource objects */ ],
     "meta": {
       "total":  1250,
       "limit":  25,
       "offset": 50
     }
   }

.. note::
   Maximum ``limit`` is **100**. Requests exceeding this are clamped
   to 100 without returning an error.

Rate Limiting
-------------

The API enforces per-token rate limits to ensure fair usage.

.. list-table:: Default rate limits
   :header-rows: 1
   :widths: 40 30 30

   * - Plan
     - Requests / minute
     - Burst (requests / second)
   * - **Free**
     - 60
     - 10
   * - **Pro**
     - 600
     - 50
   * - **Enterprise**
     - Custom
     - Custom

When a rate limit is exceeded, the API returns :http:statuscode:`429`.
Inspect the response headers to determine when to retry:

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Header
     - Description
   * - ``X-RateLimit-Limit``
     - Maximum requests allowed in the current window.
   * - ``X-RateLimit-Remaining``
     - Requests remaining in the current window.
   * - ``X-RateLimit-Reset``
     - Unix timestamp when the window resets.
   * - ``Retry-After``
     - Seconds to wait before retrying (present on 429 responses only).

.. warning::
   Automated scripts that ignore ``Retry-After`` will have their tokens
   temporarily suspended after repeated violations.

SDK & Client Libraries
----------------------

Official SDKs are available for the most common languages.
All SDKs handle token refresh, retries, and pagination automatically.

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Language
     - Install
     - Repository
   * - **Python**
     - ``pip install blueround-sdk``
     - `github.com/blueround/python-sdk <https://github.com/blueround/python-sdk>`_
   * - **Node.js**
     - ``npm install @blueround/sdk``
     - `github.com/blueround/node-sdk <https://github.com/blueround/node-sdk>`_
   * - **Go**
     - ``go get github.com/blueround/go-sdk``
     - `github.com/blueround/go-sdk <https://github.com/blueround/go-sdk>`_
   * - **Java**
     - Maven: ``com.blueround:sdk:1.2.0``
     - `github.com/blueround/java-sdk <https://github.com/blueround/java-sdk>`_

Service Status
--------------

Real-time uptime and incident history are published at
`status.blueround.com <https://status.blueround.com>`_.
Subscribe to the status page to receive email or webhook notifications
for incidents and scheduled maintenance.

Contact & Support
-----------------

.. list-table::
   :header-rows: 0
   :widths: 30 70

   * - Developer portal
     - `developer.blueround.com <https://developer.blueround.com>`_
   * - Help center
     - `help.blueround.com <https://help.blueround.com>`_
   * - Support tickets
     - `support.blueround.com/tickets <https://support.blueround.com/tickets>`_
   * - Status page
     - `status.blueround.com <https://status.blueround.com>`_

For critical production issues, include your ``X-Request-ID`` and the
affected token's ``client_id`` when opening a support ticket — this
allows the support team to locate your request in server logs immediately.
