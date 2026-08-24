import pandas as pd
import joblib
import lime
import lime.lime_tabular

print("=" * 60)
print("HPV LIME EXPLAINABLE AI")
print("=" * 60)

# Load trained HPV model
model = joblib.load("models/hpv_model.pkl")
print("Model loaded successfully.")

# Load cleaned dataset
df = pd.read_csv("dataset/cleaned_cervical_cancer.csv")

# Features and Target
X = df.drop("Dx:HPV", axis=1)
y = df["Dx:HPV"]

print("Dataset loaded successfully.")

# Create LIME Explainer
explainer = lime.lime_tabular.LimeTabularExplainer(
    training_data=X.values,
    feature_names=X.columns.tolist(),
    class_names=["Negative", "Positive"],
    mode="classification"
)

print("LIME Explainer created successfully.")

# Select Patient
patient_id = int(input("Enter Patient ID (0-857): "))

instance = X.iloc[patient_id]

print("Generating explanation...")

# Generate Explanation
exp = explainer.explain_instance(
    instance.values,
    model.predict_proba,
    num_features=10
)

# Save HTML Report
exp.save_to_file("results/hpv_lime_explanation.html")

print("LIME explanation generated successfully!")
print("Saved to: results/hpv_lime_explanation.html")

print("=" * 60)