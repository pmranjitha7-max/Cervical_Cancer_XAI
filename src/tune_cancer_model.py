import os
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import (
    RepeatedStratifiedKFold,
    RandomizedSearchCV
)
from sklearn.metrics import (
    make_scorer,
    precision_score,
    recall_score,
    f1_score
)

from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE


# =========================================================
# CONFIGURATION
# =========================================================

DATASET_PATH = "dataset/cleaned_cervical_cancer.csv"

RANDOM_STATE = 42

N_SPLITS = 3
N_REPEATS = 5

# Number of randomly sampled hyperparameter combinations
# for each model family.
N_ITER = 30


# =========================================================
# START
# =========================================================

print("=" * 100)
print("CERVIXAI - CANCER MODEL HYPERPARAMETER TUNING")
print("Target: Dx:Cancer")
print("=" * 100)


# =========================================================
# 1. LOAD DATASET
# =========================================================

df = pd.read_csv(
    DATASET_PATH
)

print("\nDataset shape:")
print(df.shape)


# =========================================================
# 2. TARGET
# =========================================================

y = df[
    "Dx:Cancer"
].astype(int)


# =========================================================
# 3. REMOVE DIAGNOSTIC / RESULT VARIABLES
# =========================================================
# These variables are deliberately excluded to reduce
# target leakage.
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


print("\nNumber of input features:")
print(X.shape[1])

print("\nTarget distribution:")
print(
    y.value_counts().sort_index()
)

print("\nTarget percentage:")
print(
    (
        y.value_counts(
            normalize=True
        ).sort_index() * 100
    ).round(2)
)


# =========================================================
# 4. CROSS-VALIDATION
# =========================================================
# Only 18 positive cases exist.
#
# Therefore we use 3-fold stratified CV instead of a
# large number of folds.
#
# Five repeats give:
#
#     3 x 5 = 15
#
# validation evaluations during tuning.
# =========================================================

cv = RepeatedStratifiedKFold(
    n_splits=N_SPLITS,
    n_repeats=N_REPEATS,
    random_state=RANDOM_STATE
)


# =========================================================
# 5. SCORING
# =========================================================
# PR-AUC / average precision is the primary refit metric
# because the positive class is extremely rare.
#
# Other metrics are recorded for comparison.
# =========================================================

scoring = {

    "pr_auc":
        "average_precision",

    "roc_auc":
        "roc_auc",

    "precision":
        make_scorer(
            precision_score,
            zero_division=0
        ),

    "recall":
        make_scorer(
            recall_score,
            zero_division=0
        ),

    "f1":
        make_scorer(
            f1_score,
            zero_division=0
        )
}


# =========================================================
# 6. SHARED RANDOM FOREST SEARCH SPACE
# =========================================================
# This is deliberately moderate.
#
# We do NOT use a huge search space because the dataset
# contains only 18 cancer-positive observations.
# Excessive tuning would increase overfitting risk.
# =========================================================

rf_parameter_space = {

    "n_estimators": [
        200,
        300,
        500,
        700
    ],

    "max_depth": [
        None,
        4,
        6,
        8,
        12
    ],

    "min_samples_split": [
        2,
        5,
        10,
        15
    ],

    "min_samples_leaf": [
        1,
        2,
        4,
        6
    ],

    "max_features": [
        "sqrt",
        "log2",
        0.5,
        None
    ]
}


# =========================================================
# 7. RF + SMOTE PIPELINE
# =========================================================
# IMPORTANT:
#
# SMOTE is inside the pipeline.
#
# Therefore synthetic samples are generated ONLY from
# each training fold and never from its validation fold.
# =========================================================

smote_pipeline = Pipeline(
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
                random_state=RANDOM_STATE,
                n_jobs=-1
            )
        )
    ]
)


smote_parameter_space = {

    "model__n_estimators":
        rf_parameter_space[
            "n_estimators"
        ],

    "model__max_depth":
        rf_parameter_space[
            "max_depth"
        ],

    "model__min_samples_split":
        rf_parameter_space[
            "min_samples_split"
        ],

    "model__min_samples_leaf":
        rf_parameter_space[
            "min_samples_leaf"
        ],

    "model__max_features":
        rf_parameter_space[
            "max_features"
        ]
}


# =========================================================
# 8. CLASS-WEIGHT RANDOM FOREST
# =========================================================

class_weight_model = RandomForestClassifier(
    random_state=RANDOM_STATE,
    n_jobs=-1
)


class_weight_parameter_space = {

    "n_estimators":
        rf_parameter_space[
            "n_estimators"
        ],

    "max_depth":
        rf_parameter_space[
            "max_depth"
        ],

    "min_samples_split":
        rf_parameter_space[
            "min_samples_split"
        ],

    "min_samples_leaf":
        rf_parameter_space[
            "min_samples_leaf"
        ],

    "max_features":
        rf_parameter_space[
            "max_features"
        ],

    "class_weight": [
        "balanced",
        "balanced_subsample",
        {
            0: 1,
            1: 2
        },
        {
            0: 1,
            1: 5
        },
        {
            0: 1,
            1: 10
        },
        {
            0: 1,
            1: 20
        }
    ]
}


# =========================================================
# 9. SEARCH DEFINITIONS
# =========================================================

searches = {

    "RF + SMOTE | 26 Features": (

        smote_pipeline,

        smote_parameter_space
    ),

    "RF Class Weight | 26 Features": (

        class_weight_model,

        class_weight_parameter_space
    )
}


# =========================================================
# 10. RUN SEARCHES
# =========================================================

summary_results = []

all_search_results = []


for model_name, (
    estimator,
    parameter_space
) in searches.items():

    print("\n")
    print("#" * 100)
    print(f"TUNING: {model_name}")
    print("#" * 100)

    print(
        f"\nRandom parameter combinations: "
        f"{N_ITER}"
    )

    print(
        f"CV evaluations per combination: "
        f"{N_SPLITS * N_REPEATS}"
    )

    print(
        f"Approximate model fits: "
        f"{N_ITER * N_SPLITS * N_REPEATS}"
    )


    # -----------------------------------------------------
    # RANDOMIZED SEARCH
    # -----------------------------------------------------

    search = RandomizedSearchCV(

        estimator=estimator,

        param_distributions=parameter_space,

        n_iter=N_ITER,

        scoring=scoring,

        refit="pr_auc",

        cv=cv,

        random_state=RANDOM_STATE,

        n_jobs=-1,

        verbose=1,

        return_train_score=False,

        error_score="raise"
    )


    search.fit(
        X,
        y
    )


    # -----------------------------------------------------
    # SEARCH RESULTS
    # -----------------------------------------------------

    search_df = pd.DataFrame(
        search.cv_results_
    )


    search_df[
        "Model"
    ] = model_name


    all_search_results.append(
        search_df
    )


    # -----------------------------------------------------
    # BEST INDEX
    # -----------------------------------------------------

    best_index = search.best_index_


    best_pr_auc = search_df.loc[
        best_index,
        "mean_test_pr_auc"
    ]

    best_pr_auc_std = search_df.loc[
        best_index,
        "std_test_pr_auc"
    ]

    best_roc_auc = search_df.loc[
        best_index,
        "mean_test_roc_auc"
    ]

    best_roc_auc_std = search_df.loc[
        best_index,
        "std_test_roc_auc"
    ]

    best_precision = search_df.loc[
        best_index,
        "mean_test_precision"
    ]

    best_recall = search_df.loc[
        best_index,
        "mean_test_recall"
    ]

    best_f1 = search_df.loc[
        best_index,
        "mean_test_f1"
    ]


    # -----------------------------------------------------
    # PRINT BEST RESULT
    # -----------------------------------------------------

    print("\nBest parameters:")

    for key, value in (
        search.best_params_.items()
    ):

        print(
            f"  {key}: {value}"
        )


    print("\nCross-validation metrics for the")
    print("PR-AUC-selected parameter configuration:")

    print(
        f"PR-AUC   : "
        f"{best_pr_auc:.4f} "
        f"+/- "
        f"{best_pr_auc_std:.4f}"
    )

    print(
        f"ROC-AUC  : "
        f"{best_roc_auc:.4f} "
        f"+/- "
        f"{best_roc_auc_std:.4f}"
    )

    print(
        f"Precision: "
        f"{best_precision:.4f}"
    )

    print(
        f"Recall   : "
        f"{best_recall:.4f}"
    )

    print(
        f"F1       : "
        f"{best_f1:.4f}"
    )


    # -----------------------------------------------------
    # STORE SUMMARY
    # -----------------------------------------------------

    summary_results.append(
        {
            "Model":
                model_name,

            "Best_PR_AUC":
                best_pr_auc,

            "PR_AUC_STD":
                best_pr_auc_std,

            "ROC_AUC":
                best_roc_auc,

            "ROC_AUC_STD":
                best_roc_auc_std,

            "Precision_050":
                best_precision,

            "Recall_050":
                best_recall,

            "F1_050":
                best_f1,

            "Best_Params":
                str(
                    search.best_params_
                )
        }
    )


# =========================================================
# 11. FINAL TUNING COMPARISON
# =========================================================

summary_df = pd.DataFrame(
    summary_results
)


summary_df = summary_df.sort_values(
    by="Best_PR_AUC",
    ascending=False
)


print("\n\n")
print("=" * 100)
print("FINAL HYPERPARAMETER TUNING COMPARISON")
print("=" * 100)


display_columns = [

    "Model",

    "Best_PR_AUC",

    "PR_AUC_STD",

    "ROC_AUC",

    "ROC_AUC_STD",

    "Precision_050",

    "Recall_050",

    "F1_050"
]


print(
    summary_df[
        display_columns
    ].round(4).to_string(
        index=False
    )
)


# =========================================================
# 12. SAVE RESULTS
# =========================================================

os.makedirs(
    "results",
    exist_ok=True
)


summary_df.to_csv(
    "results/cancer_tuning_summary.csv",
    index=False
)


all_results_df = pd.concat(
    all_search_results,
    ignore_index=True
)


all_results_df.to_csv(
    "results/cancer_tuning_all_results.csv",
    index=False
)


print("\nResults saved:")

print(
    "results/cancer_tuning_summary.csv"
)

print(
    "results/cancer_tuning_all_results.csv"
)


# =========================================================
# 13. IMPORTANT NOTE
# =========================================================

print("\n" + "=" * 100)

print(
    "NOTE: THIS SCRIPT DOES NOT SAVE OR REPLACE "
    "THE PRODUCTION CANCER MODEL."
)

print(
    "The tuning results must be evaluated before "
    "the final model is trained."
)

print("=" * 100)

print("\nCANCER MODEL TUNING COMPLETED.")