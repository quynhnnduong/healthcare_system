# Healthcare Database System

## Overview 

This project is designed to create a secure database system for managing patient data within the healthcare domain. It integrates advanced encryption standards (AES) and a role-based access control framework to ensure data security and confidentiality.

## File Description
- `base.py`: Defines the SQLAlchemy Base class, which is a foundation for all model definitions and necessary for the ORM to map objects to database tables.

- `__init__.py`: Makes the model directory a package and allows easy importing of all models within the application.

- `patients.py`: Contains the Patient class which maps to the patients table in the database, including all patient-related fields and relationships with other tables.

- `admissions.py`: Contains the Admission class which maps to the admissions table in the database, including admission details and relationships to the Patient and ICUStay models.

- `icustays.py`: Contains the ICUStay class which maps to the icustays table in the database, including fields specific to ICU stays and relationships with the Patient and Admission models.

- `main.py`: The main script for initializing the database schema by creating tables based on the defined models.

- `db.py`:
  This file sets up the SQLAlchemy engine and sessionmaker. It is the core file for database interactions.

- `schema.sql`:
  An optional SQL script containing the schema definition for the database. It can be used to set up the database schema manually using PostgreSQL commands. Run this command to do manual database setup
  `psql -U <username> -d <databasename> -a -f schema.sql`
  
## Setup Instructions

1. Install Python 3 and pip on your system.
2. Install the required Python packages using pip: `pip install -r requirements.txt`


