from fastapi import Request
from fastapi.security.api_key import APIKeyHeader
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from config.database import API_KEY

API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            # Allow unauthenticated access to docs and OpenAPI endpoints
            if request.url.path.startswith("/docs") or request.url.path.startswith("/redoc") or request.url.path.startswith("/openapi") or request.url.path.startswith("/favicon"):
                return await call_next(request)
            api_key = request.headers.get(API_KEY_NAME)
            if not api_key:
                return JSONResponse(status_code=401, content={"detail": "API key missing"})
            if api_key != API_KEY:
                return JSONResponse(status_code=403, content={"detail": "Invalid API key"})
            response = await call_next(request)
            return response
        except Exception as exc:
            # Handle unexpected errors
            return JSONResponse(status_code=500, content={"detail": f"Internal server error: {str(exc)}"})
