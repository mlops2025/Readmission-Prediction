import pandas as pd
import numpy as np
from sklearn.preprocessing import RobustScaler
import os
from logger import logging
from exceptions import CustomException
import sys


def scaling(df):
    try:
        logging.info("Starting feature scaling process...")

        # Separate target variable (readmitted)
        if 'readmitted' not in df.columns:
            raise CustomException("Target variable 'readmitted' not found in DataFrame.", sys)

        df_target = df['readmitted'].map({'Yes': 1, 'No': 0})  # Label Encoding
        df = df.drop(columns=['readmitted'])  # Remove target from feature set

        # Separate numerical and categorical features
        df_num = df.select_dtypes(include=['number'])
        df_cat = df.select_dtypes(include=['object'])

        # Apply scaling to numerical features
        scaler = RobustScaler()
        scaled_features = scaler.fit_transform(df_num)
        df_num_scaled = pd.DataFrame(scaled_features, columns=df_num.columns)

        # Handle categorical features only if they exist
        if not df_cat.empty:
            df_cat_dummy = pd.get_dummies(df_cat, drop_first=True).astype(int)
            df_cat_dummy.index = df_num_scaled.index
            df_scaled = pd.concat([df_num_scaled, df_cat_dummy], axis=1)
        else:
            logging.warning("No categorical features found. Skipping one-hot encoding.")
            df_scaled = df_num_scaled  # Only numerical features remain

        # Add target variable back to the processed DataFrame
        df_scaled['readmitted'] = df_target.values

        logging.info("Feature scaling completed successfully.")
        return df_scaled

    except Exception as e:
        logging.error("An error occurred during feature scaling.")
        raise CustomException(e, sys)
