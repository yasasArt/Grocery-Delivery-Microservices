from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.db.database import Base


class Delivery(Base):
    __tablename__ = "deliveries"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False, unique=True, index=True)
    rider_name = Column(String(100), nullable=False)
    contact_number = Column(String(20), nullable=False)
    delivery_status = Column(String(30), nullable=False, default="ASSIGNED")
    estimated_time = Column(String(50), nullable=True)
    delivery_address = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)