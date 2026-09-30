from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.orders.api.auth import FAKE_USER, create_access_token, verify_password
from src.orders.api.schemas.order_schemas import TokenResponse

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


@router.post("/token", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != FAKE_USER["username"] or not verify_password(
        form_data.password, FAKE_USER["hashed_password"]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
        )
    token = create_access_token({"sub": form_data.username})
    return TokenResponse(access_token=token)
