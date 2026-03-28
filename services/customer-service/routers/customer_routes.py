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
    add_address_to_customer,
    create_customer,
    get_all_customers,
    get_customer_addresses,
    get_customer_by_id,
    get_customer_with_addresses,
    update_customer,
    delete_customer,

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

@router.get("/{customer_id}", response_model=CustomerResponse)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = get_customer_by_id(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.put("/{customer_id}", response_model=CustomerResponse)
def update_existing_customer(
    customer_id: int,
    customer: CustomerUpdate,
    db: Session = Depends(get_db)
):
    updated_customer = update_customer(db, customer_id, customer)

    if updated_customer == "not_found":
        raise HTTPException(status_code=404, detail="Customer not found")

    if updated_customer == "email_exists":
        raise HTTPException(status_code=400, detail="Email already exists")

    return updated_customer

@router.delete("/{customer_id}")
def remove_customer(customer_id: int, db: Session = Depends(get_db)):
    deleted_customer = delete_customer(db, customer_id)
    if not deleted_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customer deleted successfully"}

@router.post("/{customer_id}/addresses", response_model=AddressResponse, status_code=status.HTTP_201_CREATED)
def create_address_for_customer(
    customer_id: int,
    address: AddressCreate,
    db: Session = Depends(get_db)
):
    created_address = add_address_to_customer(db, customer_id, address)
    if not created_address:
        raise HTTPException(status_code=404, detail="Customer not found")
    return created_address

@router.get("/{customer_id}/addresses", response_model=list[AddressResponse])
def read_customer_addresses(customer_id: int, db: Session = Depends(get_db)):
    addresses = get_customer_addresses(db, customer_id)
    if addresses is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return addresses

@router.get("/with-addresses/{customer_id}", response_model=CustomerWithAddressesResponse)
def read_customer_with_addresses(customer_id: int, db: Session = Depends(get_db)):
    customer = get_customer_with_addresses(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer