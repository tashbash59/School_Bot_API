from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class AttachmentBase(BaseModel):
    homework_id: int = Field(..., description="ID домашнего задания")
    file_id: str = Field(..., description="File ID от Telegram")
    file_type: str = Field(..., description="Тип файла")
    file_name: str = Field(..., description="Имя файла")
    caption: Optional[str] = Field(None, description="Подпись к файлу")

class AttachmentCreate(AttachmentBase):
    pass

class AttachmentUpdate(BaseModel):
    caption: Optional[str] = None

class Attachment(AttachmentBase):
    id: int
    uploaded_at: datetime

    class Config:
        from_attributes = True