from sqlalchemy import Column, Integer, String, Boolean, Numeric
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    price = Column(Numeric(precision=10, scale=2), nullable=False)
    in_stock = Column(Boolean, default=True)