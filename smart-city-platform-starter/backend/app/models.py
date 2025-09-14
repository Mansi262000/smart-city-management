from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .db import Base

def utcnow():
    return datetime.now(timezone.utc)

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    users = relationship("User", back_populates="role")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role", back_populates="users")

class Sensor(Base):
    __tablename__ = "sensors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    type = Column(String(100), index=True)
    location_lat = Column(Float, nullable=True)
    location_lng = Column(Float, nullable=True)
    metrics = relationship("Metric", back_populates="sensor")

class Metric(Base):
    __tablename__ = "metrics"
    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(Integer, ForeignKey("sensors.id"), index=True, nullable=False)
    metric_type = Column(String(100), index=True)
    value = Column(Float, nullable=False)
    ts = Column(DateTime(timezone=True), default=utcnow, index=True)
    sensor = relationship("Sensor", back_populates="metrics")

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(Integer, ForeignKey("sensors.id"), index=True, nullable=False)
    metric_type = Column(String(100), index=True)
    severity = Column(String(20), index=True)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow, index=True)
    acknowledged = Column(Boolean, default=False, index=True)
    sensor = relationship("Sensor")
