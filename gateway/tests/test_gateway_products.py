import uuid
from fastapi.testclient import TestClient
from gateway.main import app


def test_gateway_create_product(gateway_url):
    unique_name = f"Fresh Milk {uuid.uuid4().hex[:6]}"

    with TestClient(app, base_url=gateway_url) as client:
        response = client.post(
            "/api/products/",
            json={
                "name": unique_name,
                "description": "High quality fresh milk",
                "category": "Dairy",
                "price": 450.0,
                "stock_quantity": 20,
                "is_available": True
            }
        )

        assert response.status_code == 200 or response.status_code == 201
        data = response.json()
        assert data["name"] == unique_name


def test_gateway_get_all_products(gateway_url):
    with TestClient(app, base_url=gateway_url) as client:
        response = client.get("/api/products/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


def test_gateway_search_products(gateway_url):
    unique_name = f"Milk Search {uuid.uuid4().hex[:6]}"

    with TestClient(app, base_url=gateway_url) as client:
        client.post(
            "/api/products/",
            json={
                "name": unique_name,
                "description": "Testing search",
                "category": "Dairy",
                "price": 400.0,
                "stock_quantity": 10,
                "is_available": True
            }
        )

        response = client.get("/api/products/search", params={"q": "Milk"})
        assert response.status_code == 200
        assert isinstance(response.json(), list)


def test_gateway_get_products_by_category(gateway_url):
    with TestClient(app, base_url=gateway_url) as client:
        response = client.get("/api/products/category/Dairy")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


def test_gateway_get_available_products(gateway_url):
    with TestClient(app, base_url=gateway_url) as client:
        response = client.get("/api/products/available/list")
        assert response.status_code == 200
        assert isinstance(response.json(), list)