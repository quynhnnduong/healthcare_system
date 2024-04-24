-- Create patients table
CREATE TABLE patients (
    row_id SERIAL PRIMARY KEY,
    subject_id SERIAL UNIQUE NOT NULL,
    gender VARCHAR(5),
    dob VARCHAR,
    dod VARCHAR,
    dod_hosp VARCHAR,
    dod_ssn VARCHAR,
    expire_flag VARCHAR(5)
);

-- Create admissions table
CREATE TABLE admissions (
    row_id SERIAL PRIMARY KEY,
    subject_id INT NOT NULL,
    hadm_id SERIAL UNIQUE NOT NULL,
    admittime TIMESTAMP,
    dischtime TIMESTAMP,
    deathtime TIMESTAMP,
    admission_type VARCHAR(50),
    admission_location VARCHAR(50),
    discharge_location VARCHAR(50),
    insurance VARCHAR(255),
    language VARCHAR(10),
    religion VARCHAR(50),
    marital_status VARCHAR(50),
    ethnicity VARCHAR(200),
    edregtime TIMESTAMP,
    edouttime TIMESTAMP,
    diagnosis VARCHAR(300),
    hospital_expire_flag SMALLINT,
    has_chartevents_data SMALLINT,
    FOREIGN KEY (subject_id) REFERENCES patients(subject_id)
);

-- Create icustays table
CREATE TABLE icustays (
    row_id SERIAL PRIMARY KEY,
    subject_id INT NOT NULL,
    hadm_id INT NOT NULL,
    icustay_id SERIAL UNIQUE NOT NULL,
    dbsource VARCHAR(20),
    first_careunit VARCHAR(20),
    last_careunit VARCHAR(20),
    first_wardid SMALLINT,
    last_wardid SMALLINT,
    intime TIMESTAMP,
    outtime TIMESTAMP,
    los DOUBLE PRECISION,
    FOREIGN KEY (subject_id) REFERENCES patients(subject_id),
    FOREIGN KEY (hadm_id) REFERENCES admissions(hadm_id)
);


CREATE TABLE roles (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,  -- Store hashed passwords, not plain text
    role_id INT,
    FOREIGN KEY (role_id) REFERENCES roles(role_id)
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
(4, 'Patient', 'Can access patient information.');


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
