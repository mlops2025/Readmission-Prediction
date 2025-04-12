def decode_one_hot_record(record):
    def decode_field(prefix, options):
        for opt in options:
            if record.get(f"{prefix}_{opt.replace(' ', '_')}") == 1:
                return opt
        return None
 
    def decode_diag(prefix):
        diag_cats = ["Diabetes", "Genitourinary", "Injury", "Musculoskelatal", "Neoplasms", "Others", "Respiratory"]
        return decode_field(prefix, diag_cats)

    meds = ["metformin", "repaglinide", "glipizide", "glyburide", "pioglitazone", "rosiglitazone", "acarbose", "insulin"]
    selected_meds = [m.capitalize() for m in meds if record.get(m, 0) == 1]

    return {
        "fname": record["f_name"],
        "lname": record["l_name"],
        "dob": str(record["dob"]),
        "gender": "Male" if record.get("gender_male") else "Female",
        "race": "Caucasian" if record.get("race_caucasian") else "Other",
        "meds": selected_meds,
        "admission_type": decode_field("admission_type_id", ["Emergency", "New Born", "Not Available", "Trauma Center", "Urgent"]),
        "discharge_disposition": decode_field("discharge_disposition_id", ["Discharged to Home", "Other", "Unknown"]),
        "admission_source_id": decode_field("admission_source_id", ["Referral", "Others"]),
        "diag_1": decode_diag("diag_1"),
        "diag_2": decode_diag("diag_2"),
        "diag_3": decode_diag("diag_3"),
        "time_in_hospital": record["time_in_hospital"],
        "num_lab_procedures": record["num_lab_procedures"],
        "num_procedures": record["num_procedures"],
        "num_medications": record["num_medications"],
        "number_outpatient": record["number_outpatient"],
        "number_emergency": record["number_emergency"],
        "number_inpatient": record["number_inpatient"],
        "number_diagnoses": record["number_diagnoses"],
        "diabetic_medication": "Yes" if record.get("diabetesmed_yes") else "No",
        "change_num": int(not record.get("change_no", 0))  # 1 if changed
    }
