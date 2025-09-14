from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..db import get_db
from .. import models, schemas
from ..auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[schemas.AlertOut])
def list_alerts(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(models.Alert).order_by(models.Alert.created_at.desc()).limit(200).all()

@router.patch("/{alert_id}", response_model=schemas.AlertOut)
def acknowledge_alert(alert_id: int, payload: schemas.AcknowledgeIn, db: Session = Depends(get_db), user=Depends(get_current_user)):
    alert = db.query(models.Alert).get(alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert.acknowledged = payload.acknowledged
    db.commit()
    db.refresh(alert)
    return alert
