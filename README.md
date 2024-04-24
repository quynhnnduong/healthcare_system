# Healthcare Database System

## Overview 

This project is designed to create a secure database system for managing patient data within the healthcare domain. It integrates advanced encryption standards (AES) and a role-based access control framework to ensure data security and confidentiality.

## Setup Instructions

1. Install Python 3 and pip on your system. Make sure you are using Python3.10 or higher.
2. Install the required Python packages using pip: `pip install -r requirements.txt`
3. Create a `.env` in the root directory and enter credentials similar format to .env.example.
4. You can use Make file to do the setup and run the app: `make setup`

## Start Application
Navigate to root directory and run:
```
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
or run
```
make run
```
This will start application at `localhost:8000`
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
  


# Healthcare Database System Frontend

##  Overview

This project is the frontend component of the Healthcare Database System. It provides a user-friendly interface for patients, doctors, and nurses to interact with the system, view patient information, and perform various tasks securely.

## Setup Instructions

1. Clone this repository to your local machine:
   git clone <repository-url>

2. Navigate to the project directory:
   cd healthcare_system/front-end

3. Install the required dependencies:
   npm install

## Usage

To run the frontend server locally, use the following command:
npx webpack serve --open

This command will start the webpack dev server and automatically open the default web browser with the frontend application.

## Configuration

- Webpack Configuration: The webpack configuration is located in the webpack.config.js file. It is responsible for bundling the JavaScript code and assets.

- HTML Templates: HTML templates are located in the public directory. The main.html file serves as the main entry point for the application.

- JavaScript Code: JavaScript code is located in the public directory. The main.js file is located in the src directory and contains the main entry point for the application.

## Dependencies

- Node.js
- npm
- webpack
- webpack-cli
- webpack-dev-server
- html-webpack-plugin

For detailed information on dependencies, refer to the package.json file.

License

This project is licensed under the MIT License - see the LICENSE file for details.
