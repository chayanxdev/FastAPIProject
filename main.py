from fastapi import FastAPI
from auth.api_key_middleware import APIKeyMiddleware
from config.database import Base, engine
from routes.products import router as products_router

# Create tables if not exist
def create_tables():
    Base.metadata.create_all(bind=engine)

create_tables()

app = FastAPI()
app.add_middleware(APIKeyMiddleware)
app.include_router(products_router)
