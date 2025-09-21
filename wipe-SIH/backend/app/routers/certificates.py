from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app import models
from app.auth import get_current_user
from app.utils.pdf import generate_certificate_pdf

router = APIRouter()

@router.get("/{wipe_id}.pdf")
def certificate_pdf(wipe_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    log = db.query(models.WipeLog).filter(models.WipeLog.id == wipe_id, models.WipeLog.user_id == user.id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Wipe log not found")
    if log.status not in [models.WipeStatus.wiped, models.WipeStatus.verified]:
        raise HTTPException(status_code=400, detail="Wipe not completed")
    device = db.get(models.Device, log.device_id)
    pdf_bytes = generate_certificate_pdf(
        certificate_id=f"CERT-{wipe_id:06d}",
        user_email=user.email,
        device_uid=log.device_uid,
        device_name=device.name if device else "Unknown",
        method=log.method,
        status=log.status.value,
        date=datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    )
    headers = {
        "Content-Disposition": f'inline; filename="wipechain-certificate-{wipe_id}.pdf"'
    }
    return Response(content=pdf_bytes, media_type="application/pdf", headers=headers)