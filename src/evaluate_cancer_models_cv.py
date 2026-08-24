import pandas as pd
import numpy as np

from sklearn.model_selection import RepeatedStratifiedKFold, cross_validate
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import make_scorer, precision_score, recall_score, f1_score

from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE


print("=" * 75)
print("CERVIXAI - CANCER MODEL CROSS-VALIDATION COMPARISON")
print("Target: Dx:Cancer")
print("=" * 75)


# =========================================================
# 1. LOAD DATA
# =========================================================

df = pd.read_csv(
    "dataset/cleaned_cervical_cancer.csv"
)

y = df["Dx:Cancer"]


# =========================================================
# 2. REMOVE DIAGNOSTIC / RESULT COLUMNS
# =========================================================
# These variables are intentionally excluded because they
# contain diagnostic/result information that could cause
# target leakage in a pre-diagnostic risk model.
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
# REDUCED FEATURE SET FOR EXPERIMENTAL COMPARISON
# =========================================================
# These features showed the strongest exploratory
# discrimination among the non-diagnostic variables.
# Diagnostic/result variables remain excluded.
#
# IMPORTANT:
# This is an experimental feature-selection comparison.
# Final model performance must still be evaluated using
# cross-validation.
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

print("\nDataset shape:")
print(df.shape)

print("\nNumber of input features:")
print(X.shape[1])

print("\nTarget distribution:")
print(y.value_counts())

print("\nTarget percentage:")
print(
    (y.value_counts(normalize=True) * 100).round(2)
)


# =========================================================
# 3. CROSS-VALIDATION
# =========================================================
#
# 3 folds are used because there are only 18 cancer-positive
# records. Each validation fold therefore contains roughly
# 6 positive patients.
#
# Repeating the CV provides a more stable estimate than one
# single train/test split.
# =========================================================

cv = RepeatedStratifiedKFold(
    n_splits=3,
    n_repeats=5,
    random_state=42
)


# =========================================================
# 4. SCORING METRICS
# =========================================================

scoring = {
    "accuracy": "accuracy",

    "precision": make_scorer(
        precision_score,
        zero_division=0
    ),

    "recall": make_scorer(
        recall_score,
        zero_division=0
    ),

    "f1": make_scorer(
        f1_score,
        zero_division=0
    ),

    "roc_auc": "roc_auc",

    # Average precision is the area-oriented summary of
    # the precision-recall curve and is especially useful
    # for strongly imbalanced binary classification.
    "pr_auc": "average_precision"
}


# =========================================================
# 5. CANDIDATE MODELS
# =========================================================
#
# SMOTE is inside the imbalanced-learn Pipeline.
#
# This is critical:
# During cross-validation SMOTE is fitted ONLY on each
# training fold, never on the validation fold.
# =========================================================

models = {

    "Logistic Regression + SMOTE": Pipeline(
        steps=[
            (
                "smote",
                SMOTE(
                    random_state=42,
                    k_neighbors=3
                )
            ),
            (
                "model",
                LogisticRegression(
                    max_iter=5000,
                    random_state=42
                )
            )
        ]
    ),

    "Random Forest + SMOTE": Pipeline(
        steps=[
            (
                "smote",
                SMOTE(
                    random_state=42,
                    k_neighbors=3
                )
            ),
            (
                "model",
                RandomForestClassifier(
                    n_estimators=500,
                    random_state=42,
                    n_jobs=-1
                )
            )
        ]
    ),

    "Random Forest Class Weight": RandomForestClassifier(
        n_estimators=500,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    ),

    "Decision Tree Class Weight": DecisionTreeClassifier(
        class_weight="balanced",
        max_depth=5,
        min_samples_leaf=5,
        random_state=42
    )
}


# =========================================================
# 6. EVALUATE MODELS
# =========================================================

results = []


feature_sets = {
    "All 26 Features": X,
    "Reduced 8 Features": X_reduced
}

results = []


for feature_set_name, X_current in feature_sets.items():

    print("\n")
    print("#" * 75)
    print("FEATURE SET:", feature_set_name)
    print("NUMBER OF FEATURES:", X_current.shape[1])
    print("#" * 75)

    for model_name, model in models.items():

        print("\n" + "=" * 75)
        print(
            "Evaluating:",
            model_name,
            "|",
            feature_set_name
        )
        print("=" * 75)

        scores = cross_validate(
            estimator=model,
            X=X_current,
            y=y,
            cv=cv,
            scoring=scoring,
            n_jobs=-1,
            return_train_score=False
        )

        result = {

            "Feature_Set":
                feature_set_name,

            "Model":
                model_name,

            "Number_of_Features":
                X_current.shape[1],

            "Accuracy_Mean":
                np.mean(
                    scores["test_accuracy"]
                ),

            "Accuracy_STD":
                np.std(
                    scores["test_accuracy"]
                ),

            "Precision_Mean":
                np.mean(
                    scores["test_precision"]
                ),

            "Precision_STD":
                np.std(
                    scores["test_precision"]
                ),

            "Recall_Mean":
                np.mean(
                    scores["test_recall"]
                ),

            "Recall_STD":
                np.std(
                    scores["test_recall"]
                ),

            "F1_Mean":
                np.mean(
                    scores["test_f1"]
                ),

            "F1_STD":
                np.std(
                    scores["test_f1"]
                ),

            "ROC_AUC_Mean":
                np.mean(
                    scores["test_roc_auc"]
                ),

            "ROC_AUC_STD":
                np.std(
                    scores["test_roc_auc"]
                ),

            "PR_AUC_Mean":
                np.mean(
                    scores["test_pr_auc"]
                ),

            "PR_AUC_STD":
                np.std(
                    scores["test_pr_auc"]
                )
        }

        results.append(
            result
        )

        print(
            f"Accuracy : "
            f"{result['Accuracy_Mean']:.4f} "
            f"+/- {result['Accuracy_STD']:.4f}"
        )

        print(
            f"Precision: "
            f"{result['Precision_Mean']:.4f} "
            f"+/- {result['Precision_STD']:.4f}"
        )

        print(
            f"Recall   : "
            f"{result['Recall_Mean']:.4f} "
            f"+/- {result['Recall_STD']:.4f}"
        )

        print(
            f"F1 Score : "
            f"{result['F1_Mean']:.4f} "
            f"+/- {result['F1_STD']:.4f}"
        )

        print(
            f"ROC-AUC  : "
            f"{result['ROC_AUC_Mean']:.4f} "
            f"+/- {result['ROC_AUC_STD']:.4f}"
        )

        print(
            f"PR-AUC   : "
            f"{result['PR_AUC_Mean']:.4f} "
            f"+/- {result['PR_AUC_STD']:.4f}"
        )

# =========================================================
# 7. CREATE COMPARISON TABLE
# =========================================================

results_df = pd.DataFrame(
    results
)

# Sort primarily by PR-AUC
results_df = results_df.sort_values(
    by="PR_AUC_Mean",
    ascending=False
)

print("\n")
print("=" * 90)
print("FINAL CROSS-VALIDATION COMPARISON")
print("=" * 90)

display_columns = [
    "Feature_Set",
    "Model",
    "Number_of_Features",
    "Precision_Mean",
    "Recall_Mean",
    "F1_Mean",
    "ROC_AUC_Mean",
    "PR_AUC_Mean"
]

print(
    results_df[
        display_columns
    ].round(4).to_string(
        index=False
    )
)

# =========================================================
# BEST RESULT FOR EACH FEATURE SET
# =========================================================

print("\n")
print("=" * 90)
print("BEST PR-AUC RESULT FOR EACH FEATURE SET")
print("=" * 90)

best_per_feature_set = (
    results_df
    .sort_values(
        by="PR_AUC_Mean",
        ascending=False
    )
    .groupby(
        "Feature_Set",
        as_index=False
    )
    .first()
)

print(
    best_per_feature_set[
        display_columns
    ].round(4).to_string(
        index=False
    )
)

# =========================================================
# SAVE COMPLETE RESULTS
# =========================================================

results_df.to_csv(
    "results/cancer_model_cv_comparison.csv",
    index=False
)

print("\nResults saved:")
print(
    "results/cancer_model_cv_comparison.csv"
)

print("\n" + "=" * 90)
print("FEATURE-SELECTION CROSS-VALIDATION ANALYSIS COMPLETED")
print("=" * 90)

