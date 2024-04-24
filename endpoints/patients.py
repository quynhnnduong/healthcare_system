import base64
import os
from typing import List, Optional

from fastapi import Depends, HTTPException, Security, FastAPI, APIRouter
from fastapi.security import OAuth2PasswordBearer
from pydantic import Field, BaseModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload
from typing_extensions import Sequence
from sqlalchemy import func

from encryption.AESCipher import AESCipher
from endpoints.login import AdmissionInfo, ICUStayInfo, PatientInfo
from model import User, Role, Patient, Admission, ICUStay
from model.db import get_db

router = APIRouter(prefix="/patient", tags=["patient"])

# Load and initialize AES cipher
encoded_key = os.getenv("ENCRYPTION_KEY")
if not encoded_key:
    raise RuntimeError("ENCRYPTION_KEY is not set in the environment variables")
key = base64.b64decode(encoded_key)
aes_cipher = AESCipher(key)


class ICUStayRequest(BaseModel):
    icustay_id: int
    dbsource: Optional[str] = None
    first_careunit: Optional[str] = None
    last_careunit: Optional[str] = None
    first_wardid: Optional[int] = None
    last_wardid: Optional[int] = None
    intime: Optional[str] = None
    outtime: Optional[str] = None
    los: Optional[float] = None


class AdmissionRequest(BaseModel):
    hadm_id: int
    admittime: Optional[str] = None
    dischtime: Optional[str] = None
    deathtime: Optional[str] = None
    admission_type: Optional[str] = None
    admission_location: Optional[str] = None
    discharge_location: Optional[str] = None
    insurance: Optional[str] = None
    language: Optional[str] = None
    religion: Optional[str] = None
    marital_status: Optional[str] = None
    ethnicity: Optional[str] = None
    edregtime: Optional[str] = None
    edouttime: Optional[str] = None
    diagnosis: Optional[str] = None
    hospital_expire_flag: Optional[int] = None
    has_chartevents_data: Optional[int] = None
    icustays: List[ICUStayRequest] = []


class PatientUpdateRequest(BaseModel):
    subject_id: int
    gender: Optional[str] = None
    dob: Optional[str] = None
    dod: Optional[str] = None
    dod_hosp: Optional[str] = None
    dod_ssn: Optional[str] = None
    expire_flag: Optional[str] = None
    admissions: List[AdmissionRequest] = []


class ICUStayCreateRequest(BaseModel):
    dbsource: Optional[str] = None
    first_careunit: Optional[str] = None
    last_careunit: Optional[str] = None
    first_wardid: Optional[int] = None
    last_wardid: Optional[int] = None
    intime: Optional[str] = None
    outtime: Optional[str] = None
    los: Optional[float] = None


class AdmissionCreateRequest(BaseModel):
    admittime: Optional[str] = None
    dischtime: Optional[str] = None
    deathtime: Optional[str] = None
    admission_type: Optional[str] = None
    admission_location: Optional[str] = None
    discharge_location: Optional[str] = None
    insurance: Optional[str] = None
    language: Optional[str] = None
    religion: Optional[str] = None
    marital_status: Optional[str] = None
    ethnicity: Optional[str] = None
    edregtime: Optional[str] = None
    edouttime: Optional[str] = None
    diagnosis: Optional[str] = None
    hospital_expire_flag: Optional[int] = None
    has_chartevents_data: Optional[int] = None
    icustays: List[ICUStayCreateRequest] = []


class PatientCreateRequest(BaseModel):
    subject_id: Optional[int] = None
    gender: Optional[str] = None
    dob: Optional[str] = None
    dod: Optional[str] = None
    dod_hosp: Optional[str] = None
    dod_ssn: Optional[str] = None
    expire_flag: Optional[str] = None
    admissions: List[AdmissionCreateRequest] = []


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


@router.put("/{subject_id}/update", response_model=dict)
def update_patient(subject_id: int, update_data: PatientUpdateRequest, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.subject_id == subject_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    try:
        if update_data.gender is not None:
            patient.gender = update_data.gender
        if update_data.dob is not None:
            patient.dob = update_data.dob
        if update_data.dod is not None:
            patient.dod = update_data.dod
        if update_data.dod_hosp is not None:
            patient.dod_hosp = update_data.dod_hosp
        if update_data.dod_ssn is not None:
            patient.dod_ssn = update_data.dod_ssn
        if update_data.expire_flag is not None:
            patient.expire_flag = update_data.expire_flag

        # Update admission and icustay fields
        for admission_update in update_data.admissions:
            admission = db.query(Admission).filter(Admission.hadm_id == admission_update.hadm_id,
                                                   Admission.patient == patient).first()
            if admission:
                for field, value in admission_update.dict(exclude_unset=True, exclude={'icustays'}).items():
                    if value is not None:
                        setattr(admission, field, value)

                # Update icustay fields
                for icustay_update in admission_update.icustays:
                    icustay = db.query(ICUStay).filter(ICUStay.icustay_id == icustay_update.icustay_id,
                                                       ICUStay.admission == admission).first()
                    if icustay:
                        for field, value in icustay_update.dict(exclude_unset=True).items():
                            if value is not None:
                                setattr(icustay, field, value)
        db.commit()
        return {"status": "success", "message": f"Patient {subject_id} information updated successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create", response_model=dict)
def create_patient(patient_data: PatientCreateRequest, db: Session = Depends(get_db)):
    # Check if patient already exists
    existing_patient = db.query(Patient).filter(Patient.subject_id == patient_data.subject_id).first()
    if existing_patient:
        raise HTTPException(status_code=400, detail="Patient already exists with this Subject ID")

    # If subject_id is not provided, generate a new one
    if not patient_data.subject_id:
        max_id = db.query(func.max(Patient.subject_id)).scalar() or 0
        patient_data.subject_id = max_id + 1

    max_row_id = db.query(func.max(Patient.row_id)).scalar() or 0

    # Create new patient
    try:
        new_patient = Patient(
            row_id=max_row_id + 1,
            subject_id=patient_data.subject_id,
            gender=patient_data.gender,
            dob=patient_data.dob,
            dod=patient_data.dod,
            dod_hosp=patient_data.dod_hosp,
            dod_ssn=patient_data.dod_ssn,
            expire_flag=patient_data.expire_flag
        )
        db.add(new_patient)

        # Add admissions and icustays if provided
        for admission_data in patient_data.admissions:
            new_admission = Admission(
                subject_id=new_patient.subject_id,
                hadm_id=func.nextval('admissions_hadm_id_seq'),
                **admission_data.dict(exclude_unset=True, exclude={'icustays'})
            )
            db.add(new_admission)

            # Handle icustays
            for icustay_data in admission_data.icustays:
                new_icustay = ICUStay(
                    icustay_id=func.nextval('icustays_icustay_id_seq'),
                    subject_id=new_patient.subject_id,
                    hadm_id=new_admission.hadm_id,
                    **icustay_data.dict(exclude_unset=True)
                )
                db.add(new_icustay)

        db.commit()

        return {"status": "success", "message": f"New patient {patient_data.subject_id} created successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
