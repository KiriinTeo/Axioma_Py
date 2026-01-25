from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from datetime import datetime, timezone
from infra.database.base import Base

class ExportModel(Base):
    __tablename__ = "exports"

    id = Column(String(50), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    dataset_id = Column(String(50), ForeignKey("datasets.id"), index=True)
    
    file_path = Column(String(500), nullable=False)
    file_format = Column(String(20), default="csv")
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
