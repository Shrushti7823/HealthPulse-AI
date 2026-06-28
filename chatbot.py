"""
HealthPulse AI  - Conversational Assistant
A lightweight, fully self-contained intent-matching chatbot. No external API
required, which keeps the project reproducible and free to run for anyone
who clones the repo.

Design note: a rule-based intent matcher was chosen deliberately over a
generic LLM call for this assistant — it is deterministic, explainable,
works offline, and gives consistent, safe answers for a health-adjacent
use case (see README "Why rule-based?" for the full reasoning).
"""
import re
from datetime import datetime

INTENTS = {
    "greeting": {
        "patterns": [r"\bhi\b", r"\bhello\b", r"\bhey\b", r"good (morning|afternoon|evening)"],
        "responses": [
            "Hi there! I'm HealthPulse , your AI health companion. I can help you set medication reminders, log how you're feeling, or answer general questions about diabetes risk factors. What would you like to do?"
        ]
    },
    "reminder_set": {
        "patterns": [r"remind me", r"set a reminder", r"medication reminder", r"add reminder"],
        "responses": [
            "I can set that up. Use the 'Add Reminder' box on the Dashboard tab with the medicine name, time, and frequency — I'll track your adherence streak from there."
        ]
    },
    "reminder_check": {
        "patterns": [r"did i take", r"my reminders", r"medication today", r"have i taken"],
        "responses": [
            "Check your Dashboard tab — today's reminders are listed there with a 'Mark as taken' button so we can keep your adherence stats accurate."
        ]
    },
    "log_symptom": {
        "patterns": [r"feel(ing)? (tired|dizzy|thirsty|unwell)", r"log (my )?symptom", r"not feeling well", r"i feel"],
        "responses": [
            "Thanks for sharing. Frequent thirst, fatigue, or dizziness can sometimes relate to blood sugar swings — it's worth logging your glucose on the 'Check Risk' tab and mentioning this to a doctor if it continues. I'm not a substitute for medical advice, just a helpful nudge."
        ]
    },
    "diet": {
        "patterns": [r"diet", r"what (should|can) i eat", r"food", r"nutrition"],
        "responses": [
            "For diabetes risk, general guidance includes: favor high-fiber whole grains, vegetables, and lean protein; limit sugary drinks and refined carbs; and keep portions consistent across meals. This is general wellness info, not a medical prescription — a dietitian can personalize this for you."
        ]
    },
    "exercise": {
        "patterns": [r"exercise", r"workout", r"physical activity", r"how much (should i )?walk"],
        "responses": [
            "Most general guidelines suggest at least 150 minutes of moderate activity a week (e.g. brisk walking, ~30 min, 5 days a week). Regular movement helps the body use insulin more effectively. Start gradually if you're new to exercise."
        ]
    },
    "symptoms_info": {
        "patterns": [r"symptoms of diabetes", r"signs of (high|low) (blood )?sugar", r"warning signs"],
        "responses": [
            "Common warning signs include excessive thirst, frequent urination, unexplained fatigue, blurred vision, and slow-healing wounds. If you notice several of these together, it's worth getting a glucose test from a healthcare provider."
        ]
    },
    "risk_redirect": {
        "patterns": [r"check my risk", r"diabetes risk", r"am i at risk", r"predict"],
        "responses": [
            "Head over to the 'Check Risk' tab — enter your glucose, BMI, blood pressure, and a few other values, and I'll estimate your diabetes risk using a trained machine learning model."
        ]
    },
    "thanks": {
        "patterns": [r"\bthank", r"thanks", r"appreciate it"],
        "responses": ["You're very welcome! Stay on top of your health — I'm here whenever you need a check-in."]
    },
    "goodbye": {
        "patterns": [r"\bbye\b", r"goodbye", r"see you", r"that's all"],
        "responses": ["Take care of yourself! Come back anytime you want to log vitals or check in on a reminder."]
    },
}

FALLBACK_RESPONSES = [
    "I'm best at helping with medication reminders, symptom logging, and general diabetes-risk guidance. Could you rephrase, or try the 'Check Risk' tab for a personalized estimate?",
]


def get_response(message: str) -> str:
    text = message.lower().strip()

    for intent, data in INTENTS.items():
        for pattern in data["patterns"]:
            if re.search(pattern, text):
                return data["responses"][0]

    return FALLBACK_RESPONSES[0]


def get_time_greeting() -> str:
    hour = datetime.now().hour
    if hour < 12:
        return "Good morning"
    elif hour < 17:
        return "Good afternoon"
    return "Good evening"
