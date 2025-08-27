from sqlalchemy import Column, BigInteger, String, DateTime, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String(100))
    full_name = Column(String(200), nullable=False)
    role = Column(String(20), nullable=False)  # student/teacher/admin
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    created_groups = relationship("GroupModel", back_populates="creator")
    assigned_homeworks = relationship("HomeworkModel", back_populates="assigner")
    user_groups = relationship("UserGroupModel", back_populates="user")