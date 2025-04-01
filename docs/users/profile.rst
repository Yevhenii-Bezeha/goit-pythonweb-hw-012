User Profile
===========

.. http:get:: /users/me

   Get current user's profile.

   :header Authorization: Bearer {token}

   :status 200: Success
   :status 401: Not authenticated

   **Example Request:**
   .. code-block:: http
      GET /users/me
      Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...

   **Example Response:**
   .. code-block:: json
      {
         "id": 1,
         "email": "user@example.com",
         "is_active": true,
         "is_verified": true,
         "role": "admin",
         "avatar_url": "https://res.cloudinary.com/your-cloud-name/image/upload/v1234567890/avatar.jpg",
         "created_at": "2024-03-28T10:00:00",
         "updated_at": "2024-03-28T10:30:00"
      } 