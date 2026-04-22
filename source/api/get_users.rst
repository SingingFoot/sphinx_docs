Get Users
=========

This endpoint allows you to retrieve a list of users or a specific user profile.

.. http:get:: /users

   Returns a paginated list of all users in your organization.

   :query limit: Number of results per page (default: 20, max: 100).
   :query offset: Number of results to skip.
   :status 200: A JSON array of user objects.
   :status 401: Unauthorized access.

Example Request
---------------

.. code-block:: bash

   curl -X GET "https://api.blueround.com/v1/users?limit=5" \
        -H "Authorization: Bearer YOUR_TOKEN"

Response Body
-------------

The response is a JSON object containing a ``data`` array.

.. code-block:: json

   {
     "data": [
       {
         "id": "usr_98765",
         "name": "Oleg Shinkarenko",
         "email": "oleg@example.com",
         "status": "active"
       }
     ],
     "total": 1250
   }

.. tip::
   Use the ``id`` from the response to perform actions on a specific user via ``/users/{id}``.
