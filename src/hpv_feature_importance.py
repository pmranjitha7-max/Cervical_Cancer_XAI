import pandas as pd
import joblib
import matplotlib.pyplot as plt

print("=" * 60)
print("HPV FEATURE IMPORTANCE")
print("=" * 60)

# -----------------------------
# Load Model
# -----------------------------
model = joblib.load("models/hpv_model.pkl")

print("Model loaded successfully.")

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv("dataset/cleaned_cervical_cancer.csv")

print("Dataset loaded successfully.")

# -----------------------------
# Features
# -----------------------------
X = df.drop(columns=["Dx:HPV"])

feature_names = X.columns

# -----------------------------
# Feature Importance
# -----------------------------
importance = model.feature_importances_

importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": importance
})

importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
)

print("\nTop 10 Most Important Features\n")
print(importance_df.head(10))

# -----------------------------
# Plot
# -----------------------------
plt.figure(figsize=(10,6))

plt.barh(
    importance_df["Feature"][:10],
    importance_df["Importance"][:10]
)

plt.gca().invert_yaxis()

plt.title("Top 10 Feature Importance for HPV Prediction")

plt.xlabel("Importance")

plt.tight_layout()

plt.savefig("results/hpv_feature_importance.png")

plt.show()

print("\nFeature importance graph saved successfully!")

print("=" * 60)