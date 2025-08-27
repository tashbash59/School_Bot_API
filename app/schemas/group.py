from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class GroupBase(BaseModel):
    name: str = Field(..., description="Название группы")
    description: Optional[str] = Field(None, description="Описание группы")
    created_by: int = Field(..., description="ID создателя группы")

class GroupCreate(GroupBase):
    pass

class GroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class Group(GroupBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True