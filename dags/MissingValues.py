import pandas as pd
import numpy as np
from src.logger import logging
from src.exceptions import CustomExceptions

def MissingVal(df):
    try:
        
        #Case 1: Missing Values
        #Dropping columns which has more N/A values
        if 'max_glu_serum' in df.columns:
            del df['max_glu_serum'] ## 96420 Droping N/A
        if 'A1Cresult' in df.columns:
            del df['A1Cresult']  ## 84748 Droping N/A
        logger.info("Dropped N/A Values")
        
        #Case 2: Inconsistent Values
        ## Droping columns which has more '?' values 
        if 'weight' in df.columns:
            del df['weight']  ## #98569 '?' values
        logger.info("Dropped inconsistent Values")

        ## Replace columns which has more '?' values  
        df['payer_code'].replace('?','N/A')
        df['diag_1'].replace('?', 'N/A')
        df['diag_2'].replace('?', 'N/A')
        df['diag_3'].replace('?', 'N/A')
        logger.info("Replaced inconsistent Values")
        
        #Case 3: Incorrect Mapping
        #df_Patients[df_Patients["admission_type_id"] > 26] 0 rows #invalid admission Type id
        
        #Case 4: Diagnosis Anamolies
        df["Anamolies"] = np.where((df["diag_1"] == "?") & (df["diag_2"] != "?") & (df["diag_3"] != "?"),True,False,)
        df["Anamolies"] = np.where((df["diag_1"] != "?") & (df["diag_2"] == "?") & (df["diag_3"] != "?"),True,False,)
        df.drop(df[df['Anamolies']==True].index)
        logger.info("Dropped Diagnosis Anamolies Values")

    except Exception as e:
        logging.info('__.__Error occoured__.__')
        raise CustomException(e,sys)

    return df
    
   
    
