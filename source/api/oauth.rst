.. _api-oauth:

OAuth 2.0 Authentication
=========================

The BlueRound API uses **OAuth 2.0** for all authorization.
Every request must supply a valid Bearer token in the ``Authorization`` header.
Tokens are issued by the BlueRound Authorization Server and scoped to exactly
the resources your application needs.

.. code-block:: http

   GET /v1/users HTTP/1.1
   Host: api.blueround.com
   Authorization: Bearer eyJhbGciOiJSUzI1NiIs...

----

.. contents:: On This Page
   :depth: 2
   :local:
   :backlinks: none

----

Quick-Start Flow
----------------

.. mermaid::

   sequenceDiagram
     participant App   as Your Application
     participant Auth  as BlueRound Auth Server
     participant API   as BlueRound API

     App->>Auth: POST /oauth/token (client_id + client_secret)
     Auth-->>App: { access_token, refresh_token, expires_in }
     App->>API:  GET /v1/users  (Authorization: Bearer <access_token>)
     API-->>App: 200 OK — user list
     Note over App,Auth: When access_token expires (3 600 s) …
     App->>Auth: POST /oauth/token (grant_type=refresh_token)
     Auth-->>App: { new access_token, new refresh_token }

Registering Your Application
-----------------------------

Before requesting tokens, register your application in the
`Developer Dashboard <https://developer.blueround.com>`_ to receive:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Credential
     - Description
   * - ``client_id``
     - Public identifier for your application. Safe to embed in client-side code.
   * - ``client_secret``
     - Private credential used to authenticate your application server-side.

.. warning::
   Your ``client_secret`` is **private**. Never embed it in mobile apps,
   browser JavaScript, or public repositories. Rotate it immediately if exposed.

Grant Types
-----------

BlueRound supports two OAuth 2.0 grant types.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Grant Type
     - Recommended for
   * - **Authorization Code** (+ PKCE)
     - Web apps and mobile apps that act on behalf of an end-user.
   * - **Client Credentials**
     - Backend services and machine-to-machine communication (no user context).

Client Credentials Grant
~~~~~~~~~~~~~~~~~~~~~~~~

The simplest flow for server-side integrations. Exchange your
``client_id`` and ``client_secret`` for an access token directly.

**Request:**

.. code-block:: bash
   :caption: POST /oauth/token — client credentials

   curl -X POST "https://auth.blueround.com/oauth/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "grant_type=client_credentials" \
     -d "client_id=YOUR_CLIENT_ID" \
     -d "client_secret=YOUR_CLIENT_SECRET" \
     -d "scope=users:read users:write"

**Response:**

.. code-block:: json

   {
     "access_token":  "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
     "token_type":    "Bearer",
     "expires_in":    3600,
     "refresh_token": "def50200a9f3...",
     "scope":         "users:read users:write"
   }

.. list-table:: Token response fields
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Description
   * - ``access_token``
     - JWT to include in every API request.
   * - ``token_type``
     - Always ``Bearer``.
   * - ``expires_in``
     - Seconds until the access token expires (3 600 = 1 hour).
   * - ``refresh_token``
     - Long-lived token used to obtain a new access token. Valid for 30 days.
   * - ``scope``
     - Space-separated list of granted scopes.

Authorization Code Grant (+ PKCE)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For user-facing applications. The user is redirected to BlueRound's login
page, consents, and is returned to your app with an authorization code that
you exchange for tokens.

.. important::
   Always use **PKCE** (Proof Key for Code Exchange, :rfc:`7636`) with the
   Authorization Code grant — even for confidential clients — to protect
   against authorization code interception attacks.

**Step 1 — Redirect the user:**

.. code-block:: text

   https://auth.blueround.com/oauth/authorize
     ?response_type=code
     &client_id=YOUR_CLIENT_ID
     &redirect_uri=https://yourapp.com/callback
     &scope=users:read%20profile:read
     &state=RANDOM_STATE_VALUE
     &code_challenge=CODE_CHALLENGE
     &code_challenge_method=S256

**Step 2 — Exchange the code:**

.. code-block:: bash
   :caption: POST /oauth/token — authorization code exchange

   curl -X POST "https://auth.blueround.com/oauth/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "grant_type=authorization_code" \
     -d "code=AUTHORIZATION_CODE" \
     -d "redirect_uri=https://yourapp.com/callback" \
     -d "client_id=YOUR_CLIENT_ID" \
     -d "code_verifier=CODE_VERIFIER"

Scopes
------

Request only the scopes your application genuinely needs. Tokens with
unnecessary scopes increase the risk if they are compromised.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Scope
     - Grants access to
   * - ``users:read``
     - List and retrieve user profiles.
   * - ``users:write``
     - Create, update, and deactivate user accounts.
   * - ``profile:read``
     - Read the authenticated user's own profile data.
   * - ``profile:write``
     - Update the authenticated user's own profile data.
   * - ``admin``
     - Full administrative access. Requires explicit approval from BlueRound.

.. tip::
   Combine scopes as a space-separated string in the ``scope`` parameter:
   ``scope=users:read profile:read``.

Refreshing an Access Token
--------------------------

When an access token expires, use the refresh token to obtain a new pair
without requiring the user to re-authenticate.

.. code-block:: bash
   :caption: POST /oauth/token — refresh token grant

   curl -X POST "https://auth.blueround.com/oauth/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "grant_type=refresh_token" \
     -d "refresh_token=def50200a9f3..." \
     -d "client_id=YOUR_CLIENT_ID" \
     -d "client_secret=YOUR_CLIENT_SECRET"

The server responds with a **new** ``access_token`` and a rotated
``refresh_token``. Discard the old tokens immediately after a successful
refresh — they are single-use.

.. warning::
   Refresh tokens expire after **30 days** of inactivity. If a refresh
   token has expired, the user must re-authenticate from scratch.

Token Expiration Summary
------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 35 30

   * - Token Type
     - TTL
     - Rotation
   * - Access Token
     - 3 600 s (1 hour)
     - Issued on every ``/oauth/token`` call.
   * - Refresh Token
     - 30 days (sliding)
     - Rotated on every refresh — old token is invalidated.

Revoking a Token
----------------

Revoke an access or refresh token immediately — for example, on user
log-out or after a security incident.

.. http:post:: /oauth/revoke

   Revoke an active access or refresh token.

   :reqheader Content-Type: ``application/x-www-form-urlencoded``
   :form token: The token string to revoke.
   :form token_type_hint: Optional. ``access_token`` or ``refresh_token``.
   :form client_id: Your application's ``client_id``.
   :form client_secret: Your application's ``client_secret``.
   :status 200: Token revoked (or was already invalid). Body is empty.
   :status 401: Invalid ``client_id`` or ``client_secret``.

.. code-block:: bash
   :caption: Revoking a token

   curl -X POST "https://auth.blueround.com/oauth/revoke" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "token=def50200a9f3..." \
     -d "token_type_hint=refresh_token" \
     -d "client_id=YOUR_CLIENT_ID" \
     -d "client_secret=YOUR_CLIENT_SECRET"

.. note::
   Revoking a refresh token also invalidates all access tokens derived from it.

.. seealso::

   * :doc:`about` — Request format and base URLs.
   * :doc:`errors` — Error codes including ``INVALID_TOKEN`` and ``TOKEN_EXPIRED``.
   * :rfc:`6749` — The OAuth 2.0 Authorization Framework.
   * :rfc:`7636` — Proof Key for Code Exchange (PKCE).
