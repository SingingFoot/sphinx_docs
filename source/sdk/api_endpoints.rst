.. _api_endpoints:

API Endpoints Reference
=======================

The RedCore SDK exposes every REST endpoint as a typed Python/Node.js/Go method.
This page documents each endpoint with its full request parameters, response
schema, and status codes. All request and response bodies use **JSON**.

.. note::
   Rate limit: **1 000 requests per minute** per API key.
   Exceeding this returns :http:statuscode:`429`. See :doc:`/api/errors`
   for the ``RATE_LIMIT_EXCEEDED`` error and retry guidance.

----

.. contents:: On This Page
   :depth: 2
   :local:
   :backlinks: none

----

User Management
---------------

User Object
~~~~~~~~~~~

All user endpoints share the same **User** response schema:

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Field
     - Type
     - Description
   * - ``id``
     - ``string``
     - Unique resource identifier (prefix: ``usr_``).
   * - ``email``
     - ``string``
     - Primary email address. Unique per organization.
   * - ``name``
     - ``string``
     - Full display name.
   * - ``role``
     - ``string``
     - One of ``admin``, ``editor``, or ``viewer``.
   * - ``status``
     - ``string``
     - One of ``active``, ``inactive``, or ``pending_invite``.
   * - ``created_at``
     - ``string (ISO 8601)``
     - Timestamp when the record was created.
   * - ``updated_at``
     - ``string (ISO 8601)``
     - Timestamp of the most recent change.

List Users
~~~~~~~~~~

.. http:get:: /users

   Returns a paginated list of all users in the authenticated organization,
   ordered by ``created_at`` descending.

   :reqheader Authorization: ``Bearer <access_token>`` — required.
   :reqheader Accept: ``application/json``

   :query limit: Maximum results per page. Default ``20``, max ``100``.
   :query offset: Results to skip. Default ``0``.
   :query role: Filter by role: ``admin``, ``editor``, or ``viewer``.
   :query status: Filter by status: ``active``, ``inactive``, or ``pending_invite``.
   :query q: Partial-match search across ``name`` and ``email``.

   :status 200: Paginated array of User objects.
   :status 401: Missing or expired token.
   :status 403: Token lacks the ``users:read`` scope.
   :status 429: Rate limit exceeded.

**Example request:**

.. code-block:: bash
   :caption: List active admin users

   curl -X GET "https://api.redcore.com/v1/users?role=admin&status=active&limit=10" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Accept: application/json"

**Example response** (``200 OK``):

.. code-block:: json
   :caption: GET /v1/users — response body

   {
     "data": [
       {
         "id":         "usr_98765",
         "email":      "alice@example.com",
         "name":       "Alice Müller",
         "role":       "admin",
         "status":     "active",
         "created_at": "2025-11-15T08:30:00Z",
         "updated_at": "2026-04-01T14:22:00Z"
       }
     ],
     "meta": { "total": 42, "limit": 10, "offset": 0 }
   }

**SDK usage:**

.. code-block:: python
   :caption: Python — list all users with automatic pagination

   for page in client.users.list_all(status="active", page_size=50):
       for user in page:
           print(user.id, user.email)

Retrieve a User
~~~~~~~~~~~~~~~

.. http:get:: /users/(string:user_id)

   Retrieve a single user record by unique identifier.

   :param user_id: The ``usr_``-prefixed user ID.

   :reqheader Authorization: ``Bearer <access_token>`` — required.

   :status 200: Single User object.
   :status 401: Missing or expired token.
   :status 403: Token lacks the ``users:read`` scope.
   :status 404: User not found.

**Example request:**

.. code-block:: bash
   :caption: Retrieve user usr_98765

   curl -X GET "https://api.redcore.com/v1/users/usr_98765" \
     -H "Authorization: Bearer YOUR_TOKEN"

**SDK usage:**

.. code-block:: python
   :caption: Python

   from redcore.exceptions import NotFoundError

   try:
       user = client.users.get("usr_98765")
       print(user.name, user.role)
   except NotFoundError:
       print("User does not exist.")

Create a User
~~~~~~~~~~~~~

.. http:post:: /users

   Create a new user in the organization. Sends an invitation email to the
   supplied address.

   :reqheader Authorization: ``Bearer <access_token>`` — required.
   :reqheader Content-Type: ``application/json``

   :jsonparam string email: *Required.* Email address of the new user.
   :jsonparam string name: *Required.* Full display name.
   :jsonparam string role: *Required.* One of ``admin``, ``editor``, ``viewer``.

   :status 201: User created. ``Location`` header points to the new resource.
   :status 400: Missing or invalid fields — see ``details`` array.
   :status 401: Missing or expired token.
   :status 403: Token lacks the ``users:write`` scope.
   :status 409: A user with that email already exists.

**Example request:**

.. code-block:: bash
   :caption: Create a new editor user

   curl -X POST "https://api.redcore.com/v1/users" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"email": "bob@example.com", "name": "Bob Smith", "role": "editor"}'

**SDK usage:**

.. code-block:: python
   :caption: Python

   from redcore.exceptions import ValidationError, DuplicateError

   try:
       new_user = client.users.create(
           email="bob@example.com",
           name="Bob Smith",
           role="editor",
       )
       print(f"Invited: {new_user.id}")
   except ValidationError as exc:
       for detail in exc.details:
           print(detail["field"], detail["issue"])
   except DuplicateError:
       print("A user with this email already exists.")

Update a User
~~~~~~~~~~~~~

.. http:patch:: /users/(string:user_id)

   Partially update a user record. Only the supplied fields are modified;
   omitted fields remain unchanged.

   :param user_id: The ``usr_``-prefixed user ID.

   :reqheader Authorization: ``Bearer <access_token>`` — required.
   :reqheader Content-Type: ``application/json``

   :jsonparam string name: New display name.
   :jsonparam string role: New role: ``admin``, ``editor``, or ``viewer``.
   :jsonparam string status: New status: ``active`` or ``inactive``.

   :status 200: Updated User object.
   :status 400: Invalid field value.
   :status 401: Missing or expired token.
   :status 403: Token lacks the ``users:write`` scope.
   :status 404: User not found.

**Example request:**

.. code-block:: bash
   :caption: Promote a user to admin

   curl -X PATCH "https://api.redcore.com/v1/users/usr_98765" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"role": "admin"}'

**SDK usage:**

.. code-block:: python
   :caption: Python

   updated = client.users.update("usr_98765", role="admin")
   print(updated.role)   # → "admin"

Delete a User
~~~~~~~~~~~~~

.. http:delete:: /users/(string:user_id)

   Permanently deactivate and remove a user from the organization.
   This action is **irreversible**.

   :param user_id: The ``usr_``-prefixed user ID.

   :reqheader Authorization: ``Bearer <access_token>`` — required.

   :status 204: User deleted. No response body.
   :status 401: Missing or expired token.
   :status 403: Token lacks the ``users:write`` scope.
   :status 404: User not found.

.. danger::
   Deleting a user immediately revokes all their active sessions and tokens.
   Any resources exclusively owned by the user must be reassigned beforehand
   to avoid data loss.

**Example request:**

.. code-block:: bash
   :caption: Delete user usr_98765

   curl -X DELETE "https://api.redcore.com/v1/users/usr_98765" \
     -H "Authorization: Bearer YOUR_TOKEN"

**SDK usage:**

.. code-block:: python
   :caption: Python

   client.users.delete("usr_98765")   # raises NotFoundError if missing

----

Product Catalog
---------------

Product Object
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Field
     - Type
     - Description
   * - ``id``
     - ``string``
     - Unique resource identifier (prefix: ``prod_``).
   * - ``name``
     - ``string``
     - Human-readable product name.
   * - ``sku``
     - ``string``
     - Stock-keeping unit. Unique per catalog.
   * - ``price``
     - ``number``
     - Unit price in the organization's base currency (e.g., USD cents).
   * - ``stock``
     - ``integer``
     - Units currently available.
   * - ``status``
     - ``string``
     - One of ``available``, ``out_of_stock``, or ``discontinued``.
   * - ``created_at``
     - ``string (ISO 8601)``
     - Timestamp when the product was added to the catalog.

List Products
~~~~~~~~~~~~~

.. http:get:: /products

   Returns a paginated list of products in the catalog.

   :reqheader Authorization: ``Bearer <access_token>`` — required.

   :query limit: Max results per page. Default ``20``, max ``100``.
   :query offset: Results to skip. Default ``0``.
   :query status: Filter by status: ``available``, ``out_of_stock``, ``discontinued``.
   :query q: Full-text search across ``name`` and ``sku``.

   :status 200: Paginated array of Product objects.
   :status 401: Missing or expired token.
   :status 403: Token lacks the ``products:read`` scope.
   :status 429: Rate limit exceeded.

**Example request:**

.. code-block:: bash
   :caption: Fetch the first 5 available products

   curl -X GET "https://api.redcore.com/v1/products?status=available&limit=5" \
     -H "Authorization: Bearer YOUR_TOKEN"

**Example response** (``200 OK``):

.. code-block:: json
   :caption: GET /v1/products — response body

   {
     "data": [
       {
         "id":         "prod_00123",
         "name":       "Titanium Widget Pro",
         "sku":        "TWP-001",
         "price":      4999,
         "stock":      250,
         "status":     "available",
         "created_at": "2026-01-10T12:00:00Z"
       }
     ],
     "meta": { "total": 87, "limit": 5, "offset": 0 }
   }

Retrieve a Product
~~~~~~~~~~~~~~~~~~

.. http:get:: /products/(string:product_id)

   Retrieve a single product by its unique identifier.

   :param product_id: The ``prod_``-prefixed product ID.

   :reqheader Authorization: ``Bearer <access_token>`` — required.

   :status 200: Single Product object.
   :status 401: Missing or expired token.
   :status 404: Product not found.

**Example request:**

.. code-block:: bash
   :caption: Retrieve product prod_00123

   curl -X GET "https://api.redcore.com/v1/products/prod_00123" \
     -H "Authorization: Bearer YOUR_TOKEN"

**SDK usage:**

.. code-block:: python
   :caption: Python

   product = client.products.get("prod_00123")
   print(f"{product.name} — ${product.price / 100:.2f}")

----

Pagination
----------

All list endpoints use **offset-based pagination**. The ``meta`` block
in every response provides the values you need to walk through pages:

.. code-block:: python
   :caption: Python — generic paginator helper

   def iter_pages(list_fn, **kwargs):
       """Yield individual items from any SDK list method."""
       limit, offset = kwargs.pop("limit", 100), 0
       while True:
           page = list_fn(limit=limit, offset=offset, **kwargs)
           yield from page["data"]
           if offset + limit >= page["meta"]["total"]:
               break
           offset += limit

   # Usage
   for user in iter_pages(client.users.list, status="active"):
       print(user["email"])

.. seealso::

   * :doc:`getting_started` — Installing and initializing the SDK.
   * :doc:`authentication` — Choosing and configuring an auth method.
   * :doc:`/api/get_users` — REST-level Users endpoint documentation.
   * :doc:`/api/errors` — Error codes and retry strategies.
