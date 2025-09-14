# Smart City Management Platform — Starter Kit

This starter provides:
- FastAPI backend with JWT auth
- PostgreSQL + SQLAlchemy models
- MQTT ingestion via Mosquitto
- Threshold-based rule engine for alerts
- HTTP ingestion fallback
- Minimal React (Vite) UI
- Sensor simulator

## Quick start
1. `cp .env.example .env`
2. `docker compose up --build`
3. Open API docs: http://localhost:8000/docs
4. Default demo user (if seeding enabled): `admin@city.local` / `admin123`

## Notes
Harden security, add migrations and tests for production use.
