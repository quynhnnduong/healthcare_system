from sqlalchemy import Column, Integer, ForeignKey, String, TIMESTAMP, Float, Sequence
from sqlalchemy.orm import relationship

from model import Base


class ICUStay(Base):
    __tablename__ = 'icustays'
    icustay_id = Column(Integer, Sequence('icustays_icustay_id_seq'), primary_key=True, autoincrement=True)
    subject_id = Column(Integer, ForeignKey('patients.subject_id'))
    hadm_id = Column(Integer, ForeignKey('admissions.hadm_id'))
    dbsource = Column(String(20))
    first_careunit = Column(String(20))
    last_careunit = Column(String(20))
    first_wardid = Column(Integer)
    last_wardid = Column(Integer)
    intime = Column(TIMESTAMP)
    outtime = Column(TIMESTAMP)
    los = Column(Float)

    # patient = relationship("Patient", back_populates="icustays")
    admission = relationship("Admission", back_populates="icustays")