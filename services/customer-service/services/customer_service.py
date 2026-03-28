from sqlalchemy.orm import Session
from models.customer import Customer
from models.address import Address
from schemas.customer import CustomerCreate, CustomerUpdate
from schemas.address import AddressCreate


def create_customer(db: Session, customer_data: CustomerCreate):
    existing_customer = db.query(Customer).filter(Customer.email == customer_data.email).first()
    if existing_customer:
        return None

    customer = Customer(**customer_data.model_dump())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def get_all_customers(db: Session):
    return db.query(Customer).all()

def get_customer_by_id(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.id == customer_id).first()

def update_customer(db: Session, customer_id: int, customer_data: CustomerUpdate):
    customer = get_customer_by_id(db, customer_id)
    if not customer:
        return "not_found"

    if customer_data.email and customer_data.email != customer.email:
        existing_customer = db.query(Customer).filter(Customer.email == customer_data.email).first()
        if existing_customer:
            return "email_exists"

    update_data = customer_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(customer, key, value)

    db.commit()
    db.refresh(customer)
    return customer

def delete_customer(db: Session, customer_id: int):
    customer = get_customer_by_id(db, customer_id)
    if not customer:
        return None

    db.delete(customer)
    db.commit()
    return customer


def add_address_to_customer(db: Session, customer_id: int, address_data: AddressCreate):
    customer = get_customer_by_id(db, customer_id)
    if not customer:
        return None

    address = Address(customer_id=customer_id, **address_data.model_dump())
    db.add(address)
    db.commit()
    db.refresh(address)
    return address

def get_customer_addresses(db: Session, customer_id: int):
    customer = get_customer_by_id(db, customer_id)
    if not customer:
        return None

    return db.query(Address).filter(Address.customer_id == customer_id).all()


def get_customer_with_addresses(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.id == customer_id).first()