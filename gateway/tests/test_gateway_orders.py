import requests


def test_gateway_create_cart(gateway_url):
    response = requests.post(
        f"{gateway_url}/api/carts",
        json={"customer_id": 9001}
    )

    assert response.status_code in [200, 201]
    assert response.json()["customer_id"] == 9001