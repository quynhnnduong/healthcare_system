import { getPatientInfo, updatePatientInfo } from './appService.js';

document.addEventListener('DOMContentLoaded', function() {
    const subjectId = sessionStorage.getItem('subjectId');
    const isPatient = sessionStorage.getItem('isPatient') === 'true'; // Convert string to boolean
    
    if (subjectId) {
        getPatientInfo(subjectId)
            .then(patientInfo => {
                populateInformation(patientInfo, isPatient);
                populateAdmissions(patientInfo.admissions, isPatient);
                populateICUStays(patientInfo.admissions, isPatient); // Assuming ICU stays are nested within admissions
            })
            .catch(error => console.error('Failed to fetch patient info:', error));
    }
});

function populateInformation(patientInfo, isPatient) {
    const container = document.getElementById('informationTab');
    container.innerHTML = `
        <div class="form-group">
            <label for="subjectId">Subject ID:</label>
            <input type="text" class="form-control" value="${patientInfo.subjectId || ''}" readonly>
        </div>
        <div class="form-group">
            <label for="gender">Gender:</label>
            <input type="text" class="form-control" value="${patientInfo.gender || ''}" ${isPatient ? 'readonly' : ''}>
        </div>
        <div class="form-group">
            <label for="dob">Date of Birth:</label>
            <input type="text" class="form-control" value="${patientInfo.dob || ''}" ${isPatient ? 'readonly' : ''}>
        </div>
        <div class="form-group">
            <label for="dod">Date of Death:</label>
            <input type="text" class="form-control" value="${patientInfo.dod || ''}" ${isPatient ? 'readonly' : ''}>
        </div>
        <div class="form-group">
            <label for="dodHosp">Date of Death (Hospital):</label>
            <input type="text" class="form-control" value="${patientInfo.dodHosp || ''}" ${isPatient ? 'readonly' : ''}>
        </div>
        <div class="form-group">
            <label for="dodSsn">Date of Death (SSN):</label>
            <input type="text" class="form-control" value="${patientInfo.dodSsn || ''}" ${isPatient ? 'readonly' : ''}>
        </div>
        <div class="form-group">
            <label for="expireFlag">Expire Flag:</label>
            <input type="text" class="form-control" value="${patientInfo.expireFlag || ''}" ${isPatient ? 'readonly' : ''}>
        </div>
    `;
}


function populateAdmissions(admissions, isPatient) {
    const container = document.getElementById('admissionsTab');
    container.innerHTML = ''; // Clear previous entries
    admissions.forEach(admission => {
        const card = document.createElement('div');
        card.className = 'card';
        // Populate each admission's detail
        card.innerHTML = admissionDetailsHTML(admission, isPatient);
        container.appendChild(card);
    });
}

function admissionDetailsHTML(admission, isPatient) {
    return `
        <div class="card-body">
            <p><strong>Admission ID:</strong> ${admission.hadmId || 'N/A'}</p>
            <p><strong>Admission Type:</strong> <input type="text" class="form-control" value="${admission.admissionType || ''}" ${isPatient ? 'readonly' : ''}></p>
            <p><strong>Admission Time:</strong> <input type="text" class="form-control" value="${admission.admittime || ''}" ${isPatient ? 'readonly' : ''}></p>
            <p><strong>Discharge Time:</strong> <input type="text" class="form-control" value="${admission.dischtime || ''}" ${isPatient ? 'readonly' : ''}></p>
            <p><strong>Death Time:</strong> <input type="text" class="form-control" value="${admission.deathtime || 'N/A'}" ${isPatient ? 'readonly' : ''}></p>
            <p><strong>Admission Location:</strong> <input type="text" class="form-control" value="${admission.admissionLocation || ''}" ${isPatient ? 'readonly' : ''}></p>
            <p><strong>Discharge Location:</strong> <input type="text" class="form-control" value="${admission.dischargeLocation || ''}" ${isPatient ? 'readonly' : ''}></p>
            <p><strong>Insurance:</strong> <input type="text" class="form-control" value="${admission.insurance || ''}" ${isPatient ? 'readonly' : ''}></p>
            <p><strong>Language:</strong> <input type="text" class="form-control" value="${admission.language || 'N/A'}" ${isPatient ? 'readonly' : ''}></p>
            <p><strong>Religion:</strong> <input type="text" class="form-control" value="${admission.religion || 'N/A'}" ${isPatient ? 'readonly' : ''}></p>
            <p><strong>Marital Status:</strong> <input type="text" class="form-control" value="${admission.maritalStatus || 'N/A'}" ${isPatient ? 'readonly' : ''}></p>
            <p><strong>Ethnicity:</strong> <input type="text" class="form-control" value="${admission.ethnicity || 'N/A'}" ${isPatient ? 'readonly' : ''}></p>
            <p><strong>ED Registration Time:</strong> <input type="text" class="form-control" value="${admission.edregtime || ''}" ${isPatient ? 'readonly' : ''}></p>
            <p><strong>ED Out Time:</strong> <input type="text" class="form-control" value="${admission.edouttime || ''}" ${isPatient ? 'readonly' : ''}></p>
            <p><strong>Diagnosis:</strong> <input type="text" class="form-control" value="${admission.diagnosis || 'N/A'}" ${isPatient ? 'readonly' : ''}></p>
            <p><strong>Hospital Expire Flag:</strong> <input type="text" class="form-control" value="${admission.hospitalExpireFlag ? 'Yes' : 'No'}" ${isPatient ? 'readonly' : ''}></p>
            <p><strong>Has Chartevents Data:</strong> <input type="text" class="form-control" value="${admission.hasCharteventsData ? 'Yes' : 'No'}" ${isPatient ? 'readonly' : ''}></p>
        </div>
    `;
}



function populateICUStays(admissions, isPatient) {
    const container = document.getElementById('icuStaysTab');
    container.innerHTML = ''; // Clear previous entries
    admissions.forEach(admission => {
        admission.icustays.forEach(icustay => {
            const card = document.createElement('div');
            card.className = 'card';
            card.innerHTML = icuStayDetailsHTML(icustay, isPatient);
            container.appendChild(card);
        });
    });
}

function icuStayDetailsHTML(icustay, isPatient) {
    return `
        <div class="card-body">
            <p><strong>ICU Stay ID:</strong> ${icustay.icustayId || 'N/A'}</p>
            <p><strong>DB Source:</strong> <input type="text" class="form-control" value="${icustay.dbsource || ''}" ${isPatient ? 'readonly' : ''}></p>
            <p><strong>First Care Unit:</strong> <input type="text" class="form-control" value="${icustay.firstCareunit || ''}" ${isPatient ? 'readonly' : ''}></p>
            <p><strong>Last Care Unit:</strong> <input type="text" class="form-control" value="${icustay.lastCareunit || ''}" ${isPatient ? 'readonly' : ''}></p>
            <p><strong>First Ward ID:</strong> <input type="text" class="form-control" value="${icustay.firstWardid || 'N/A'}" ${isPatient ? 'readonly' : ''}></p>
            <p><strong>Last Ward ID:</strong> <input type="text" class="form-control" value="${icustay.lastWardid || 'N/A'}" ${isPatient ? 'readonly' : ''}></p>
            <p><strong>Intime:</strong> <input type="text" class="form-control" value="${icustay.intime || ''}" ${isPatient ? 'readonly' : ''}></p>
            <p><strong>Outtime:</strong> <input type="text" class="form-control" value="${icustay.outtime || ''}" ${isPatient ? 'readonly' : ''}></p>
            <p><strong>LOS:</strong> <input type="text" class="form-control" value="${icustay.los || 'N/A'}" ${isPatient ? 'readonly' : ''}></p>
            <!-- Add more ICU stay details similarly -->
        </div>
    `;
}



function updateInfo() {
    const patientData = collectPatientData(); // Function to collect data from form inputs
    updatePatientInfo(subjectId, patientData)
        .then(() => {
            document.getElementById('successMessage').style.display = 'block';
        })
        .catch(error => {
            console.error('Error updating patient information:', error);
            alert('Failed to update patient data.');
        });
}



function collectPatientData() {
    // Collect data from form fields to send to the backend
    const subjectId = document.getElementById('subjectId').value || null;
    const gender = document.getElementById('gender').value || '';
    const dob = document.getElementById('dob').value || '';
    const dod = document.getElementById('dod').value || '';
    const dodHosp = document.getElementById('dodHosp').value || '';
    const dodSsn = document.getElementById('dodSsn').value || '';
    const expireFlag = document.getElementById('expireFlag').value || '';
    
    const admissions = [];
    const admissionElements = document.getElementsByClassName('admission');
    for (let i = 0; i < admissionElements.length; i++) {
        const admission = collectAdmissionData(admissionElements[i]);
        admissions.push(admission);
    }
    
    return {
        subjectId: subjectId,
        gender: gender,
        dob: dob,
        dod: dod,
        dodHosp: dodHosp,
        dodSsn: dodSsn,
        expireFlag: expireFlag,
        admissions: admissions
    };
}

function collectAdmissionData(admissionElement) {
    const hadmId = admissionElement.querySelector('.hadmId').value || null;
    const admittime = admissionElement.querySelector('.admittime').value || '';
    const dischtime = admissionElement.querySelector('.dischtime').value || '';
    const deathtime = admissionElement.querySelector('.deathtime').value || null;
    const admissionType = admissionElement.querySelector('.admissionType').value || '';
    const admissionLocation = admissionElement.querySelector('.admissionLocation').value || '';
    const dischargeLocation = admissionElement.querySelector('.dischargeLocation').value || '';
    const insurance = admissionElement.querySelector('.insurance').value || '';
    const language = admissionElement.querySelector('.language').value || null;
    const religion = admissionElement.querySelector('.religion').value || '';
    const maritalStatus = admissionElement.querySelector('.maritalStatus').value || '';
    const ethnicity = admissionElement.querySelector('.ethnicity').value || '';
    const edregtime = admissionElement.querySelector('.edregtime').value || '';
    const edouttime = admissionElement.querySelector('.edouttime').value || '';
    const diagnosis = admissionElement.querySelector('.diagnosis').value || '';
    const hospitalExpireFlag = admissionElement.querySelector('.hospitalExpireFlag').value || null;
    const hasCharteventsData = admissionElement.querySelector('.hasCharteventsData').value || null;
    
    const icustays = [];
    const icustayElements = admissionElement.getElementsByClassName('icustay');
    for (let i = 0; i < icustayElements.length; i++) {
        const icustay = collectIcustayData(icustayElements[i]);
        icustays.push(icustay);
    }
    
    return {
        hadmId: hadmId,
        admittime: admittime,
        dischtime: dischtime,
        deathtime: deathtime,
        admissionType: admissionType,
        admissionLocation: admissionLocation,
        dischargeLocation: dischargeLocation,
        insurance: insurance,
        language: language,
        religion: religion,
        maritalStatus: maritalStatus,
        ethnicity: ethnicity,
        edregtime: edregtime,
        edouttime: edouttime,
        diagnosis: diagnosis,
        hospitalExpireFlag: hospitalExpireFlag,
        hasCharteventsData: hasCharteventsData,
        icustays: icustays
    };
}

function collectIcustayData(icustayElement) {
    const icustayId = icustayElement.querySelector('.icustayId').value || null;
    const dbsource = icustayElement.querySelector('.dbsource').value || '';
    const firstCareunit = icustayElement.querySelector('.firstCareunit').value || '';
    const lastCareunit = icustayElement.querySelector('.lastCareunit').value || '';
    const firstWardid = icustayElement.querySelector('.firstWardid').value || null;
    const lastWardid = icustayElement.querySelector('.lastWardid').value || null;
    const intime = icustayElement.querySelector('.intime').value || '';
    const outtime = icustayElement.querySelector('.outtime').value || '';
    const los = icustayElement.querySelector('.los').value || null;
    
    return {
        icustayId: icustayId,
        dbsource: dbsource,
        firstCareunit: firstCareunit,
        lastCareunit: lastCareunit,
        firstWardid: firstWardid,
        lastWardid: lastWardid,
        intime: intime,
        outtime: outtime,
        los: los
    };
}


function hideSuccessMessage() {
    document.getElementById('successMessage').style.display = 'none';
}

function goBack() {
    window.history.back();
}

function showTab(tabName) {
    // Hide all tabs and show selected tab
    document.querySelectorAll('.tab-pane').forEach(tab => tab.classList.remove('show', 'active'));
    document.getElementById(`${tabName}Tab`).classList.add('show', 'active');
}