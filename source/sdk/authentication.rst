.. _authentication:

Authentication
==============

.. meta::
   :description: Learn how to authenticate with the RedCore SDK using OAuth2 and SAML.
   :keywords: authentication, oauth, saml, security

The RedCore SDK supports several authentication methods to ensure your data remains secure. 

Available Methods
-----------------

.. list-table:: 
   :widths: 25 25 50
   :header-rows: 1

   * - Method
     - Security Level
     - Recommended For
   * - **API Key**
     - Medium
     - Server-to-server communication
   * - **OAuth2**
     - High
     - User-facing applications
   * - **SAML**
     - Enterprise
     - Corporate single sign-on (SSO)

OAuth2 Flow
-----------

To use OAuth2, you must first register your application in the developer portal.

.. hint::
   We recommend using the Authorization Code Flow for mobile and web apps.

1. **Authorize**: Redirect the user to the authorization URL.
2. **Exchange**: Swap the code for an access token.
3. **Refresh**: Use the refresh token to maintain the session.

.. warning::
   Access tokens expire every 60 minutes. Your application must handle token refreshing automatically.

Code Example
~~~~~~~~~~~~

.. code-block:: python
   :caption: Initializing with OAuth2

   from redcore import Client

   client = Client(
       client_id="YOUR_ID",
       client_secret="YOUR_SECRET",
       token="ACCESS_TOKEN"
   )

