import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from . import models
from .auth import get_password_hash

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "smartcity")
DB_USER = os.getenv("DB_USER", "city")
DB_PASSWORD = os.getenv("DB_PASSWORD", "city")
ALLOW_DEMO_SEED = os.getenv("ALLOW_DEMO_SEED", "false").lower() == "true"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def seed_demo_user_if_enabled():
    if not ALLOW_DEMO_SEED:
        return
    db = SessionLocal()
    try:
        Base.metadata.create_all(bind=engine)
        # Roles
        for r in ["admin", "environment_officer", "utility_officer", "traffic_control", "viewer"]:
            if not db.query(models.Role).filter_by(name=r).first():
                db.add(models.Role(name=r))
        db.commit()
        # Sensors
        if db.query(models.Sensor).count() == 0:
            db.add_all([
                models.Sensor(name="AQM-001", type="air_quality_pm25", location_lat=12.97, location_lng=77.59),
                models.Sensor(name="TRF-101", type="traffic_congestion", location_lat=12.98, location_lng=77.60),
                models.Sensor(name="WST-201", type="waste_level", location_lat=12.99, location_lng=77.61),
                models.Sensor(name="ENG-301", type="energy_usage", location_lat=13.00, location_lng=77.62),
            ])
            db.commit()
        # Admin
        admin_email = "admin@city.local"
        if not db.query(models.User).filter_by(email=admin_email).first():
            admin_role = db.query(models.Role).filter_by(name="admin").first()
            user = models.User(email=admin_email, password_hash=get_password_hash("admin123"), role_id=admin_role.id)
            db.add(user)
            db.commit()
    finally:
        db.close()
