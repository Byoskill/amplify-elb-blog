# This module is loading the model trained from the Jupyter notebook 'jupyterPrediction.ipynb'
# When the module is loaded, we turn a flag on to indicate that the website is ready.
from sklearn.externals import joblib

model_ready = False

def set_model_ready():
    global model_ready
    model_ready = True


# Load the model from the file
model = joblib.load('model.pkl')
set_model_ready()


# Use the model for prediction or further analysis
def predict_salary(features):
    global model_ready
    if not model_ready:
        raise Exception("The model is not ready yet. Please wait for the website to be ready.")
    return model.predict(features)