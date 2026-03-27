from datetime import datetime
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import relationship
from app.db.database import Base


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, nullable=False, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    items = relationship(
        "CartItem",
        back_populates="cart",
        cascade="all, delete-orphan"
    )