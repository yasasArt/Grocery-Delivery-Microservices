from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.delivery import DeliveryCreate, DeliveryStatusUpdate, DeliveryResponse
from app.services.delivery_service import (
    create_delivery,
    get_all_deliveries,
    get_delivery_by_id,
    get_delivery_by_order_id,
    update_delivery_status,
)

router = APIRouter()


@router.post("/", response_model=DeliveryResponse, status_code=status.HTTP_201_CREATED)
def create_new_delivery(delivery: DeliveryCreate, db: Session = Depends(get_db)):
    created_delivery = create_delivery(db, delivery)
    if created_delivery == "delivery_exists":
        raise HTTPException(status_code=400, detail="Delivery already exists for this order")
    return created_delivery


@router.get("/", response_model=list[DeliveryResponse])
def read_all_deliveries(db: Session = Depends(get_db)):
    return get_all_deliveries(db)


@router.get("/order/{order_id}", response_model=DeliveryResponse)
def read_delivery_by_order(order_id: int, db: Session = Depends(get_db)):
    delivery = get_delivery_by_order_id(db, order_id)
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found for this order")
    return delivery


@router.get("/{delivery_id}", response_model=DeliveryResponse)
def read_delivery(delivery_id: int, db: Session = Depends(get_db)):
    delivery = get_delivery_by_id(db, delivery_id)
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return delivery


@router.put("/{delivery_id}/status", response_model=DeliveryResponse)
def update_existing_delivery_status(
    delivery_id: int,
    status_data: DeliveryStatusUpdate,
    db: Session = Depends(get_db)
):
    updated_delivery = update_delivery_status(db, delivery_id, status_data)

    if updated_delivery == "not_found":
        raise HTTPException(status_code=404, detail="Delivery not found")

    if updated_delivery == "invalid_status":
        raise HTTPException(
            status_code=400,
            detail="Invalid status. Use ASSIGNED, PICKED_UP, ON_THE_WAY, or DELIVERED"
        )

    return updated_delivery