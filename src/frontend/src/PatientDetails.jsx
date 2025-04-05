import React, { useEffect, useState } from "react";
import { Switch, Button } from "@mui/material";

const fieldLabels = {
  fname: "First Name",
  lname: "Last Name",
  age: "Age",
  meds: "Medications",
  gender: "Gender",
  race: "Race",
  admission_type: "Admission Type",
  discharge_disposition: "Discharge Disposition",
  admission_source_id: "Admission Source",
  diag_1: "Diagnosis 1",
  diag_2: "Diagnosis 2",
  diag_3: "Diagnosis 3",
  time_in_hospital: "Time in Hospital",
  num_lab_procedures: "Number of Lab Procedures",
  num_procedures: "Number of Procedures",
  num_medications: "Number of Medications",
  number_outpatient: "Number of Outpatient Visits",
  number_emergency: "Number of Emergency Visits",
  number_inpatient: "Number of Inpatient Visits",
  number_diagnoses: "Number of Diagnoses",
  diabetic_medication: "Diabetic Medication",
  change_num: "Change Number",
};

const PatientDetailsPage = () => {
  const [patient, setPatient] = useState(null);
  const [actualResult, setActualResult] = useState(null); // true for "Yes", false for "No"
  const [predictedResult, setPredictedResult] = useState("No");

  useEffect(() => {
    const mockPatientData = {
      fname: "Prat",
      lname: "Veera",
      age: 52,
      meds: ["Metformin", "Insulin", "Pioglitazone"],
      gender: "Female",
      race: "Caucasian",
      admission_type: "Emergency",
      discharge_disposition: "Discharged to Home",
      diag_1: "Diabetes",
      diag_2: "Neoplasms",
      diag_3: "Respiratory",
      time_in_hospital: 4,
      num_lab_procedures: 35,
      num_procedures: 1,
      num_medications: 10,
      number_outpatient: 0,
      number_emergency: 1,
      number_inpatient: 1,
      number_diagnoses: 5,
      admission_source_id: "Referral",
      diabetic_medication: "Yes",
      change_num: 1,
    };
    setPatient(mockPatientData);
  }, []);

  const handleUpdate = async () => {
    try {
      const response = await fetch("http://localhost:8000/update-actual-result", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          patient_id: "1234", 
          actual_result: actualResult ? "Yes" : "No",
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to update result.");
      }

      const result = await response.json();
      alert("Actual result updated successfully.");
      console.log(result);
    } catch (err) {
      console.error("Update error:", err);
    }
  };

  if (!patient) return <div>Loading...</div>;

  return (
    <div className="flex items-center justify-center py-20">
      <div className="w-3/4 bg-white p-10 drop-shadow-xl rounded-3xl">
        <div className="text-2xl font-bold mb-6">Patient Details</div>
        <div className="grid grid-cols-2 gap-4 mb-8">
          {Object.entries(patient).map(([key, value]) => (
            <div key={key} className="flex flex-row">
              <label className="text-md text-gray-600 font-bold mb-1">
                {fieldLabels[key] || key}:
              </label>
              <div className="text-base text-gray-800 ml-2">
                {Array.isArray(value) ? value.join(", ") : value}
              </div>
            </div>
          ))}
        </div>

        <div className="flex flex-row">
          <div className="text-md font-semibold text-gray-700 mb-1">Predicted Result:</div>
          <div
            className={`text-md font-bold ml-2 ${
              predictedResult === "Yes" ? "text-red-600" : "text-green-600"
            }`}
          >
            {predictedResult === "Yes"
              ? "Patient is at risk of readmission"
              : "Patient is not at risk of readmission"}
          </div>
        </div>

        <div className="mb-6">
          <div className="text-md font-semibold text-gray-700 mb-2">Mark Actual Result:</div>
          <div className="flex items-center gap-4">
            <label className="font-medium">No</label>
            <Switch
              checked={actualResult === true}
              onChange={(e) => setActualResult(e.target.checked)}
              color="primary"
            />
            <label className="font-medium">Yes</label>
          </div>
        </div>

        <button
          className="border-2 border-teal px-6 py-2 rounded-full font-medium hover:bg-white bg-teal hover:opacity-95 transition"
          onClick={handleUpdate}
          disabled={actualResult === null}
        >
          Update Actual Result
        </button>
      </div>
    </div>
  );
};

export default PatientDetailsPage;
