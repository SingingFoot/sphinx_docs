.. _authentication:

Authentication
==============

.. meta::
   :description: Learn how to authenticate with the RedCore SDK using API Key, OAuth 2.0, and SAML.
   :keywords: authentication, oauth2, saml, api key, token refresh, security

The RedCore SDK supports three authentication methods. Choose the one that
matches your application architecture and security requirements.

----

.. contents:: On This Page
   :depth: 2
   :local:
   :backlinks: none

----

Method Comparison
-----------------

.. list-table::
   :header-rows: 1
   :widths: 20 18 18 44

   * - Method
     - Security Level
     - Complexity
     - Recommended For
   * - **API Key**
     - Medium
     - Low
     - Server-to-server integrations, scripts, CI/CD pipelines.
   * - **OAuth 2.0**
     - High
     - Medium
     - Web apps and mobile apps acting on behalf of an end user.
   * - **SAML 2.0**
     - Enterprise
     - High
     - Corporate SSO environments (Okta, Azure AD, Google Workspace).

.. important::
   Store all credentials — API keys, client secrets, SAML private keys —
   in environment variables or a dedicated secrets manager. Never commit
   them to source control.

----

API Key Authentication
----------------------

API keys are long-lived static credentials scoped to your RedCore project.
They are the simplest authentication method and are recommended for
**backend services** that do not operate on behalf of individual users.

Obtaining an API Key
~~~~~~~~~~~~~~~~~~~~

1. Log in to the `RedCore Dashboard <https://dashboard.redcore.com>`_.
2. Navigate to **Settings → API Keys**.
3. Click **Generate New Key**, choose a descriptive name, and select the
   required scopes.
4. Copy the key immediately — it is shown **only once**.

.. warning::
   API keys cannot be recovered after creation. If lost, revoke the old
   key and generate a new one. See :ref:`key-rotation` for the safe rotation
   procedure.

Using an API Key
~~~~~~~~~~~~~~~~

.. code-block:: python
   :caption: Python — API key initialization

   import os
   from redcore import Client

   client = Client(api_key=os.environ["REDCORE_API_KEY"])

.. code-block:: javascript
   :caption: Node.js — API key initialization

   const { RedcoreClient } = require("@redcore/sdk");

   const client = new RedcoreClient({
     apiKey: process.env.REDCORE_API_KEY,
   });

.. code-block:: bash
   :caption: cURL — API key in the Authorization header

   curl -X GET "https://api.redcore.com/v1/users" \
     -H "Authorization: Bearer $REDCORE_API_KEY" \
     -H "Accept: application/json"

.. _key-rotation:

API Key Rotation
~~~~~~~~~~~~~~~~

Rotate keys periodically (recommended: every 90 days) and immediately
after any suspected exposure.

.. code-block:: bash
   :caption: Safe zero-downtime key rotation

   # 1. Generate the new key in the Dashboard and set it in the new env var
   export REDCORE_API_KEY_NEW=rk_live_newkey...

   # 2. Deploy the new key to your application (rolling deploy / blue-green)
   # 3. Confirm all traffic is using the new key (check logs / metrics)
   # 4. Revoke the old key in the Dashboard

.. note::
   Both the old and new key are valid simultaneously during the rotation
   window, so there is no service interruption.

----

OAuth 2.0 Authentication
------------------------

OAuth 2.0 is required when your application acts on behalf of an end user
and needs to access resources scoped to that user's account.

.. hint::
   Use the **Authorization Code + PKCE** flow for web and mobile apps.
   Use **Client Credentials** for pure machine-to-machine communication.

OAuth 2.0 Flow Diagram
~~~~~~~~~~~~~~~~~~~~~~

.. mermaid::

   sequenceDiagram
     participant User   as End User
     participant App    as Your App
     participant Auth   as RedCore Auth Server
     participant API    as RedCore API

     User->>App:  Click "Connect with RedCore"
     App->>Auth:  Redirect → /oauth/authorize?client_id=...&code_challenge=...
     Auth->>User: Show consent screen
     User->>Auth: Grant permission
     Auth->>App:  Redirect → /callback?code=AUTH_CODE
     App->>Auth:  POST /oauth/token (code + code_verifier)
     Auth-->>App: { access_token, refresh_token, expires_in: 3600 }
     App->>API:   GET /v1/users  (Authorization: Bearer access_token)
     API-->>App:  200 OK — user data
     Note over App,Auth: After 3 600 s the access_token expires…
     App->>Auth:  POST /oauth/token (grant_type=refresh_token)
     Auth-->>App: { new access_token, new refresh_token }

Step 1 — Register Your Application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Register at `developer.redcore.com <https://developer.redcore.com>`_ to
obtain your ``client_id`` and ``client_secret``, and to configure your
allowed redirect URIs.

Step 2 — Initialize the Client
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python
   :caption: Python — OAuth 2.0 initialization

   import os
   from redcore import Client

   client = Client(
       client_id=os.environ["REDCORE_CLIENT_ID"],
       client_secret=os.environ["REDCORE_CLIENT_SECRET"],
   )
   # The SDK automatically requests and caches a token on the first API call.

.. code-block:: javascript
   :caption: Node.js — OAuth 2.0 initialization

   const { RedcoreClient } = require("@redcore/sdk");

   const client = new RedcoreClient({
     clientId:     process.env.REDCORE_CLIENT_ID,
     clientSecret: process.env.REDCORE_CLIENT_SECRET,
   });

Step 3 — Handle Token Refresh
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The SDK refreshes the access token automatically before it expires.
If you need to persist tokens across restarts (e.g., in a long-running
server), implement the ``on_token_refreshed`` callback to save the new
tokens to your storage layer.

.. code-block:: python
   :caption: Python — persisting refreshed tokens

   import json, os
   from redcore import Client

   def save_tokens(token_data: dict) -> None:
       """Callback invoked whenever the SDK refreshes a token pair."""
       with open(".tokens.json", "w") as f:
           json.dump(token_data, f)

   # Load previously persisted tokens (if any)
   stored = {}
   if os.path.exists(".tokens.json"):
       with open(".tokens.json") as f:
           stored = json.load(f)

   client = Client(
       client_id=os.environ["REDCORE_CLIENT_ID"],
       client_secret=os.environ["REDCORE_CLIENT_SECRET"],
       access_token=stored.get("access_token"),
       refresh_token=stored.get("refresh_token"),
       on_token_refreshed=save_tokens,
   )

.. warning::
   Access tokens expire after **60 minutes**. Refresh tokens expire after
   **30 days** of inactivity. If the refresh token expires, the user must
   re-authenticate from scratch.

Token Lifetimes
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 35 30

   * - Token Type
     - TTL
     - Rotation
   * - Access Token
     - 3 600 s (1 hour)
     - Issued on every token request.
   * - Refresh Token
     - 30 days (sliding)
     - Rotated on every refresh — old token is immediately invalidated.

----

SAML 2.0 Authentication
-----------------------

SAML 2.0 enables your organization's Identity Provider (IdP) — such as
Okta, Azure Active Directory, or Google Workspace — to act as the
authority for user authentication. RedCore acts as the **Service Provider (SP)**.

.. note::
   SAML is available on **Enterprise plans** only. Contact
   `enterprise@redcore.com <mailto:enterprise@redcore.com>`_ to enable it
   for your organization.

SAML Flow Overview
~~~~~~~~~~~~~~~~~~

.. mermaid::

   sequenceDiagram
     participant User as End User
     participant SP   as RedCore (Service Provider)
     participant IdP  as Your IdP (Okta / Azure AD)

     User->>SP:  Access protected resource
     SP->>User:  Redirect → IdP login page
     User->>IdP: Authenticate (username + password / MFA)
     IdP->>SP:   POST SAMLResponse (signed XML assertion)
     SP->>SP:    Validate signature & extract attributes
     SP->>User:  Issue session / access token

Configuration
~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Setting
     - Description
   * - **SP Entity ID**
     - ``https://auth.redcore.com/saml/metadata``
   * - **ACS URL**
     - ``https://auth.redcore.com/saml/acs``
   * - **Metadata URL**
     - ``https://auth.redcore.com/saml/metadata.xml``
   * - **NameID format**
     - ``urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress``
   * - **Signature algorithm**
     - RSA-SHA256

Provide these values to your IdP administrator when setting up the
RedCore application in your IdP's dashboard.

.. code-block:: python
   :caption: Python — SAML initialization using an IdP-issued assertion

   from redcore import Client

   # Exchange a SAML assertion for a RedCore access token
   client = Client.from_saml_assertion(
       assertion=idp_saml_response_xml,   # raw XML string from IdP POST
       client_id=os.environ["REDCORE_CLIENT_ID"],
   )

----

Authentication Errors
---------------------

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Error / Status Code
     - Meaning and fix
   * - ``401 INVALID_TOKEN``
     - Token is malformed or does not exist. Re-acquire a fresh token.
   * - ``401 TOKEN_EXPIRED``
     - Access token has passed its TTL. The SDK retries with the refresh
       token automatically; if this still fails, re-authenticate.
   * - ``403 INSUFFICIENT_SCOPE``
     - Token lacks the required scope. Request a token with the missing
       scope(s) added.
   * - ``AuthenticationError`` (SDK)
     - Raised when the server returns 401. Inspect ``exc.code`` for the
       specific error code.
   * - ``PermissionError`` (SDK)
     - Raised when the server returns 403.

.. seealso::

   * :doc:`getting_started` — Installing the SDK and initializing the client.
   * :doc:`api_endpoints` — Full method reference.
   * :doc:`/api/oauth` — REST-level OAuth 2.0 token endpoints.
   * :doc:`/api/errors` — Complete error code catalogue.
