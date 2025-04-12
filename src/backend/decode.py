def get_category_from_prefix(record, prefix):
    for key, value in record.items():
        if key.startswith(prefix) and value == 1.0:
            return key.replace(prefix, "").replace("_", " ").title()
    return "—"  # placeholder if nothing matches

def decode_one_hot_record(record):
    return {
        "fname": record.get("f_name", ""),
        "lname": record.get("l_name", ""),
        "dob": str(record.get("dob", "")),
        "age": record.get("age", ""),
        "gender": get_category_from_prefix(record, "gender_"),
        "race": get_category_from_prefix(record, "race_"),
        "admission_type": get_category_from_prefix(record, "admission_type_id_"),
        "admission_source_id": get_category_from_prefix(record, "admission_source_id_"),
        "discharge_disposition": get_category_from_prefix(record, "discharge_disposition_id_"),
        "diag_1": get_category_from_prefix(record, "diag_1_"),
        "diag_2": get_category_from_prefix(record, "diag_2_"),
        "diag_3": get_category_from_prefix(record, "diag_3_"),
        "time_in_hospital": record.get("time_in_hospital", ""),
        "num_lab_procedures": record.get("num_lab_procedures", ""),
        "num_procedures": record.get("num_procedures", ""),
        "num_medications": record.get("num_medications", ""),
        "number_outpatient": record.get("number_outpatient", ""),
        "number_emergency": record.get("number_emergency", ""),
        "number_inpatient": record.get("number_inpatient", ""),
        "number_diagnoses": record.get("number_diagnoses", ""),
        "diabetic_medication": "Yes" if record.get("diabetesmed_yes", 0) == 1 else "No",
        "change_num": int(record.get("change_no", 0)),
        "meds": [med for med in [
            "metformin", "repaglinide", "glipizide", "glyburide",
            "pioglitazone", "rosiglitazone", "acarbose", "insulin"
        ] if record.get(med, 0) == 1.0],
    }
