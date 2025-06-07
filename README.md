# FastAPI Product Management API

This project is a beginner-friendly FastAPI application for managing product data, using SQLite and SQLAlchemy for the database, modular code structure, API key authentication, and Pydantic schemas for validation.

## Features
- CRUD operations for products (create, read, update, delete)
- Product schema supports nested fields (dimensions, reviews, meta, etc.)
- API key authentication via header (`X-API-KEY`)
- SQLite database with SQLAlchemy ORM
- Modular project structure
- Automatic interactive API docs (Swagger UI and ReDoc)

## Project Structure
```
FastAPIProject/
├── main.py                # FastAPI app startup
├── requirements.txt       # Python dependencies
├── postman_collection.json# Postman collection for testing
├── schemas.py             # Pydantic schemas
├── models/                # SQLAlchemy models
├── routes/                # API routes
├── config/                # Database config
├── auth/                  # API key middleware
└── products.db            # SQLite database (auto-created)
```

## Setup Instructions

1. **Clone or download the project**
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set your API key**
   - Create a `.env` file in the project root:
     ```env
     API_KEY=your-secret-api-key
     ```
4. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```
   - The server will start at `http://localhost:8000`

## API Authentication
- All endpoints require an API key in the header:
  - Header name: `X-API-KEY`
  - Value: The value you set in your `.env` file

## Interactive API Documentation
- FastAPI automatically generates interactive docs:
  - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
  - ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Testing with Postman
- Import `postman_collection.json` into Postman
- All requests include the `X-API-KEY` header
- Test all CRUD endpoints easily

## Database
- SQLite database file (`products.db`) is created automatically
- Tables are auto-generated on app startup

## Customization
- Update models in `models/product.py` and schemas in `schemas.py` to match your product data
- Add more routes in `routes/products.py` as needed

## Useful Links
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

---

**Enjoy building with FastAPI!**
