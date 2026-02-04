from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from datetime import datetime, timezone
from infra.database.base import Base

class FilterModel(Base):
    __tablename__ = "filters"

    id = Column(String(50), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    dataset_id = Column(String(50), ForeignKey("datasets.id"), index=True)
    
    column_name = Column("col_name", String(100), nullable=False)
    operator = Column(String(20), nullable=False)
    value = Column(String(255), nullable=False)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
