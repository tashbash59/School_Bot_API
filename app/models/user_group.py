from sqlalchemy import Column, BigInteger, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class UserGroup(Base):
    __tablename__ = "user_groups"

    user_id = Column(BigInteger, ForeignKey("users.id"), primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"), primary_key=True)
    user_role = Column(String(20), nullable=False)

    user = relationship("User", back_populates="user_groups")
    group = relationship("Group", back_populates="user_groups")