Read Contacts
============

.. http:get:: /contacts/

   Get all contacts for the current user.

   :header Authorization: Bearer {token}
   :query skip: Number of records to skip (optional, default: 0)
   :query limit: Maximum number of records to return (optional, default: 100)

   :status 200: Success
   :status 401: Not authenticated

   **Example Request:**
   .. code-block:: http
      GET /contacts/?skip=0&limit=10
      Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...

   **Example Response:**
   .. code-block:: json
      [
         {
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "phone": "+1234567890",
            "birthday": "1990-01-01",
            "owner_id": 1,
            "created_at": "2024-03-28T10:00:00",
            "updated_at": "2024-03-28T10:00:00"
         }
      ]

.. http:get:: /contacts/{contact_id}

   Get a specific contact by ID.

   :header Authorization: Bearer {token}
   :param contact_id: Contact ID

   :status 200: Success
   :status 401: Not authenticated
   :status 404: Contact not found

   **Example Request:**
   .. code-block:: http
      GET /contacts/1
      Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...

   **Example Response:**
   .. code-block:: json
      {
         "id": 1,
         "first_name": "John",
         "last_name": "Doe",
         "email": "john@example.com",
         "phone": "+1234567890",
         "birthday": "1990-01-01",
         "owner_id": 1,
         "created_at": "2024-03-28T10:00:00",
         "updated_at": "2024-03-28T10:00:00"
      } 