import joblib
import os
import traceback
from predict_model import scaler as shared_scaler  # initial import

# Global fallback in case scaler isn't set
scaler = shared_scaler

# Path fallback
SCALER_PATH = "models/scalar_weight.pkl"

NUMERIC_COLUMNS = [
    "age", "time_in_hospital", "num_lab_procedures", "num_procedures",
    "num_medications", "number_outpatient", "number_emergency",
    "number_inpatient", "number_diagnoses", "health_index",
    "severity_of_disease", "number_of_changes"
]

def get_category_from_prefix(record, prefix):
    for key, value in record.items():
        if key.startswith(prefix) and value == 1.0:
            return key.replace(prefix, "").replace("_", " ").title()
    return "—"

def load_scaler_fallback():
    global scaler
    try:
        print("[INFO] Fallback: Attempting to load scaler locally...")
        scaler = joblib.load(SCALER_PATH)
        print("[INFO] Fallback scaler loaded successfully.")
    except Exception as e:
        print(f"[ERROR] Fallback scaler load failed: {e}")
        traceback.print_exc()

def decode_one_hot_record(record):
    global scaler
    print("[INFO] Starting decoding of patient record...")

    # Step 1: Extract numeric fields
    try:
        numeric_scaled = [[record.get(col, 0) for col in NUMERIC_COLUMNS]]
        print("[DEBUG] Scaled numeric input:", numeric_scaled)
    except Exception as e:
        print(f"[ERROR] Failed to extract numeric fields: {e}")
        traceback.print_exc()
        return {}

    # Step 2: Try to inverse scale
    if scaler is None:
        load_scaler_fallback()

    if scaler:
        try:
            print("[INFO] Scaler is available. Inverse transforming...")
            print("[DEBUG] Scaler expects columns:", list(scaler.feature_names_in_))
            numeric_original = scaler.inverse_transform(numeric_scaled)[0]
            print("[DEBUG] Inverse transformed values:", numeric_original)
        except Exception as e:
            print(f"[ERROR] Inverse transform failed: {e}")
            traceback.print_exc()
            numeric_original = numeric_scaled[0]
    else:
        print("[WARNING] Scaler not loaded. Using scaled values.")
        numeric_original = numeric_scaled[0]

    # Step 3: Decode record
    decoded = {
        "fname": record.get("f_name", ""),
        "lname": record.get("l_name", ""),
        "dob": str(record.get("dob", "")),
        "gender": get_category_from_prefix(record, "gender_"),
        "race": get_category_from_prefix(record, "race_"),
        "admission_type": get_category_from_prefix(record, "admission_type_id_"),
        "admission_source_id": get_category_from_prefix(record, "admission_source_id_"),
        "discharge_disposition": get_category_from_prefix(record, "discharge_disposition_id_"),
        "diag_1": get_category_from_prefix(record, "diag_1_"),
        "diag_2": get_category_from_prefix(record, "diag_2_"),
        "diag_3": get_category_from_prefix(record, "diag_3_"),
        "diabetic_medication": "Yes" if record.get("diabetesmed_yes", 0) == 1 else "No",
        "change_num": int(record.get("change_no", 0)),
        "meds": [med for med in [
            "metformin", "repaglinide", "glipizide", "glyburide",
            "pioglitazone", "rosiglitazone", "acarbose", "insulin"
        ] if record.get(med, 0) == 1.0],
    }

    # Step 4: Add numeric values
    decoded.update({
        col: round(val, 2) for col, val in zip(NUMERIC_COLUMNS, numeric_original)
    })

    print("[INFO] Decoding completed successfully.")
    return decoded
