import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    roc_auc_score
)

from imblearn.over_sampling import SMOTE


print("=" * 70)
print("SCHILLER MODEL IMPROVEMENT AND THRESHOLD EVALUATION")
print("=" * 70)


# --------------------------------------------------
# LOAD DATASET
# --------------------------------------------------

df = pd.read_csv("dataset/cleaned_cervical_cancer.csv")

y = df["Schiller"]

columns_to_remove = [
    "Schiller",
    "Hinselmann",
    "Citology",
    "Biopsy"
]

X = df.drop(columns=columns_to_remove)


print("\nDataset shape:", df.shape)

print("\nSchiller distribution:")
print(y.value_counts())


# --------------------------------------------------
# TRAIN / TEST SPLIT
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# --------------------------------------------------
# SMOTE ONLY ON TRAINING DATA
# --------------------------------------------------

smote = SMOTE(random_state=42)

X_train_smote, y_train_smote = smote.fit_resample(
    X_train,
    y_train
)


print("\nTraining distribution after SMOTE:")
print(y_train_smote.value_counts())


# --------------------------------------------------
# MODELS TO COMPARE
# --------------------------------------------------

models = {

    "RF_SMOTE": RandomForestClassifier(
        n_estimators=300,
        random_state=42,
        n_jobs=-1
    ),

    "RF_BALANCED": RandomForestClassifier(
        n_estimators=300,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    ),

    "RF_BALANCED_SUBSAMPLE": RandomForestClassifier(
        n_estimators=300,
        class_weight="balanced_subsample",
        max_depth=10,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
}


# --------------------------------------------------
# FUNCTION FOR METRICS
# --------------------------------------------------

def show_metrics(
    model_name,
    threshold,
    y_true,
    probabilities
):

    predictions = (
        probabilities >= threshold
    ).astype(int)

    accuracy = accuracy_score(
        y_true,
        predictions
    )

    precision = precision_score(
        y_true,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        y_true,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        y_true,
        predictions,
        zero_division=0
    )

    cm = confusion_matrix(
        y_true,
        predictions
    )

    print("\n--------------------------------------")
    print("Model:", model_name)
    print("Threshold:", threshold)
    print("--------------------------------------")

    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1 Score : {f1:.4f}")

    print("Confusion Matrix:")
    print(cm)


# --------------------------------------------------
# TRAIN AND EVALUATE
# --------------------------------------------------

thresholds = [
    0.50,
    0.40,
    0.30,
    0.25,
    0.20,
    0.15,
    0.10
]


for model_name, model in models.items():

    print("\n")
    print("=" * 70)
    print("TRAINING:", model_name)
    print("=" * 70)

    # RF_SMOTE uses SMOTE training data
    if model_name == "RF_SMOTE":

        model.fit(
            X_train_smote,
            y_train_smote
        )

    # Balanced models use original training data
    else:

        model.fit(
            X_train,
            y_train
        )

    probabilities = model.predict_proba(
        X_test
    )[:, 1]

    auc = roc_auc_score(
        y_test,
        probabilities
    )

    print(
        "\nROC-AUC:",
        round(auc, 4)
    )

    for threshold in thresholds:

        show_metrics(
            model_name,
            threshold,
            y_test,
            probabilities
        )


print("\n")
print("=" * 70)
print("SCHILLER EVALUATION COMPLETED")
print("=" * 70)