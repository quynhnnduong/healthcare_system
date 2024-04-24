import { doctorNurseLogin, patientLogin } from './appService.js';

document.addEventListener('DOMContentLoaded', function() {
    const roleLabel = document.getElementById('roleLabel');
    const doctorNurseForm = document.getElementById('doctorNurseForm');
    const patientForm = document.getElementById('patientForm');
    const doctorNurseLoginButton = document.getElementById('doctorNurseLoginButton');
    const patientLoginButton = document.getElementById('patientLoginButton');
    const username = document.getElementById('username');
    const password = document.getElementById('password');
    const subjectId = document.getElementById('subjectId');
    const ssn = document.getElementById('ssn');

    // Retrieve role from URL query parameters
    const urlParams = new URLSearchParams(window.location.search);
    const role = urlParams.get('role');

    updateUIForRole();
    setupEventListeners();

    function updateUIForRole() {
        roleLabel.innerText = `Login as ${getRoleLabel(role)}`;
        if (role === 'doctor/nurse') {
            doctorNurseForm.style.display = 'block';
            patientForm.style.display = 'none';
        } else {
            doctorNurseForm.style.display = 'none';
            patientForm.style.display = 'block';
        }
    }

    function setupEventListeners() {
        if (role === 'doctor/nurse') {
            username.addEventListener('input', validateDoctorNurseForm);
            password.addEventListener('input', validateDoctorNurseForm);
            doctorNurseLoginButton.addEventListener('click', onLogin);
        } else {
            subjectId.addEventListener('input', validatePatientForm);
            ssn.addEventListener('input', validatePatientForm);
            patientLoginButton.addEventListener('click', onLogin);
        }
    }

    function getRoleLabel(role) {
        return role === 'doctor/nurse' ? 'Doctor/Nurse' : 'Patient';
    }

    function validateDoctorNurseForm() {
        doctorNurseLoginButton.disabled = !username.value.trim() || !password.value.trim();
    }

    function validatePatientForm() {
        patientLoginButton.disabled = !subjectId.value.trim() || !ssn.value.trim();
    }

    function onLogin() {
        if (role === 'doctor/nurse') {
            doctorNurseLogin(username.value, password.value)
                .then(data => {
                    console.log('Login successful:', data);
                    sessionStorage.setItem('patientIds', JSON.stringify(data));
                    window.location.href = 'patient-list.html';
                })
                .catch(error => {
                    console.error('Login failed:', error);
                });
        } else {
            patientLogin(parseInt(subjectId.value, 10), ssn.value)
                .then(data => {
                    console.log('Login successful:', data);
                    sessionStorage.setItem('subjectId', data);
                    sessionStorage.setItem('isPatient', true);
                    window.location.href = 'patient-info.html';
                })
                .catch(error => {
                    console.error('Login failed:', error);
                });
        }
    }
});
