from sqlalchemy import Column, String, ForeignKey, DateTime, Integer, Text
from datetime import datetime, timezone
from infra.database.base import Base

class DatasetModel(Base):
    __tablename__ = "datasets"

    id = Column(String(50), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    name = Column(String(100))

    num_rows = Column("row_count", Integer)
    num_columns = Column("column_count", Integer)
    metadados = Column(Text)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
