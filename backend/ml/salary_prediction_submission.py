from dataclasses import dataclass
from pydantic import BaseModel


@dataclass
class SalaryPredictionSubmission:
    work_year: str
    experience_level: str
    employment_type: str
    job_title: str
    employee_residence: str
    remote_ratio: int
    company_location: str
    company_size: str