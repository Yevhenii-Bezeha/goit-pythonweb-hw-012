Register User
=============

.. http:post:: /api/auth/register

   Register a new user.

   **Request Body**

   .. code-block:: json

      {
         "email": "user@example.com",
         "password": "string"
      }

   **Response**

   .. code-block:: json

      {
         "email": "user@example.com",
         "id": 1,
         "is_active": true,
         "is_verified": false,
         "created_at": "2024-03-20T10:00:00",
         "updated_at": "2024-03-20T10:00:00"
      }

   :statuscode 201: User successfully created
   :statuscode 400: Email already registered
   :statuscode 422: Validation Error 