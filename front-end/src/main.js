

document.addEventListener('DOMContentLoaded', function() {
  const patientButton = document.getElementById('patientButton');
  const doctorNurseButton = document.getElementById('doctorNurseButton');

  patientButton.addEventListener('click', () => {
      window.location.href = `login.html?role=patient`;
  });

  doctorNurseButton.addEventListener('click', () => {
      window.location.href = `login.html?role=doctor/nurse`;
  });
});
