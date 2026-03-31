from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schemas.cart import (
    CartCreate,
    CartItemCreate,
    CartItemUpdate,
    CartResponse,
    CartItemResponse,
)
from schemas.order import OrderResponse
from services.order_service import (
    create_cart,
    get_cart_by_customer_id,
    add_item_to_cart,
    update_cart_item,
    remove_cart_item,
    place_order_from_cart,
    get_all_orders,
    get_order_by_id,
    get_orders_by_customer_id,
)

router = APIRouter()


@router.post("/carts", response_model=CartResponse, status_code=status.HTTP_201_CREATED)
def create_new_cart(cart: CartCreate, db: Session = Depends(get_db)):
    created_cart = create_cart(db, cart)
    if created_cart == "cart_exists":
        raise HTTPException(status_code=400, detail="Cart already exists for this customer")
    return created_cart


@router.get("/carts/{customer_id}", response_model=CartResponse)
def read_cart(customer_id: int, db: Session = Depends(get_db)):
    cart = get_cart_by_customer_id(db, customer_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart


@router.post("/carts/{customer_id}/items", response_model=CartItemResponse, status_code=status.HTTP_201_CREATED)
def add_new_item_to_cart(
    customer_id: int,
    item: CartItemCreate,
    db: Session = Depends(get_db)
):
    created_item = add_item_to_cart(db, customer_id, item)
    if created_item == "cart_not_found":
        raise HTTPException(status_code=404, detail="Cart not found")
    return created_item


@router.put("/carts/{customer_id}/items/{product_id}", response_model=CartItemResponse)
def update_existing_cart_item(
    customer_id: int,
    product_id: int,
    item: CartItemUpdate,
    db: Session = Depends(get_db)
):
    updated_item = update_cart_item(db, customer_id, product_id, item)

    if updated_item == "cart_not_found":
        raise HTTPException(status_code=404, detail="Cart not found")

    if updated_item == "item_not_found":
        raise HTTPException(status_code=404, detail="Cart item not found")

    return updated_item


@router.delete("/carts/{customer_id}/items/{product_id}")
def remove_existing_cart_item(customer_id: int, product_id: int, db: Session = Depends(get_db)):
    deleted_item = remove_cart_item(db, customer_id, product_id)

    if deleted_item == "cart_not_found":
        raise HTTPException(status_code=404, detail="Cart not found")

    if deleted_item == "item_not_found":
        raise HTTPException(status_code=404, detail="Cart item not found")

    return {"message": "Cart item removed successfully"}


@router.post("/orders/place/{customer_id}", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def place_order(customer_id: int, db: Session = Depends(get_db)):
    order = place_order_from_cart(db, customer_id)

    if order == "cart_not_found":
        raise HTTPException(status_code=404, detail="Cart not found")

    if order == "empty_cart":
        raise HTTPException(status_code=400, detail="Cart is empty")

    return order


@router.get("/orders", response_model=list[OrderResponse])
def read_all_orders(db: Session = Depends(get_db)):
    return get_all_orders(db)


@router.get("/orders/customer/{customer_id}", response_model=list[OrderResponse])
def read_orders_by_customer(customer_id: int, db: Session = Depends(get_db)):
    return get_orders_by_customer_id(db, customer_id)


@router.get("/orders/{order_id}", response_model=OrderResponse)
def read_order(order_id: int, db: Session = Depends(get_db)):
    order = get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order