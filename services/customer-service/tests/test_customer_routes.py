def test_create_customer(client):
    response = client.post(
        "/customers/",
        json={
            "full_name": "Nimal Perera",
            "email": "nimal@example.com",
            "phone": "0771234567"
        }
    )
    assert response.status_code == 201
    assert response.json()["email"] == "nimal@example.com"


def test_get_all_customers(client):
    client.post(
        "/customers/",
        json={
            "full_name": "Kamal Silva",
            "email": "kamal@example.com",
            "phone": "0779876543"
        }
    )

    response = client.get("/customers/")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_customer_by_id(client):
    create_response = client.post(
        "/customers/",
        json={
            "full_name": "Asha Fernando",
            "email": "asha@example.com",
            "phone": "0711111111"
        }
    )
    customer_id = create_response.json()["id"]

    response = client.get(f"/customers/{customer_id}")
    assert response.status_code == 200
    assert response.json()["id"] == customer_id


def test_update_customer(client):
    create_response = client.post(
        "/customers/",
        json={
            "full_name": "Saman Jayasuriya",
            "email": "saman@example.com",
            "phone": "0722222222"
        }
    )
    customer_id = create_response.json()["id"]

    response = client.put(
        f"/customers/{customer_id}",
        json={"phone": "0770000000"}
    )
    assert response.status_code == 200
    assert response.json()["phone"] == "0770000000"


def test_delete_customer(client):
    create_response = client.post(
        "/customers/",
        json={
            "full_name": "Mali Perera",
            "email": "mali@example.com",
            "phone": "0744444444"
        }
    )
    customer_id = create_response.json()["id"]

    response = client.delete(f"/customers/{customer_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Customer deleted successfully"


def test_add_address_to_customer(client):
    create_response = client.post(
        "/customers/",
        json={
            "full_name": "Sunil Silva",
            "email": "sunil@example.com",
            "phone": "0755555555"
        }
    )
    customer_id = create_response.json()["id"]

    response = client.post(
        f"/customers/{customer_id}/addresses",
        json={
            "label": "Home",
            "address_line": "No 25, Galle Road",
            "city": "Kalutara",
            "postal_code": "12000"
        }
    )
    assert response.status_code == 201
    assert response.json()["label"] == "Home"


def test_get_customer_addresses(client):
    create_response = client.post(
        "/customers/",
        json={
            "full_name": "Chathura Kumara",
            "email": "chathura@example.com",
            "phone": "0766666666"
        }
    )
    customer_id = create_response.json()["id"]

    client.post(
        f"/customers/{customer_id}/addresses",
        json={
            "label": "Office",
            "address_line": "Main Street",
            "city": "Colombo",
            "postal_code": "00100"
        }
    )

    response = client.get(f"/customers/{customer_id}/addresses")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_customer_with_addresses(client):
    create_response = client.post(
        "/customers/",
        json={
            "full_name": "Iresha Silva",
            "email": "iresha@example.com",
            "phone": "0788888888"
        }
    )
    customer_id = create_response.json()["id"]

    client.post(
        f"/customers/{customer_id}/addresses",
        json={
            "label": "Home",
            "address_line": "Temple Road",
            "city": "Matara",
            "postal_code": "81000"
        }
    )

    response = client.get(f"/customers/with-addresses/{customer_id}")
    assert response.status_code == 200
    assert len(response.json()["addresses"]) == 1