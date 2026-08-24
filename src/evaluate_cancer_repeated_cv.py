import os
import numpy as np
import pandas as pd

from sklearn.base import clone
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix
)
from sklearn.model_selection import RepeatedStratifiedKFold

from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE


# =========================================================
# CONFIGURATION
# =========================================================

DATASET_PATH = "dataset/cleaned_cervical_cancer.csv"

N_SPLITS = 3
N_REPEATS = 10
RANDOM_STATE = 42

THRESHOLDS = [
    0.05,
    0.10,
    0.15,
    0.20,
    0.25,
    0.30,
    0.35,
    0.40,
    0.45,
    0.50
]


# =========================================================
# LOAD DATA
# =========================================================

print("=" * 100)
print("CERVIXAI - REPEATED STRATIFIED CROSS-VALIDATION")
print("Target: Dx:Cancer")
print("=" * 100)

df = pd.read_csv(DATASET_PATH)

print("\nDataset shape:")
print(df.shape)


# =========================================================
# TARGET
# =========================================================

y = df["Dx:Cancer"].astype(int)


# =========================================================
# REMOVE DIAGNOSTIC / RESULT VARIABLES
# =========================================================
# These variables are deliberately excluded from the
# main cancer-risk model to reduce target leakage.
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
# REDUCED FEATURE SET
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


# =========================================================
# DATASET INFORMATION
# =========================================================

print("\nTarget distribution:")
print(y.value_counts().sort_index())

print("\nTarget percentage:")
print(
    (
        y.value_counts(normalize=True)
        .sort_index()
        * 100
    ).round(2)
)

print("\nAll-feature model features:")
print(X.shape[1])

print("\nReduced model features:")
print(X_reduced.shape[1])

print("\nCross-validation configuration:")
print(f"Folds   : {N_SPLITS}")
print(f"Repeats : {N_REPEATS}")
print(
    f"Total train/test evaluations per model: "
    f"{N_SPLITS * N_REPEATS}"
)


# =========================================================
# MODELS
# =========================================================

models = {

    "RF + SMOTE | 26 Features": (
        X,
        Pipeline(
            steps=[
                (
                    "smote",
                    SMOTE(
                        random_state=RANDOM_STATE,
                        k_neighbors=5
                    )
                ),
                (
                    "model",
                    RandomForestClassifier(
                        n_estimators=300,
                        random_state=RANDOM_STATE,
                        n_jobs=-1
                    )
                )
            ]
        )
    ),

    "RF Class Weight | 26 Features": (
        X,
        RandomForestClassifier(
            n_estimators=300,
            random_state=RANDOM_STATE,
            class_weight="balanced",
            n_jobs=-1
        )
    ),

    "RF Class Weight | 8 Features": (
        X_reduced,
        RandomForestClassifier(
            n_estimators=300,
            random_state=RANDOM_STATE,
            class_weight="balanced",
            n_jobs=-1
        )
    )
}


# =========================================================
# REPEATED STRATIFIED CV
# =========================================================

cv = RepeatedStratifiedKFold(
    n_splits=N_SPLITS,
    n_repeats=N_REPEATS,
    random_state=RANDOM_STATE
)


# =========================================================
# STORAGE
# =========================================================

fold_results = []
threshold_results = []


# =========================================================
# EVALUATE EACH MODEL
# =========================================================

for model_name, (X_model, estimator) in models.items():

    print("\n")
    print("#" * 100)
    print(f"MODEL: {model_name}")
    print(f"NUMBER OF FEATURES: {X_model.shape[1]}")
    print("#" * 100)

    model_fold_results = []

    split_number = 0

    for train_index, test_index in cv.split(
        X_model,
        y
    ):

        split_number += 1

        X_train = X_model.iloc[
            train_index
        ].copy()

        X_test = X_model.iloc[
            test_index
        ].copy()

        y_train = y.iloc[
            train_index
        ].copy()

        y_test = y.iloc[
            test_index
        ].copy()


        # -------------------------------------------------
        # TRAIN A FRESH MODEL FOR THIS FOLD
        # -------------------------------------------------

        fold_model = clone(
            estimator
        )

        fold_model.fit(
            X_train,
            y_train
        )


        # -------------------------------------------------
        # PROBABILITIES
        # -------------------------------------------------

        probability = fold_model.predict_proba(
            X_test
        )[:, 1]


        # -------------------------------------------------
        # PROBABILITY METRICS
        # -------------------------------------------------

        roc_auc = roc_auc_score(
            y_test,
            probability
        )

        pr_auc = average_precision_score(
            y_test,
            probability
        )


        # -------------------------------------------------
        # DEFAULT THRESHOLD = 0.50
        # -------------------------------------------------

        prediction_050 = (
            probability >= 0.50
        ).astype(int)

        precision_050 = precision_score(
            y_test,
            prediction_050,
            zero_division=0
        )

        recall_050 = recall_score(
            y_test,
            prediction_050,
            zero_division=0
        )

        f1_050 = f1_score(
            y_test,
            prediction_050,
            zero_division=0
        )


        fold_record = {

            "Model":
                model_name,

            "Split":
                split_number,

            "ROC_AUC":
                roc_auc,

            "PR_AUC":
                pr_auc,

            "Precision_050":
                precision_050,

            "Recall_050":
                recall_050,

            "F1_050":
                f1_050
        }

        fold_results.append(
            fold_record
        )

        model_fold_results.append(
            fold_record
        )


        # -------------------------------------------------
        # THRESHOLD EVALUATION INSIDE THIS TEST FOLD
        # -------------------------------------------------

        for threshold in THRESHOLDS:

            prediction = (
                probability >= threshold
            ).astype(int)

            tn, fp, fn, tp = confusion_matrix(
                y_test,
                prediction,
                labels=[0, 1]
            ).ravel()

            precision = precision_score(
                y_test,
                prediction,
                zero_division=0
            )

            recall = recall_score(
                y_test,
                prediction,
                zero_division=0
            )

            f1 = f1_score(
                y_test,
                prediction,
                zero_division=0
            )

            accuracy = accuracy_score(
                y_test,
                prediction
            )

            specificity = (
                tn / (tn + fp)
                if (tn + fp) > 0
                else 0.0
            )

            threshold_results.append(
                {
                    "Model":
                        model_name,

                    "Split":
                        split_number,

                    "Threshold":
                        threshold,

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


    # =====================================================
    # MODEL-LEVEL PROBABILITY SUMMARY
    # =====================================================

    model_fold_df = pd.DataFrame(
        model_fold_results
    )

    print("\nRepeated-CV probability metrics:")

    print(
        f"ROC-AUC : "
        f"{model_fold_df['ROC_AUC'].mean():.4f} "
        f"+/- "
        f"{model_fold_df['ROC_AUC'].std():.4f}"
    )

    print(
        f"PR-AUC  : "
        f"{model_fold_df['PR_AUC'].mean():.4f} "
        f"+/- "
        f"{model_fold_df['PR_AUC'].std():.4f}"
    )

    print("\nDefault threshold 0.50:")

    print(
        f"Precision: "
        f"{model_fold_df['Precision_050'].mean():.4f} "
        f"+/- "
        f"{model_fold_df['Precision_050'].std():.4f}"
    )

    print(
        f"Recall   : "
        f"{model_fold_df['Recall_050'].mean():.4f} "
        f"+/- "
        f"{model_fold_df['Recall_050'].std():.4f}"
    )

    print(
        f"F1       : "
        f"{model_fold_df['F1_050'].mean():.4f} "
        f"+/- "
        f"{model_fold_df['F1_050'].std():.4f}"
    )


# =========================================================
# CONVERT RESULTS TO DATAFRAMES
# =========================================================

fold_df = pd.DataFrame(
    fold_results
)

threshold_df = pd.DataFrame(
    threshold_results
)


# =========================================================
# AGGREGATE THRESHOLD PERFORMANCE
# =========================================================

summary_df = (

    threshold_df

    .groupby(
        [
            "Model",
            "Threshold"
        ],
        as_index=False
    )

    .agg(
        Precision_Mean=(
            "Precision",
            "mean"
        ),

        Precision_STD=(
            "Precision",
            "std"
        ),

        Recall_Mean=(
            "Recall",
            "mean"
        ),

        Recall_STD=(
            "Recall",
            "std"
        ),

        F1_Mean=(
            "F1",
            "mean"
        ),

        F1_STD=(
            "F1",
            "std"
        ),

        Specificity_Mean=(
            "Specificity",
            "mean"
        ),

        Accuracy_Mean=(
            "Accuracy",
            "mean"
        ),

        TP_Mean=(
            "TP",
            "mean"
        ),

        FN_Mean=(
            "FN",
            "mean"
        ),

        FP_Mean=(
            "FP",
            "mean"
        ),

        TN_Mean=(
            "TN",
            "mean"
        )
    )
)


# =========================================================
# ADD ROC-AUC / PR-AUC SUMMARY
# =========================================================

probability_summary = (

    fold_df

    .groupby(
        "Model",
        as_index=False
    )

    .agg(
        ROC_AUC_Mean=(
            "ROC_AUC",
            "mean"
        ),

        ROC_AUC_STD=(
            "ROC_AUC",
            "std"
        ),

        PR_AUC_Mean=(
            "PR_AUC",
            "mean"
        ),

        PR_AUC_STD=(
            "PR_AUC",
            "std"
        )
    )
)


summary_df = summary_df.merge(
    probability_summary,
    on="Model",
    how="left"
)


# =========================================================
# DISPLAY ALL THRESHOLD RESULTS
# =========================================================

print("\n\n")
print("=" * 100)
print("REPEATED-CV THRESHOLD SUMMARY")
print("=" * 100)

display_columns = [
    "Model",
    "Threshold",
    "Precision_Mean",
    "Recall_Mean",
    "F1_Mean",
    "Specificity_Mean",
    "ROC_AUC_Mean",
    "PR_AUC_Mean"
]

print(
    summary_df[
        display_columns
    ].round(4).to_string(
        index=False
    )
)


# =========================================================
# BEST F1 THRESHOLD PER MODEL
# =========================================================

best_f1_rows = []

for model_name in summary_df[
    "Model"
].unique():

    model_rows = summary_df[
        summary_df["Model"] == model_name
    ]

    best_index = model_rows[
        "F1_Mean"
    ].idxmax()

    best_f1_rows.append(
        summary_df.loc[
            best_index
        ]
    )


best_f1_df = pd.DataFrame(
    best_f1_rows
)


print("\n\n")
print("=" * 100)
print("BEST MEAN F1 THRESHOLD PER MODEL")
print("=" * 100)

print(
    best_f1_df[
        display_columns
    ].round(4).to_string(
        index=False
    )
)


# =========================================================
# RECALL-ORIENTED CANDIDATES
# =========================================================
# We also display thresholds with mean recall >= 0.30.
# This is NOT automatically the final threshold.
# It gives us candidates to examine where sensitivity
# is less poor than the default threshold.
# =========================================================

recall_candidates = summary_df[
    summary_df["Recall_Mean"] >= 0.30
].copy()

recall_candidates = recall_candidates.sort_values(
    by=[
        "Recall_Mean",
        "Precision_Mean"
    ],
    ascending=[
        False,
        False
    ]
)


print("\n\n")
print("=" * 100)
print("THRESHOLDS WITH MEAN RECALL >= 0.30")
print("=" * 100)

if len(recall_candidates) == 0:

    print(
        "No evaluated threshold achieved "
        "mean recall >= 0.30."
    )

else:

    print(
        recall_candidates[
            display_columns
        ].round(4).to_string(
            index=False
        )
    )


# =========================================================
# SAVE RESULTS
# =========================================================

os.makedirs(
    "results",
    exist_ok=True
)

fold_df.to_csv(
    "results/cancer_repeated_cv_folds.csv",
    index=False
)

threshold_df.to_csv(
    "results/cancer_repeated_cv_threshold_folds.csv",
    index=False
)

summary_df.to_csv(
    "results/cancer_repeated_cv_threshold_summary.csv",
    index=False
)

best_f1_df.to_csv(
    "results/cancer_repeated_cv_best_f1.csv",
    index=False
)


print("\n\nResults saved:")

print(
    "results/cancer_repeated_cv_folds.csv"
)

print(
    "results/cancer_repeated_cv_threshold_folds.csv"
)

print(
    "results/cancer_repeated_cv_threshold_summary.csv"
)

print(
    "results/cancer_repeated_cv_best_f1.csv"
)


print("\n" + "=" * 100)
print("REPEATED CROSS-VALIDATION ANALYSIS COMPLETED")
print("=" * 100)
