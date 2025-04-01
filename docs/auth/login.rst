Login User
==========

.. http:post:: /api/auth/login

   Login user with email and password.

   **Request Body**

   .. code-block:: json

      {
         "email": "user@example.com",
         "password": "string"
      }

   **Response**

   .. code-block:: json

      {
         "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
         "token_type": "bearer"
      }

   :statuscode 200: Successfully logged in
   :statuscode 401: Invalid credentials
   :statuscode 422: Validation Error 