import random
from typing import Annotated
import uuid
from fastapi import FastAPI, Form
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

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

# working_year: 10
# experience_level: MI
# employment_type: FT
# remote_ratio: 50
# employment_residence: BB
# company_location: AX
# company_size: S
class FormSubmission(BaseModel):
    prediction_id: str    
    working_year: int
    experience_level: str
    employment_type: str
    remote_ratio: int
    employment_residence: str
    company_location: str
    company_size: str
    predicted_salary: int | None
    low_salary_range: int | None
    high_salary_range: int | None
    status_id : str


fake_cache_prediction = dict()


# Requests for the prediction
@app.post("/api/v1/predict")
async def predict(working_year: Annotated[int, Form()],
                  experience_level: Annotated[str, Form()],
                  employment_type: Annotated[str, Form()],
                  remote_ratio: Annotated[int, Form()],
                  employment_residence: Annotated[str, Form()],
                  company_location: Annotated[str, Form()],
                  company_size: Annotated[str, Form()]):
    
    submission = FormSubmission(
        prediction_id=str(uuid.uuid4()),
        working_year= working_year,
        experience_level= experience_level,
        employment_type= employment_type,
        remote_ratio= remote_ratio,
        employment_residence= employment_residence,
        company_location= company_location,
        company_size= company_size,
        predicted_salary= None,
        low_salary_range= None,
        high_salary_range= None,
        status_id= "not_ready"
    )
    prediction_id = submission.prediction_id
    fake_cache_prediction[prediction_id] = submission    
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
        return { "status": submission.status_id}


    