import pandas as pd
import numpy as np
from sklearn.preprocessing import RobustScaler
import os
from src.logger import logging
from src.exceptions import CustomExceptions
import sys

def scaling(df):
    try:
        logging.info("Starting feature selection process...")
    
        df_num=df.select_dtypes(include=['number'])
        df_cat=df.select_dtypes(include=['object'])

        scaler = RobustScaler()
        scaled_features = scaler.fit_transform(df_num)
        df_num_scaled=pd.DataFrame(scaled_features,columns=df_num.columns)

        df_cat_dummy=pd.get_dummies(df_cat,drop_first=True)
        df_cat_dummy.index=df_num_scaled.index
        df_scaled=pd.concat([df_num_scaled,df_cat_dummy],axis=1)
    
        logging.info("Feature selection completed successfully.")
        return df_scaled
    
    except Exception as e:
        logging.error("An error occurred during feature scaling.")
        raise CustomException(e, sys)