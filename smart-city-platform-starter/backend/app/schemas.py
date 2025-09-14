from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class SensorCreate(BaseModel):
    name: str
    type: str
    location_lat: Optional[float] = None
    location_lng: Optional[float] = None

class SensorOut(BaseModel):
    id: int
    name: str
    type: str
    location_lat: Optional[float]
    location_lng: Optional[float]
    class Config:
        from_attributes = True

class MetricIn(BaseModel):
    sensor_id: int
    type: str = Field(alias="metric_type")
    value: float
    ts: Optional[datetime] = None

class MetricOut(BaseModel):
    id: int
    sensor_id: int
    metric_type: str
    value: float
    ts: datetime
    class Config:
        from_attributes = True

class AlertOut(BaseModel):
    id: int
    sensor_id: int
    metric_type: str
    severity: str
    message: str
    created_at: datetime
    acknowledged: bool
    class Config:
        from_attributes = True

class AcknowledgeIn(BaseModel):
    acknowledged: bool = True

class SummaryPoint(BaseModel):
    metric_type: str
    count: int
    avg: float
    min: float
    max: float
