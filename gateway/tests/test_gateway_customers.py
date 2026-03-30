import uuid
import requests


def test_gateway_create_customer(gateway_url):
    unique_email = f"user_{uuid.uuid4().hex[:6]}@example.com"

    response = requests.post(
        f"{gateway_url}/api/customers/",
        json={
            "full_name": "Nimal Perera",
            "email": unique_email,
            "phone": "0771234567"
        }
    )

    assert response.status_code in [200, 201]
    assert response.json()["email"] == unique_email