from pydantic import BaseModel, Field

class UserGroupBase(BaseModel):
    user_id: int = Field(..., description="ID пользователя")
    group_id: int = Field(..., description="ID группы")
    user_role: str = Field(..., description="Роль в группе (member/admin)")

class UserGroupCreate(UserGroupBase):
    pass

class UserGroup(UserGroupBase):
    class Config:
        from_attributes = True