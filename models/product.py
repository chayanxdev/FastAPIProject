from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from config.database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    category = Column(String)
    price = Column(Float)
    discount_percentage = Column(Float)
    rating = Column(Float)
    stock = Column(Integer)
    brand = Column(String)
    sku = Column(String)
    weight = Column(Float)
    warranty_information = Column(String)
    shipping_information = Column(String)
    availability_status = Column(String)
    return_policy = Column(String)
    minimum_order_quantity = Column(Integer)
    meta = Column(JSON, nullable=True)
    images = Column(JSON, nullable=True)
    thumbnail = Column(String)
    tags = Column(JSON, nullable=True)
    dimensions = relationship("Dimensions", uselist=False, backref="product", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="product", cascade="all, delete-orphan")

class Dimensions(Base):
    __tablename__ = "dimensions"
    id = Column(Integer, primary_key=True, index=True)
    width = Column(Float)
    height = Column(Float)
    depth = Column(Float)
    product_id = Column(Integer, ForeignKey("products.id"))

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer)
    comment = Column(String)
    date = Column(DateTime, nullable=True)
    reviewer_name = Column(String, nullable=True)
    reviewer_email = Column(String, nullable=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    product = relationship("Product", back_populates="reviews")
