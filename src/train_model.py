import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

def train():
    print("Loading data...")
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'student_performance_data.csv')
    df = pd.read_csv(data_path)
    
    # Drop Student_ID as it's not a predictive feature
    X = df.drop(columns=['Student_ID', 'Performance_Class'])
    y = df['Performance_Class']
    
    # Define features
    numeric_features = ['Study_Hours_Per_Week', 'Attendance_Percentage', 'Assignments_Completed', 'Extracurricular_Activities', 'Quiz_Scores_Avg']
    categorical_features = ['Gender', 'Parent_Education']
    
    print("Setting up preprocessing pipeline...")
    # Preprocessing for numeric data
    numeric_transformer = StandardScaler()
    
    # Preprocessing for categorical data
    categorical_transformer = OneHotEncoder(handle_unknown='ignore')
    
    # Combine preprocessing steps
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])
    
    # Create a full pipeline with a Random Forest Classifier
    pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                               ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))])
    
    # Split the data
    print("Splitting data into train and test sets...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Train the model
    print("Training Random Forest model...")
    pipeline.fit(X_train, y_train)
    
    # Predict and evaluate
    print("Evaluating model...")
    y_pred = pipeline.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nAccuracy: {accuracy:.4f}")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save confusion matrix plot
    cm = confusion_matrix(y_test, y_pred, labels=['Low', 'Medium', 'High'])
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Low', 'Medium', 'High'], yticklabels=['Low', 'Medium', 'High'])
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix')
    
    img_dir = os.path.join(os.path.dirname(__file__), '..', 'images')
    os.makedirs(img_dir, exist_ok=True)
    plt.savefig(os.path.join(img_dir, 'confusion_matrix.png'))
    plt.close()
    
    # Feature Importance
    # Get feature names after one hot encoding
    cat_encoder = pipeline.named_steps['preprocessor'].named_transformers_['cat']
    cat_feature_names = cat_encoder.get_feature_names_out(categorical_features)
    all_feature_names = numeric_features + list(cat_feature_names)
    
    importances = pipeline.named_steps['classifier'].feature_importances_
    
    feature_importance_df = pd.DataFrame({
        'Feature': all_feature_names,
        'Importance': importances
    }).sort_values(by='Importance', ascending=False)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=feature_importance_df, x='Importance', y='Feature', palette='viridis')
    plt.title('Feature Importance')
    plt.tight_layout()
    plt.savefig(os.path.join(img_dir, 'feature_importance.png'))
    plt.close()
    
    # Save the model
    models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    model_path = os.path.join(models_dir, 'student_performance_model.pkl')
    joblib.dump(pipeline, model_path)
    print(f"\nModel pipeline saved successfully to {os.path.abspath(model_path)}")

if __name__ == "__main__":
    train()
