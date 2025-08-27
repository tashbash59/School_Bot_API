from sqlalchemy import Column, BigInteger, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class UserGroupModel(Base):
    __tablename__ = "user_groups"

    user_id = Column(BigInteger, ForeignKey("users.id"), primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"), primary_key=True)
    user_role = Column(String(20), nullable=False)

    user = relationship("UserModel", back_populates="user_groups")
    group = relationship("GroupModel", back_populates="user_groups")