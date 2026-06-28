"""
HealthPulse AI  - Diabetes Risk Model Training
Trains a RandomForest classifier on the Pima Indians Diabetes dataset
and saves it for use by the Flask app.
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
import joblib
import os

COLUMNS = [
    "pregnancies", "glucose", "blood_pressure", "skin_thickness",
    "insulin", "bmi", "diabetes_pedigree", "age", "outcome"
]

def load_data():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "diabetes.csv")
    df = pd.read_csv(path, names=COLUMNS)

    # Some columns use 0 as a placeholder for "missing" — replace with median
    cols_with_invalid_zero = ["glucose", "blood_pressure", "skin_thickness", "insulin", "bmi"]
    for col in cols_with_invalid_zero:
        df[col] = df[col].replace(0, np.nan)
        df[col] = df[col].fillna(df[col].median())
    return df

def train():
    df = load_data()
    X = df.drop("outcome", axis=1)
    y = df["outcome"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = RandomForestClassifier(
        n_estimators=200, max_depth=6, min_samples_leaf=4, random_state=42
    )
    model.fit(X_train_scaled, y_train)

    preds = model.predict(X_test_scaled)
    proba = model.predict_proba(X_test_scaled)[:, 1]

    print("Accuracy:", round(accuracy_score(y_test, preds), 3))
    print("ROC-AUC:", round(roc_auc_score(y_test, proba), 3))
    print(classification_report(y_test, preds))

    out_dir = os.path.dirname(__file__)
    joblib.dump(model, os.path.join(out_dir, "diabetes_model.pkl"))
    joblib.dump(scaler, os.path.join(out_dir, "scaler.pkl"))
    print("Model + scaler saved to model/")

    # Feature importance for transparency in the dashboard
    importances = dict(zip(X.columns, model.feature_importances_.round(3)))
    print("Feature importances:", importances)

if __name__ == "__main__":
    train()
