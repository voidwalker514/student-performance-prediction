import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def run_eda():
    print("Starting Exploratory Data Analysis...")
    
    # Load data
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'student_performance_data.csv')
    df = pd.read_csv(data_path)
    
    print("\nDataset Info:")
    print(df.info())
    
    print("\nMissing Values:")
    print(df.isnull().sum())
    
    print("\nSummary Statistics:")
    print(df.describe())
    
    # Create images directory
    img_dir = os.path.join(os.path.dirname(__file__), '..', 'images')
    os.makedirs(img_dir, exist_ok=True)
    
    # 1. Target Variable Distribution
    plt.figure(figsize=(8, 5))
    sns.countplot(data=df, x='Performance_Class', order=['Low', 'Medium', 'High'], palette='viridis')
    plt.title('Distribution of Performance Classes')
    plt.savefig(os.path.join(img_dir, 'target_distribution.png'))
    plt.close()
    
    # 2. Correlation Matrix (Numerical features)
    plt.figure(figsize=(10, 8))
    numerical_cols = df.select_dtypes(include=['float64', 'int64', 'int32']).columns
    # Exclude Student_ID
    numerical_cols = [col for col in numerical_cols if col != 'Student_ID']
    
    corr_matrix = df[numerical_cols].corr()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Feature Correlation Matrix')
    plt.savefig(os.path.join(img_dir, 'correlation_matrix.png'))
    plt.close()
    
    # 3. Attendance vs Study Hours colored by Performance
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='Attendance_Percentage', y='Study_Hours_Per_Week', hue='Performance_Class', palette='viridis', alpha=0.7)
    plt.title('Attendance vs Study Hours by Performance')
    plt.savefig(os.path.join(img_dir, 'attendance_vs_study.png'))
    plt.close()
    
    print(f"\nEDA Complete. Visualizations saved to {os.path.abspath(img_dir)}")

if __name__ == "__main__":
    run_eda()
