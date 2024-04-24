import base64

from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship

from encryption.AESCipher import AESCipher
from .base import Base
from dotenv import load_dotenv
import os

load_dotenv()

encoded_key = os.getenv("ENCRYPTION_KEY")
if encoded_key is None:
    raise ValueError("ENCRYPTION_KEY is not set in the environment variables")

key = base64.b64decode(encoded_key)
aes_cipher = AESCipher(key)


class Patient(Base):
    __tablename__ = 'patients'
    row_id = Column(Integer, primary_key=True, autoincrement=True)
    subject_id = Column(Integer, unique=True, nullable=False)
    gender = Column(String(5))
    _dob = Column("dob", String)
    _dod = Column("dod", String)
    _dod_hosp = Column("dod_hosp", String)
    _dod_ssn = Column("dod_ssn", String)
    expire_flag = Column(String(5))
    admissions = relationship("Admission", back_populates="patient")

    @property
    def dob(self):
        try:
            return aes_cipher.decrypt(self._dob) if self._dob else None
        except Exception as e:
            raise ValueError(f"Error decrypting DOB: {e}")

    @dob.setter
    def dob(self, value):
        try:
            self._dob = aes_cipher.encrypt(value) if value else None
        except Exception as e:
            raise ValueError(f"Error encrypting DOB: {e}")

    @property
    def dod(self):
        try:
            return aes_cipher.decrypt(self._dod) if self._dod else None
        except Exception as e:
            raise ValueError(f"Error decrypting DOD: {e}")

    @dod.setter
    def dod(self, value):
        try:
            self._dod = aes_cipher.encrypt(value) if value else None
        except Exception as e:
            raise ValueError(f"Error encrypting DOD: {e}")

    @property
    def dod_hosp(self):
        try:
            return aes_cipher.decrypt(self._dod_hosp) if self._dod_hosp else None
        except Exception as e:
            raise ValueError(f"Error decrypting DOD_HOSP: {e}")

    @dod_hosp.setter
    def dod_hosp(self, value):
        try:
            self._dod_hosp = aes_cipher.encrypt(value) if value else None
        except Exception as e:
            raise ValueError(f"Error encrypting DOD_HOSP: {e}")

    @property
    def dod_ssn(self):
        try:
            return aes_cipher.decrypt(self._dod_ssn) if self._dod_ssn else None
        except Exception as e:
            raise ValueError(f"Error decrypting DOD_SSN: {e}")

    @dod_ssn.setter
    def dod_ssn(self, value):
        try:
            self._dod_ssn = aes_cipher.encrypt(value) if value else None
        except Exception as e:
            raise ValueError(f"Error encrypting DOD_SSN: {e}")