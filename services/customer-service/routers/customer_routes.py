from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schemas.customer import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse,
    CustomerWithAddressesResponse,
)
from schemas.address import AddressCreate, AddressResponse
from services.customer_service import (
    create_customer,
    get_all_customers,
    # get_customer_by_id,
    # update_customer,
    # delete_customer,
    # add_address_to_customer,
    # get_customer_addresses,
    # get_customer_with_addresses,
)

router = APIRouter()


@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_new_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    created_customer = create_customer(db, customer)
    if created_customer is None:
        raise HTTPException(status_code=400, detail="Email already exists")
    return created_customer


@router.get("/", response_model=list[CustomerResponse])
def read_all_customers(db: Session = Depends(get_db)):
    return get_all_customers(db)

