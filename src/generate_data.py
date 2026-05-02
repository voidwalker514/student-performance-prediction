import numpy as np
import pandas as pd
import os

def generate_synthetic_student_data(num_samples=2000):
    """
    Generates synthetic data for a Student Performance Prediction System.
    """
    np.random.seed(42)

    # 1. Demographics & Background
    student_id = np.arange(1, num_samples + 1)
    gender = np.random.choice(['Male', 'Female'], num_samples)
    parent_education = np.random.choice(['High School', 'Bachelor', 'Master', 'PhD'], num_samples, p=[0.4, 0.4, 0.15, 0.05])
    
    # 2. Academic Behavior (Features that will influence the target)
    study_hours_per_week = np.random.normal(loc=12, scale=5, size=num_samples).clip(0, 40)
    attendance_percentage = np.random.normal(loc=85, scale=10, size=num_samples).clip(0, 100)
    assignments_completed = np.random.randint(0, 11, size=num_samples) # 0 to 10 assignments
    extracurricular_activities = np.random.choice([0, 1], size=num_samples, p=[0.6, 0.4])
    
    # 3. Intermediate Academic Performance
    # We create correlated features to make the model realistic
    # Higher attendance and study hours usually lead to better quiz scores
    quiz_scores_avg = (attendance_percentage * 0.4) + (study_hours_per_week * 1.5) + np.random.normal(0, 5, num_samples)
    quiz_scores_avg = quiz_scores_avg.clip(0, 100)
    
    # 4. Generate Target Variable (Final Performance Category)
    # Let's create a hidden 'true score' to determine the category
    true_score = (
        (attendance_percentage * 0.3) +
        (study_hours_per_week * 2.0) +
        (assignments_completed * 3.0) +
        (quiz_scores_avg * 0.4) +
        (extracurricular_activities * 2.0) +
        np.random.normal(0, 5, num_samples) # Add some noise
    )
    
    # Determine percentiles for categories
    # Low: Bottom 20%, Medium: Middle 60%, High: Top 20%
    threshold_low = np.percentile(true_score, 20)
    threshold_high = np.percentile(true_score, 80)
    
    performance_class = []
    for score in true_score:
        if score <= threshold_low:
            performance_class.append('Low')
        elif score >= threshold_high:
            performance_class.append('High')
        else:
            performance_class.append('Medium')
            
    # Combine into DataFrame
    df = pd.DataFrame({
        'Student_ID': student_id,
        'Gender': gender,
        'Parent_Education': parent_education,
        'Study_Hours_Per_Week': np.round(study_hours_per_week, 1),
        'Attendance_Percentage': np.round(attendance_percentage, 1),
        'Assignments_Completed': assignments_completed,
        'Extracurricular_Activities': extracurricular_activities,
        'Quiz_Scores_Avg': np.round(quiz_scores_avg, 1),
        'Performance_Class': performance_class
    })
    
    return df

if __name__ == "__main__":
    print("Generating synthetic student data...")
    df = generate_synthetic_student_data(2000)
    
    # Create directory if it doesn't exist
    os.makedirs('../data', exist_ok=True)
    
    output_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'student_performance_data.csv')
    df.to_csv(output_path, index=False)
    
    print(f"Data successfully generated and saved to {os.path.abspath(output_path)}")
    print("\nClass Distribution:")
    print(df['Performance_Class'].value_counts())
    print("\nSample Data:")
    print(df.head())
