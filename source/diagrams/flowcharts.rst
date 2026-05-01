.. _flowcharts:

Business Process Flowcharts
===========================

This page collects decision and process flowcharts for the most common
operational and development workflows in the BlueRound platform.
Each diagram is followed by a decision-point reference table for
quick scanning.

----

.. contents:: On This Page
   :depth: 2
   :local:
   :backlinks: none

----

Authentication & Token Flow
----------------------------

Decision logic when a client attempts to access a protected resource,
covering valid tokens, silent refresh, and forced re-authentication.

.. mermaid::

   flowchart TD
     A(["Client makes API request"]) --> B{"access_token\npresent?"}
     B -- No --> LOGIN["Redirect to login /\nRequest new token"]
     B -- Yes --> C{"Token\nexpired?"}
     C -- No --> D{"Scope\nsufficient?"}
     C -- Yes --> E{"refresh_token\npresent?"}
     E -- No --> LOGIN
     E -- Yes --> F["POST /oauth/token\ngrant_type=refresh_token"]
     F --> G{"Refresh\nsucceeded?"}
     G -- No --> LOGIN
     G -- Yes --> H["Store new token pair"]
     H --> D
     D -- No --> SCOPE_ERR(["Return 403 INSUFFICIENT_SCOPE"])
     D -- Yes --> API["Forward request to API"]
     API --> I{"HTTP status?"}
     I -- 2xx --> SUCCESS(["Return response to caller"])
     I -- 4xx --> CLIENT_ERR(["Raise client error exception"])
     I -- 5xx --> RETRY["Enter retry loop\n(see Error Retry flow)"]

.. list-table:: Authentication decision points
   :header-rows: 1
   :widths: 30 35 35

   * - Decision
     - Yes branch
     - No branch
   * - ``access_token`` present?
     - Check expiry
     - Redirect to login
   * - Token expired?
     - Try refresh token
     - Check scope
   * - ``refresh_token`` present?
     - Call ``/oauth/token``
     - Redirect to login
   * - Refresh succeeded?
     - Store new token pair
     - Redirect to login
   * - Scope sufficient?
     - Forward request
     - Return 403

----

Error Handling & Retry Logic
-----------------------------

How the SDK implements exponential back-off for transient server-side
errors (5xx), distinguishing retryable from non-retryable failures.

.. mermaid::

   flowchart TD
     A(["API call initiated"]) --> B["Send HTTP request\nAttempt = 1"]
     B --> C{"HTTP\nstatus?"}
     C -- 2xx --> SUCCESS(["Return response"])
     C -- 4xx --> NON_RETRY(["Raise typed exception\nNo retry"])
     C -- 429 --> RATE["Read Retry-After header"]
     RATE --> WAIT_RATE["Sleep(Retry-After seconds)"]
     WAIT_RATE --> INCR
     C -- 5xx --> CHECK{"Attempt\n≤ max_retries?"}
     CHECK -- No --> EXHAUST(["Raise RedcoreAPIError\nMax retries exceeded"])
     CHECK -- Yes --> BACKOFF["Sleep(2^attempt seconds)\nJitter ±10 %"]
     BACKOFF --> INCR["Attempt += 1"]
     INCR --> B

.. list-table:: Retry behaviour by status code
   :header-rows: 1
   :widths: 15 20 30 35

   * - Status
     - Retryable?
     - Wait strategy
     - Notes
   * - ``2xx``
     - N/A
     - None
     - Success — return immediately.
   * - ``400``
     - No
     - None
     - Fix the request payload before retrying.
   * - ``401``
     - Yes (once)
     - Token refresh
     - SDK attempts silent token refresh first.
   * - ``403``
     - No
     - None
     - Scope issue — requires credential change.
   * - ``404``
     - No
     - None
     - Resource does not exist.
   * - ``429``
     - Yes
     - ``Retry-After`` header
     - Respect the exact wait time from the server.
   * - ``5xx``
     - Yes (up to 3)
     - Exponential + jitter
     - 1 s → 2 s → 4 s with ±10 % random jitter.

----

User Onboarding Workflow
------------------------

End-to-end flow from invitation creation by an admin to the new user
completing setup and gaining access.

.. mermaid::

   flowchart TD
     A(["Admin: POST /users"]) --> B{"Email already\nregistered?"}
     B -- Yes --> DUP(["Return 409 DUPLICATE_RESOURCE"])
     B -- No --> C["Create user record\nstatus = pending_invite"]
     C --> D["Enqueue invitation email"]
     D --> E["Email sent with\ntime-limited signup link\n(expires in 48 h)"]
     E --> F{"User clicks\nlink within 48 h?"}
     F -- No --> G["Link expires"]
     G --> H{"Admin resends\ninvitation?"}
     H -- Yes --> D
     H -- No --> CANCEL(["User remains pending_invite"])
     F -- Yes --> I["User sets password\n+ optional MFA setup"]
     I --> J["status → active"]
     J --> K(["User can now authenticate\nand access the API"])

.. list-table:: Onboarding states
   :header-rows: 1
   :widths: 28 72

   * - Status value
     - Meaning
   * - ``pending_invite``
     - User record created; invitation email sent or queued.
   * - ``active``
     - User completed signup; can authenticate.
   * - ``inactive``
     - Admin-disabled account; all tokens revoked.

----

Docs-as-Code CI/CD Pipeline
-----------------------------

The automated pipeline that builds, validates, and publishes documentation
on every push to the ``main`` branch via GitHub Actions.

.. mermaid::

   flowchart TD
     A(["git push → main"]) --> B["GitHub Actions triggered"]
     B --> C["Checkout repo\nSet up Python 3.12"]
     C --> D["pip install -r requirements.txt"]
     D --> E["sphinx-build -W -b html\nsource/ build/html"]
     E --> F{"Build\nsuccessful?"}
     F -- No --> FAIL(["❌ Workflow fails\nAuthor notified by email"])
     F -- Yes --> G["sphinx-build -b linkcheck\nsource/ build/linkcheck"]
     G --> H{"Broken\nlinks found?"}
     H -- Yes --> FAIL
     H -- No --> I["Upload build artifact\nbuild/html/"]
     I --> J{"Branch =\nmain?"}
     J -- No --> PREVIEW(["📦 Preview artifact\navailable for 7 days"])
     J -- Yes --> DEPLOY["Deploy to GitHub Pages\npeaciris/actions-gh-pages@v4"]
     DEPLOY --> K(["✅ Docs live at\ndocs.blueround.com"])

.. list-table:: CI/CD stage reference
   :header-rows: 1
   :widths: 25 30 45

   * - Stage
     - Command / Action
     - Fails on
   * - Install
     - ``pip install -r requirements.txt``
     - Missing package or version conflict.
   * - Build
     - ``sphinx-build -W -b html``
     - Any Sphinx warning (``-W`` = warnings as errors).
   * - Link check
     - ``sphinx-build -b linkcheck``
     - Any external URL returning non-2xx.
   * - Deploy
     - ``peaceiris/actions-gh-pages@v4``
     - GitHub API error or permission issue.

----

Rate Limit Handling
-------------------

Decision logic for a client that respects the ``X-RateLimit-*`` headers
and backs off gracefully before hitting a hard ``429``.

.. mermaid::

   flowchart TD
     A(["Prepare API request"]) --> B["Read X-RateLimit-Remaining\nfrom last response"]
     B --> C{"Remaining\n= 0?"}
     C -- No --> D["Send request"]
     C -- Yes --> E["Read X-RateLimit-Reset\n(Unix timestamp)"]
     E --> F["Calculate sleep =\nReset - now() + 0.1 s"]
     F --> G["Sleep(sleep seconds)"]
     G --> D
     D --> H{"Response\nstatus?"}
     H -- 429 --> I["Read Retry-After header"]
     I --> J["Sleep(Retry-After seconds)"]
     J --> D
     H -- 2xx --> K(["Process response"])
     H -- other --> ERR(["Handle error per\nError Retry flowchart"])

.. note::
   Proactive rate-limit checking (the left branch) prevents ever receiving
   a ``429``. The ``429`` branch is a safety net for edge cases such as
   clock skew or concurrent workers sharing the same API key.

----

SDK Initialization
------------------

Step-by-step initialization sequence from application startup to the
first successful API call, including environment validation.

.. mermaid::

   flowchart TD
     A(["Application starts"]) --> B["Load environment variables\n(REDCORE_API_KEY, etc.)"]
     B --> C{"Required vars\npresent?"}
     C -- No --> ENV_ERR(["Raise ConfigurationError:\nMissing REDCORE_API_KEY"])
     C -- Yes --> D["Instantiate SDK Client\nClient(api_key=..., timeout=...)"]
     D --> E{"base_url\noverridden?"}
     E -- Yes --> F["Validate URL format\n(must be HTTPS)"]
     F --> G{"Valid?"}
     G -- No --> URL_ERR(["Raise ConfigurationError:\nInvalid base_url"])
     G -- Yes --> H["Client ready"]
     E -- No --> H
     H --> I["First API call triggered"]
     I --> J["GET /v1/me (implicit health-check)"]
     J --> K{"HTTP 200?"}
     K -- Yes --> READY(["✅ SDK fully initialized"])
     K -- No --> INIT_ERR(["Raise AuthenticationError\nor RedcoreAPIError"])

.. seealso::

   * :doc:`architecture` — System components and deployment topology.
   * :doc:`/sdk/authentication` — Auth method decision guide.
   * :doc:`/api/errors` — Error code catalogue referenced in retry flows.
