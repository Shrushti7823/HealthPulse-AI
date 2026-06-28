"""
HealthPulse AI  - Flask Backend
SDG 3: Good Health and Well-being

Combines three AI-powered features into one app:
  1. Conversational chatbot for reminders, symptom logging & health Q&A
  2. ML-based diabetes risk prediction (RandomForest, trained on Pima dataset)
  3. Dashboard with vitals trends, risk history & medication adherence
"""
from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import pandas as pd
import os

import database
import chatbot

app = Flask(__name__)

MODEL_DIR = os.path.join(os.path.dirname(__file__), "model")
model = joblib.load(os.path.join(MODEL_DIR, "diabetes_model.pkl"))
scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))

FEATURE_ORDER = [
    "pregnancies", "glucose", "blood_pressure", "skin_thickness",
    "insulin", "bmi", "diabetes_pedigree", "age"
]

database.init_db()


@app.route("/")
def index():
    return render_template("index.html")


# ---------- ML Risk Prediction ----------
@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.get_json()

    try:
        features = [float(data.get(f, 0)) for f in FEATURE_ORDER]
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid input. All fields must be numeric."}), 400

    X = pd.DataFrame([features], columns=FEATURE_ORDER)
    X_scaled = scaler.transform(X)

    proba = model.predict_proba(X_scaled)[0][1]
    risk_score = round(proba * 100, 1)

    if risk_score < 30:
        label = "Low Risk"
    elif risk_score < 60:
        label = "Moderate Risk"
    else:
        label = "High Risk"

    # Save to history for the dashboard
    database.add_vitals_entry(
        glucose=features[1],
        bmi=features[5],
        blood_pressure=features[2],
        risk_score=risk_score,
        risk_label=label
    )

    top_factors = []
    importances = dict(zip(FEATURE_ORDER, model.feature_importances_))
    sorted_factors = sorted(importances.items(), key=lambda x: x[1], reverse=True)[:3]
    for factor, _ in sorted_factors:
        top_factors.append(factor.replace("_", " ").title())

    return jsonify({
        "risk_score": risk_score,
        "risk_label": label,
        "top_factors": top_factors
    })


# ---------- Chatbot ----------
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")

    if not message:
        return jsonify({"error": "No message provided"}), 400

    database.log_chat("user", message)
    reply = chatbot.get_response(message)
    database.log_chat("bot", reply)

    return jsonify({"reply": reply})


@app.route("/api/chat/history", methods=["GET"])
def chat_history():
    return jsonify(database.get_chat_history())


# ---------- Dashboard data ----------
@app.route("/api/history", methods=["GET"])
def history():
    return jsonify(database.get_vitals_history())


# ---------- Reminders ----------
@app.route("/api/reminders", methods=["GET"])
def get_reminders():
    return jsonify(database.get_reminders())


@app.route("/api/reminders", methods=["POST"])
def add_reminder():
    data = request.get_json()
    med_name = data.get("med_name")
    reminder_time = data.get("reminder_time")
    frequency = data.get("frequency", "Daily")

    if not med_name or not reminder_time:
        return jsonify({"error": "med_name and reminder_time are required"}), 400

    database.add_reminder(med_name, reminder_time, frequency)
    return jsonify({"status": "ok"})


@app.route("/api/reminders/<int:reminder_id>/taken", methods=["POST"])
def mark_taken(reminder_id):
    data = request.get_json() or {}
    taken = 1 if data.get("taken", True) else 0
    database.mark_reminder_taken(reminder_id, taken)
    return jsonify({"status": "ok"})


@app.route("/api/adherence", methods=["GET"])
def adherence():
    return jsonify(database.get_adherence_stats())


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)