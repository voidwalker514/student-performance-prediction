document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prediction-form');
    const initialState = document.getElementById('initial-state');
    const loadingState = document.getElementById('loading-state');
    const resultState = document.getElementById('result-state');
    
    // Navigation Elements
    const navDashboard = document.getElementById('nav-dashboard');
    const navStudents = document.getElementById('nav-students');
    const navAnalytics = document.getElementById('nav-analytics');
    const views = document.querySelectorAll('.view');
    const navLinks = document.querySelectorAll('.nav-menu a');

    // View Containers
    const dashboardView = document.getElementById('dashboard-view');
    const studentsView = document.getElementById('students-view');
    const analyticsView = document.getElementById('analytics-view');

    // UI Elements for Results
    const riskBadge = document.getElementById('risk-badge');
    const predClass = document.getElementById('pred-class');
    const predConfidence = document.getElementById('pred-confidence');
    const interventionBox = document.getElementById('intervention-box');
    const interventionText = document.getElementById('intervention-text');
    const exportBtn = document.getElementById('export-btn');

    // Navigation Logic
    function switchView(viewId, activeLink) {
        views.forEach(view => view.classList.add('hidden'));
        document.getElementById(viewId).classList.remove('hidden');
        
        navLinks.forEach(link => link.classList.remove('active'));
        activeLink.classList.add('active');
        
        if (viewId === 'students-view') {
            populateStudentsTable();
        }
    }

    navDashboard.addEventListener('click', () => switchView('dashboard-view', navDashboard));
    navStudents.addEventListener('click', () => switchView('students-view', navStudents));
    navAnalytics.addEventListener('click', () => switchView('analytics-view', navAnalytics));

    // Export Logic
    exportBtn.addEventListener('click', () => {
        window.print();
    });

    // Mock Student Data
    const mockStudents = [
        { id: "STU001", gender: "Male", attendance: 92, hours: 25, quiz: 88, risk: "Low" },
        { id: "STU002", gender: "Female", attendance: 45, hours: 5, quiz: 32, risk: "High" },
        { id: "STU003", gender: "Female", attendance: 78, hours: 15, quiz: 65, risk: "Medium" },
        { id: "STU004", gender: "Male", attendance: 95, hours: 30, quiz: 92, risk: "Low" },
        { id: "STU005", gender: "Male", attendance: 60, hours: 8, quiz: 45, risk: "High" },
        { id: "STU006", gender: "Female", attendance: 82, hours: 18, quiz: 70, risk: "Medium" },
    ];

    function populateStudentsTable() {
        const tbody = document.getElementById('students-table-body');
        tbody.innerHTML = '';
        
        mockStudents.forEach(student => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${student.id}</td>
                <td>${student.gender}</td>
                <td>${student.attendance}%</td>
                <td>${student.hours}h</td>
                <td>${student.quiz}</td>
                <td><span class="risk-tag ${student.risk.toLowerCase()}">${student.risk} Risk</span></td>
            `;
            tbody.appendChild(tr);
        });
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Hide initial and result states, show loading
        initialState.classList.add('hidden');
        resultState.classList.add('hidden');
        loadingState.classList.remove('hidden');

        // Gather form data
        const payload = {
            Gender: document.getElementById('gender').value,
            Parent_Education: document.getElementById('parent_education').value,
            Study_Hours_Per_Week: parseFloat(document.getElementById('study_hours').value),
            Attendance_Percentage: parseFloat(document.getElementById('attendance').value),
            Assignments_Completed: parseInt(document.getElementById('assignments').value, 10),
            Extracurricular_Activities: parseInt(document.getElementById('extracurricular').value, 10),
            Quiz_Scores_Avg: parseFloat(document.getElementById('quiz_scores').value)
        };

        try {
            // Call the FastAPI endpoint
            const response = await fetch('http://localhost:8001/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                throw new Error('Prediction failed. Is the backend running?');
            }

            const data = await response.json();
            
            // Artificial delay to simulate processing and show off the loading animation
            setTimeout(() => {
                displayResults(data, payload);
            }, 800);

        } catch (error) {
            console.error(error);
            alert("Error: Could not connect to the Prediction API. Please ensure the backend is running on http://localhost:8001.");
            loadingState.classList.add('hidden');
            initialState.classList.remove('hidden');
        }
    });

    function displayResults(data, payload) {
        // Hide loading
        loadingState.classList.add('hidden');
        
        // Update DOM elements
        predClass.textContent = data.prediction;
        predConfidence.textContent = (data.confidence * 100).toFixed(1) + '%';
        
        // Configure Risk Badge and Intervention based on Risk Level
        riskBadge.className = 'risk-badge'; // reset
        
        let iconHtml = '';
        let titleText = '';
        
        if (data.risk_level === 'High Risk') {
            riskBadge.classList.add('high-risk');
            iconHtml = '<i data-lucide="alert-triangle"></i>';
            titleText = 'High Risk of Failure';
            interventionBox.style.borderLeftColor = 'var(--danger)';
            
            // Generate tailored intervention
            let reasons = [];
            if (payload.Attendance_Percentage < 75) reasons.push("Low attendance");
            if (payload.Study_Hours_Per_Week < 10) reasons.push("Insufficient study hours");
            if (payload.Assignments_Completed < 5) reasons.push("Missing assignments");
            
            let reasonText = reasons.length > 0 ? ` (Factors: ${reasons.join(', ')}). ` : ". ";
            interventionText.textContent = `Immediate intervention required${reasonText}Schedule a 1-on-1 meeting with the academic counselor. Recommend mandatory tutoring sessions.`;
            
        } else if (data.risk_level === 'Medium Risk') {
            riskBadge.classList.add('medium-risk');
            iconHtml = '<i data-lucide="alert-circle"></i>';
            titleText = 'Medium Risk (Monitor)';
            interventionBox.style.borderLeftColor = 'var(--warning)';
            
            interventionText.textContent = "Student is passing but underperforming. Send a check-in email and recommend joining a study group. Monitor attendance closely.";
            
        } else {
            riskBadge.classList.add('low-risk');
            iconHtml = '<i data-lucide="check-circle"></i>';
            titleText = 'Low Risk (On Track)';
            interventionBox.style.borderLeftColor = 'var(--secondary)';
            
            interventionText.textContent = "Student is performing excellently. No intervention needed. Consider recommending advanced coursework or peer mentoring roles.";
        }
        
        riskBadge.innerHTML = `${iconHtml}<h4>${titleText}</h4>`;
        
        // Re-initialize icons for dynamically inserted HTML
        lucide.createIcons();
        
        // Show result
        resultState.classList.remove('hidden');
    }
});
