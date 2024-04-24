
document.addEventListener('DOMContentLoaded', function() {
    const patientList = document.getElementById('patientList');
    const noPatients = document.getElementById('noPatients');
    const logoutButton = document.getElementById('logoutButton');

    // Fetch patient IDs from session storage
    const patientIds = JSON.parse(sessionStorage.getItem('patientIds')) || [];

    if (patientIds.length > 0) {
        patientIds.forEach(patientId => {
            const listItem = document.createElement('li');
            listItem.textContent = patientId;
            listItem.style.cursor = 'pointer';
            listItem.onclick = function() {
                viewPatientInfo(patientId);
            };
            patientList.appendChild(listItem);
        });
    } else {
        noPatients.style.display = 'block'; // Show "No patients available" if the list is empty
    }

    function viewPatientInfo(patientId) {
        sessionStorage.setItem('subjectId', patientId);
        sessionStorage.setItem('isPatient', false);
        window.location.href = 'patient-info.html';
    }
    
    if (logoutButton) {
        logoutButton.addEventListener('click', function() {
            sessionStorage.clear();  // Clear session storage
            window.location.href = 'main.html';  // Redirect to the main screen
        });
    }
});
