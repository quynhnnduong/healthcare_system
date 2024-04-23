import csv
from fastapi import Depends, FastAPI, HTTPException, APIRouter
from sqlalchemy.orm import Session
from model.db import get_db
from model.patients import Patient  # Ensure your patient model import is correct

router = APIRouter(prefix="/encrypt", tags=["encrypt"])


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
