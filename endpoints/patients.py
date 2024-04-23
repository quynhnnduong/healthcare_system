# from typing import List
#
# from fastapi import Depends, HTTPException, Security, FastAPI
# from fastapi.security import OAuth2PasswordBearer
# from sqlalchemy.orm import Session
#
# from model import User, Role, role_permissions, Permission, Patient
# from model.db import get_db
# from schema.patient import PatientInfo
#
# app = FastAPI()
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#
#
# def get_current_user_permissions(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> list:
#     user = db.query(User).filter(User.username == token).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     permissions = [perm.permission_name for perm in user.role.permissions]
#     return permissions
#
#
# def has_permission(permission: str):
#     def permission_checker(permissions: list = Depends(get_current_user_permissions)):
#         if permission not in permissions:
#             raise HTTPException(status_code=403, detail="Permission denied")
#
#     return permission_checker
#
#
# @app.get("/patients/", response_model=List[PatientInfo])
# def view_all_patients(permissions: List[str] = Depends(get_current_user_permissions), db: Session = Depends(get_db)):
#     if 'view_all_patients' not in permissions:
#         raise HTTPException(status_code=403, detail="Permission denied")
#
#     patients = db.query(Patient).all()
#     return patients
#
#
# @app.get("/patients/{subject_id}")
# def read_patient(subject_id: int, permissions: list = Depends(get_current_user_permissions),
#                  db: Session = Depends(get_db)):
#     if 'view_patient' not in permissions:
#         raise HTTPException(status_code=403, detail="Permission denied")
#
#     patient = db.query(Patient).filter(Patient.subject_id == subject_id).first()
#     if patient is None:
#         raise HTTPException(status_code=404, detail="Patient not found")
#
#     # if 'Doctor' in permissions: return full patient record
#     # if 'Patient' in permissions: return limited fields
#     return patient
#
#
# @app.put("/patients/{subject_id}")
# def update_patient(subject_id: int, patient_data: PatientInfo,
#                    permissions: list = Depends(get_current_user_permissions), db: Session = Depends(get_db)):
#     if 'edit_patient' not in permissions:
#         raise HTTPException(status_code=403, detail="Permission denied")
#
#     # Retrieve the existing patient record
#     patient = db.query(Patient).filter(Patient.subject_id == subject_id).first()
#     if not patient:
#         raise HTTPException(status_code=404, detail="Patient not found")
#
#     # Update fields if provided
#     if patient_data.gender:
#         patient.gender = patient_data.gender
#     if patient_data.dob:
#         patient.dob = patient_data.dob
#     if patient_data.dod:
#         patient.dod = patient_data.dod
#     if patient_data.dod_hosp:
#         patient.dod_hosp = patient_data.dod_hosp
#     if patient_data.dod_ssn:
#         patient.dod_ssn = patient_data.dod_ssn
#     if patient_data.expire_flag:
#         patient.expire_flag = patient_data.expire_flag
#
#     db.commit()
#     return {"message": "Patient updated successfully", "patient": patient}
