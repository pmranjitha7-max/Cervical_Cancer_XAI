import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

from imblearn.over_sampling import SMOTE

print("=" * 60)
print("TRAINING RANDOM FOREST WITH SMOTE")
print("=" * 60)

# Load cleaned dataset
df = pd.read_csv("dataset/cleaned_cervical_cancer.csv")

# Features and Target
X = df.drop("Biopsy", axis=1)
y = df["Biopsy"]

print("\nOriginal Class Distribution:")
print(y.value_counts())

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Apply SMOTE ONLY on training data
smote = SMOTE(random_state=42)

X_train_smote, y_train_smote = smote.fit_resample(
    X_train,
    y_train
)

print("\nClass Distribution After SMOTE:")
print(y_train_smote.value_counts())

# Train Random Forest
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train_smote, y_train_smote)

print("\nModel trained successfully with SMOTE!")

# Save Model
joblib.dump(model, "models/random_forest_smote.pkl")

# Save Test Data
X_test.to_csv("results/X_test_smote.csv", index=False)
y_test.to_csv("results/y_test_smote.csv", index=False)

print("\nSMOTE model saved successfully.")
print("Test data saved successfully.")

print("\nTraining completed.")