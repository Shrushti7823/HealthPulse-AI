# HealthPulse AI  🩺

**Capstone Project — AI Final Project**
**SDG 3: Good Health and Well-being**

An AI-powered health companion that helps people manage chronic-disease risk through three integrated features: a conversational assistant, a machine-learning diabetes risk predictor, and a personal health dashboard.

---

## 1. Problem Statement

Millions of people with — or at risk of — chronic conditions like diabetes struggle with two things: **forgetting medications** and **having no easy way to track health trends** over time. This is especially true in underserved communities with limited access to regular doctor visits. Missed doses and unnoticed risk factors (rising glucose, climbing BMI) often go unaddressed until they become serious complications, even though early awareness is one of the most effective and low-cost ways to prevent that outcome.

## 2. Project Objective

To build a single, accessible AI application that:
- Answers everyday health questions and manages medication reminders through a chatbot
- Estimates a user's diabetes risk using a trained machine learning model
- Visualizes vitals trends and medication adherence so users (and caregivers) can spot patterns early

## 3. Solution Description

HealthPulse AI  is a Flask web application with three integrated modules:

| Module | How it works |
|---|---|
| **Chat Assistant** | An intent-matching conversational engine recognizes patterns in user messages (greetings, diet questions, symptom logging, reminder requests, etc.) and responds with relevant, safe guidance. |
| **Risk Check** | A user enters 8 health indicators (glucose, BMI, blood pressure, age, etc.). A `RandomForestClassifier` trained on the Pima Indians Diabetes dataset returns a risk score (0–100%), a risk category, and the top contributing factors. |
| **Dashboard** | Charts (via Chart.js) plot risk-score history and glucose/BMI trends over time. A reminder tracker lets users log medications and see their adherence percentage. |

All three modules share the same backend and database, so a risk check automatically logs into the dashboard's history.

## 4. Project Features

- 🤖 **Conversational health assistant** — reminders, symptom check-ins, diet/exercise guidance, no external API required (fully offline-capable)
- 📊 **ML diabetes risk prediction** — RandomForest model, 75% accuracy / 0.81 ROC-AUC on held-out test data
- 🧠 **Explainable predictions** — shows the top 3 factors driving each risk score
- 📈 **Personal health dashboard** — risk history chart, glucose/BMI trend chart, medication adherence ring
- ⏰ **Medication reminders** — add reminders, mark as taken, track adherence over time
- 💾 **Persistent storage** — SQLite database, no setup required

## 5. Technology Stack

- **Backend:** Python, Flask
- **Machine Learning:** scikit-learn (RandomForestClassifier), pandas, NumPy
- **Dataset:** [Pima Indians Diabetes Dataset](https://github.com/jbrownlee/Datasets) (public, UCI-derived)
- **Frontend:** HTML5, CSS3, vanilla JavaScript, Chart.js
- **Database:** SQLite
- **Chatbot:** Rule-based intent matching (regex), chosen deliberately for reliability, transparency, and zero external dependency — see *Design Notes* below

## 6. Project Screenshots

> Add your own screenshots here after running the app locally (see Setup below):
> - Chat Assistant tab in use
> - Risk Check form + result
> - Dashboard with charts and reminders

## 7. Setup & Run Locally

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd HealthPulse -ai

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Already trained, but to retrain the model yourself)
python model/train_model.py

# 4. Run the app
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

## 8. Design Notes — Why a rule-based chatbot?

For a health-adjacent assistant, predictable and explainable answers matter more than open-ended generative responses. A regex/intent-matching approach guarantees the bot never gives unsafe or hallucinated medical advice, works without an internet connection or API key, and makes the system's behavior fully auditable — appropriate for a real-world deployment in low-connectivity or resource-constrained settings, which is central to this SDG's goal of equitable healthcare access.

## 9. Future Scope

- Add user authentication for multi-patient/family support
- Integrate wearable device data (e.g. Fitbit, smartwatch API) for automatic vitals logging
- Add SMS/push notifications for medication reminders
- Expand the ML model to predict additional conditions (hypertension, heart disease)
- Add multilingual chatbot support for wider accessibility
- Deploy to the cloud (Render/Railway/Azure) with a production WSGI server
- Add a caregiver/doctor view to monitor adherence and risk trends remotely

## 10. License

This project was built for educational purposes as part of the Lenovo AI Capstone Project (Bharat Cares LEAP program).
