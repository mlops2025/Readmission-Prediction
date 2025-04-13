from predict_model import scaler

def get_category_from_prefix(record, prefix):
    for key, value in record.items():
        if key.startswith(prefix) and value == 1.0:
            return key.replace(prefix, "").replace("_", " ").title()
    return "—"

def decode_one_hot_record(record):
    """
    Decodes a patient record with one-hot and scaled numeric features
    into human-readable, unscaled format.
    """
    if not scaler:
        print("[WARNING] Scaler not loaded. Returning scaled values.")
        numeric_original = [record.get(col, 0) for col in scaler.feature_names_in_]
    else:
        try:
            # Use scaler's original columns
            scaled_input = [[record.get(col, 0) for col in scaler.feature_names_in_]]
            numeric_original = scaler.inverse_transform(scaled_input)[0]
        except Exception as e:
            print(f"[ERROR] Failed to inverse-transform numeric fields: {e}")
            numeric_original = [record.get(col, 0) for col in scaler.feature_names_in_]

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

    # Map back the inverse-transformed values using scaler's feature list
    decoded.update({
        col: round(val, 2) for col, val in zip(scaler.feature_names_in_, numeric_original)
    })

    return decoded
