from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db, SessionLocal
from app import models
from app.schemas import StartWipeRequest, VerifyWipeRequest, WipeHistoryResponse, WipeLogOut
from app.auth import get_current_user
from app.utils.wipe_engine import run_wipe

router = APIRouter()

WIPE_METHODS = {"NIST", "DoD 5220.22-M", "Gutmann", "Quick Zero Fill"}

def _do_wipe_background(wipe_id: int, method: str, device_uid: str, size_mb: int):
    db: Session = SessionLocal()
    try:
        log = db.get(models.WipeLog, wipe_id)
        if not log:
            return
        try:
            # Run actual wiping logic (virtual device file)
            run_wipe(method=method, device_uid=device_uid, wipe_id=wipe_id, size_mb=size_mb)
            log.status = models.WipeStatus.wiped
            log.completed_at = datetime.utcnow()
        except Exception as e:
            log.status = models.WipeStatus.failed
        db.add(log)
        db.commit()
    finally:
        db.close()

@router.post("/start", response_model=WipeLogOut)
def start_wipe(
    payload: StartWipeRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    if payload.method not in WIPE_METHODS:
        raise HTTPException(status_code=400, detail="Unsupported wipe method")
    device = db.query(models.Device).filter(models.Device.device_uid == payload.device_uid).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    log = models.WipeLog(
        device_id=device.id,
        device_uid=device.device_uid,
        method=payload.method,
        status=models.WipeStatus.in_progress,
        user_id=user.id,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    # Launch background wipe with DoD and NIST logic implemented
    background_tasks.add_task(_do_wipe_background, log.id, payload.method, device.device_uid, payload.size_mb)
    return WipeLogOut.model_validate(log)

@router.post("/verify", response_model=WipeLogOut)
def verify_wipe(payload: VerifyWipeRequest, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    log = db.query(models.WipeLog).filter(models.WipeLog.id == payload.wipe_id, models.WipeLog.user_id == user.id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Wipe log not found")
    # Prototype AI verification -> mark as verified if wiped already
    if log.status == models.WipeStatus.wiped:
        log.status = models.WipeStatus.verified
        db.add(log)
        db.commit()
        db.refresh(log)
    return WipeLogOut.model_validate(log)

@router.get("", response_model=WipeHistoryResponse)
def history(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    logs = (
        db.query(models.WipeLog)
        .filter(models.WipeLog.user_id == user.id)
        .order_by(models.WipeLog.started_at.desc())
        .all()
    )
    return {"items": [WipeLogOut.model_validate(x) for x in logs]}