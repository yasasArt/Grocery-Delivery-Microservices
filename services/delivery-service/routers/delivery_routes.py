from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from database import get_db
from schemas.delivery import (
    DeliveryCreate,
    DeliveryResponse,
    DeliveryStatusUpdate,
    DeliveryUpdate,
)
from services.delivery_service import (
    create_delivery,
    delete_delivery,
    get_all_deliveries,
    get_deliveries_by_status,
    get_delivery_by_id,
    get_delivery_by_order_id,
    update_delivery,
    update_delivery_status,
)

router = APIRouter()


@router.post("/", response_model=DeliveryResponse, status_code=status.HTTP_201_CREATED)
def create_new_delivery(delivery: DeliveryCreate, db: Session = Depends(get_db)):
    created_delivery = create_delivery(db, delivery)

    if created_delivery == "delivery_exists":
        raise HTTPException(
            status_code=400,
            detail="Delivery already exists for this order",
        )

    return created_delivery


@router.get("/", response_model=list[DeliveryResponse])
def read_all_deliveries(
    status_filter: str | None = Query(default=None, alias="status"),
    db: Session = Depends(get_db),
):
    if status_filter:
        return get_deliveries_by_status(db, status_filter)
    return get_all_deliveries(db)


@router.get("/order/{order_id}", response_model=DeliveryResponse)
def read_delivery_by_order(order_id: int, db: Session = Depends(get_db)):
    delivery = get_delivery_by_order_id(db, order_id)
    if not delivery:
        raise HTTPException(
            status_code=404,
            detail="Delivery not found for this order",
        )
    return delivery


@router.get("/{delivery_id}", response_model=DeliveryResponse)
def read_delivery(delivery_id: int, db: Session = Depends(get_db)):
    delivery = get_delivery_by_id(db, delivery_id)
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return delivery


@router.put("/{delivery_id}", response_model=DeliveryResponse)
def update_existing_delivery(
    delivery_id: int,
    delivery: DeliveryUpdate,
    db: Session = Depends(get_db),
):
    updated_delivery = update_delivery(db, delivery_id, delivery)

    if updated_delivery == "not_found":
        raise HTTPException(status_code=404, detail="Delivery not found")

    return updated_delivery


@router.put("/{delivery_id}/status", response_model=DeliveryResponse)
def update_existing_delivery_status(
    delivery_id: int,
    status_data: DeliveryStatusUpdate,
    db: Session = Depends(get_db),
):
    updated_delivery = update_delivery_status(db, delivery_id, status_data)

    if updated_delivery == "not_found":
        raise HTTPException(status_code=404, detail="Delivery not found")

    if updated_delivery == "invalid_status":
        raise HTTPException(
            status_code=400,
            detail="Invalid status. Use ASSIGNED, PICKED_UP, ON_THE_WAY, DELIVERED, or CANCELLED",
        )

    return updated_delivery


@router.delete("/{delivery_id}")
def remove_delivery(delivery_id: int, db: Session = Depends(get_db)):
    deleted_delivery = delete_delivery(db, delivery_id)

    if not deleted_delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")

    return {"message": "Delivery deleted successfully"}

@router.get("/", response_model=list[DeliveryResponse])
def read_all_deliveries(
    status_filter: str | None = Query(default=None, alias="status"),
    db: Session = Depends(get_db),
):
    if status_filter:
        return get_deliveries_by_status(db, status_filter)
    return get_all_deliveries(db)

@router.put("/{delivery_id}", response_model=DeliveryResponse)
def update_existing_delivery(
    delivery_id: int,
    delivery: DeliveryUpdate,
    db: Session = Depends(get_db),
):
    updated_delivery = update_delivery(db, delivery_id, delivery)

    if updated_delivery == "not_found":
        raise HTTPException(status_code=404, detail="Delivery not found")

    return updated_delivery