from sqlalchemy.orm import Session

from models.delivery import Delivery
from schemas.delivery import DeliveryCreate, DeliveryStatusUpdate, DeliveryUpdate

VALID_STATUSES = {"ASSIGNED", "PICKED_UP", "ON_THE_WAY", "DELIVERED", "CANCELLED"}


def create_delivery(db: Session, delivery_data: DeliveryCreate):
    existing_delivery = (
        db.query(Delivery)
        .filter(Delivery.order_id == delivery_data.order_id)
        .first()
    )
    if existing_delivery:
        return "delivery_exists"

    delivery = Delivery(
        order_id=delivery_data.order_id,
        rider_name=delivery_data.rider_name,
        contact_number=delivery_data.contact_number,
        delivery_status="ASSIGNED",
        estimated_time=delivery_data.estimated_time,
        delivery_address=delivery_data.delivery_address,
        notes=delivery_data.notes,
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


def get_deliveries_by_status(db: Session, delivery_status: str):
    normalized_status = delivery_status.strip().upper()
    return (
        db.query(Delivery)
        .filter(Delivery.delivery_status == normalized_status)
        .all()
    )


def update_delivery(db: Session, delivery_id: int, delivery_data: DeliveryUpdate):
    delivery = get_delivery_by_id(db, delivery_id)
    if not delivery:
        return "not_found"

    update_data = delivery_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(delivery, key, value)

    db.commit()
    db.refresh(delivery)
    return delivery


def update_delivery_status(
    db: Session,
    delivery_id: int,
    status_data: DeliveryStatusUpdate,
):
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


def delete_delivery(db: Session, delivery_id: int):
    delivery = get_delivery_by_id(db, delivery_id)
    if not delivery:
        return None

    db.delete(delivery)
    db.commit()
    return delivery