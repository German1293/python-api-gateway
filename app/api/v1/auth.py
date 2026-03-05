from fastapi import APIRouter, Header, HTTPException, Response, status
from jose import jwt, JWTError
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_service import authenticate_user
from app.core.security import create_access_token, create_refresh_token
from app.core.config import settings
router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest):
    user = authenticate_user(data.username, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    return TokenResponse(
        access_token=create_access_token(user["username"], user["email"]),
        refresh_token=create_refresh_token(user["username"]),
    )

@router.get("/verify")
def verify_token(authorization: str = Header(...), response: Response = None):
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError()

        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )

        if payload.get("type") != "access":
            raise ValueError()

        email = payload.get("email")
        if response is not None and email is not None:
            response.headers["X-User-Email"] = email

    except (JWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )