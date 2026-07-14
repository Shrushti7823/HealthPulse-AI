# 🩺 HealthPulse AI

## AI-Powered Health Companion
 
**SDG 3: Good Health and Well-being**

HealthPulse AI is a healthcare web application that helps users monitor their health through AI-powered features. It combines a health chatbot, a diabetes risk prediction model, and a personal dashboard to support better health awareness and medication management.

---

# Problem Statement

Many people living with or at risk of diabetes find it difficult to monitor their health regularly and remember their medications. Lack of continuous health tracking can delay the identification of health risks and lead to serious complications.

HealthPulse AI aims to provide an easy-to-use digital solution that encourages preventive healthcare and improves health awareness.

---

# Project Objective

- Provide an AI-based health assistant for common health queries.
- Predict diabetes risk using Machine Learning.
- Track health records through an interactive dashboard.
- Help users manage medication reminders.
- Promote healthy lifestyle awareness.

---

# HealthPulse AI consists of three main modules.

### Health Chat Assistant

A rule-based chatbot that can:

- Answer common health questions
- Provide basic diet and exercise suggestions
- Record simple symptom information
- Assist with medication reminders

---

### 📊 Diabetes Risk Prediction

Users enter important health information such as:

- Pregnancies
- Glucose
- Blood Pressure
- Skin Thickness
- Insulin
- BMI
- Diabetes Pedigree Function
- Age

A trained **Random Forest Classifier** predicts:

- Diabetes Risk Percentage
- Risk Category
- Important health factors affecting the prediction

---

### 📈 Health Dashboard

The dashboard displays:

- Diabetes risk history
- Glucose trend
- BMI trend
- Medication reminders
- Medication adherence statistics

---

# Features

- AI-based Health Chatbot
- Diabetes Risk Prediction
- Explainable Machine Learning Results
- Interactive Dashboard
- Medication Reminder Management
- Health History Tracking
- SQLite Database Storage
- Offline Functionality

---

# Technology Stack

### Frontend
- HTML5
- CSS3
- JavaScript
- Chart.js

### Backend
- Python
- Flask

### Machine Learning
- Scikit-learn
- Pandas
- NumPy

### Database
- SQLite

### Dataset
Pima Indians Diabetes Dataset (UCI Repository)

---

#  Installation

### Clone Repository

```bash
git clone https://github.com/Shrushti7823/HealthPulse-AI.git
```

#  Why Rule-Based Chatbot?

The chatbot uses rule-based intent matching instead of a generative AI model. This approach provides consistent responses, works offline, avoids unpredictable answers, and does not require any external API.

---

#  Future Improvements

- User Login System
- Family Health Profiles
- Cloud Deployment
- SMS or Email Medication Reminders
- Wearable Device Integration
- Heart Disease Prediction
- Multi-language Support
- Doctor/Caregiver Dashboard

#  Sustainable Development Goal

**SDG 3 – Good Health and Well-being**

HealthPulse AI supports preventive healthcare by helping users monitor their health, assess diabetes risk, and improve medication adherence through Artificial Intelligence.

---

# 📄 License

This project was developed for educational purposes as part of the **Lenovo AI Capstone Project (Bharat Cares LEAP Program)**.
