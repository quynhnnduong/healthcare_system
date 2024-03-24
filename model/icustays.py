from sqlalchemy import Column, Integer, ForeignKey, String, TIMESTAMP, Float
from sqlalchemy.orm import relationship

from model import Base


class ICUStay(Base):
    __tablename__ = 'icustays'

    ROW_ID = Column(Integer, primary_key=True)
    SUBJECT_ID = Column(Integer, ForeignKey('patients.SUBJECT_ID'))
    HADM_ID = Column(Integer, ForeignKey('admissions.HADM_ID'))
    ICUSTAY_ID = Column(Integer, unique=True, nullable=False)
    DBSOURCE = Column(String(20))
    FIRST_CAREUNIT = Column(String(20))
    LAST_CAREUNIT = Column(String(20))
    FIRST_WARDID = Column(Integer)
    LAST_WARDID = Column(Integer)
    INTIME = Column(TIMESTAMP)
    OUTTIME = Column(TIMESTAMP)
    LOS = Column(Float)

    patient = relationship("Patient", back_populates="icustays")
    admission = relationship("Admission", back_populates="icustays")