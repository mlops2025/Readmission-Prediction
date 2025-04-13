from predict_model import scaler  # Import the shared scaler
import traceback

# These are the features scaled during preprocessing
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

def decode_one_hot_record(record):

    print("[INFO] Starting decoding of patient record...")

    # --- Step 1: Extract scaled numeric values ---
    try:
        numeric_scaled = [[record.get(col, 0) for col in NUMERIC_COLUMNS]]
        print("[DEBUG] Scaled numeric input:", numeric_scaled)
    except Exception as e:
        print("[ERROR] Failed to extract numeric fields:", str(e))
        traceback.print_exc()
        return {}

    # --- Step 2: Attempt inverse scaling ---
    if scaler:
        print("[INFO] Scaler is available. Attempting inverse transform...")
        try:
            print("[DEBUG] Scaler expects columns:", list(scaler.feature_names_in_))
            numeric_original = scaler.inverse_transform(numeric_scaled)[0]
            print("[DEBUG] Inverse transformed numeric values:", numeric_original)
        except Exception as e:
            print("[ERROR] Failed during inverse scaling:", str(e))
            traceback.print_exc()
            numeric_original = numeric_scaled[0]
    else:
        print("[WARNING] Scaler not loaded. Using raw scaled values.")
        numeric_original = numeric_scaled[0]

    # --- Step 3: Decode categorical and boolean fields ---
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

    # --- Step 4: Add inverse-scaled numeric values ---
    for col, val in zip(NUMERIC_COLUMNS, numeric_original):
        decoded[col] = round(val, 2)

    print("[INFO] Decoding completed successfully.")
    return decoded
