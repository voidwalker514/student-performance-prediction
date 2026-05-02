# Student Performance Prediction System 🎓🤖

An industry-ready end-to-end Machine Learning pipeline that predicts a student's end-term performance based on semester-long academic signals.

## 🌟 Project Overview

### What is Student Performance Prediction?
This system uses current student habits (attendance, study hours, assignments, engagement) to predict whether they are likely to pass, fail, or excel at the end of the term.

### Why is it Important?
Schools and EdTech companies use these AI models to shift from *reactive* to *proactive* education:
- **Identifying Weak Students:** Early warning system for "at-risk" students.
- **Personalized Learning:** Recommends specific interventions.
- **Dropout Prevention:** Intervening before a student fails out.

## 🛠️ Tech Stack
- **Data Engineering:** Python, Pandas, Numpy (Synthetic Data Generation)
- **Machine Learning:** Scikit-Learn (Random Forest Classification), Joblib
- **Backend API:** FastAPI, Uvicorn, Pydantic
- **Frontend Dashboard:** Vanilla HTML5, CSS3 (Premium UI), Vanilla JS
- **Data Visualization:** Matplotlib, Seaborn

## 🧠 Architecture & Data Flow

1. **Synthetic Data Generator** (`src/generate_data.py`): Creates realistic, statistically correlated student records.
2. **Preprocessing & EDA** (`notebooks/01_EDA_and_Training.py`): Visualizes feature correlations and distributions.
3. **Model Training** (`src/train_model.py`): Trains a Scikit-Learn `RandomForestClassifier` pipeline (with `StandardScaler` and `OneHotEncoder`).
4. **FastAPI Backend** (`main.py`): Serves the `.pkl` model via a RESTful `/predict` endpoint.
5. **Frontend Dashboard** (`frontend/index.html`): A beautiful, modern interface to input student data and view AI risk assessments.

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/Student-Performance-Prediction.git
cd Student-Performance-Prediction
```

### 2. Create a Virtual Environment and Install Dependencies
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
# source venv/bin/activate

pip install -r requirements.txt
```

### 3. Generate Data and Train the Model
If you want to run the pipeline from scratch:
```bash
python src/generate_data.py
python src/train_model.py
```
*(This will generate the CSV in `data/` and the `.pkl` file in `models/`)*

## 🏃‍♂️ Running the Project

You need to run the **Backend API** and open the **Frontend Dashboard**.

### Step 1: Start the Backend (FastAPI)
Run this command from the root directory:
```bash
python -m uvicorn main:app --reload --port 8001
```
The API will be live at `http://127.0.0.1:8001`.
You can view the interactive API documentation at `http://127.0.0.1:8001/docs`.

### Step 2: Open the Frontend
Since the frontend is built with pure HTML/JS/CSS, no server is required! 
Simply double-click the `index.html` file inside the `frontend/` folder, or right-click it and select "Open with your browser".

## 📊 Virtual Simulation Explanation
Since real academic records are highly confidential (FERPA), this project utilizes a custom data synthesizer.
- **Correlated Variables:** The script mathematically ties `Study_Hours` and `Attendance` to the `Quiz_Scores_Avg` to mimic real-world behavior.
- **Noise Injection:** Gaussian noise is added to prevent the model from achieving 100% unrealistic accuracy.
- **Performance Classes:** Target variables are segmented into percentiles (High, Medium, Low Risk).

## 💼 Proof Strategy (For Placements/Internships)
When explaining this in an interview:
1. **Explain the "Why":** "I wanted to solve the problem of student dropouts using AI."
2. **Explain the "How":** "Since I didn't have school data, I simulated a statistically sound dataset, trained a Random Forest model, and deployed it as a microservice using FastAPI."
3. **Show the UI:** Demonstrate the sleek frontend and how the "Interventions" change dynamically based on the risk level.

## 📊 Data Insights & Visualizations

### 1. Feature Correlations
Understanding how different academic signals relate to each other.
![Correlation Matrix](./images/correlation_matrix.png)

### 2. Attendance vs Study Hours
A look at the distribution of the two most critical features.
![Attendance vs Study](./images/attendance_vs_study.png)

### 3. Model Performance
How well the Random Forest model is performing.
![Confusion Matrix](./images/confusion_matrix.png)

### 4. Feature Importance
Which factors actually drive student performance?
![Feature Importance](./images/feature_importance.png)

## ⚖️ License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

---
*Built with ❤️ for Data Science & ML Engineering Portfolios.*
