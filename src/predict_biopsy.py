import pandas as pd
import joblib

print("=" * 60)
print("BIOPSY PREDICTION")
print("=" * 60)

# -----------------------------
# Load Model
# -----------------------------
model = joblib.load("models/biopsy_model.pkl")

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
X = patient.drop(columns=["Biopsy"])

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
    print("Biopsy Prediction : POSITIVE")
else:
    print("Biopsy Prediction : NEGATIVE")

print(f"Probability (Negative): {probability[0]*100:.2f}%")
print(f"Probability (Positive): {probability[1]*100:.2f}%")

# -----------------------------
# Recommendation
# -----------------------------
print("\nRecommendation")
print("-" * 30)

if prediction == 1:
    print("High cervical cancer risk predicted.")
    print("Consult a gynecologist immediately.")
    print("Further diagnostic tests are recommended.")
else:
    print("Low cervical cancer risk predicted.")
    print("Continue regular cervical screening.")

print("=" * 60)