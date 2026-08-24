import pandas as pd
import joblib

from lime.lime_tabular import LimeTabularExplainer

print("=" * 60)
print("LIME EXPLAINABLE AI")
print("=" * 60)

# Load trained SMOTE model
model = joblib.load("models/random_forest_smote.pkl")
print("Model loaded successfully.")

# Load dataset
df = pd.read_csv("dataset/cleaned_cervical_cancer.csv")

# Features only
X = df.drop("Biopsy", axis=1)

print("Dataset loaded successfully.")

# Create LIME Explainer
explainer = LimeTabularExplainer(
    training_data=X.values,
    feature_names=X.columns.tolist(),
    class_names=["No Cancer", "Cancer"],
    mode="classification"
)

# Select one patient
patient = X.iloc[0]

print("Explaining prediction for Patient 1...")

# Explain prediction
explanation = explainer.explain_instance(
    patient.values,
    model.predict_proba,
    num_features=10
)

# Save explanation
explanation.save_to_file("results/lime_explanation.html")

print("LIME explanation saved successfully!")
print("Location: results/lime_explanation.html")