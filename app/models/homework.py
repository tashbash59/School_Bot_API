from sqlalchemy import Column, Integer, BigInteger, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class HomeworkModel(Base):
    __tablename__ = "homeworks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    assigned_by = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    deadline = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    group = relationship("GroupModel", back_populates="homeworks")
    assigner = relationship("UserModel", back_populates="assigned_homeworks")
    attachments = relationship("AttachmentModel", back_populates="homework")