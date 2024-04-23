import base64
import os
from typing import List

from fastapi import Depends, HTTPException, Security, FastAPI, APIRouter
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session, joinedload

from encryption.AESCipher import AESCipher
from endpoints.login import AdmissionInfo, ICUStayInfo, PatientInfo
from model import User, Role, Patient, Admission
from model.db import get_db

router = APIRouter(prefix="/patient", tags=["patient"])

# Load and initialize AES cipher
encoded_key = os.getenv("ENCRYPTION_KEY")
if not encoded_key:
    raise RuntimeError("ENCRYPTION_KEY is not set in the environment variables")
key = base64.b64decode(encoded_key)
aes_cipher = AESCipher(key)


@router.get("/{subject_id}", response_model=PatientInfo)
def get_patient(subject_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).options(joinedload(Patient.admissions).joinedload(Admission.icustays)).filter_by(
        subject_id=subject_id).first()

    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    return PatientInfo(
        subject_id=patient.subject_id,
        gender=patient.gender,
        dob=patient.dob,
        dod=patient.dod,
        dod_hosp=patient.dod_hosp,
        dod_ssn=patient.dod_ssn,
        expire_flag=patient.expire_flag,
        admissions=[
            AdmissionInfo(
                hadm_id=admission.hadm_id,
                admittime=admission.admittime.isoformat() if admission.admittime else None,
                dischtime=admission.dischtime.isoformat() if admission.dischtime else None,
                deathtime=admission.deathtime.isoformat() if admission.deathtime else None,
                admission_type=admission.admission_type,
                admission_location=admission.admission_location,
                discharge_location=admission.discharge_location,
                insurance=admission.insurance,
                language=admission.language,
                religion=admission.religion,
                marital_status=admission.marital_status,
                ethnicity=admission.ethnicity,
                edregtime=admission.edregtime.isoformat() if admission.edregtime else None,
                edouttime=admission.edouttime.isoformat() if admission.edouttime else None,
                diagnosis=admission.diagnosis,
                hospital_expire_flag=admission.hospital_expire_flag,
                has_chartevents_data=admission.has_chartevents_data,
                icustays=[
                    ICUStayInfo(
                        icustay_id=icustay.icustay_id,
                        dbsource=icustay.dbsource,
                        first_careunit=icustay.first_careunit,
                        last_careunit=icustay.last_careunit,
                        first_wardid=icustay.first_wardid,
                        last_wardid=icustay.last_wardid,
                        intime=icustay.intime.isoformat() if icustay.intime else None,
                        outtime=icustay.outtime.isoformat() if icustay.outtime else None,
                        los=icustay.los
                    )
                    for icustay in admission.icustays
                ]
            )
            for admission in patient.admissions
        ]
    )
