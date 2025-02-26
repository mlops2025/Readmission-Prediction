import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from src.logger import logging
from src.exceptions import CustomExceptions
from fairlearn.metrics import demographic_parity_ratio, equalized_odds_ratio
from fairlearn.reductions import DemographicParity
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder ##


#1: Evaluating the dataset and checking whether bias exists in demographics features (age,race and gender)
def Bias_Dataset_Evaluation(df):
    try:
       
        fig, axes = plt.subplots(1, 3, figsize=(10, 5))

        axes[0].hist(df['gender'], bins=5, color='blue', alpha=0.5)
        axes[0].set_title('Gender')

        axes[1].hist(df['age'], bins=5, color='green', alpha=0.5)
        axes[1].set_title('Age')

        axes[2].hist(df['race'], bins=5, color='red', alpha=0.5)
        axes[2].set_title('Race')

        #plt.tight_layout()
        #plt.show()
        logger.info("Data Visualization of demographic groups")
    
    except Exception as e:
         logging.info('__.__Error occoured__.__')
         raise CustomException(e,sys)

    return df

#2: Evaluating the bias condition by doing a test Model build and considering columns (Race and Gender)
#from the above step its noted that Age has massive records between 60 and 70 age groups so excluded Age feature in this step

def Bias_Model_Evaluation(df):
    try:
        target_labels = df['readmitted']
        sensitive_features = df[['gender','race']]

        (X_train, X_test, y_train, y_test, A_train, A_test) = train_test_split(
            df, target_labels, sensitive_features, test_size=0.3, random_state=12345, stratify=target_labels
        )

        model = RandomForestClassifier() 
        model.fit(X_train, y_train)

        y_pred  = model.predict(X_test) 
        m_dpr = demographic_parity_ratio(y_test, y_pred , sensitive_features=A_test)
        m_eqo = equalized_odds_ratio(y_test, y_pred , sensitive_features=A_test)
        logger.info(f'Value of demographic parity ratio: {round(m_dpr, 2)}') #0.78
        logger.info(f'Value of equal odds ratio: {round(m_eqo, 2)}') #1
    
    except Exception as e:
         logging.info('__.__Error occoured__.__')
         raise CustomException(e,sys)
    return df


##Demographic parity ratio: 
# ##Ratio of selection rates between smallest and largest groups. Return type is a decimal value. 
# ##A ratio of 1 means all groups have same selection rate.
##Equalized odds ratio: 
# ##The equalized odds ratio of 1 means that all groups have the same true positive, true negative, false positive, and false negative rates.

