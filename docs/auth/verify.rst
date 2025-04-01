Verify Email
===========

.. http:get:: /verify/{token}

   Verify user's email address.

   :param token: Verification token from email

   :status 200: Email verified successfully
   :status 400: Invalid token
   :status 404: User not found

   **Example Request:**
   .. code-block:: http
      GET /verify/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...

   **Example Response:**
   .. code-block:: json
      {
         "message": "Email verified successfully"
      } 