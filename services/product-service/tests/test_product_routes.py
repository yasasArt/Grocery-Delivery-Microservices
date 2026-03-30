def test_create_product(client):
    response = client.post(
        "/products/",
        json={
            "name": "Fresh Milk 1L",
            "description": "High quality fresh milk",
            "category": "Dairy",
            "price": 450.0,
            "stock_quantity": 20,
            "is_available": True
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Fresh Milk 1L"
    assert data["category"] == "Dairy"

def test_get_all_products(client):
    client.post(
        "/products/",
        json={
            "name": "Brown Bread",
            "description": "Healthy whole wheat bread",
            "category": "Bakery",
            "price": 220.0,
            "stock_quantity": 15,
            "is_available": True
        }
    )

    response = client.get("/products/")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_product_by_id(client):
    create_response = client.post(
        "/products/",
        json={
            "name": "Eggs 10 Pack",
            "description": "Farm fresh eggs",
            "category": "Dairy",
            "price": 600.0,
            "stock_quantity": 10,
            "is_available": True
        }
    )
    product_id = create_response.json()["id"]

    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["id"] == product_id


def test_update_product(client):
    create_response = client.post(
        "/products/",
        json={
            "name": "Orange Juice",
            "description": "Natural juice",
            "category": "Beverages",
            "price": 500.0,
            "stock_quantity": 8,
            "is_available": True
        }
    )
    product_id = create_response.json()["id"]

    response = client.put(
        f"/products/{product_id}",
        json={
            "price": 550.0,
            "stock_quantity": 12
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["price"] == 550.0
    assert data["stock_quantity"] == 12


def test_delete_product(client):
    create_response = client.post(
        "/products/",
        json={
            "name": "Butter",
            "description": "Salted butter",
            "category": "Dairy",
            "price": 700.0,
            "stock_quantity": 5,
            "is_available": True
        }
    )
    product_id = create_response.json()["id"]

    response = client.delete(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Product deleted successfully"

def test_get_products_by_category(client):
    client.post(
        "/products/",
        json={
            "name": "Yogurt Cup",
            "description": "Strawberry yogurt",
            "category": "Dairy",
            "price": 180.0,
            "stock_quantity": 12,
            "is_available": True
        }
    )

    response = client.get("/products/category/Dairy")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_available_products(client):
    client.post(
        "/products/",
        json={
            "name": "Rice 1kg",
            "description": "White rice",
            "category": "Grocery",
            "price": 300.0,
            "stock_quantity": 0,
            "is_available": True
        }
    )
    client.post(
        "/products/",
        json={
            "name": "Milk Powder",
            "description": "Full cream milk powder",
            "category": "Dairy",
            "price": 1200.0,
            "stock_quantity": 5,
            "is_available": True
        }
    )

    response = client.get("/products/available/list")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Milk Powder"


def test_search_products(client):
    client.post(
        "/products/",
        json={
            "name": "Fresh Milk 1L",
            "description": "High quality fresh milk",
            "category": "Dairy",
            "price": 450.0,
            "stock_quantity": 20,
            "is_available": True
        }
    )

    response = client.get("/products/search?q=milk")
    assert response.status_code == 200
    assert len(response.json()) == 1