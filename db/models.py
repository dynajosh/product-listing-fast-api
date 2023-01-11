from sqlalchemy import Column, String, Float, Integer, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship



Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    index =Column(Integer, unique=True)
    sku = Column(String, primary_key=True)
    name = Column(String)
    category = Column(String)
    price = Column(Float)
    discount_percentage = Column(Float)
    
class Discount(Base):
    __tablename__ = "discounts"
    id = Column(Integer, unique=True, primary_key=True)
    percentage = Column(Float)
    sku = Column(String, unique=True)
    category = Column(String, unique=True)
   