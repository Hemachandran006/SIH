from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, func, Text
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class WipeStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    wiped = "wiped"
    verified = "verified"
    failed = "failed"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    logs = relationship("WipeLog", back_populates="user")

class Device(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, index=True)
    device_uid = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)  # disk, phone
    logs = relationship("WipeLog", back_populates="device")

class WipeLog(Base):
    __tablename__ = "wipe_logs"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    device_uid = Column(String(255), index=True, nullable=False)
    method = Column(String(100), nullable=False) # NIST, DoD, etc.
    status = Column(Enum(WipeStatus), default=WipeStatus.pending, nullable=False)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    certificate_url = Column(Text, nullable=True)

    device = relationship("Device", back_populates="logs")
    user = relationship("User", back_populates="logs")