from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship

from .base import Base


class Patient(Base):
    __tablename__ = 'patients'
    subject_id = Column(Integer, primary_key=True)
    gender = Column(String(5))
    dob = Column(TIMESTAMP)
    dod = Column(TIMESTAMP)
    dod_hosp = Column(TIMESTAMP)
    dod_ssn = Column(TIMESTAMP)
    expire_flag = Column(String(5))
    admissions = relationship("Admission", back_populates="patient")

