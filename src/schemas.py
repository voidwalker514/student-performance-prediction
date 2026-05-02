from pydantic import BaseModel, Field

class StudentFeatures(BaseModel):
    Gender: str = Field(..., description="Student's gender ('Male' or 'Female')")
    Parent_Education: str = Field(..., description="Parent's highest education level ('High School', 'Bachelor', 'Master', 'PhD')")
    Study_Hours_Per_Week: float = Field(..., description="Number of hours the student studies per week")
    Attendance_Percentage: float = Field(..., description="Percentage of classes attended")
    Assignments_Completed: int = Field(..., description="Number of assignments completed (0-10)")
    Extracurricular_Activities: int = Field(..., description="Participates in extracurriculars (1) or not (0)")
    Quiz_Scores_Avg: float = Field(..., description="Average score on quizzes")

class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
    risk_level: str
