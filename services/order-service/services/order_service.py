from sqlalchemy.orm import Session
from models.cart import Cart
from models.cart_item import CartItem
from models.order import Order
from models.order_item import OrderItem
from schemas.cart import CartCreate, CartItemCreate, CartItemUpdate


def create_cart(db: Session, cart_data: CartCreate):
    existing_cart = db.query(Cart).filter(Cart.customer_id == cart_data.customer_id).first()
    if existing_cart:
        return "cart_exists"

    cart = Cart(customer_id=cart_data.customer_id)
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart


def get_cart_by_customer_id(db: Session, customer_id: int):
    return db.query(Cart).filter(Cart.customer_id == customer_id).first()


def add_item_to_cart(db: Session, customer_id: int, item_data: CartItemCreate):
    cart = get_cart_by_customer_id(db, customer_id)
    if not cart:
        return "cart_not_found"

    existing_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == item_data.product_id
    ).first()

    if existing_item:
        existing_item.quantity += item_data.quantity
        existing_item.unit_price = item_data.unit_price
        db.commit()
        db.refresh(existing_item)
        return existing_item

    new_item = CartItem(
        cart_id=cart.id,
        product_id=item_data.product_id,
        quantity=item_data.quantity,
        unit_price=item_data.unit_price
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


def update_cart_item(db: Session, customer_id: int, product_id: int, item_data: CartItemUpdate):
    cart = get_cart_by_customer_id(db, customer_id)
    if not cart:
        return "cart_not_found"

    item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == product_id
    ).first()

    if not item:
        return "item_not_found"

    item.quantity = item_data.quantity
    db.commit()
    db.refresh(item)
    return item


def remove_cart_item(db: Session, customer_id: int, product_id: int):
    cart = get_cart_by_customer_id(db, customer_id)
    if not cart:
        return "cart_not_found"

    item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == product_id
    ).first()

    if not item:
        return "item_not_found"

    db.delete(item)
    db.commit()
    return item


def place_order_from_cart(db: Session, customer_id: int):
    cart = get_cart_by_customer_id(db, customer_id)
    if not cart:
        return "cart_not_found"

    if not cart.items:
        return "empty_cart"

    total_amount = sum(item.quantity * item.unit_price for item in cart.items)

    order = Order(
        customer_id=customer_id,
        status="PENDING",
        total_amount=total_amount
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    for item in cart.items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            line_total=item.quantity * item.unit_price
        )
        db.add(order_item)

    db.commit()
    db.refresh(order)

    for item in cart.items[:]:
        db.delete(item)

    db.commit()
    return order


def get_all_orders(db: Session):
    return db.query(Order).all()


def get_order_by_id(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()


def get_orders_by_customer_id(db: Session, customer_id: int):
    return db.query(Order).filter(Order.customer_id == customer_id).all()