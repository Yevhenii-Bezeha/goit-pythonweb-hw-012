Update Contact
=============

.. http:put:: /contacts/{contact_id}

   Update a contact.

   :header Authorization: Bearer {token}
   :param contact_id: Contact ID
   :json first_name: Contact's first name (optional)
   :json last_name: Contact's last name (optional)
   :json email: Contact's email address (optional)
   :json phone: Contact's phone number (optional)
   :json birthday: Contact's birthday (optional, YYYY-MM-DD)

   :status 200: Contact updated successfully
   :status 401: Not authenticated
   :status 404: Contact not found
   :status 422: Validation error

   **Example Request:**
   .. code-block:: http
      PUT /contacts/1
      Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
      Content-Type: application/json

      {
         "first_name": "John",
         "last_name": "Smith",
         "email": "john.smith@example.com",
         "phone": "+1987654321",
         "birthday": "1990-01-01"
      }

   **Example Response:**
   .. code-block:: json
      {
         "id": 1,
         "first_name": "John",
         "last_name": "Smith",
         "email": "john.smith@example.com",
         "phone": "+1987654321",
         "birthday": "1990-01-01",
         "owner_id": 1,
         "created_at": "2024-03-28T10:00:00",
         "updated_at": "2024-03-28T10:30:00"
      } 