import os
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    roc_auc_score,
    average_precision_score,
    accuracy_score
)

from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE


# =========================================================
# CERVIXAI - CANCER THRESHOLD CROSS-VALIDATION ANALYSIS
# =========================================================

print("=" * 80)
print("CERVIXAI - CANCER MODEL THRESHOLD ANALYSIS")
print("Target: Dx:Cancer")
print("=" * 80)


# =========================================================
# 1. LOAD DATASET
# =========================================================

df = pd.read_csv(
    "dataset/cleaned_cervical_cancer.csv"
)

print("\nDataset shape:")
print(df.shape)


# =========================================================
# 2. TARGET
# =========================================================

y = df["Dx:Cancer"]


# =========================================================
# 3. REMOVE DIAGNOSTIC / RESULT VARIABLES
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


# =========================================================
# 4. REDUCED FEATURE SET
# =========================================================

reduced_features = [
    "Age",
    "First sexual intercourse",
    "IUD (years)",
    "IUD",
    "Num of pregnancies",
    "Hormonal Contraceptives (years)",
    "Number of sexual partners",
    "STDs:HPV"
]

X_reduced = X[
    reduced_features
].copy()


print("\nTarget distribution:")
print(y.value_counts())

print("\nTarget percentage:")
print(
    (y.value_counts(normalize=True) * 100).round(2)
)


# =========================================================
# 5. STRATIFIED CROSS-VALIDATION
# =========================================================
# There are only 18 positive samples.
# Five folds keeps positive cases represented in every fold.
# =========================================================

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)


# =========================================================
# 6. CANDIDATE MODELS
# =========================================================
#
# Candidate A:
# Random Forest + SMOTE using all 26 non-diagnostic features
#
# Candidate B:
# Class-weighted Random Forest using all 26 features
#
# Candidate C:
# Class-weighted Random Forest using reduced 8 features
#
# SMOTE is inside the pipeline so synthetic samples are
# generated ONLY from each training fold.
# =========================================================

rf_smote_26 = Pipeline(
    steps=[
        (
            "smote",
            SMOTE(
                random_state=42,
                k_neighbors=5
            )
        ),
        (
            "model",
            RandomForestClassifier(
                n_estimators=300,
                random_state=42,
                n_jobs=-1
            )
        )
    ]
)


rf_weighted_26 = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1
)


rf_weighted_8 = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1
)


candidates = {
    "RF + SMOTE | 26 Features": (
        rf_smote_26,
        X
    ),

    "RF Class Weight | 26 Features": (
        rf_weighted_26,
        X
    ),

    "RF Class Weight | 8 Features": (
        rf_weighted_8,
        X_reduced
    )
}


# =========================================================
# 7. THRESHOLDS TO TEST
# =========================================================
#
# 0.50 is the standard classifier threshold.
# Lower thresholds are investigated because the cancer
# positive class is extremely rare.
# =========================================================

thresholds = np.arange(
    0.05,
    0.51,
    0.05
)


# =========================================================
# 8. GENERATE OUT-OF-FOLD PROBABILITIES
# =========================================================

all_results = []


for model_name, (model, X_current) in candidates.items():

    print("\n")
    print("#" * 80)
    print("MODEL:", model_name)
    print("NUMBER OF FEATURES:", X_current.shape[1])
    print("#" * 80)

    print(
        "\nGenerating out-of-fold probabilities..."
    )

    oof_probability = cross_val_predict(
        estimator=model,
        X=X_current,
        y=y,
        cv=cv,
        method="predict_proba",
        n_jobs=-1
    )[:, 1]


    # -----------------------------------------------------
    # Threshold-independent metrics
    # -----------------------------------------------------

    roc_auc = roc_auc_score(
        y,
        oof_probability
    )

    pr_auc = average_precision_score(
        y,
        oof_probability
    )


    print(
        f"\nOOF ROC-AUC: {roc_auc:.4f}"
    )

    print(
        f"OOF PR-AUC : {pr_auc:.4f}"
    )


    # -----------------------------------------------------
    # Evaluate each probability threshold
    # -----------------------------------------------------

    print("\nThreshold results:")

    print(
        "Threshold | Precision | Recall | "
        "F1 | Specificity | Accuracy | TN FP FN TP"
    )


    for threshold in thresholds:

        y_pred = (
            oof_probability >= threshold
        ).astype(int)


        tn, fp, fn, tp = confusion_matrix(
            y,
            y_pred,
            labels=[0, 1]
        ).ravel()


        precision = precision_score(
            y,
            y_pred,
            zero_division=0
        )

        recall = recall_score(
            y,
            y_pred,
            zero_division=0
        )

        f1 = f1_score(
            y,
            y_pred,
            zero_division=0
        )

        accuracy = accuracy_score(
            y,
            y_pred
        )


        if (tn + fp) > 0:

            specificity = (
                tn / (tn + fp)
            )

        else:

            specificity = 0.0


        all_results.append(
            {
                "Model":
                    model_name,

                "Number_of_Features":
                    X_current.shape[1],

                "Threshold":
                    round(
                        float(threshold),
                        2
                    ),

                "Precision":
                    precision,

                "Recall":
                    recall,

                "F1":
                    f1,

                "Specificity":
                    specificity,

                "Accuracy":
                    accuracy,

                "ROC_AUC":
                    roc_auc,

                "PR_AUC":
                    pr_auc,

                "TN":
                    int(tn),

                "FP":
                    int(fp),

                "FN":
                    int(fn),

                "TP":
                    int(tp)
            }
        )


        print(
            f"{threshold:9.2f} | "
            f"{precision:9.4f} | "
            f"{recall:6.4f} | "
            f"{f1:6.4f} | "
            f"{specificity:11.4f} | "
            f"{accuracy:8.4f} | "
            f"{tn:3d} {fp:3d} {fn:2d} {tp:2d}"
        )


# =========================================================
# 9. CREATE RESULTS TABLE
# =========================================================

results_df = pd.DataFrame(
    all_results
)


# =========================================================
# 10. SHOW BEST F1 THRESHOLD FOR EACH MODEL
# =========================================================

best_f1_rows = (
    results_df
    .sort_values(
        by=[
            "Model",
            "F1",
            "Recall"
        ],
        ascending=[
            True,
            False,
            False
        ]
    )
    .groupby(
        "Model",
        as_index=False
    )
    .first()
)


print("\n")
print("=" * 100)
print("BEST F1 THRESHOLD FOR EACH MODEL")
print("=" * 100)

display_columns = [
    "Model",
    "Threshold",
    "Precision",
    "Recall",
    "F1",
    "Specificity",
    "ROC_AUC",
    "PR_AUC",
    "TN",
    "FP",
    "FN",
    "TP"
]

print(
    best_f1_rows[
        display_columns
    ].round(4).to_string(
        index=False
    )
)


# =========================================================
# 11. SHOW THRESHOLDS WITH RECALL >= 0.50
# =========================================================
#
# This is NOT automatically the final model selection rule.
# It gives us clinically relevant candidate operating points
# where at least half of positive cases are detected.
# =========================================================

recall_candidates = results_df[
    results_df["Recall"] >= 0.50
].copy()


if not recall_candidates.empty:

    recall_candidates = (
        recall_candidates
        .sort_values(
            by=[
                "F1",
                "Precision"
            ],
            ascending=False
        )
    )

    print("\n")
    print("=" * 100)
    print("CANDIDATE THRESHOLDS WITH RECALL >= 0.50")
    print("=" * 100)

    print(
        recall_candidates[
            display_columns
        ].round(4).to_string(
            index=False
        )
    )

else:

    print("\n")
    print("=" * 100)
    print(
        "NO TESTED THRESHOLD ACHIEVED "
        "RECALL >= 0.50"
    )
    print("=" * 100)


# =========================================================
# 12. SAVE RESULTS
# =========================================================

os.makedirs(
    "results",
    exist_ok=True
)

results_df.to_csv(
    "results/cancer_threshold_cv_results.csv",
    index=False
)

best_f1_rows.to_csv(
    "results/cancer_threshold_best_f1.csv",
    index=False
)


print("\nResults saved:")
print(
    "results/cancer_threshold_cv_results.csv"
)

print(
    "results/cancer_threshold_best_f1.csv"
)


print("\n" + "=" * 100)
print("CANCER THRESHOLD ANALYSIS COMPLETED")
print("=" * 100)