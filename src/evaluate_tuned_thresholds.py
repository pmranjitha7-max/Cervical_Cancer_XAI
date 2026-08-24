import os
import numpy as np
import pandas as pd

from sklearn.base import clone
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    roc_auc_score,
    average_precision_score
)

from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE


print("=" * 90)
print("CERVIXAI - TUNED MODEL THRESHOLD EVALUATION")
print("=" * 90)


# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv(
    "dataset/cleaned_cervical_cancer.csv"
)

y = df["Dx:Cancer"].astype(int)

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


print("\nDataset shape:", df.shape)
print("Features:", X.shape[1])

print("\nTarget distribution:")
print(y.value_counts())


# =========================================================
# TUNED MODEL 1 - RF + SMOTE
# =========================================================

tuned_smote_model = Pipeline(
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
                n_estimators=700,
                min_samples_split=5,
                min_samples_leaf=1,
                max_features=0.5,
                max_depth=12,
                random_state=42,
                n_jobs=-1
            )
        )
    ]
)


# =========================================================
# TUNED MODEL 2 - CLASS WEIGHT RF
# =========================================================

tuned_weighted_model = RandomForestClassifier(
    n_estimators=500,
    min_samples_split=10,
    min_samples_leaf=1,
    max_features="log2",
    max_depth=6,
    class_weight={
        0: 1,
        1: 5
    },
    random_state=42,
    n_jobs=-1
)


models = {
    "Tuned RF + SMOTE": tuned_smote_model,
    "Tuned RF Class Weight": tuned_weighted_model
}


# =========================================================
# REPEATED STRATIFIED CV
# =========================================================

cv = RepeatedStratifiedKFold(
    n_splits=3,
    n_repeats=10,
    random_state=42
)


thresholds = [
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


results = []


# =========================================================
# EVALUATE
# =========================================================

for model_name, model in models.items():

    print("\n" + "=" * 90)
    print("MODEL:", model_name)
    print("=" * 90)

    fold_number = 0

    for train_index, test_index in cv.split(X, y):

        fold_number += 1

        X_train = X.iloc[train_index]
        X_test = X.iloc[test_index]

        y_train = y.iloc[train_index]
        y_test = y.iloc[test_index]

        fold_model = clone(model)

        fold_model.fit(
            X_train,
            y_train
        )

        probability = fold_model.predict_proba(
            X_test
        )[:, 1]

        roc_auc = roc_auc_score(
            y_test,
            probability
        )

        pr_auc = average_precision_score(
            y_test,
            probability
        )

        for threshold in thresholds:

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

            specificity = (
                tn / (tn + fp)
                if (tn + fp) > 0
                else 0
            )

            results.append(
                {
                    "Model": model_name,
                    "Fold": fold_number,
                    "Threshold": threshold,
                    "Precision": precision,
                    "Recall": recall,
                    "F1": f1,
                    "Specificity": specificity,
                    "ROC_AUC": roc_auc,
                    "PR_AUC": pr_auc
                }
            )


# =========================================================
# SUMMARY
# =========================================================

results_df = pd.DataFrame(results)

summary = (
    results_df
    .groupby(
        [
            "Model",
            "Threshold"
        ],
        as_index=False
    )
    .agg(
        Precision_Mean=("Precision", "mean"),
        Recall_Mean=("Recall", "mean"),
        F1_Mean=("F1", "mean"),
        Specificity_Mean=("Specificity", "mean"),
        ROC_AUC_Mean=("ROC_AUC", "mean"),
        PR_AUC_Mean=("PR_AUC", "mean")
    )
)


print("\n")
print("=" * 100)
print("TUNED MODEL THRESHOLD RESULTS")
print("=" * 100)

print(
    summary.round(4).to_string(
        index=False
    )
)


# =========================================================
# BEST F1 FOR EACH MODEL
# =========================================================

best_rows = []

for model_name in summary["Model"].unique():

    model_results = summary[
        summary["Model"] == model_name
    ]

    best_index = model_results[
        "F1_Mean"
    ].idxmax()

    best_rows.append(
        summary.loc[best_index]
    )


best_df = pd.DataFrame(best_rows)


print("\n")
print("=" * 100)
print("BEST THRESHOLD FOR EACH TUNED MODEL")
print("=" * 100)

print(
    best_df.round(4).to_string(
        index=False
    )
)


# =========================================================
# SAVE
# =========================================================

os.makedirs(
    "results",
    exist_ok=True
)

summary.to_csv(
    "results/tuned_cancer_threshold_results.csv",
    index=False
)

best_df.to_csv(
    "results/tuned_cancer_best_threshold.csv",
    index=False
)


print("\nResults saved.")

print("\n" + "=" * 100)
print("TUNED THRESHOLD EVALUATION COMPLETED")
print("=" * 100)