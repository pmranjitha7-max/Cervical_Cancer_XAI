import os
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier


# =========================================================
# FINAL CERVIXAI CANCER MODEL
# =========================================================

print("=" * 80)
print("CERVIXAI - FINAL CERVICAL CANCER MODEL TRAINING")
print("Target: Dx:Cancer")
print("=" * 80)


# =========================================================
# 1. LOAD CLEANED DATASET
# =========================================================

df = pd.read_csv(
    "dataset/cleaned_cervical_cancer.csv"
)

print("\nDataset shape:")
print(df.shape)


# =========================================================
# 2. TARGET
# =========================================================

y = df["Dx:Cancer"].astype(int)


print("\nTarget distribution:")
print(y.value_counts())

print("\nTarget percentage:")
print(
    y.value_counts(
        normalize=True
    ).mul(100).round(2)
)


# =========================================================
# 3. REMOVE DIAGNOSTIC / RESULT COLUMNS
# =========================================================
# These variables are excluded from the cancer model
# because they contain diagnostic/result information and
# could cause target leakage.
# =========================================================

excluded_columns = [
    "Dx:Cancer",
    "Dx:CIN",
    "Dx:HPV",
    "Dx",
    "Hinselmann",
    "Schiller",
    "Citology",
    "Biopsy"
]


X = df.drop(
    columns=excluded_columns
)


print("\nNumber of final cancer-model features:")
print(X.shape[1])

print("\nFinal cancer-model features:")

for feature in X.columns:
    print("-", feature)


# =========================================================
# 4. FINAL MODEL CONFIGURATION
# =========================================================
#
# Selected after:
# - model comparison
# - repeated stratified cross-validation
# - hyperparameter tuning
# - threshold evaluation
#
# Final model:
# Random Forest with class weighting
#
# =========================================================

model = RandomForestClassifier(
    n_estimators=500,
    max_depth=6,
    min_samples_split=10,
    min_samples_leaf=1,
    max_features="log2",
    class_weight={
        0: 1,
        1: 5
    },
    random_state=42,
    n_jobs=-1
)


# =========================================================
# 5. FINAL CLASSIFICATION THRESHOLD
# =========================================================
#
# The standard Random Forest threshold is 0.50.
#
# Repeated cross-validation threshold analysis showed that
# 0.30 provided a better balance for this highly imbalanced
# cancer target.
#
# IMPORTANT:
# predict_proba() must be used with this threshold when
# generating the final cancer classification.
# =========================================================

FINAL_CANCER_THRESHOLD = 0.30


# =========================================================
# 6. TRAIN FINAL MODEL ON COMPLETE DEVELOPMENT DATASET
# =========================================================
#
# Cross-validation has already been used for model selection
# and performance estimation.
#
# The final deployable model is therefore fitted using all
# available rows with the selected feature set.
# =========================================================

print("\nTraining final cancer model...")

model.fit(
    X,
    y
)

print("Training completed.")


# =========================================================
# 7. CREATE MODEL DIRECTORY
# =========================================================

os.makedirs(
    "models",
    exist_ok=True
)


# =========================================================
# 8. SAVE FINAL MODEL
# =========================================================

joblib.dump(
    model,
    "models/cancer_model.pkl"
)


# =========================================================
# 9. SAVE EXACT FEATURE ORDER
# =========================================================

joblib.dump(
    list(X.columns),
    "models/cancer_features.pkl"
)


# =========================================================
# 10. SAVE FINAL THRESHOLD
# =========================================================

joblib.dump(
    FINAL_CANCER_THRESHOLD,
    "models/cancer_threshold.pkl"
)


# =========================================================
# 11. SAVE MODEL INFORMATION
# =========================================================

model_info = {
    "model_name":
        "Random Forest Class Weight",

    "target":
        "Dx:Cancer",

    "number_of_features":
        int(X.shape[1]),

    "n_estimators":
        500,

    "max_depth":
        6,

    "min_samples_split":
        10,

    "min_samples_leaf":
        1,

    "max_features":
        "log2",

    "class_weight_negative":
        1,

    "class_weight_positive":
        5,

    "classification_threshold":
        FINAL_CANCER_THRESHOLD,

    "random_state":
        42,

    "selection_method":
        (
            "Repeated stratified cross-validation, "
            "hyperparameter tuning and threshold evaluation"
        )
}


joblib.dump(
    model_info,
    "models/cancer_model_info.pkl"
)


# =========================================================
# 12. FINAL CONFIRMATION
# =========================================================

print("\n" + "=" * 80)
print("FINAL MODEL SAVED")
print("=" * 80)

print("\nModel:")
print("models/cancer_model.pkl")

print("\nFeature list:")
print("models/cancer_features.pkl")

print("\nClassification threshold:")
print("models/cancer_threshold.pkl")

print("\nModel information:")
print("models/cancer_model_info.pkl")

print("\nFinal threshold:")
print(FINAL_CANCER_THRESHOLD)

print("\nFinal model configuration:")
print(model)

print("\n" + "=" * 80)
print("FINAL CANCER MODEL TRAINING COMPLETED")
print("=" * 80)