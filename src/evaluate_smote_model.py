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
print("SMOTE MODEL EVALUATION")
print("=" * 60)

# Load SMOTE-trained model
model = joblib.load("models/random_forest_smote.pkl")
print("SMOTE model loaded successfully.")

# Load test data
X_test = pd.read_csv("results/X_test_smote.csv")
y_test = pd.read_csv("results/y_test_smote.csv").squeeze()

print("Test data loaded successfully.")

# Make predictions
y_pred = model.predict(X_test)

print("Prediction completed successfully.")

# Accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"\nAccuracy: {accuracy * 100:.2f}%")

# Confusion Matrix
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Precision
precision = precision_score(y_test, y_pred)
print(f"\nPrecision: {precision:.4f}")

# Recall
recall = recall_score(y_test, y_pred)
print(f"Recall   : {recall:.4f}")

# F1 Score
f1 = f1_score(y_test, y_pred)
print(f"F1 Score : {f1:.4f}")

# Classification Report
print("\nClassification Report:")
print(classification_report(y_test, y_pred))