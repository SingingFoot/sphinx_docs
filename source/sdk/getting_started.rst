.. _sdk-getting-started:

Getting Started with the RedCore SDK
=====================================

The **RedCore SDK** is the fastest way to integrate with the RedCore platform.
It is available for Python, Node.js, Go, and Java, wraps every REST endpoint
in a typed, idiomatic interface, and handles token refresh and retries
automatically — so you focus on your product, not on HTTP plumbing.

----

.. contents:: On This Page
   :depth: 2
   :local:
   :backlinks: none

----

How the SDK Fits In
-------------------

.. mermaid::

   flowchart LR
     App["Your Application"]
     SDK["RedCore SDK"]
     Auth["Auth Server\n(OAuth 2.0)"]
     API["RedCore REST API"]

     App  -->|"SDK method call"| SDK
     SDK  -->|"POST /oauth/token\n(auto-refresh)"| Auth
     Auth -->|"access_token"| SDK
     SDK  -->|"HTTPS + Bearer token"| API
     API  -->|"JSON response"| SDK
     SDK  -->|"typed object / exception"| App

The SDK manages token acquisition and renewal transparently —
you never touch raw HTTP or handle token expiry manually.

Prerequisites
-------------

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Requirement
     - Details
   * - **RedCore account**
     - An active project in the `RedCore Dashboard <https://dashboard.redcore.com>`_.
   * - **Credentials**
     - An API Key **or** OAuth 2.0 ``client_id`` + ``client_secret`` pair.
   * - **Runtime**
     - Python ≥ 3.8 · Node.js ≥ 18 · Go ≥ 1.21 · Java ≥ 17

Installation
------------

Python
~~~~~~

We recommend using a **virtual environment** to isolate dependencies.

.. code-block:: bash
   :caption: Python — install via pip

   python3 -m venv .venv
   source .venv/bin/activate       # Windows: .venv\Scripts\activate
   pip install redcore-sdk

Node.js
~~~~~~~

.. code-block:: bash
   :caption: Node.js — install via npm

   npm install @redcore/sdk

Go
~~

.. code-block:: bash
   :caption: Go — add the module

   go get github.com/redcore/go-sdk@latest

Java (Maven)
~~~~~~~~~~~~

.. code-block:: xml
   :caption: pom.xml — Maven dependency

   <dependency>
     <groupId>com.redcore</groupId>
     <artifactId>sdk</artifactId>
     <version>2.1.0</version>
   </dependency>

Configuration
-------------

The SDK client accepts the following options. Supplying credentials via
**environment variables** is strongly recommended so they never appear
in source code or version control.

.. list-table:: Client configuration options
   :header-rows: 1
   :widths: 28 14 58

   * - Option
     - Required
     - Description
   * - ``api_key``
     - Yes *
     - Static API key. Use for server-to-server calls without a user context.
   * - ``client_id``
     - Yes *
     - OAuth 2.0 client identifier. Required when using the OAuth flow.
   * - ``client_secret``
     - Yes *
     - OAuth 2.0 client secret. Required when using the OAuth flow.
   * - ``base_url``
     - No
     - Override the API root. Default: ``https://api.redcore.com/v1``.
   * - ``timeout``
     - No
     - Request timeout in seconds. Default: ``30``.
   * - ``max_retries``
     - No
     - Automatic retries on 5xx responses. Default: ``3``.
   * - ``environment``
     - No
     - ``production`` (default) or ``staging``.

\* Supply either ``api_key`` **or** the ``client_id`` + ``client_secret`` pair.

.. important::
   Never hardcode credentials in source files or commit them to version control.
   Use environment variables or a secrets manager such as AWS Secrets Manager
   or HashiCorp Vault.

.. code-block:: bash
   :caption: .env — recommended credential pattern

   REDCORE_API_KEY=rk_live_abc123...
   REDCORE_BASE_URL=https://api.redcore.com/v1
   REDCORE_TIMEOUT=30

Initializing the Client
-----------------------

Python
~~~~~~

.. code-block:: python
   :caption: app.py — read credentials from the environment
   :linenos:
   :emphasize-lines: 5,6,7

   import os
   from redcore import Client

   client = Client(
       api_key=os.environ["REDCORE_API_KEY"],
       base_url=os.environ.get("REDCORE_BASE_URL"),
       timeout=int(os.environ.get("REDCORE_TIMEOUT", 30)),
   )

Node.js
~~~~~~~

.. code-block:: javascript
   :caption: app.js — read credentials from the environment

   const { RedcoreClient } = require("@redcore/sdk");

   const client = new RedcoreClient({
     apiKey:  process.env.REDCORE_API_KEY,
     timeout: parseInt(process.env.REDCORE_TIMEOUT ?? "30", 10),
   });

Go
~~

.. code-block:: go
   :caption: main.go — functional options pattern

   import (
       "os"
       "github.com/redcore/go-sdk/redcore"
   )

   client := redcore.NewClient(
       redcore.WithAPIKey(os.Getenv("REDCORE_API_KEY")),
       redcore.WithTimeout(30),
   )

Your First API Call
-------------------

Retrieve your own profile to confirm the SDK and credentials are
correctly configured.

.. code-block:: python
   :caption: Python — smoke test with error handling

   from redcore.exceptions import AuthenticationError, RedcoreAPIError

   try:
       me = client.users.get_me()
       print(f"Connected as: {me.name} <{me.email}>")
   except AuthenticationError:
       print("Invalid or expired API key — check REDCORE_API_KEY.")
   except RedcoreAPIError as exc:
       print(f"API error {exc.status_code}: {exc.message}")

.. code-block:: javascript
   :caption: Node.js — smoke test with error handling

   try {
     const me = await client.users.getMe();
     console.log(`Connected as: ${me.name} <${me.email}>`);
   } catch (err) {
     if (err.status === 401) console.error("Invalid API key.");
     else console.error(`API error ${err.status}: ${err.message}`);
   }

.. tip::
   Add this snippet as a **health-check step** in your CI pipeline to catch
   credential drift before it reaches production.

Error Handling
--------------

Every SDK method raises (or rejects with) a typed exception rather than
returning raw HTTP objects. All exceptions inherit from ``RedcoreError``
so you can catch selectively or broadly.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Exception
     - When it is raised
   * - ``AuthenticationError``
     - API key or token is missing, invalid, or expired (HTTP 401).
   * - ``PermissionError``
     - Credentials lack the required scope (HTTP 403).
   * - ``NotFoundError``
     - The requested resource does not exist (HTTP 404).
   * - ``ValidationError``
     - Request body failed server-side validation (HTTP 400 / 422).
   * - ``RateLimitError``
     - Rate limit exceeded (HTTP 429). Carries a ``retry_after`` attribute.
   * - ``RedcoreAPIError``
     - Any other 4xx / 5xx response. Carries ``status_code`` and ``message``.
   * - ``NetworkError``
     - Connection timeout or DNS failure (no HTTP response received).

.. code-block:: python
   :caption: Python — graceful retry on rate-limit and transient errors

   import time
   from redcore.exceptions import RateLimitError, RedcoreAPIError

   def safe_get_user(client, user_id: str, max_retries: int = 3):
       for attempt in range(max_retries):
           try:
               return client.users.get(user_id)
           except RateLimitError as exc:
               time.sleep(exc.retry_after)
           except RedcoreAPIError as exc:
               if exc.status_code >= 500 and attempt < max_retries - 1:
                   time.sleep(2 ** attempt)
                   continue
               raise
       raise RuntimeError("Max retries exceeded.")

Next Steps
----------

.. list-table::
   :header-rows: 0
   :widths: 40 60

   * - :doc:`authentication`
     - API Key, OAuth 2.0, and SAML authentication in depth.
   * - :doc:`api_endpoints`
     - Full method reference with request / response schemas.
   * - :doc:`/api/oauth`
     - REST-level OAuth 2.0 token lifecycle and revocation.
   * - :doc:`/api/errors`
     - Complete error-code catalogue and retry guidance.

.. seealso::

   * `RedCore Dashboard <https://dashboard.redcore.com>`_ — manage API keys
     and OAuth credentials.
   * `Changelog <https://docs.redcore.com/sdk/changelog>`_ — release notes
     and migration guides.
   * :ref:`architecture` — system architecture diagrams.
