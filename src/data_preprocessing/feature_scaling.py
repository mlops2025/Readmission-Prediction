import pandas as pd
import numpy as np
from sklearn.preprocessing import RobustScaler
import os
import joblib
from logger import logging
from exceptions import CustomException
import sys

PROJECT_DIR = os.path.abspath(os.path.join(os.getcwd(), ".."))
models_dir=os.path.join(PROJECT_DIR, "airflow", "final_model")

def scaling(df, model_output_dir="models/best_final_model"):
    try:
        logging.info("Starting feature scaling process...")

        # Ensure target variable exists
        if 'readmitted' not in df.columns:
            raise CustomException("Target variable 'readmitted' not found in DataFrame.", sys)

        # Extract target
        df_target = df['readmitted'].map({'Yes': 1, 'No': 0})  # Label encoding
        df = df.drop(columns=['readmitted'])

        # Separate numeric and categorical
        df_num = df.select_dtypes(include=['number'])
        df_cat = df.select_dtypes(include=['object'])

        # Fit scaler
        scaler = RobustScaler()
        scaled_array = scaler.fit_transform(df_num)
        df_num_scaled = pd.DataFrame(scaled_array, columns=df_num.columns, index=df.index)

        # Handle categorical
        if not df_cat.empty:
            df_cat_dummy = pd.get_dummies(df_cat, drop_first=True).astype(int)
            df_cat_dummy.index = df.index
            df_scaled = pd.concat([df_num_scaled, df_cat_dummy], axis=1)
        else:
            logging.warning("No categorical features found. Skipping one-hot encoding.")
            df_scaled = df_num_scaled

        # Add back target
        df_scaled['readmitted'] = df_target

        # Ensure output path exists
        os.makedirs(model_output_dir, exist_ok=True)

        # Save scaler to disk
        scaler_path = os.path.join(models_dir, f"scalar_weight.pkl")
        
        joblib.dump(scaler, scaler_path)
        logging.info(f"Scaler saved at {scaler_path}")

        logging.info("Feature scaling completed successfully.")
        return df_scaled

    except Exception as e:
        logging.error("An error occurred during feature scaling.")
        raise CustomException(e, sys)
