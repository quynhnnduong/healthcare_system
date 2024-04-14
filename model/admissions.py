from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, String
from sqlalchemy.orm import relationship

from model import Base


class Admission(Base):
    __tablename__ = 'admissions'
    row_id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey('patients.subject_id'))
    hadm_id = Column(Integer, unique=True, nullable=False)
    admittime = Column(TIMESTAMP)
    dischtime = Column(TIMESTAMP)
    deathtime = Column(TIMESTAMP)
    admission_type = Column(String(50))
    admission_location = Column(String(50))
    discharge_location = Column(String(50))
    insurance = Column(String(255))
    language = Column(String(10))
    religion = Column(String(50))
    marital_status = Column(String(50))
    ethnicity = Column(String(200))
    edregtime = Column(TIMESTAMP)
    edouttime = Column(TIMESTAMP)
    diagnosis = Column(String(300))
    hospital_expire_flag = Column(Integer)
    has_chartevents_data = Column(Integer)

    patient = relationship("Patient", back_populates="admissions")
    icustays = relationship("ICUStay", back_populates="admission")
