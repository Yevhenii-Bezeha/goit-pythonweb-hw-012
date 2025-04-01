Create Contact
=============

.. http:post:: /contacts/

   Create a new contact.

   :header Authorization: Bearer {token}
   :json first_name: Contact's first name
   :json last_name: Contact's last name
   :json email: Contact's email address
   :json phone: Contact's phone number
   :json birthday: Contact's birthday (YYYY-MM-DD)

   :status 200: Contact created successfully
   :status 401: Not authenticated
   :status 422: Validation error

   **Example Request:**
   .. code-block:: http
      POST /contacts/
      Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
      Content-Type: application/json

      {
         "first_name": "John",
         "last_name": "Doe",
         "email": "john@example.com",
         "phone": "+1234567890",
         "birthday": "1990-01-01"
      }

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