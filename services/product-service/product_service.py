from sqlalchemy.orm import Session
from sqlalchemy import func
from models.product_model import Product
from product_schema import ProductCreate, ProductUpdate

def create_product(db: Session, product_data: ProductCreate):
    normalized_category = product_data.category.strip().lower()

    new_product = Product(
        name = product_data.name.strip(),
        description = product_data.description.strip(),
        category = normalized_category,
        price = product_data.price,
        stock_quantity = product_data.stock_quantity,
        is_available = product_data.is_available
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

def get_all_products(db: Session):
    return db.query(Product).all()

def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def update_product(db: Session, product_id: int, product_data: ProductUpdate):
    
    product = get_product_by_id(db, product_id)
    
    if not product:
        return None
    
    update_data = product_data.model_dump(exclude_unset=True)

    if "name" in update_data and update_data["name"] is not None:
        product.name = update_data["name"].strip()

    if "description" in update_data and update_data["description"] is not None:
        product.description = update_data["description"].strip()
    
    if "category" in update_data and update_data["category"] is not None:
        product.category = update_data["category"].strip().lower()
    
    if "price" in update_data and update_data["price"] is not None:
        product.price = update_data["price"]
    
    for key, value in update_data.items():
        setattr(product, key, value)
    
    db.commit()
    db.refresh(product)

    return product

def delete_product(db: Session, product_id: int):

    product = get_product_by_id(db, product_id)

    if not product:
        return None
    
    db.delete(product)
    db.commit()

    return product

def get_products_by_category(db: Session, category: str):

    return db.query(Product).filter(
        func.lower(Product.category) == category.strip().lower()
    ).all()

def get_available_products(db: Session):
    return db.query(Product).filter(
        Product.is_available == True, 
        Product.stock_quantity > 0
    ).all()

def search_products(db: Session, query: str):
    search_query = f"%{query.strip().lower()}%"
    return db.query(Product).filter(
        func.lower(Product.name).like(search_query) | 
        func.lower(Product.description).like(search_query)
    ).all()