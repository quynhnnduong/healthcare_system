import csv
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from model import Patient, Admission
from model.db import get_db

router = APIRouter(prefix="/data-import", tags=["data-import"])


@router.post("/encrypt-patients/")
def encrypt_patients(db: Session = Depends(get_db)):
    try:
        with open('patientData/PATIENTS.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for idx, row in enumerate(reader):
                if row:  # Ensure the row is not None
                    try:
                        patient = db.query(Patient).filter_by(subject_id=int(row['subject_id'])).first()
                        if patient:
                            # Update existing patient
                            patient.gender = row['gender']  # Assuming gender is not encrypted
                            patient.dob = row['dob'] if row['dob'].strip() else None
                            patient.dod = row['dod'] if row['dod'].strip() else None
                            patient.dod_hosp = row['dod_hosp'] if row['dod_hosp'].strip() else None
                            patient.dod_ssn = row['dod_ssn'] if row['dod_ssn'].strip() else None
                            patient.expire_flag = row['expire_flag']
                        else:
                            # Add new patient
                            new_patient = Patient(
                                subject_id=int(row['subject_id']),
                                gender=row['gender'],
                                dob=row['dob'] if row['dob'].strip() else None,
                                dod=row['dod'] if row['dod'].strip() else None,
                                dod_hosp=row['dod_hosp'] if row['dod_hosp'].strip() else None,
                                dod_ssn=row['dod_ssn'] if row['dod_ssn'].strip() else None,
                                expire_flag=row['expire_flag']
                            )
                            db.add(new_patient)
                    except Exception as e:
                        print(f"Error processing row {idx}: {row}")
                        print(f"Error: {str(e)}")
                        continue
            db.commit()
        return {"status": "success", "message": "Patient data encrypted and stored successfully"}
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}


@router.post("/admissions/")
def import_admissions(db: Session = Depends(get_db)):
    try:
        with open('patientData/ADMISSIONS.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if not row:
                    continue
                hadm_id = int(row['hadm_id'])
                admission = db.query(Admission).filter(Admission.hadm_id == hadm_id).first()
                if admission:
                    # Update existing record
                    admission.subject_id = int(row['subject_id'])
                    admission.admittime = row['admittime'] if row['admittime'].strip() else None
                    admission.dischtime = row['dischtime'] if row['dischtime'].strip() else None
                    admission.deathtime = row['deathtime'].strip() if row['deathtime'].strip() else None
                    admission.admission_type = row['admission_type'].strip() if row['admission_type'].strip() else None
                    admission.admission_location = row['admission_location'].strip() if row[
                        'admission_location'].strip() else None
                    admission.discharge_location = row['discharge_location'].strip() if row[
                        'discharge_location'].strip() else None
                    admission.insurance = row['insurance'].strip() if row['insurance'].strip() else None
                    admission.language = row['language'].strip() if row['language'].strip() else None
                    admission.religion = row['religion'].strip() if row['religion'].strip() else None
                    admission.marital_status = row['marital_status'].strip() if row['marital_status'].strip() else None
                    admission.ethnicity = row['ethnicity'].strip() if row['ethnicity'].strip() else None
                    admission.edregtime = row['edregtime'] if row['edregtime'].strip() else None
                    admission.edouttime = row['edouttime'] if row['edouttime'].strip() else None
                    admission.diagnosis = row['diagnosis'].strip() if row['diagnosis'].strip() else None
                    admission.hospital_expire_flag = int(row['hospital_expire_flag']) if row[
                        'hospital_expire_flag'].strip() else 0
                    admission.has_chartevents_data = int(row['has_chartevents_data']) if row[
                        'has_chartevents_data'].strip() else 0
                else:
                    # Insert new record
                    new_admission = Admission(
                        hadm_id=hadm_id,
                        subject_id=int(row['subject_id']),
                        admittime=row['admittime'] if row['admittime'].strip() else None,
                        dischtime=row['dischtime'] if row['dischtime'].strip() else None,
                        deathtime=row['deathtime'].strip() if row['deathtime'].strip() else None,
                        admission_type=row['admission_type'].strip() if row['admission_type'].strip() else None,
                        admission_location=row['admission_location'].strip() if row[
                            'admission_location'].strip() else None,
                        discharge_location=row['discharge_location'].strip() if row[
                            'discharge_location'].strip() else None,
                        insurance=row['insurance'].strip() if row['insurance'].strip() else None,
                        language=row['language'].strip() if row['language'].strip() else None,
                        religion=row['religion'].strip() if row['religion'].strip() else None,
                        marital_status=row['marital_status'].strip() if row['marital_status'].strip() else None,
                        ethnicity=row['ethnicity'].strip() if row['ethnicity'].strip() else None,
                        edregtime=row['edregtime'].strip() if row['edregtime'].strip() else None,
                        edouttime=row['edouttime'].strip() if row['edouttime'].strip() else None,
                        diagnosis=row['diagnosis'].strip() if row['diagnosis'].strip() else None,
                        hospital_expire_flag=int(row['hospital_expire_flag']),
                        has_chartevents_data=int(row['has_chartevents_data'])
                    )
                    db.add(new_admission)
                try:
                    db.commit()
                except Exception as e:
                    db.rollback()
                    print(f"Failed to commit changes for row {hadm_id}: {e}")
        return {"status": "success", "message": "Admissions data imported successfully"}
    except Exception as e:
        db.rollback()
        print(f"Failed to import admissions data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
