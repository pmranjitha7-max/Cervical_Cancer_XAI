import pandas as pd
import joblib

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report,
    precision_score,
    recall_score,
    f1_score
)

print("=" * 60)
print("BIOPSY MODEL EVALUATION")
print("=" * 60)

# -----------------------------
# Load Trained Biopsy Model
# -----------------------------
model = joblib.load("models/biopsy_model.pkl")

print("Model loaded successfully.")

# -----------------------------
# Load Biopsy Test Data
# -----------------------------
X_test = pd.read_csv("results/biopsy_X_test.csv")
y_test = pd.read_csv("results/biopsy_y_test.csv")

# Convert DataFrame to Series
y_test = y_test.squeeze()

print("Test data loaded successfully.")

# -----------------------------
# Prediction
# -----------------------------
y_pred = model.predict(X_test)

print("Prediction completed successfully.")

# -----------------------------
# Evaluation Metrics
# -----------------------------
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print(f"\nAccuracy: {accuracy * 100:.2f}%")

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print(f"\nPrecision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("=" * 60)
print("BIOPSY MODEL EVALUATION COMPLETED")
print("=" * 60)