import uuid
import requests


def test_full_workflow_through_gateway(gateway_url):
    unique_product_name = f"Milk {uuid.uuid4().hex[:6]}"
    unique_email = f"user_{uuid.uuid4().hex[:6]}@example.com"

    product_response = requests.post(
        f"{gateway_url}/api/products/",
        json={
            "name": unique_product_name,
            "description": "High quality milk",
            "category": "Dairy",
            "price": 450.0,
            "stock_quantity": 20,
            "is_available": True
        }
    )
    assert product_response.status_code in [200, 201]
    product_id = product_response.json()["id"]

    customer_response = requests.post(
        f"{gateway_url}/api/customers/",
        json={
            "full_name": "Nimal Perera",
            "email": unique_email,
            "phone": "0771234567"
        }
    )
    assert customer_response.status_code in [200, 201]
    customer_id = customer_response.json()["id"]

    address_response = requests.post(
        f"{gateway_url}/api/customers/{customer_id}/addresses",
        json={
            "label": "Home",
            "address_line": "No 25, Galle Road",
            "city": "Kalutara",
            "postal_code": "12000"
        }
    )
    assert address_response.status_code in [200, 201]

    cart_response = requests.post(
        f"{gateway_url}/api/carts",
        json={"customer_id": customer_id}
    )
    assert cart_response.status_code in [200, 201]

    cart_item_response = requests.post(
        f"{gateway_url}/api/carts/{customer_id}/items",
        json={
            "product_id": product_id,
            "quantity": 2,
            "unit_price": 450
        }
    )
    assert cart_item_response.status_code in [200, 201]

    order_response = requests.post(f"{gateway_url}/api/orders/place/{customer_id}")
    assert order_response.status_code in [200, 201]
    order_id = order_response.json()["id"]

    delivery_response = requests.post(
        f"{gateway_url}/api/deliveries/",
        json={
            "order_id": order_id,
            "rider_name": "Kasun Silva",
            "contact_number": "0774567890",
            "estimated_time": "30 minutes",
            "delivery_address": "No 25, Galle Road, Kalutara"
        }
    )
    assert delivery_response.status_code in [200, 201]
    delivery_id = delivery_response.json()["id"]

    status_response = requests.put(
        f"{gateway_url}/api/deliveries/{delivery_id}/status",
        json={"delivery_status": "DELIVERED"}
    )
    assert status_response.status_code == 200
    assert status_response.json()["delivery_status"] == "DELIVERED"