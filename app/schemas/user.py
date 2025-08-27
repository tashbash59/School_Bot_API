from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    telegram_id: int = Field(..., description="Уникальный ID в Telegram")
    username: Optional[str] = Field(None, description="Юзернейм")
    full_name: str = Field(..., description="ФИО пользователя")
    role: str = Field(..., description="Роль (student/teacher/admin)")

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    username: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[str] = None

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True