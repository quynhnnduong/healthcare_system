from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, String
from sqlalchemy.orm import relationship

from model import Base


class Admission(Base):
    __tablename__ = 'admissions'

    ROW_ID = Column(Integer, primary_key=True)
    SUBJECT_ID = Column(Integer, ForeignKey('patients.SUBJECT_ID'))
    HADM_ID = Column(Integer, unique=True, nullable=False)
    ADMITTIME = Column(TIMESTAMP)
    DISCHTIME = Column(TIMESTAMP)
    DEATHTIME = Column(TIMESTAMP)
    ADMISSION_TYPE = Column(String(50))
    ADMISSION_LOCATION = Column(String(50))
    DISCHARGE_LOCATION = Column(String(50))
    INSURANCE = Column(String(255))
    LANGUAGE = Column(String(10))
    RELIGION = Column(String(50))
    MARITAL_STATUS = Column(String(50))
    ETHNICITY = Column(String(200))
    EDREGTIME = Column(TIMESTAMP)
    EDOUTTIME = Column(TIMESTAMP)
    DIAGNOSIS = Column(String(300))
    HOSPITAL_EXPIRE_FLAG = Column(Integer)
    HAS_CHARTEVENTS_DATA = Column(Integer)

    patient = relationship("Patient", back_populates="admissions")
    icustays = relationship("ICUStay", back_populates="admission")