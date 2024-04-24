from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class PatientInfo(BaseModel):
    row_id: int
    subject_id: int
    gender: Optional[str] = Field(None, max_length=5)
    dob: Optional[datetime] = None
    dod: Optional[datetime] = None
    dod_hosp: Optional[datetime] = None
    dod_ssn: Optional[datetime] = None
    expire_flag: Optional[str] = Field(None, max_length=5)

    class Config:
        orm_mode = True
