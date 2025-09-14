from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import Base, engine, seed_demo_user_if_enabled
from .routers import auth, sensors, metrics, alerts
from .mqtt_client import start_mqtt_background

app = FastAPI(title="Smart City Platform API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
seed_demo_user_if_enabled()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(sensors.router, prefix="/sensors", tags=["sensors"])
app.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
app.include_router(alerts.router, prefix="/alerts", tags=["alerts"])

@app.on_event("startup")
async def startup_event():
    start_mqtt_background()

@app.get("/health")
def health():
    return {"status": "ok"}
