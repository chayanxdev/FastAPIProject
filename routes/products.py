from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import SessionLocal
from models.product import Product, Review, Dimensions
from schemas import Product as ProductSchema, ProductCreate, ProductUpdate
from typing import List
from datetime import datetime
from fastapi.encoders import jsonable_encoder

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def product_to_schema(product: Product):
    # Map DB model to Pydantic schema, handling field name differences
    return ProductSchema(
        id=product.id,
        title=product.title,
        description=product.description,
        category=product.category,
        price=product.price,
        discountPercentage=product.discount_percentage,
        rating=product.rating,
        stock=product.stock,
        tags=product.tags or [],
        brand=product.brand,
        sku=product.sku,
        weight=product.weight,
        dimensions=product.dimensions and {
            "width": product.dimensions.width,
            "height": product.dimensions.height,
            "depth": product.dimensions.depth
        },
        warrantyInformation=product.warranty_information,
        shippingInformation=product.shipping_information,
        availabilityStatus=product.availability_status,
        reviews=[
            {
                "id": r.id,
                "rating": r.rating,
                "comment": r.comment,
                "date": r.date,
                "reviewerName": r.reviewer_name,
                "reviewerEmail": r.reviewer_email
            } for r in product.reviews
        ],
        returnPolicy=product.return_policy,
        minimumOrderQuantity=product.minimum_order_quantity,
        meta=product.meta,
        images=product.images or [],
        thumbnail=product.thumbnail
    )

@router.get("/products", response_model=List[ProductSchema])
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return [product_to_schema(p) for p in products]

@router.get("/products/{product_id}", response_model=ProductSchema)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product_to_schema(product)

@router.post("/products", response_model=ProductSchema, status_code=201)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(
        title=product.title,
        description=product.description,
        category=product.category,
        price=product.price,
        discount_percentage=product.discountPercentage,
        rating=product.rating,
        stock=product.stock,
        tags=product.tags,
        brand=product.brand,
        sku=product.sku,
        weight=product.weight,
        warranty_information=product.warrantyInformation,
        shipping_information=product.shippingInformation,
        availability_status=product.availabilityStatus,
        return_policy=product.returnPolicy,
        minimum_order_quantity=product.minimumOrderQuantity,
        meta=product.meta.model_dump() if product.meta else None,
        images=product.images,
        thumbnail=product.thumbnail
    )
    # Convert datetime fields in meta to isoformat strings for JSON serialization
    if db_product.meta:
        for key in ["createdAt", "updatedAt"]:
            if db_product.meta.get(key) and isinstance(db_product.meta[key], datetime):
                db_product.meta[key] = db_product.meta[key].isoformat()
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    # Add dimensions
    dims = Dimensions(
        width=product.dimensions.width,
        height=product.dimensions.height,
        depth=product.dimensions.depth,
        product_id=db_product.id
    )
    db.add(dims)
    db.commit()
    # Add reviews
    for review in product.reviews or []:
        db_review = Review(
            rating=review.rating,
            comment=review.comment,
            date=review.date,
            reviewer_name=review.reviewerName,
            reviewer_email=review.reviewerEmail,
            product_id=db_product.id
        )
        db.add(db_review)
    db.commit()
    db.refresh(db_product)
    return product_to_schema(db_product)

@router.put("/products/{product_id}", response_model=ProductSchema)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db_product.title = product.title
    db_product.description = product.description
    db_product.category = product.category
    db_product.price = product.price
    db_product.discount_percentage = product.discountPercentage
    db_product.rating = product.rating
    db_product.stock = product.stock
    db_product.tags = product.tags
    db_product.brand = product.brand
    db_product.sku = product.sku
    db_product.weight = product.weight
    db_product.warranty_information = product.warrantyInformation
    db_product.shipping_information = product.shippingInformation
    db_product.availability_status = product.availabilityStatus
    db_product.return_policy = product.returnPolicy
    db_product.minimum_order_quantity = product.minimumOrderQuantity
    # Convert datetime fields in meta to isoformat strings for JSON serialization
    meta_dict = product.meta.model_dump() if product.meta else None
    if meta_dict:
        for key in ["createdAt", "updatedAt"]:
            if meta_dict.get(key) and hasattr(meta_dict[key], 'isoformat'):
                meta_dict[key] = meta_dict[key].isoformat()
    db_product.meta = meta_dict
    db_product.images = product.images
    db_product.thumbnail = product.thumbnail
    # Update dimensions
    if db_product.dimensions:
        db_product.dimensions.width = product.dimensions.width
        db_product.dimensions.height = product.dimensions.height
        db_product.dimensions.depth = product.dimensions.depth
    else:
        dims = Dimensions(
            width=product.dimensions.width,
            height=product.dimensions.height,
            depth=product.dimensions.depth,
            product_id=db_product.id
        )
        db.add(dims)
    # Update reviews
    db.query(Review).filter(Review.product_id == product_id).delete()
    for review in product.reviews or []:
        db_review = Review(
            rating=review.rating,
            comment=review.comment,
            date=review.date,
            reviewer_name=review.reviewerName,
            reviewer_email=review.reviewerEmail,
            product_id=db_product.id
        )
        db.add(db_review)
    db.commit()
    db.refresh(db_product)
    return product_to_schema(db_product)

@router.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return None
