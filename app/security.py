import secrets

from fastapi import Header, HTTPException
from app.config import get_settings


def validate_admin_token(token: str | None, configured_token: str) -> None:
    if not configured_token:
        raise HTTPException(status_code=503, detail="Admin API token is not configured on the server")
    if not token or not secrets.compare_digest(token, configured_token):
        raise HTTPException(status_code=401, detail="Invalid or missing admin token")


def require_admin(x_admin_token: str | None = Header(default=None, alias="X-Admin-Token")) -> str:
    validate_admin_token(x_admin_token, get_settings().admin_api_token)
    return "admin"
