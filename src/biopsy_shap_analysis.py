import pandas as pd
import joblib
import shap
import matplotlib.pyplot as plt

print("=" * 60)
print("SHAP EXPLAINABLE AI")
print("=" * 60)

# Load trained SMOTE model
model = joblib.load("models/random_forest_smote.pkl")
print("Model loaded successfully.")

# Load cleaned dataset
df = pd.read_csv("dataset/cleaned_cervical_cancer.csv")

# Features only
X = df.drop("Biopsy", axis=1)

print("Dataset loaded successfully.")

# Create SHAP Explainer
explainer = shap.Explainer(model, X)

print("Calculating SHAP values...")

# Calculate SHAP values
shap_values = explainer(X)

print("SHAP values calculated successfully.")

print(type(shap_values.values))
print(shap_values.values.shape)

# Select SHAP values for the positive class (Biopsy = 1)
shap_values_positive = shap.Explanation(
    values=shap_values.values[:, :, 1],
    base_values=shap_values.base_values[:, 1],
    data=shap_values.data,
    feature_names=X.columns
)
# SHAP Beeswarm Plot
shap.plots.beeswarm(shap_values_positive, max_display=10, show=False)

plt.tight_layout()
plt.savefig("results/shap_summary.png", dpi=300)

print("SHAP summary plot saved successfully!")
print("Location: results/shap_summary.png")

plt.show()