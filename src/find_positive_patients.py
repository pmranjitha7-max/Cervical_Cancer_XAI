import pandas as pd
import joblib

print("=" * 70)
print("FIND POSITIVE PATIENT PREDICTIONS")
print("=" * 70)

# Load dataset
df = pd.read_csv("dataset/cleaned_cervical_cancer.csv")

# Load models
biopsy_model = joblib.load("models/biopsy_model.pkl")
hpv_model = joblib.load("models/hpv_model.pkl")

print("Dataset and models loaded successfully.")

# Prepare features for each model
biopsy_X = df.drop(columns=["Biopsy"])
hpv_X = df.drop(columns=["Dx:HPV"])

# Make predictions for all patients
biopsy_predictions = biopsy_model.predict(biopsy_X)
hpv_predictions = hpv_model.predict(hpv_X)

biopsy_probabilities = biopsy_model.predict_proba(biopsy_X)[:, 1]
hpv_probabilities = hpv_model.predict_proba(hpv_X)[:, 1]

# Store positive predictions
positive_rows = []

for patient_id in range(len(df)):
    biopsy_positive = int(biopsy_predictions[patient_id]) == 1
    hpv_positive = int(hpv_predictions[patient_id]) == 1

    if biopsy_positive or hpv_positive:
        positive_rows.append(
            {
                "patient_id": patient_id,
                "actual_biopsy": int(df.iloc[patient_id]["Biopsy"]),
                "predicted_biopsy": int(biopsy_predictions[patient_id]),
                "biopsy_positive_probability": round(
                    float(biopsy_probabilities[patient_id]) * 100, 2
                ),
                "actual_hpv": int(df.iloc[patient_id]["Dx:HPV"]),
                "predicted_hpv": int(hpv_predictions[patient_id]),
                "hpv_positive_probability": round(
                    float(hpv_probabilities[patient_id]) * 100, 2
                ),
            }
        )

results = pd.DataFrame(positive_rows)

print("\nPOSITIVE PREDICTION RESULTS")
print("-" * 70)

if results.empty:
    print("No positive predictions found.")
else:
    print(results.to_string(index=False))

    # Save results
    results.to_csv(
        "results/positive_patient_predictions.csv",
        index=False
    )

    print("\nResults saved to:")
    print("results/positive_patient_predictions.csv")

print("\nSUMMARY")
print("-" * 70)
print("Biopsy positive predictions:",
      int((biopsy_predictions == 1).sum()))
print("HPV positive predictions:",
      int((hpv_predictions == 1).sum()))
print("Patients positive in either model:",
      len(results))

print("=" * 70)