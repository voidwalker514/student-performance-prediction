from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd
import os
import numpy as np
from src.schemas import StudentFeatures, PredictionResponse

app = FastAPI(title="Student Performance Prediction API")

# Add CORS middleware to allow the frontend to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, modify in production
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Global variable for the model
model_pipeline = None

@app.on_event("startup")
def load_model():
    global model_pipeline
    model_path = os.path.join(os.path.dirname(__file__), 'models', 'student_performance_model.pkl')
    try:
        model_pipeline = joblib.load(model_path)
        print(f"Model loaded successfully from {model_path}")
    except Exception as e:
        print(f"Error loading model: {e}")
        # In a real app we might raise an error, but here we'll just print it
        # and handle it in the predict endpoint.

@app.get("/")
def read_root():
    return {"message": "Welcome to the Student Performance Prediction API. Use the /predict endpoint."}

@app.post("/predict", response_model=PredictionResponse)
def predict_performance(features: StudentFeatures):
    if model_pipeline is None:
        raise HTTPException(status_code=500, detail="Model is not loaded.")
        
    try:
        # Convert Pydantic model to DataFrame
        # The model pipeline expects a DataFrame with specific column names
        data = {
            'Gender': [features.Gender],
            'Parent_Education': [features.Parent_Education],
            'Study_Hours_Per_Week': [features.Study_Hours_Per_Week],
            'Attendance_Percentage': [features.Attendance_Percentage],
            'Assignments_Completed': [features.Assignments_Completed],
            'Extracurricular_Activities': [features.Extracurricular_Activities],
            'Quiz_Scores_Avg': [features.Quiz_Scores_Avg]
        }
        df = pd.DataFrame(data)
        
        # Make prediction
        prediction_class = model_pipeline.predict(df)[0]
        
        # Get probability (confidence)
        # Note: pipeline.predict_proba returns probabilities for all classes.
        # We need to find the index of the predicted class to get its confidence.
        probabilities = model_pipeline.predict_proba(df)[0]
        classes = model_pipeline.named_steps['classifier'].classes_
        class_index = np.where(classes == prediction_class)[0][0]
        confidence = probabilities[class_index]
        
        # Determine risk level
        risk_level = "Low Risk"
        if prediction_class == "Low":
            risk_level = "High Risk"
        elif prediction_class == "Medium":
            risk_level = "Medium Risk"
            
        return PredictionResponse(
            prediction=prediction_class,
            confidence=float(confidence),
            risk_level=risk_level
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
