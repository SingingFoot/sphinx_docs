.. _api_endpoints:

API Endpoints Reference
=======================

Our API is organized around **REST**. All request and response bodies use the ``JSON`` format.

User Management
---------------

.. http:get:: /users/{id}

   Retrieves the details of an existing user.

   :param id: The unique identifier of the user.
   :type id: string
   :status 200: Successfully retrieved.
   :status 404: User not found.

   **Request Example**:

   .. code-block:: bash

      curl -X GET "https://api.redcore.com/v1/users/123" \
           -H "Authorization: Bearer YOUR_TOKEN"

   **Response Structure**:

   id
       *(string)* Unique identifier for the object.
   email
       *(string)* The user's primary email address.
   role
       *(string)* Can be ``admin``, ``editor``, or ``viewer``.

Product Catalog
---------------

.. note::
   Rate limits apply: **1000 requests per minute** per API key.

.. error::
   Exceeding the rate limit will result in a ``429 Too Many Requests`` error.

.. seealso::
   For more advanced queries, check our :doc:`/api/get_users` detailed guide.
