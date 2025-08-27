from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class HomeworkBase(BaseModel):
    group_id: int = Field(..., description="ID группы")
    assigned_by: int = Field(..., description="ID назначившего")
    title: str = Field(..., description="Заголовок задания")
    description: Optional[str] = Field(None, description="Описание задания")
    deadline: datetime = Field(..., description="Срок сдачи")

class HomeworkCreate(HomeworkBase):
    pass

class HomeworkUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[datetime] = None

class Homework(HomeworkBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True