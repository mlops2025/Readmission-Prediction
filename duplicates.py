import pandas as pd
from src.logger import logging
from src.exceptions import CustomException
import sys

logging.basicConfig(level=logging.INFO, filename="logs.log", filemode="w",format="%(asctime)s -%(levelname)s -%(message)s")
try:
    df= pd.read_csv("data/diabetic_data.csv") 
    logging.info("File reading begins")
    
    #duplicate
    
    duplicates=df.duplicated()
    count= duplicates.shape[0]
    if count<0:
        logging.warning(f"Found {count} duplicate rows!")
    else:
        logging.info("No duplicate data found")
        
    # drop
    drop_col =['encounter_id', 'patient_nbr']
    df.drop(drop_col, axis=1, inplace=True)
    #logging.info(f"Dropped columns {drop_col}")
    
    unwanted =[11,19,20,21]# ids which are expired, homefacility, hospice etc
    df=df[~df['discharge_disposition_id'].isin(unwanted)]
    df.reset_index(drop=True, inplace=True)
    #logging.info("desposition ids")
    
    df.to_csv("data/cleaned_diabetic_data.csv", index=False)
    logging.info("File Saved")
    
except FileNotFoundError as e:
    logging.info("FileNotFoundError: The file does not exist in the folder.", exc_info=True)
    raise CustomException(e,sys)



    
