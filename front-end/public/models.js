function createPatientInfo(data) {
    return {
        subjectId: data.subjectId || null,
        gender: data.gender || '',
        dob: data.dob || '',
        dod: data.dod || '',
        dodHosp: data.dodHosp || '',
        dodSsn: data.dodSsn || '',
        expireFlag: data.expireFlag || '',
        admissions: data.admissions ? data.admissions.map(createAdmission) : []
    };
}

function createAdmission(data) {
    return {
        hadmId: data.hadmId || null,
        admittime: data.admittime || '',
        dischtime: data.dischtime || '',
        deathtime: data.deathtime || null,
        admissionType: data.admissionType || '',
        admissionLocation: data.admissionLocation || '',
        dischargeLocation: data.dischargeLocation || '',
        insurance: data.insurance || '',
        language: data.language || null,
        religion: data.religion || '',
        maritalStatus: data.maritalStatus || '',
        ethnicity: data.ethnicity || '',
        edregtime: data.edregtime || '',
        edouttime: data.edouttime || '',
        diagnosis: data.diagnosis || '',
        hospitalExpireFlag: data.hospitalExpireFlag || null,
        hasCharteventsData: data.hasCharteventsData || null,
        icustays: data.icustays ? data.icustays.map(createIcustay) : []
    };
}

function createIcustay(data) {
    return {
        icustayId: data.icustayId || null,
        dbsource: data.dbsource || '',
        firstCareunit: data.firstCareunit || '',
        lastCareunit: data.lastCareunit || '',
        firstWardid: data.firstWardid || null,
        lastWardid: data.lastWardid || null,
        intime: data.intime || '',
        outtime: data.outtime || '',
        los: data.los || null
    };
}
