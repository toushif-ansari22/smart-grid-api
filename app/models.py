from sqlalchemy import Column, String, Float, DateTime, Integer
from pydantic import BaseModel
from datetime import datetime
from .database import Base

# SQLAlchemy DB Model
class MeterReading(Base):
    __tablename__ = "meter_readings"
    id = Column(Integer, primary_key=True, index=True)
    meter_id = Column(String, index=True)
    voltage = Column(Float)
    current = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    city_zone = Column(String)

# Pydantic Request Model
class MeterReadingIn(BaseModel):
    meter_id: str
    voltage: float
    current: float
    city_zone: str

# Pydantic Response Model
class MeterReadingOut(MeterReadingIn):
    id: int
    timestamp: datetime
    class Config:
        from_attributes = True