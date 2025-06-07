from fastapi import Request, HTTPException
from fastapi.security.api_key import APIKeyHeader
from starlette.middleware.base import BaseHTTPMiddleware
from config.database import API_KEY

API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Allow unauthenticated access to docs and OpenAPI endpoints
        if request.url.path.startswith("/docs") or request.url.path.startswith("/redoc") or request.url.path.startswith("/openapi") or request.url.path.startswith("/favicon"):
            return await call_next(request)
        api_key = request.headers.get(API_KEY_NAME)
        if not api_key or api_key != API_KEY:
            raise HTTPException(status_code=401, detail="Unauthorized")
        return await call_next(request)
