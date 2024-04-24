-- Create patients table
CREATE TABLE IF NOT EXISTS patients (
    ROW_ID INT PRIMARY KEY,
    SUBJECT_ID INT UNIQUE NOT NULL,
    GENDER VARCHAR(5),
    DOB TIMESTAMP(0),
    DOD TIMESTAMP(0),
    DOD_HOSP TIMESTAMP(0),
    DOD_SSN TIMESTAMP(0),
    EXPIRE_FLAG VARCHAR(5)
);

-- Create admissions table
CREATE TABLE IF NOT EXISTS admissions (
    ROW_ID INT PRIMARY KEY,
    SUBJECT_ID INT NOT NULL,
    HADM_ID INT UNIQUE NOT NULL,
    ADMITTIME TIMESTAMP(0),
    DISCHTIME TIMESTAMP(0),
    DEATHTIME TIMESTAMP(0),
    ADMISSION_TYPE VARCHAR(50),
    ADMISSION_LOCATION VARCHAR(50),
    DISCHARGE_LOCATION VARCHAR(50),
    INSURANCE VARCHAR(255),
    LANGUAGE VARCHAR(10),
    RELIGION VARCHAR(50),
    MARITAL_STATUS VARCHAR(50),
    ETHNICITY VARCHAR(200),
    EDREGTIME TIMESTAMP(0),
    EDOUTTIME TIMESTAMP(0),
    DIAGNOSIS VARCHAR(300),
    HOSPITAL_EXPIRE_FLAG SMALLINT,
    HAS_CHARTEVENTS_DATA SMALLINT,
    FOREIGN KEY (SUBJECT_ID) REFERENCES patients(SUBJECT_ID)
);

-- Create icustays table
CREATE TABLE IF NOT EXISTS icustays (
    ROW_ID INT PRIMARY KEY,
    SUBJECT_ID INT NOT NULL,
    HADM_ID INT NOT NULL,
    ICUSTAY_ID INT UNIQUE NOT NULL,
    DBSOURCE VARCHAR(20),
    FIRST_CAREUNIT VARCHAR(20),
    LAST_CAREUNIT VARCHAR(20),
    FIRST_WARDID SMALLINT,
    LAST_WARDID SMALLINT,
    INTIME TIMESTAMP(0),
    OUTTIME TIMESTAMP(0),
    LOS DOUBLE PRECISION,
    FOREIGN KEY (SUBJECT_ID) REFERENCES patients(SUBJECT_ID),
    FOREIGN KEY (HADM_ID) REFERENCES admissions(HADM_ID)
);

CREATE TABLE users (
    user_id INT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,  -- Store hashed passwords, not plain text
    role_id INT,
    FOREIGN KEY (role_id) REFERENCES roles(role_id)
);
CREATE TABLE roles (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(255) UNIQUE NOT NULL
    description TEXT
);

CREATE TABLE permissions (
    permission_id SERIAL PRIMARY KEY,
    permission_name VARCHAR(255) UNIQUE NOT NULL
    description TEXT
);

CREATE TABLE role_permissions (
    role_id INT,
    permission_id INT,
    PRIMARY KEY (role_id, permission_id),
    FOREIGN KEY (role_id) REFERENCES roles(role_id),
    FOREIGN KEY (permission_id) REFERENCES permissions(permission_id)
);

-- roles
INSERT INTO roles (role_id, role_name, description) VALUES
(1, 'Administrator', 'Can access and manage all records.'),
(2, 'Doctor', 'Can view and edit patient records they are assigned to.'),
(3, 'Nurse', 'Can view patient records and update certain health metrics.'),
(4, 'Patient', 'Can access patient contact information and manage appointments.');

-- permissions
INSERT INTO permissions (permission_id, permission_name, description) VALUES
(1, 'view_patient', 'View patient details.'),
(2, 'edit_patient', 'Edit patient details.'),
(3, 'view_all_patients', 'View all patient records.'),

-- Link roles to permissions
INSERT INTO role_permissions (role_id, permission_id) VALUES
(1, 3),         -- Administrator
(2, 1), (2, 2), -- Doctor
(3, 1),         -- Nurse
(4, 1);         -- Patient


