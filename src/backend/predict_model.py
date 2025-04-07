import joblib
from models import PredictionRequest
import pandas as pd
from db import insert_prediction

model = None
feature_columns = None  # Optional if you saved expected column order

def load_model(path: str):
    global model
    print(f"[INFO] Loading model from {path}")
    model = joblib.load(path)
    print("[INFO] Model loaded successfully.")

def transform_input(data: PredictionRequest):
    features = {}

    # --- 1. Direct fields from form ---
    features["age"] = data.age
    features["time_in_hospital"] = data.time_in_hospital
    features["num_lab_procedures"] = data.num_lab_procedures
    features["num_procedures"] = data.num_procedures
    features["num_medications"] = data.num_medications
    features["number_outpatient"] = data.number_outpatient
    features["number_emergency"] = data.number_emergency
    features["number_inpatient"] = data.number_inpatient
    features["number_diagnoses"] = data.number_diagnoses

    # Dummy features for model compatibility (replace with real logic if needed)
    features["health_index"] = 0.5
    features["severity_of_disease"] = 0.5
    features["number_of_changes"] = data.change_num

    # --- 2. Medications ---
    all_meds = [
        "metformin", "repaglinide", "glipizide", "glyburide", "pioglitazone",
        "rosiglitazone", "acarbose", "insulin"
    ]
    meds_set = set(m.lower() for m in data.meds)
    for med in all_meds:
        features[med] = 1 if med in meds_set else 0

    # --- 3. Race ---
    features["race_Caucasian"] = 1 if data.race == "Caucasian" else 0
    features["race_Other"] = 1 if data.race == "Other" else 0

    # --- 4. Gender ---
    features["gender_Male"] = 1 if data.gender == "Male" else 0

    # --- 5. Admission type ---
    adm_map = [
        "Emergency", "New Born", "Not Available", "Trauma Center", "Urgent"
    ]
    for val in adm_map:
        features[f"admission_type_id_{val}"] = 1 if data.admission_type == val else 0

    # --- 6. Discharge disposition ---
    discharges = ["Discharged to Home", "Other", "Unknown"]
    for val in discharges:
        features[f"discharge_disposition_id_{val}"] = 1 if data.discharge_disposition == val else 0

    # --- 7. Admission source ---
    features["admission_source_id_Referral"] = 1 if data.admission_source_id == "Referral" else 0
    features["admission_source_id_Others"] = 1 if data.admission_source_id == "Others" else 0

    # --- 8. Diagnosis (3 × 7) ---
    diag_cats = ["Diabetes", "Genitourinary", "Injury", "Musculoskelatal", "Neoplasms", "Others", "Respiratory"]
    for i in ["diag_1", "diag_2", "diag_3"]:
        value = getattr(data, i)
        for cat in diag_cats:
            features[f"{i}_{cat}"] = 1 if value == cat else 0

    # --- 9. Special binary fields ---
    features["change_No"] = 1 if data.change_num == 0 else 0
    features["diabetesMed_Yes"] = 1 if data.diabetic_medication == "Yes" else 0

    # --- 10. Final column order ---
    final_columns = [
        "age", "time_in_hospital", "num_lab_procedures", "num_procedures", "num_medications",
        "number_outpatient", "number_emergency", "number_inpatient", "number_diagnoses",
        "metformin", "repaglinide", "glipizide", "glyburide", "pioglitazone",
        "rosiglitazone", "acarbose", "insulin", "health_index", "severity_of_disease",
        "number_of_changes", "race_Caucasian", "race_Other", "gender_Male",
        "admission_type_id_Emergency", "admission_type_id_New Born", "admission_type_id_Not Available",
        "admission_type_id_Trauma Center", "admission_type_id_Urgent",
        "discharge_disposition_id_Discharged to Home", "discharge_disposition_id_Other",
        "discharge_disposition_id_Unknown", "admission_source_id_Others",
        "admission_source_id_Referral",
        # diag_1
        "diag_1_Diabetes", "diag_1_Genitourinary", "diag_1_Injury", "diag_1_Musculoskelatal",
        "diag_1_Neoplasms", "diag_1_Others", "diag_1_Respiratory",
        # diag_2
        "diag_2_Diabetes", "diag_2_Genitourinary", "diag_2_Injury", "diag_2_Musculoskelatal",
        "diag_2_Neoplasms", "diag_2_Others", "diag_2_Respiratory",
        # diag_3
        "diag_3_Diabetes", "diag_3_Genitourinary", "diag_3_Injury", "diag_3_Musculoskelatal",
        "diag_3_Neoplasms", "diag_3_Others", "diag_3_Respiratory",
        "change_No", "diabetesMed_Yes"
    ]

    # Fill missing with 0
    for col in final_columns:
        if col not in features:
            features[col] = 0

    return pd.DataFrame([features])[final_columns]

def normalize_keys(data: dict) -> dict:
    return {
        k.replace(" ", "_").replace("-", "_").lower(): v
        for k, v in data.items()
    }


def make_prediction(data: PredictionRequest):
    global model
    if model is None:
        raise ValueError("Model is not loaded.")

    df = transform_input(data)
    prediction = model.predict(df)[0]
    prediction_label = "Yes" if prediction == 1 else "No"

    # Merge features and extra fields to DB payload
    record = df.to_dict(orient="records")[0]
    record["predict"] = float(prediction)
    record["f_name"] = data.fname
    record["l_name"] = data.lname
    record["DOB"] = "2000-01-01"  # <- Replace with actual input if DOB is added to form

    normalized_record = normalize_keys(record)
    insert_prediction(normalized_record)


    return prediction_label


