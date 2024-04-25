# Healthcare Database System

#### By: Quynh Duong, Minh Le, Saumya Shukla​

## Overview 

This project is designed to create a secure database system for managing patient data within the healthcare domain. It integrates advanced encryption standards (AES) and a role-based access control framework to ensure data security and confidentiality.

## Setup Instructions Backend

1. Install Python 3 and pip on your system. Make sure you are using Python3.10 or higher.
2. Install the required Python packages using pip: `pip install -r requirements.txt`
3. Create a `.env` in the backend directory and enter credentials similar format to .env.example.
4. You can use Make file to do the setup and run the app: `make setup`

## Start Backend Application
Navigate to backend directory and run:
```
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
or run
```
make run
```
This will start application at `localhost:8000`
## File Description
- `backend/patientData/`: Contains csv patient data from MIMIC-III Clinical Database.
- `backend/model/`: Contains all the schema and table definitions for the application. 
- `backend/encryption/`: Contains AES encryption and decryption methods for the application
- `backend/endpoints/`: Contains all the api calls for creating, updating, and viewing patient information.
- `backend/model/schema.sql`: An optional SQL script containing the schema definition for the database. 
  It can be used to set up the database schema manually using PostgreSQL commands. Run this command to do manual database setup
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
```
npx webpack serve --open
```

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
