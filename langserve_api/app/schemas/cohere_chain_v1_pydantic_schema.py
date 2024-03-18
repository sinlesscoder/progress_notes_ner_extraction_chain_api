from langchain.pydantic_v1 import BaseModel

# CohereV1 Data Model
class CohereV1(BaseModel):
    admission_date: str
    discharge_date: str
    date_of_birth: str
    chief_complaint: str
    allergies: str
    patient_age: str
    smoking_status: str
    surgical_invasive_procedure: str