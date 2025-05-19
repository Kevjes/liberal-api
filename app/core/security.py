from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.core.config import settings
from app.features.users.dependencies import get_users_service
from app.features.users.models import UserModel
from app.features.users.services import UsersService

oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_admin(
    token: str = Depends(oauth2_scheme), service: UsersService = Depends(get_users_service)
) -> UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str|None = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await service.repository.get_by_email(email)
    if user is None or not user.is_admin:
        raise credentials_exception
    return user

async def get_current_user(token: str = Depends(oauth2_scheme), service: UsersService = Depends(get_users_service)) -> UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str|None = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await service.repository.get_by_email(email)
    if user is None:
        raise credentials_exception
    return user

async def get_current_user_optional(token: Optional[str] = Depends(oauth2_scheme_optional), service: UsersService = Depends(get_users_service)) -> Optional[UserModel]:
    if token is None:
        return None
    try:
        return await get_current_user(token=token, service=service)
    except HTTPException:
        return None