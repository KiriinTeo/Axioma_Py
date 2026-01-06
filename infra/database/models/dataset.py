from sqlalchemy import Column, String, ForeignKey, DateTime, Integer
from datetime import datetime, timezone
from infra.database.base import Base

class DatasetModel(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.id"), index=True)
    name = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
