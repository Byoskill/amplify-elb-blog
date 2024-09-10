# This module is loading the model trained from the Jupyter notebook 'jupyterPrediction.ipynb'
# When the module is loaded, we turn a flag on to indicate that the website is ready.
import numpy as np
import joblib

from ml.feature_preparation import FeaturePreprocessor
from ml.salary_prediction_submission import SalaryPredictionSubmission

model_ready = False

def set_model_ready():
    global model_ready
    print("Model is ready for prediction.")
    model_ready = True


# Load the model from the file
model = joblib.load('model/salary_prediction_model.pkl')
lowb_model = joblib.load('model/low_bound_model.pkl')
highb_model = joblib.load('model/high_bound_model.pkl')


# Initializes the feature preprocessor
feature_processor = FeaturePreprocessor()


set_model_ready()

# Use the model for prediction or further analysis
async def predict_salary(features: SalaryPredictionSubmission): 
    global model_ready
    if not model_ready:
        raise Exception("The model is not ready yet. Please wait for the website to be ready.")
    X = feature_processor.transform_input(features)
    prediction = np.exp(model.predict(X))
    salary = prediction[0]
    min_salary = np.exp(lowb_model.predict(X))[0]
    max_salary = np.exp(highb_model.predict(X))[0]
    return (salary, min_salary, max_salary)