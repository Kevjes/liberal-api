# app/core/helper.py
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional
import uuid, os
from fastapi import UploadFile
from app.core.config import settings
from passlib.context import CryptContext
from jose import jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AppHelper:

    @staticmethod
    def generate_new_uuid()-> str:
        return uuid.uuid4().hex
    
    @staticmethod
    def generate_random_bytes(length: int)-> bytes:
        return os.urandom(length)
    @staticmethod
    def is_date_valid(date_value: Any) -> bool:
        if not isinstance(date_value, datetime):
            try:
                date_value = datetime.fromisoformat(date_value)
            except ValueError:
                return False
        return date_value >= datetime.now(timezone.utc)

    @staticmethod
    def save_file(file: UploadFile, path: Path, file_name:Optional[str]=None) -> str:
        if file_name:
            new_file_name = file_name
        else:
            extension = file.filename.split('.')[-1] if file.filename is not None else 'jpg'
            new_file_name = f"{AppHelper.generate_new_uuid().replace('-', '')}.{extension}"
        file_path = path / new_file_name
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
        base_url = settings.DOMAIN_URL
        url = f"{base_url}/{path.parent}/{path.name}/{file_path.name}"
        return url
    
    @staticmethod
    def delete_file_from_url(url: Optional[str])-> None:
        if url is not None:
            base_url = settings.DOMAIN_URL
            file_path = url.replace(f"{base_url}/", "")
            file_path = Path(file_path)
            try:
                file_path.unlink()
            except FileNotFoundError:
                pass
            except PermissionError:
                pass

    @staticmethod
    def get_file_from_url(url: str)-> bytes:
        try:
            base_url = settings.DOMAIN_URL
            file_path = url.replace(f"{base_url}/", "")

            with open(file_path, "rb") as file:
                return file.read()
        except FileNotFoundError:
            raise FileNotFoundError
        
    @staticmethod
    def read_file(file_dir: Path)-> bytes:
        try:
            with open(file_dir, "rb") as file:
                return file.read()
        except FileNotFoundError:
            raise FileNotFoundError
        except PermissionError:
            raise PermissionError
        
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
        to_encode.update({"exp": int(expire.timestamp())})
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    @staticmethod
    def create_reset_token(email: str) -> str:
        expires = timedelta(minutes=settings.RESET_TOKEN_EXPIRE_MINUTES)
        return AppHelper.create_access_token({"sub": email}, expires_delta=expires)
    
    @staticmethod
    def add_days_without_timedelta(dt: datetime, days: int) -> datetime:
        new_date = datetime.fromordinal(dt.toordinal() + days)
        return datetime.combine(new_date.date(), dt.time())
    