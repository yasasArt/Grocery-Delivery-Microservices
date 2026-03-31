from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db
from main import app

TEST_DATABASE_URL = "sqlite:///./test_delivery.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_delivery():
    response = client.post(
        "/deliveries/",
        json={
            "order_id": 101,
            "rider_name": "Kamal",
            "contact_number": "0771234567",
            "estimated_time": "30 mins",
            "delivery_address": "Negombo, Sri Lanka",
            "notes": "Call before delivery",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["order_id"] == 101
    assert data["delivery_status"] == "ASSIGNED"


def test_get_all_deliveries():
    response = client.get("/deliveries/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_delivery_by_id():
    response = client.get("/deliveries/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_delivery_by_order_id():
    response = client.get("/deliveries/order/101")
    assert response.status_code == 200
    assert response.json()["order_id"] == 101


def test_update_delivery():
    response = client.put(
        "/deliveries/1",
        json={
            "rider_name": "Nimal",
            "estimated_time": "20 mins",
            "notes": "Handle carefully",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["rider_name"] == "Nimal"
    assert data["estimated_time"] == "20 mins"


def test_update_delivery_status():
    response = client.put(
        "/deliveries/1/status",
        json={"delivery_status": "DELIVERED"},
    )

    assert response.status_code == 200
    assert response.json()["delivery_status"] == "DELIVERED"


def test_filter_deliveries_by_status():
    response = client.get("/deliveries/?status=DELIVERED")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["delivery_status"] == "DELIVERED"


def test_delete_delivery():
    response = client.delete("/deliveries/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Delivery deleted successfully"