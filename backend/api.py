from asgiref.wsgi import WsgiToAsgi
from flask import Flask
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from numpy import float64
from pydantic import BaseModel
from typing import Annotated
import asyncio
import os
import random
import uuid

from ml.predictions import predict_salary
from ml.salary_prediction_submission import SalaryPredictionSubmission

FRONTEND_URL = os.getenv('FRONTEND_URL')

# creating API
app = FastAPI()
origins = [
    FRONTEND_URL,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# default route
@app.get("/")
async def root():
    return {
            "welcome_message": "AWS Amplify + Elasticbeanstalk Demo",
            "actions": [
                {
                    "predict": "http://localhost:8000/api/v1/predict"
                },
                {
                    "prediction": "http://localhost:8000/api/v1/prediction"
                }
            ]
    };

fake_cache_prediction = dict()

class PredictionStatus(BaseModel):
    input: SalaryPredictionSubmission
    status: str
    salary: float
    min_salary: float
    max_salary: float
    prediction_id: str



async def predict_salary_task(prediction: PredictionStatus):
    prediction.status = "processing"
    (salary, min_salary, max_salary) = await predict_salary(prediction.input)
    print(f"Predicted salary for {prediction.input.job_title}: ${salary}")
    prediction.salary = salary
    prediction.min_salary = min_salary
    prediction.max_salary = max_salary
    prediction.status = "ready"
    # Redirect to the prediction page with the prediction ID
    return prediction

# Requests for the prediction
@app.post("/api/v1/predict")
async def predict(
                experience_level: Annotated[str, Form()],
                employment_type: Annotated[str, Form()],
                remote_ratio: Annotated[int, Form()],
                work_year: Annotated[str, Form()],
                employee_residence: Annotated[str, Form()],
                job_title: Annotated[str, Form()],
                company_location: Annotated[str, Form()],
                company_size: Annotated[str, Form()]):

    submission = SalaryPredictionSubmission(
        work_year= work_year,
        experience_level= experience_level,
        employment_type= employment_type,
        employee_residence= employee_residence,
        job_title= job_title,
        remote_ratio= remote_ratio,
        company_location= company_location,
        company_size= company_size,
    )


    prediction = PredictionStatus(
        input= submission, 
        status="not_ready", 
        salary=-1, 
        prediction_id = str(uuid.uuid4()),
        min_salary=0, 
        max_salary=0
    )
    prediction_id = prediction.prediction_id
    fake_cache_prediction[prediction_id] = prediction
    # Create a thread and launch the task to make the prediction
    task = asyncio.create_task(predict_salary_task(prediction))
    response = RedirectResponse(url=f'{FRONTEND_URL}/prediction?prediction={prediction_id}'  )
    return response


# Returns the prediction if available otherwise 400
@app.get("/api/v1/prediction/{prediction_id}")
async def get_prediction(prediction_id: str):
    return fake_cache_prediction[prediction_id]

# Check if the prediction has been established
@app.get("/api/v1/prediction/status/{prediction_id}")
async def get_prediction(prediction_id: str):
    submission = fake_cache_prediction.get(prediction_id)
    if submission is None:
        return { "status": "not_found" }
    else:
        return { "status": submission.status}

## Flask integration

# Flask App
flask_app = Flask(__name__)

@flask_app.route("/flask")
def flask_route():
    return "This is a Flask route!"

# Wrap Flask app with WsgiToAsgi    
wsgi_app = WsgiToAsgi(flask_app)

# Mount the Flask app in FastAPI
app.mount("/flask", wsgi_app)