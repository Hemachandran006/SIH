from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
from app.auth import get_password_hash
from datetime import datetime, timedelta
import random

def seed_demo():
    db: Session = SessionLocal()
    try:
        # Seed user
        demo = db.query(models.User).filter(models.User.email == "demo@wipechain.dev").first()
        if not demo:
            demo = models.User(email="demo@wipechain.dev", hashed_password=get_password_hash("demo1234"), full_name="Demo User")
            db.add(demo)
            db.commit()
            db.refresh(demo)

        # Seed devices
        device_uids = ["DEV-ALPHA01", "DEV-BRAVO02", "DEV-CHARLIE3"]
        names = ["Aurora", "Nimbus", "Zenith"]
        types = ["disk", "phone", "disk"]
        for uid, n, t in zip(device_uids, names, types):
            if not db.query(models.Device).filter(models.Device.device_uid == uid).first():
                db.add(models.Device(device_uid=uid, name=n, type=t))
        db.commit()

        # Seed wipe logs
        methods = ["NIST", "DoD 5220.22-M", "Gutmann", "Quick Zero Fill"]
        devices = db.query(models.Device).all()
        existing = db.query(models.WipeLog).count()
        if existing < 5:
            for i in range(5):
                d = random.choice(devices)
                status = random.choice([models.WipeStatus.wiped, models.WipeStatus.verified])
                started = datetime.utcnow() - timedelta(days=random.randint(1, 10), hours=random.randint(0, 23))
                completed = started + timedelta(minutes=random.randint(2, 30))
                db.add(models.WipeLog(
                    device_id=d.id,
                    device_uid=d.device_uid,
                    method=random.choice(methods),
                    status=status,
                    started_at=started,
                    completed_at=completed,
                    user_id=demo.id,
                    certificate_url=None
                ))
            db.commit()
    finally:
        db.close()