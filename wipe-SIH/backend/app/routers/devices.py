from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.schemas import ScanResponse, DeviceOut
import random, string

router = APIRouter()

DEVICE_NAMES = ["Aurora", "Nimbus", "Zenith", "Quasar", "Vertex", "Onyx"]
DEVICE_TYPES = ["disk", "phone"]

def random_uid():
    return "DEV-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))

@router.post("/scan", response_model=ScanResponse)
def scan_device(db: Session = Depends(get_db)):
    # Simulate discovering a device
    uid = random_uid()
    name = random.choice(DEVICE_NAMES)
    dtype = random.choice(DEVICE_TYPES)
    device = models.Device(device_uid=uid, name=name, type=dtype)
    db.add(device)
    db.commit()
    db.refresh(device)
    return {"device": DeviceOut.model_validate(device)}