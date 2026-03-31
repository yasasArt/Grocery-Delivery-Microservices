def test_create_cart(client):
    response = client.post("/carts", json={"customer_id": 1})
    assert response.status_code == 201
    assert response.json()["customer_id"] == 1


def test_get_cart(client):
    client.post("/carts", json={"customer_id": 1})

    response = client.get("/carts/1")
    assert response.status_code == 200
    assert response.json()["customer_id"] == 1


def test_add_item_to_cart(client):
    client.post("/carts", json={"customer_id": 1})

    response = client.post(
        "/carts/1/items",
        json={
            "product_id": 101,
            "quantity": 2,
            "unit_price": 450
        }
    )
    assert response.status_code == 201
    assert response.json()["product_id"] == 101


def test_update_cart_item(client):
    client.post("/carts", json={"customer_id": 1})
    client.post(
        "/carts/1/items",
        json={
            "product_id": 101,
            "quantity": 2,
            "unit_price": 450
        }
    )

    response = client.put(
        "/carts/1/items/101",
        json={"quantity": 5}
    )
    assert response.status_code == 200
    assert response.json()["quantity"] == 5


def test_remove_cart_item(client):
    client.post("/carts", json={"customer_id": 1})
    client.post(
        "/carts/1/items",
        json={
            "product_id": 101,
            "quantity": 2,
            "unit_price": 450
        }
    )

    response = client.delete("/carts/1/items/101")
    assert response.status_code == 200
    assert response.json()["message"] == "Cart item removed successfully"


def test_place_order_from_cart(client):
    client.post("/carts", json={"customer_id": 1})
    client.post(
        "/carts/1/items",
        json={
            "product_id": 101,
            "quantity": 2,
            "unit_price": 450
        }
    )
    client.post(
        "/carts/1/items",
        json={
            "product_id": 102,
            "quantity": 1,
            "unit_price": 800
        }
    )

    response = client.post("/orders/place/1")
    assert response.status_code == 201
    data = response.json()
    assert data["customer_id"] == 1
    assert data["total_amount"] == 1700


def test_get_all_orders(client):
    client.post("/carts", json={"customer_id": 1})
    client.post(
        "/carts/1/items",
        json={
            "product_id": 101,
            "quantity": 2,
            "unit_price": 450
        }
    )
    client.post("/orders/place/1")

    response = client.get("/orders")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_order_by_id(client):
    client.post("/carts", json={"customer_id": 1})
    client.post(
        "/carts/1/items",
        json={
            "product_id": 101,
            "quantity": 2,
            "unit_price": 450
        }
    )
    create_order = client.post("/orders/place/1")
    order_id = create_order.json()["id"]

    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    assert response.json()["id"] == order_id


def test_get_orders_by_customer(client):
    client.post("/carts", json={"customer_id": 1})
    client.post(
        "/carts/1/items",
        json={
            "product_id": 101,
            "quantity": 2,
            "unit_price": 450
        }
    )
    client.post("/orders/place/1")

    response = client.get("/orders/customer/1")
    assert response.status_code == 200
    assert len(response.json()) == 1