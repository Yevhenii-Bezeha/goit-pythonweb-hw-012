import pytest
from fastapi.testclient import TestClient

def test_create_contact(client, test_user_token):
    contact_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "1234567890",
        "birthday": "1990-01-01",
        "additional_info": "Test contact"
    }
    response = client.post(
        "/contacts/",
        headers={"Authorization": f"Bearer {test_user_token}"},
        json=contact_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == contact_data["first_name"]
    assert data["last_name"] == contact_data["last_name"]
    assert data["email"] == contact_data["email"]
    assert "id" in data

def test_read_contacts(client, test_user_token):
    # First, create a contact
    contact_data = {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@example.com",
        "phone": "0987654321",
        "birthday": "1992-02-02",
        "additional_info": "Another test contact"
    }
    client.post(
        "/contacts/",
        headers={"Authorization": f"Bearer {test_user_token}"},
        json=contact_data
    )

    # Now read all contacts
    response = client.get(
        "/contacts/",
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["email"] == contact_data["email"]

def test_read_contact(client, test_user_token):
    # First, create a contact
    contact_data = {
        "first_name": "Bob",
        "last_name": "Johnson",
        "email": "bob.johnson@example.com",
        "phone": "5555555555",
        "birthday": "1985-03-03",
        "additional_info": "Test contact details"
    }
    create_response = client.post(
        "/contacts/",
        headers={"Authorization": f"Bearer {test_user_token}"},
        json=contact_data
    )
    contact_id = create_response.json()["id"]

    # Now read the specific contact
    response = client.get(
        f"/contacts/{contact_id}",
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == contact_id
    assert data["email"] == contact_data["email"]

def test_update_contact(client, test_user_token):
    # First, create a contact
    contact_data = {
        "first_name": "Alice",
        "last_name": "Brown",
        "email": "alice.brown@example.com",
        "phone": "1112223333",
        "birthday": "1988-04-04",
        "additional_info": "Original info"
    }
    create_response = client.post(
        "/contacts/",
        headers={"Authorization": f"Bearer {test_user_token}"},
        json=contact_data
    )
    contact_id = create_response.json()["id"]

    # Update the contact
    updated_data = dict(contact_data)
    updated_data["first_name"] = "Alicia"
    updated_data["additional_info"] = "Updated info"
    
    response = client.put(
        f"/contacts/{contact_id}",
        headers={"Authorization": f"Bearer {test_user_token}"},
        json=updated_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == contact_id
    assert data["first_name"] == "Alicia"
    assert data["additional_info"] == "Updated info"

def test_delete_contact(client, test_user_token):
    # First, create a contact
    contact_data = {
        "first_name": "Charlie",
        "last_name": "Wilson",
        "email": "charlie.wilson@example.com",
        "phone": "9998887777",
        "birthday": "1995-05-05",
        "additional_info": "Contact to be deleted"
    }
    create_response = client.post(
        "/contacts/",
        headers={"Authorization": f"Bearer {test_user_token}"},
        json=contact_data
    )
    contact_id = create_response.json()["id"]

    # Delete the contact
    response = client.delete(
        f"/contacts/{contact_id}",
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == contact_id

    # Verify the contact is deleted
    response = client.get(
        f"/contacts/{contact_id}",
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    assert response.status_code == 404

def test_unauthorized_access(client):
    # Try to access contacts without authentication
    response = client.get("/contacts/")
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]

def test_contact_not_found(client, test_user_token):
    response = client.get(
        "/contacts/999999",  # Non-existent ID
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    assert response.status_code == 404
    assert "Contact not found" in response.json()["detail"] 