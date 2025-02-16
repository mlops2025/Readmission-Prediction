import pandas as pd
import sys
from src.exceptions import CustomException
from src.logger import logging

logging.basicConfig(level=logging.INFO, filename="logs.log", filemode="w",format="%(asctime)s -%(levelname)s -%(message)s")
def duplicates(df):
    try:
        duplicates=df.duplicated()
         #df= pd.read_csv("data/diabetic_data.csv") 
         #logging.info("File reading begins")
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
        return df
    except Exception as e:
        logging.info('__.__Error occoured__.__')
        raise CustomException(e,sys)
    #return df

    
