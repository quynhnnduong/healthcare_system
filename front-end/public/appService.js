const baseUrl = 'http://localhost:8000';

export function doctorNurseLogin(username, password) {
    const url = `${baseUrl}/login/doctorNurse`;
    const body = JSON.stringify({ username, password });
    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: body
    }).then(response => response.json());
}

export function patientLogin(subjectId, ssn) {
    const url = `${baseUrl}/login/patient`;
    const body = JSON.stringify({ subjectId, ssn });
    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: body
    }).then(response => response.json());
}

export function getPatientInfo(subjectId) {
    const url = `${baseUrl}/patients/${subjectId}`;
    return fetch(url, {
        method: 'GET'
    }).then(response => response.json())
    .then(data => createPatientInfo(data));
}

export function updatePatientInfo(subjectId, patientData) {
    const url = `${baseUrl}/patients/${subjectId}`;
    const preparedData = preparePatientInfoForUpdate(patientData);  // Process the data before sending

    return fetch(url, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(preparedData)  // Send the prepared data as JSON
    }).then(response => {
        if (!response.ok) {
            throw new Error('Failed to update patient info');
        }
        return response.json();
    });
}
