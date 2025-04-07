from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import PredictionRequest, ActualResultUpdate
from gcs_utils import download_model_from_gcs
from predict_model import load_model, make_prediction

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
        download_model_from_gcs(bucket_name, blob_name, local_path)
        load_model(local_path)
    except Exception as e:
        print(f"Error loading model on startup: {e}")

@app.post("/predict")
def predict(data: PredictionRequest):
    try:
        prediction = make_prediction(data)
        return {"predicted_result": prediction}
    except Exception as e:
        import traceback
        print("[ERROR] Exception in /predict:")
        traceback.print_exc()  # <-- This will show the full error in the terminal
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/update-actual-result")
def update_actual_result(payload: ActualResultUpdate):
    print(f"[INFO] Received actual result: {payload.patient_id} = {payload.actual_result}")
    return {"message": "Actual result updated successfully."}
