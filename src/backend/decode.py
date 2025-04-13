
from predict_model import scaler

# These are the features you scaled before prediction
NUMERIC_COLUMNS = [
    "age", "time_in_hospital", "num_lab_procedures", "num_procedures",
    "num_medications", "number_outpatient", "number_emergency",
    "number_inpatient", "number_diagnoses", "health_index",
    "severity_of_disease", "number_of_changes"
]

def get_category_from_prefix(record, prefix):
    """
    Extracts the human-readable category from a one-hot-encoded field.
    """
    for key, value in record.items():
        if key.startswith(prefix) and value == 1.0:
            return key.replace(prefix, "").replace("_", " ").title()
    return "—"  # Default if not found

def decode_one_hot_record(record):
    """
    Decodes a patient record with one-hot and scaled numeric features
    into human-readable, unscaled format.
    """
    # --- Step 1: Extract scaled values ---
    numeric_scaled = [[record.get(col, 0) for col in NUMERIC_COLUMNS]]

    # --- Step 2: Inverse scale if scaler is loaded ---
    if scaler:
        try:
            numeric_original = scaler.inverse_transform(numeric_scaled)[0]
        except Exception as e:
            print(f"[ERROR] Failed to inverse-transform numeric fields: {e}")
            numeric_original = numeric_scaled[0]
    else:
        print("[WARNING] Scaler not loaded. Returning scaled values.")
        numeric_original = numeric_scaled[0]

    # --- Step 3: Decode the record ---
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

    # --- Step 4: Add unscaled numeric values back ---
    decoded.update({
        col: round(val, 2) for col, val in zip(NUMERIC_COLUMNS, numeric_original)
    })

    return decoded
