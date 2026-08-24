import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

from imblearn.over_sampling import SMOTE

print("=" * 60)
print("HPV PREDICTION MODEL")
print("=" * 60)

# Load cleaned dataset
df = pd.read_csv("dataset/cleaned_cervical_cancer.csv")

# -----------------------------
# Target Variable
# -----------------------------
y = df["Dx:HPV"]

# Features
X = df.drop(columns=["Dx:HPV"])

# -----------------------------
# Train Test Split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# -----------------------------
# Apply SMOTE
# -----------------------------
print("\nApplying SMOTE...")

smote = SMOTE(random_state=42)

X_train_smote, y_train_smote = smote.fit_resample(
    X_train,
    y_train
)

print("Before SMOTE:")
print(y_train.value_counts())

print("\nAfter SMOTE:")
print(y_train_smote.value_counts())

# -----------------------------
# Train Model
# -----------------------------
print("\nTraining Random Forest...")

model = RandomForestClassifier(
    random_state=42,
    n_estimators=100
)

model.fit(X_train_smote, y_train_smote)

# -----------------------------
# Prediction
# -----------------------------
y_pred = model.predict(X_test)

# -----------------------------
# Evaluation
# -----------------------------
print("\nAccuracy:")
print(accuracy_score(y_test, y_pred))

print("\nClassification Report")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix")
print(confusion_matrix(y_test, y_pred))

# -----------------------------
# Save Model
# -----------------------------
joblib.dump(model, "models/hpv_model.pkl")
# -----------------------------
# Save Test Data
# -----------------------------
X_test.to_csv("results/hpv_X_test.csv", index=False)
y_test.to_csv("results/hpv_y_test.csv", index=False)

print("\nHPV model saved successfully!")
print("HPV test dataset saved successfully.")
print("=" * 60)