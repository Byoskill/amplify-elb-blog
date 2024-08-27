from typing import Annotated
from fastapi import FastAPI, Form
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import os

FRONTEND_URL = os.getenv('FRONTEND_URL')

# creating API
app = FastAPI()

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
    working_year: int
    experience_level: str
    employment_type: str
    remote_ratio: int
    employment_residence: str
    company_location: str
    company_size: str

# burgers route
@app.post("/api/v1/predict")
async def predict(working_year: Annotated[int, Form()],
                  experience_level: Annotated[str, Form()],
                  employment_type: Annotated[str, Form()],
                  remote_ratio: Annotated[int, Form()],
                  employment_residence: Annotated[str, Form()],
                  company_location: Annotated[str, Form()],
                  company_size: Annotated[str, Form()]):
    
    submission = FormSubmission(
        working_year= working_year,
        experience_level= experience_level,
        employment_type= employment_type,
        remote_ratio= remote_ratio,
        employment_residence= employment_residence,
        company_location= company_location,
        company_size= company_size
    )
    prediction_id = 10
    response = RedirectResponse(url=f'{FRONTEND_URL}/prediction?prediction={prediction_id}'  )
    return response


# sandwiches route
@app.get("/api/v1/prediction")
async def get_prediction():
    return {
        "Egg sandwich": "10$",
        "cheesy sandwich": "11$",
        "Chicken sandwich": "13$"
    }