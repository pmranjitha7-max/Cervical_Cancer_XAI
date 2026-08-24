import pandas as pd
import joblib

print("=" * 60)
print("HPV PREDICTION")
print("=" * 60)

# -----------------------------
# Load Model
# -----------------------------
model = joblib.load("models/hpv_model.pkl")

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv("dataset/cleaned_cervical_cancer.csv")

# -----------------------------
# Select Patient
# -----------------------------
patient_id = int(input("Enter Patient ID (0-857): "))

patient = df.iloc[[patient_id]]

# -----------------------------
# Remove Target Column
# -----------------------------
X = patient.drop(columns=["Dx:HPV"])

# -----------------------------
# Prediction
# -----------------------------
prediction = model.predict(X)[0]

probability = model.predict_proba(X)[0]

# -----------------------------
# Display Result
# -----------------------------
print("\nPrediction Result")
print("-" * 30)

if prediction == 1:
    print("HPV Prediction : POSITIVE")
else:
    print("HPV Prediction : NEGATIVE")

print(f"Probability (Negative): {probability[0]*100:.2f}%")
print(f"Probability (Positive): {probability[1]*100:.2f}%")

# -----------------------------
# Recommendation
# -----------------------------
print("\nRecommendation")
print("-" * 30)

if prediction == 1:
    print("Patient may have HPV.")
    print("Consult a gynecologist for further evaluation.")
    print("Regular follow-up is recommended.")
else:
    print("Low HPV risk predicted.")
    print("Continue regular cervical screening.")

print("=" * 60)