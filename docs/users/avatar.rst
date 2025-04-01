User Avatar
==========

.. http:put:: /users/avatar/

   Update user's avatar (admin only).

   :header Authorization: Bearer {token}
   :form file: Avatar image file (multipart/form-data)

   :status 200: Avatar updated successfully
   :status 401: Not authenticated
   :status 403: Not enough permissions (not admin)
   :status 500: Error uploading avatar

   **Example Request:**
   .. code-block:: http
      PUT /users/avatar/
      Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
      Content-Type: multipart/form-data

      file: <binary_file_data>

   **Example Response:**
   .. code-block:: json
      {
         "message": "Avatar updated successfully",
         "avatar_url": "https://res.cloudinary.com/your-cloud-name/image/upload/v1234567890/avatar.jpg"
      } 