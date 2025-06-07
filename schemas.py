from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class DimensionsSchema(BaseModel):
    width: float
    height: float
    depth: float

class ReviewSchema(BaseModel):
    id: Optional[int] = None
    rating: int = Field(..., ge=1, le=5)
    comment: str
    date: Optional[datetime] = None
    reviewerName: Optional[str] = None
    reviewerEmail: Optional[str] = None

class MetaSchema(BaseModel):
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    barcode: Optional[str] = None
    qrCode: Optional[str] = None

class ProductBase(BaseModel):
    title: str
    description: str
    category: str
    price: float
    discountPercentage: float
    rating: float
    stock: int
    tags: List[str]
    brand: str
    sku: str
    weight: float
    dimensions: DimensionsSchema
    warrantyInformation: str
    shippingInformation: str
    availabilityStatus: str
    returnPolicy: str
    minimumOrderQuantity: int
    meta: Optional[MetaSchema] = None
    images: List[str]
    thumbnail: str

class ProductCreate(ProductBase):
    reviews: Optional[List[ReviewSchema]] = []

class ProductUpdate(ProductBase):
    reviews: Optional[List[ReviewSchema]] = []

class Product(ProductBase):
    id: int
    reviews: List[ReviewSchema] = []

    class Config:
        orm_mode = True
