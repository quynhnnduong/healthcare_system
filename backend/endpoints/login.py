from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel
import bcrypt
from model import User, Patient, Admission
from model.db import get_db
from encryption.AESCipher import AESCipher
import os, base64
from typing import List, Optional

router = APIRouter(prefix="/login", tags=["login"])

# Load and initialize AES cipher
encoded_key = os.getenv("ENCRYPTION_KEY")
if not encoded_key:
    raise RuntimeError("ENCRYPTION_KEY is not set in the environment variables")
key = base64.b64decode(encoded_key)
aes_cipher = AESCipher(key)


class ICUStayInfo(BaseModel):
    icustay_id: int
    dbsource: str
    first_careunit: str
    last_careunit: str
    first_wardid: int
    last_wardid: int
    intime: str
    outtime: str
    los: float


class AdmissionInfo(BaseModel):
    hadm_id: int
    admittime: str
    dischtime: str
    deathtime: Optional[str]
    admission_type: str
    admission_location: str
    discharge_location: str
    insurance: str
    language: Optional[str]
    religion: Optional[str]
    marital_status: Optional[str]
    ethnicity: str
    edregtime: Optional[str]
    edouttime: Optional[str]
    diagnosis: str
    hospital_expire_flag: int
    has_chartevents_data: int
    icustays: List[ICUStayInfo] = []


class PatientInfo(BaseModel):
    subject_id: int
    gender: str
    dob: Optional[str] = None
    dod: Optional[str] = None
    dod_hosp: Optional[str] = None
    dod_ssn: Optional[str] = None
    expire_flag: str
    admissions: List[AdmissionInfo] = []


@router.post("/patient")
def patient_login(subject_id: int, dod_ssn: str, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter_by(subject_id=subject_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    if patient.dod_ssn != dod_ssn:
        raise HTTPException(status_code=401, detail="Unauthorized access: SSN mismatch")

    return {"subject_id": subject_id}


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return user
    return None


@router.post("/doctorNurse", response_model=List[PatientInfo])
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = authenticate_user(db, username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if user.role.role_name not in ["Doctor", "Nurse"]:
        raise HTTPException(status_code=403, detail="Access Denied")

    patients_treated = [10006, 10032, 10036, 10038, 10040, 10064, 10065, 10067, 10069, 10074]

    if user.role.role_name == "Doctor":
        # Only fetch patients that the doctor has treated
        patients = db.query(Patient).filter(Patient.subject_id.in_(patients_treated)).options(
            joinedload(Patient.admissions).joinedload(Admission.icustays)).all()

    elif user.role.role_name == "Nurse":
        patients = db.query(Patient).options(
            joinedload(Patient.admissions).joinedload(Admission.icustays)).all()
    else:
        raise HTTPException(status_code=404, detail="Role not found")

    return [PatientInfo(
        subject_id=patient.subject_id,
        gender=patient.gender,
        dob=patient.dob,
        dod=patient.dod,
        dod_hosp=patient.dod_hosp,
        dod_ssn=patient.dod_ssn,
        expire_flag=patient.expire_flag,
        admissions=[AdmissionInfo(
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
            icustays=[ICUStayInfo(
                icustay_id=icustay.icustay_id,
                dbsource=icustay.dbsource,
                first_careunit=icustay.first_careunit,
                last_careunit=icustay.last_careunit,
                first_wardid=icustay.first_wardid,
                last_wardid=icustay.last_wardid,
                intime=icustay.intime.isoformat() if icustay.intime else None,
                outtime=icustay.outtime.isoformat() if icustay.outtime else None,
                los=icustay.los
            ) for icustay in admission.icustays]
        ) for admission in patient.admissions]
    ) for patient in patients]
