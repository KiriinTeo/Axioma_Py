from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Text
from datetime import datetime, timezone
from infra.database.base import Base

class AnalysisModel(Base):
    __tablename__ = "analyses"

    id = Column(String(50), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    dataset_id = Column(String(50), ForeignKey("datasets.id"), index=True)
    
    analysis_type = Column(String(50), nullable=False)
    result = Column(Text, nullable=False)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
