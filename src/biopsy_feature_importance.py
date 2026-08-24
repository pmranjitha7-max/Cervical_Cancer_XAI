import pandas as pd
import joblib
import matplotlib.pyplot as plt

print("=" * 60)
print("FEATURE IMPORTANCE ANALYSIS")
print("=" * 60)

# Load SMOTE-trained model
model = joblib.load("models/random_forest_smote.pkl")
print("Model loaded successfully.")

# Load cleaned dataset
df = pd.read_csv("dataset/cleaned_cervical_cancer.csv")

# Separate features
X = df.drop("Biopsy", axis=1)

# Get feature importance
importance = model.feature_importances_

# Create DataFrame
feature_df = pd.DataFrame({
    "Feature": X.columns,
    "Importance": importance
})

# Sort by importance
feature_df = feature_df.sort_values(
    by="Importance",
    ascending=False
)

print("\nTop 10 Important Features\n")
print(feature_df.head(10))

# Plot
plt.figure(figsize=(10,6))
plt.barh(
    feature_df["Feature"][:10],
    feature_df["Importance"][:10]
)

plt.gca().invert_yaxis()

plt.title("Top 10 Important Features")
plt.xlabel("Importance")
plt.tight_layout()

plt.savefig("results/feature_importance.png")

plt.show()

print("\nFeature importance graph saved successfully!")
print("Location: results/feature_importance.png")
