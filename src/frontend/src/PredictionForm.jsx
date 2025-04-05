import React, { useState } from "react";
import {
  TextField,
  MenuItem,
  Box,
  Modal,
  FormControl,
  InputLabel,
  Select,
} from "@mui/material";

const PredictionForm = () => {
  const [formData, setFormData] = useState({
    fname: "",
    lname: "",
    age: "",
    meds: [],
    gender: "",
    race: "",
    admission_type: "",
    discharge_disposition: "",
    diag_1: "",
    diag_2: "",
    diag_3: "",
    time_in_hospital: "",
    num_lab_procedures: "",
    num_procedures: "",
    num_medications: "",
    number_outpatient: "",
    number_emergency: "",
    number_inpatient: "",
    number_diagnoses: "",
    admission_source_id: "",
    diabetic_medication: "",
    change_num: "",
  });
  const [open, setOpen] = useState(false);
  const [predictedResult, setPredictedResult] = useState(null);
  const [step, setStep] = useState(1);

  const sendToFastAPI = async (data) => {
    try {
      const response = await fetch("http://localhost:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const result = await response.json();
      console.log("Prediction result:", result);
      // setPredictedResult(result.predicted_result);
      setPredictedResult("No");
      setOpen(true);
    } catch (error) {
      console.error("Error sending data to FastAPI:", error.message, data);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
  
    if (name === "age") {
      if (value === "" || (Number(value) >= 1 && Number(value) <= 150)) {
        setFormData({ ...formData, [name]: value });
      }
      return;
    }
  
    setFormData({ ...formData, [name]: value });
  };  

  const handleSubmit = (e) => {
    e.preventDefault();
    sendToFastAPI(formData);
    setOpen(true);
  };
  const validateStep1 = () => {
    const requiredFields = [
      "fname",
      "lname",
      "age",
      "meds",
      "gender",
      "race",
      "admission_type",
      "discharge_disposition",
      "admission_source_id",
      "diag_1",
      "diag_2",
      "diag_3",
    ];

    for (let field of requiredFields) {
      if (
        formData[field] === "" ||
        formData[field] === null ||
        (Array.isArray(formData[field]) && formData[field].length === 0)
      ) {
        return false;
      }
    }

    return true;
  };

  const diag = [
    "Diabetes",
    "Genitourinary",
    "Injury",
    "Musculoskeletal",
    "Neoplasms",
    "Respiratory",
    "Others",
  ];

  return (
    <div className="flex items-center justify-center py-20">
      <div className="w-3/4 bg-white flex items-center justify-center p-6 drop-shadow-xl rounded-3xl">
        <div className="p-6 w-full">
          <div className="text-2xl font-bold mb-6">Prediction Form</div>
          <form onSubmit={handleSubmit}>
            <div className="grid grid-cols-2 gap-6">
              {step === 1 && (
                <>
                  <TextField
                    label="First Name"
                    name="fname"
                    value={formData.fname}
                    variant="outlined"
                    fullWidth
                    onChange={handleChange}
                    required
                  />
                  <TextField
                    label="Last Name"
                    name="lname"
                    value={formData.lname}
                    variant="outlined"
                    fullWidth
                    onChange={handleChange}
                    required
                  />
                  <TextField
                    label="Age"
                    name="age"
                    value={formData.age}
                    type="number"
                    variant="outlined"
                    fullWidth
                    onChange={(e) => {
                      handleChange(e);
                    }}
                    inputProps={{
                      min: 1,
                      max: 150,
                      inputMode: "numeric",
                      pattern: "[0-9]*",
                    }}
                    required
                  />
                  <FormControl fullWidth required>
                    <InputLabel id="meds">Medications</InputLabel>
                    <Select
                      labelId="meds"
                      name="meds"
                      multiple
                      value={formData.meds}
                      onChange={(e) =>
                        setFormData({ ...formData, meds: e.target.value })
                      }
                      renderValue={(selected) => selected.join(", ")}
                    >
                      {[
                        "Metformin",
                        "Repaglinide",
                        "Glipizide",
                        "Glyburide",
                        "Pioglitazone",
                        "Rosiglitazone",
                        "Acarbose",
                        "Insulin",
                      ].map((item) => (
                        <MenuItem key={item} value={item}>
                          {item}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>

                  <TextField
                    label="Gender"
                    name="gender"
                    value={formData.gender}
                    select
                    variant="outlined"
                    fullWidth
                    onChange={handleChange}
                    required
                  >
                    <MenuItem value="">Select Gender</MenuItem>
                    {["Male", "Female"].map((item) => (
                      <MenuItem key={item} value={item}>
                        {item}
                      </MenuItem>
                    ))}
                  </TextField>
                  <TextField
                    label="Race"
                    name="race"
                    value={formData.race}
                    select
                    variant="outlined"
                    fullWidth
                    onChange={handleChange}
                    required
                  >
                    <MenuItem value="">Select Race</MenuItem>
                    {["Caucasian", "AfricanAmerican", "Other"].map((item) => (
                      <MenuItem key={item} value={item}>
                        {item}
                      </MenuItem>
                    ))}
                  </TextField>
                  <TextField
                    label="Admission Type"
                    name="admission_type"
                    value={formData.admission_type}
                    select
                    variant="outlined"
                    fullWidth
                    onChange={handleChange}
                    required
                  >
                    <MenuItem value="">Select Admission Type</MenuItem>
                    {[
                      "Emergency",
                      "Urgent",
                      "Elective",
                      "New Born",
                      "Trauma Center",
                      "Not Available",
                    ].map((item) => (
                      <MenuItem key={item} value={item}>
                        {item}
                      </MenuItem>
                    ))}
                  </TextField>
                  <TextField
                    label="Discharge Disposition"
                    name="discharge_disposition"
                    value={formData.discharge_disposition}
                    select
                    variant="outlined"
                    fullWidth
                    onChange={handleChange}
                    required
                  >
                    <MenuItem value="">Select Discharge Disposition</MenuItem>
                    {[
                      "Discharged to Home",
                      "Care/Nursing",
                      "Other",
                      "Unknown",
                    ].map((item) => (
                      <MenuItem key={item} value={item}>
                        {item}
                      </MenuItem>
                    ))}
                  </TextField>
                  <TextField
                    label="Admission Source"
                    name="admission_source_id"
                    value={formData.admission_source_id}
                    select
                    variant="outlined"
                    fullWidth
                    onChange={handleChange}
                    required
                  >
                    <MenuItem value="">Select Admission Source</MenuItem>
                    {["Referral", "Emergency room", "Others"].map((item) => (
                      <MenuItem key={item} value={item}>
                        {item}
                      </MenuItem>
                    ))}
                  </TextField>
                  {["diag_1", "diag_2", "diag_3"].map((diagno, index) => (
                    <TextField
                      key={diagno}
                      label={`Diagnosis ${index + 1}`}
                      name={diagno}
                      value={formData[diagno]}
                      select
                      variant="outlined"
                      fullWidth
                      onChange={handleChange}
                      required
                    >
                      <MenuItem value="">Select Diagnosis {index + 1}</MenuItem>
                      {diag.map((item) => (
                        <MenuItem key={item} value={item}>
                          {item}
                        </MenuItem>
                      ))}
                    </TextField>
                  ))}
                </>
              )}
              {step === 2 && (
                <>
                  <TextField
                    label="Time in Hospital"
                    name="time_in_hospital"
                    value={formData.time_in_hospital}
                    type="number"
                    variant="outlined"
                    fullWidth
                    onChange={(e) => {
                      const value = parseInt(e.target.value, 10);
                      if (value >= 1 && value <= 150) {
                        handleChange(e);
                      }
                    }}
                    inputProps={{
                      min: 1,
                      max: 150,
                      inputMode: "numeric",
                      pattern: "[0-9]*",
                    }}
                    required
                  />
                  <TextField
                    label="Number of Lab Procedures"
                    name="num_lab_procedures"
                    value={formData.num_lab_procedures}
                    type="number"
                    variant="outlined"
                    fullWidth
                    onChange={(e) => {
                      const value = parseInt(e.target.value, 10);
                      if (value >= 1 && value <= 150) {
                        handleChange(e);
                      }
                    }}
                    inputProps={{
                      min: 1,
                      max: 150,
                      inputMode: "numeric",
                      pattern: "[0-9]*",
                    }}
                    required
                  />
                  <TextField
                    label="Number of Procedures"
                    name="num_procedures"
                    value={formData.num_procedures}
                    type="number"
                    variant="outlined"
                    fullWidth
                    onChange={(e) => {
                      const value = parseInt(e.target.value, 10);
                      if (value >= 1 && value <= 150) {
                        handleChange(e);
                      }
                    }}
                    inputProps={{
                      min: 1,
                      max: 150,
                      inputMode: "numeric",
                      pattern: "[0-9]*",
                    }}
                    required
                  />
                  <TextField
                    label="Number of Medications"
                    name="num_medications"
                    value={formData.num_medications}
                    type="number"
                    variant="outlined"
                    fullWidth
                    onChange={(e) => {
                      const value = parseInt(e.target.value, 10);
                      if (value >= 1 && value <= 150) {
                        handleChange(e);
                      }
                    }}
                    inputProps={{
                      min: 1,
                      max: 150,
                      inputMode: "numeric",
                      pattern: "[0-9]*",
                    }}
                    required
                  />
                  <TextField
                    label="Number of Outpatient"
                    name="number_outpatient"
                    value={formData.number_outpatient}
                    type="number"
                    variant="outlined"
                    fullWidth
                    onChange={(e) => {
                      const value = parseInt(e.target.value, 10);
                      if (value >= 1 && value <= 150) {
                        handleChange(e);
                      }
                    }}
                    inputProps={{
                      min: 1,
                      max: 150,
                      inputMode: "numeric",
                      pattern: "[0-9]*",
                    }}
                    required
                  />
                  <TextField
                    label="Number of Emergency"
                    name="number_emergency"
                    value={formData.number_emergency}
                    type="number"
                    variant="outlined"
                    fullWidth
                    onChange={(e) => {
                      const value = parseInt(e.target.value, 10);
                      if (value >= 1 && value <= 150) {
                        handleChange(e);
                      }
                    }}
                    inputProps={{
                      min: 1,
                      max: 150,
                      inputMode: "numeric",
                      pattern: "[0-9]*",
                    }}
                    required
                  />
                  <TextField
                    label="Number of Inpatient"
                    name="number_inpatient"
                    value={formData.number_inpatient}
                    type="number"
                    variant="outlined"
                    fullWidth
                    onChange={(e) => {
                      const value = parseInt(e.target.value, 10);
                      if (value >= 1 && value <= 150) {
                        handleChange(e);
                      }
                    }}
                    inputProps={{
                      min: 1,
                      max: 150,
                      inputMode: "numeric",
                      pattern: "[0-9]*",
                    }}
                    required
                  />
                  <TextField
                    label="Number of Diagnoses"
                    name="number_diagnoses"
                    value={formData.number_diagnoses}
                    type="number"
                    variant="outlined"
                    fullWidth
                    onChange={(e) => {
                      const value = parseInt(e.target.value, 10);
                      if (value >= 1 && value <= 150) {
                        handleChange(e);
                      }
                    }}
                    inputProps={{
                      min: 1,
                      max: 150,
                      inputMode: "numeric",
                      pattern: "[0-9]*",
                    }}
                    required
                  />
                  <TextField
                    label="Change Number"
                    name="change_num"
                    value={formData.change_num}
                    type="number"
                    variant="outlined"
                    fullWidth
                    onChange={(e) => {
                      const value = parseInt(e.target.value, 10);
                      if (value >= 1 && value <= 150) {
                        handleChange(e);
                      }
                    }}
                    inputProps={{
                      min: 1,
                      max: 150,
                      inputMode: "numeric",
                      pattern: "[0-9]*",
                    }}
                    required
                  />
                  <TextField
                    label="Discharge Disposition"
                    name="diabetic_medication"
                    value={formData.diabetic_medication}
                    select
                    variant="outlined"
                    fullWidth
                    onChange={handleChange}
                    required
                  >
                    <MenuItem value="">Select Discharge Disposition</MenuItem>
                    {["Yes", "No"].map((item) => (
                      <MenuItem key={item} value={item}>
                        {item}
                      </MenuItem>
                    ))}
                  </TextField>
                </>
              )}
            </div>

            <Box className="flex justify-between mt-8">
              {step > 1 && (
                <button
                  className="border-2 border-teal px-6 py-2 rounded-full font-medium hover:bg-teal hover:opacity-95 transition"
                  onClick={() => setStep(step - 1)}
                  type="button"
                >
                  Back
                </button>
              )}
              {step < 2 && (
                <button
                  className="border-2 border-teal px-6 py-2 rounded-full font-medium bg-teal  hover:bg-white transition"
                  onClick={() => {
                    if (validateStep1()) {
                      setStep(step + 1);
                    } else {
                      alert(
                        "Please fill all required fields before continuing."
                      );
                    }
                  }}
                  type="button"
                >
                  Next
                </button>
              )}
              {step === 2 && (
                <button
                  type="submit"
                  className="border-2 border-teal px-6 py-2 rounded-full font-medium bg-teal  hover:bg-white transition"
                >
                  Predict
                </button>
              )}
            </Box>
          </form>
          <Modal open={open} onClose={() => setOpen(false)}>
            <Box className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white/90 backdrop-blur-md border border-gray-200 rounded-3xl shadow-2xl p-8 w-[440px] max-w-[90%] animate-fadeInUp">
              <div
                className={`w-24 h-24 rounded-full flex items-center justify-center mx-auto mb-6 text-5xl animate-bounceSlow shadow-md ${
                  predictedResult === "Yes"
                    ? "bg-red-100 text-red-500"
                    : "bg-green-100 text-green-500"
                }`}
              >
                {predictedResult === "Yes" ? "🚨" : "🎉"}
              </div>
              <div
                className={`text-2xl font-bold text-center font-bold mb-2 ${
                  predictedResult === "Yes" ? "text-red-600" : "text-green-600"
                }`}
              >
                {predictedResult === "Yes"
                  ? "Readmission Risk Detected"
                  : "All Clear!"}
              </div>

              <div className="text-center text-gray-700 text-md mb-8 leading-relaxed">
                {predictedResult === "Yes"
                  ? "Our prediction model indicates a high risk of readmission. Please take action."
                  : "No risk detected. Continue with standard care and follow-up."}
              </div>

              <div className="flex justify-center mt-2">
                <button
                  onClick={() => {
                    setOpen(false);
                    setPredictedResult(null);
                  }}
                  className={`px-6 py-2 rounded-full font-semibold text-white transition duration-300 ${
                    predictedResult === "Yes"
                      ? "bg-red-500 hover:bg-red-600"
                      : "bg-green-500 hover:bg-green-600"
                  }`}
                  style={{
                    animation: "fadeIn 0.5s ease-in-out 0.3s forwards",
                    opacity: 100,
                  }}
                >
                  Close
                </button>
              </div>
            </Box>
          </Modal>
        </div>
      </div>
    </div>
  );
};

export default PredictionForm;
