from sqlalchemy.orm import Session
from app.models.delivery import Delivery
from app.schemas.delivery import DeliveryCreate, DeliveryStatusUpdate

VALID_STATUSES = {"ASSIGNED", "PICKED_UP", "ON_THE_WAY", "DELIVERED"}


def create_delivery(db: Session, delivery_data: DeliveryCreate):
    existing_delivery = db.query(Delivery).filter(Delivery.order_id == delivery_data.order_id).first()
    if existing_delivery:
        return "delivery_exists"

    delivery = Delivery(
        order_id=delivery_data.order_id,
        rider_name=delivery_data.rider_name,
        contact_number=delivery_data.contact_number,
        delivery_status="ASSIGNED",
        estimated_time=delivery_data.estimated_time,
        delivery_address=delivery_data.delivery_address,
    )
    db.add(delivery)
    db.commit()
    db.refresh(delivery)
    return delivery


def get_all_deliveries(db: Session):
    return db.query(Delivery).all()


def get_delivery_by_id(db: Session, delivery_id: int):
    return db.query(Delivery).filter(Delivery.id == delivery_id).first()


def get_delivery_by_order_id(db: Session, order_id: int):
    return db.query(Delivery).filter(Delivery.order_id == order_id).first()


def update_delivery_status(db: Session, delivery_id: int, status_data: DeliveryStatusUpdate):
    delivery = get_delivery_by_id(db, delivery_id)
    if not delivery:
        return "not_found"

    new_status = status_data.delivery_status.strip().upper()
    if new_status not in VALID_STATUSES:
        return "invalid_status"

    delivery.delivery_status = new_status
    db.commit()
    db.refresh(delivery)
    return delivery