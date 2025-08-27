from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String(100))
    full_name = Column(String(200), nullable=False)
    role = Column(String(20), nullable=False)  # student/teacher/admin
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    created_groups = relationship("Group", back_populates="creator")
    assigned_homeworks = relationship("Homework", back_populates="assigner")
    user_groups = relationship("UserGroup", back_populates="user")