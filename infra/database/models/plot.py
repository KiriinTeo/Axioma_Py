from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from datetime import datetime, timezone
from infra.database.base import Base

class PlotModel(Base):
    __tablename__ = "plots"

    id = Column(String(50), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    dataset_id = Column(String(50), ForeignKey("datasets.id"), index=True)
    
    plot_type = Column(String(50), nullable=False)
    x_axis = Column(String(100))
    y_axis = Column(String(100))
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
