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


