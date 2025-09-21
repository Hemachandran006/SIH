from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from app.models import WipeStatus

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class DeviceOut(BaseModel):
    id: int
    device_uid: str
    name: str
    type: str
    class Config:
        from_attributes = True

class ScanResponse(BaseModel):
    device: DeviceOut

class StartWipeRequest(BaseModel):
    device_uid: str
    method: str = Field(description="Wipe method: NIST, DoD 5220.22-M, Gutmann, Quick Zero Fill")
    size_mb: int = Field(default=32, ge=1, le=512, description="Virtual device size for wiping (MB).")

class VerifyWipeRequest(BaseModel):
    wipe_id: int

class WipeLogOut(BaseModel):
    id: int
    device_uid: str
    method: str
    status: WipeStatus
    started_at: datetime
    completed_at: Optional[datetime] = None
    certificate_url: Optional[str] = None
    class Config:
        from_attributes = True

class WipeHistoryResponse(BaseModel):
    items: List[WipeLogOut]