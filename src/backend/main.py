from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from models import PredictionRequest, ActualResultUpdate
from gcs_utils import download_model_from_gcs
from predict_model import load_model, make_prediction
from db import get_patient_by_identity, update_actual_result_in_db
from decode import decode_one_hot_record


from datetime import datetime

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    bucket_name = "readmission_prediction"
    blob_name = "models/best_xgboost_model/model.pkl"
    local_path = "models/my_model.pkl"

    try:
        print("[INFO] Downloading model from GCS...")
        download_model_from_gcs(bucket_name, blob_name, local_path)
        load_model(local_path)
    except Exception as e:
        print(f"Error loading model on startup: {e}")

@app.post("/predict")
async def predict(request: Request):
    body = await request.json()
    print("[DEBUG] Raw request body:", body)

    try:
        data = PredictionRequest(**body)
        prediction = make_prediction(data)
        return {"prediction": prediction}
    except Exception as e:
        import traceback
        print("[ERROR] Exception in /predict:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/update-actual-result")
def update_actual_result(payload: ActualResultUpdate):
    print(f"[INFO] Received actual result payload: {payload}")
    try:
        dob_parsed = datetime.strptime(payload.dob, "%Y-%m-%d").date()
        print(f"[DEBUG] Parsed DOB: {dob_parsed}")
        update_actual_result_in_db(payload.fname, payload.lname, dob_parsed, payload.actual_result)
        print("[INFO] Actual result update successful")
        return {"message": "Actual result updated successfully."}
    except Exception as e:
        import traceback
        print("[ERROR] Exception during actual result update:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Failed to update result.")

@app.post("/search-patient")
async def search_patient(request: Request):
    body = await request.json()
    print(f"[DEBUG] Search patient request body: {body}")
    fname = body.get("fname")
    lname = body.get("lname")
    dob = body.get("dob")

    if not (fname and lname and dob):
        return JSONResponse(status_code=400, content={"error": "Missing input fields"})

    record = get_patient_by_identity(fname, lname, dob)
    print(f"[DEBUG] Retrieved patient record: {record}")
    if not record:
        return JSONResponse(status_code=404, content={"error": "Patient not found"})

    parsed = decode_one_hot_record(record)
    print(f"[DEBUG] Decoded patient data: {parsed}")
    return {
        "predicted_result": int(record.get("predict", 0)),
        "actual_result": int(record.get("readmitted", -1)) if record.get("readmitted") is not None else -1,
        **parsed
    }
