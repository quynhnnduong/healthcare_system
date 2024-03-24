from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship

from .base import Base

class Patient(Base):
    __tablename__ = 'patients'

    ROW_ID = Column(Integer, primary_key=True)
    SUBJECT_ID = Column(Integer, unique=True, nullable=False)
    GENDER = Column(String(5))
    DOB = Column(TIMESTAMP)
    DOD = Column(TIMESTAMP)
    DOD_HOSP = Column(TIMESTAMP)
    DOD_SSN = Column(TIMESTAMP)
    EXPIRE_FLAG = Column(String(5))

    admissions = relationship("Admission", back_populates="patient")
    icustays = relationship("ICUStay", back_populates="patient")
