from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Liberal"
    DATABASE_URL: str
    SECRET_KEY: str 
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_FROM: str
    ALGORITHM: str = "HS256"
    DOMAIN_URL: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 3600
    RESET_TOKEN_EXPIRE_MINUTES: int = 15
    STATIC_FILES_DIR: Path = Path("static")
    PROFILE_IMAGE_DIR: Path = Path("static/profile_images")
    CARD_BACKGROUND_IMAGE_PATH: str = "static/card_background.png"
    CARD_DEFAULT_FONT: str = "Helvetica"
    ALLOWED_IMAGE_TYPES: set[str] = {"image/jpeg", "image/png", "image/webp"}

    class Config:
        env_file = ".env"

settings = Settings()