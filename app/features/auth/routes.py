from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError, jwt
from app.core.config import settings

# from app.core.security import get_current_admin
from app.core.email import send_email
from app.core.helper import AppHelper
from app.core.templates.reset_email_successful_template import password_change_alert_template
from app.core.templates.reset_email_template import reset_email_template
from app.features.auth.dependencies import get_auth_service
from app.features.auth.schemas import EmailPasswordRequestForm, PasswordReset, PasswordResetRequest, Token, UserCreate
from app.features.auth.services import AuthService
# from app.features.users.models import UserModel

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=Token)
async def signup(
    user_data: UserCreate,
    service: AuthService = Depends(get_auth_service),
):
    token = await service.create_user(user_data, is_admin=False)
    return token

@router.post("/login", response_model=Token)
async def login(
    form_data: EmailPasswordRequestForm,
    service: AuthService = Depends(get_auth_service),
):
    return await service.login(form_data.email, form_data.password)

@router.post("/admin/create", response_model=Token)
async def create_admin(
    user_data: UserCreate,
    # current_admin: UserModel = Depends(get_current_admin),
    auth_service: AuthService = Depends(get_auth_service),
):
    existing_user = await auth_service.repo.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return await auth_service.create_user(user_data, is_admin=True)

@router.post("/forgot-password", response_model=dict[str, str])
async def forgot_password(
    request: PasswordResetRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    user = await auth_service.get_user_by_email(request.email)
    if user:
        reset_token = AppHelper.create_reset_token(user.email)
        reset_link = f"https://cli.menosi.net/auth/reset-password?token={reset_token}"
        body = f"""
Hello {user.first_name},

You have requested to reset your Menosi CLI password.
Please click the following link to reset your password:
{reset_link}

If you have not requested to reset your password, you can ignore this email.

Sincerely,
The Menosi CLI Team
"""
        await send_email(
            to=user.email,
            subject="Resetting your Menosi CLI password",
            body= body,
            html_body=reset_email_template(user.first_name, reset_link, f"{settings.RESET_TOKEN_EXPIRE_MINUTES}", user.email)
        )
        print(f"Reset token for {user.email}: {reset_token}")
    
    return {"message": "If the email exists, a reset link will be sent", "email": request.email, "expired_in": f"{settings.RESET_TOKEN_EXPIRE_MINUTES}"}

@router.post("/reset-password")
async def reset_password(
    reset_data: PasswordReset,
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        payload = jwt.decode(
            reset_data.token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        email: Optional[str] = payload.get("sub")
        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token"
        )
    await auth_service.update_password(email, reset_data.new_password)
    user = await auth_service.get_user_by_email(email)
    # Send reset successful email
    reset_time = datetime.now().strftime("%B %d, %Y at %I:%M %p %Z")
    body = f"""
Password Successfully Changed

Hello {user.first_name},

This email confirms that the password for your Menosi CLI account associated with {user.email} was successfully changed on {reset_time}.

If you did not request this change, please contact our support team immediately to secure your account.

Best regards,
The Menosi CLI Team
"""
    body_html = password_change_alert_template(user.first_name, email, reset_time)
    await send_email(email, "Password Reset Successful", body, body_html)
    return {"message": "Password reset successful"}

