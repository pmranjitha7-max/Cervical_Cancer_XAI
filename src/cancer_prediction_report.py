import pandas as pd
import joblib
import shap
import numpy as np


print("=" * 72)
print("CERVIXAI - CERVICAL CANCER XAI PATIENT REPORT")
print("=" * 72)


# ---------------------------------------------------------
# 1. LOAD DATASET
# ---------------------------------------------------------

df = pd.read_csv(
    "dataset/cleaned_cervical_cancer.csv"
)


# ---------------------------------------------------------
# 2. LOAD CANCER MODEL + FEATURE LIST
# ---------------------------------------------------------

cancer_model = joblib.load(
    "models/cancer_model.pkl"
)

cancer_features = joblib.load(
    "models/cancer_features.pkl"
)


# ---------------------------------------------------------
# 3. LOAD SUPPORTING MODELS
# ---------------------------------------------------------

biopsy_model = joblib.load(
    "models/biopsy_model.pkl"
)

hpv_model = joblib.load(
    "models/hpv_model.pkl"
)


# ---------------------------------------------------------
# 4. ENTER PATIENT ID
# ---------------------------------------------------------

patient_id = int(
    input("\nEnter Patient ID: ")
)


# ---------------------------------------------------------
# 5. VALIDATE PATIENT ID
# ---------------------------------------------------------

if patient_id < 0 or patient_id >= len(df):

    print("\nInvalid Patient ID.")
    print(
        f"Please enter an ID between 0 and {len(df) - 1}."
    )

    raise SystemExit


# ---------------------------------------------------------
# 6. PATIENT DATA
# ---------------------------------------------------------

patient_row = df.iloc[[patient_id]]

cancer_patient = patient_row[
    cancer_features
]


# ---------------------------------------------------------
# 7. MAIN CANCER PREDICTION
# ---------------------------------------------------------

cancer_prediction = cancer_model.predict(
    cancer_patient
)[0]

cancer_probabilities = cancer_model.predict_proba(
    cancer_patient
)[0]

cancer_negative_probability = float(
    cancer_probabilities[0]
)

cancer_positive_probability = float(
    cancer_probabilities[1]
)


# ---------------------------------------------------------
# 8. SUPPORTING BIOPSY PREDICTION
# ---------------------------------------------------------

biopsy_X = df.drop(
    columns=["Biopsy"]
)

biopsy_patient = biopsy_X.iloc[
    [patient_id]
]

biopsy_prediction = biopsy_model.predict(
    biopsy_patient
)[0]

biopsy_probability = biopsy_model.predict_proba(
    biopsy_patient
)[0]


# ---------------------------------------------------------
# 9. SUPPORTING HPV PREDICTION
# ---------------------------------------------------------

hpv_X = df.drop(
    columns=["Dx:HPV"]
)

hpv_patient = hpv_X.iloc[
    [patient_id]
]

hpv_prediction = hpv_model.predict(
    hpv_patient
)[0]

hpv_probability = hpv_model.predict_proba(
    hpv_patient
)[0]


# ---------------------------------------------------------
# 10. SHAP XAI
# ---------------------------------------------------------

explainer = shap.TreeExplainer(
    cancer_model
)

shap_output = explainer.shap_values(
    cancer_patient
)


if isinstance(shap_output, list):

    shap_values = shap_output[1][0]

else:

    shap_array = np.array(
        shap_output
    )

    if shap_array.ndim == 3:

        shap_values = shap_array[
            0,
            :,
            1
        ]

    elif shap_array.ndim == 2:

        shap_values = shap_array[0]

    else:

        shap_values = shap_array


# ---------------------------------------------------------
# 11. BUILD XAI TABLE
# ---------------------------------------------------------

xai_data = pd.DataFrame(
    {
        "Feature": cancer_features,

        "Patient_Value":
            cancer_patient.iloc[0].values,

        "SHAP_Value":
            shap_values
    }
)


xai_data["Absolute_Impact"] = (
    xai_data["SHAP_Value"].abs()
)


xai_data = xai_data.sort_values(
    by="Absolute_Impact",
    ascending=False
)


# ---------------------------------------------------------
# 12. CHOOSE FACTORS THAT SUPPORT FINAL PREDICTION
# ---------------------------------------------------------

if cancer_prediction == 1:

    supporting_factors = xai_data[
        xai_data["SHAP_Value"] > 0
    ].head(5)

else:

    supporting_factors = xai_data[
        xai_data["SHAP_Value"] < 0
    ].head(5)


# ---------------------------------------------------------
# 13. FORMAT SUPPORTING RESULTS
# ---------------------------------------------------------

biopsy_result = (
    "Positive"
    if biopsy_prediction == 1
    else "Negative"
)

hpv_result = (
    "Positive"
    if hpv_prediction == 1
    else "Negative"
)


# ---------------------------------------------------------
# 14. FINAL REPORT
# ---------------------------------------------------------

print("\n")
print("=" * 72)
print("CERVIXAI - PATIENT PREDICTION REPORT")
print("=" * 72)


print(
    f"\nPatient ID: {patient_id}"
)


print("\n----------------------------------------")
print("OVERALL CERVICAL CANCER PREDICTION")
print("----------------------------------------")


if cancer_prediction == 1:

    print(
        "\nPrediction: CANCER POSITIVE"
    )

else:

    print(
        "\nPrediction: CANCER NEGATIVE"
    )


print(
    f"Cancer probability: "
    f"{cancer_positive_probability * 100:.2f}%"
)

print(
    f"No-cancer probability: "
    f"{cancer_negative_probability * 100:.2f}%"
)


# ---------------------------------------------------------
# SUPPORTING PREDICTIONS
# ---------------------------------------------------------

print("\n----------------------------------------")
print("SUPPORTING MODEL RESULTS")
print("----------------------------------------")


print(
    f"\nBiopsy prediction: {biopsy_result}"
)

print(
    f"Biopsy positive probability: "
    f"{float(biopsy_probability[1]) * 100:.2f}%"
)


print(
    f"\nHPV prediction: {hpv_result}"
)

print(
    f"HPV positive probability: "
    f"{float(hpv_probability[1]) * 100:.2f}%"
)


# ---------------------------------------------------------
# XAI EXPLANATION
# ---------------------------------------------------------

print("\n----------------------------------------")
print("XAI EXPLANATION")
print("----------------------------------------")


if cancer_prediction == 1:

    print(
        "\nThe following patient factors contributed "
        "most strongly to the model's positive prediction:"
    )

else:

    print(
        "\nThe following patient factors contributed "
        "most strongly to the model's negative prediction:"
    )


for number, (_, row) in enumerate(
    supporting_factors.iterrows(),
    start=1
):

    print(
        f"\n{number}. {row['Feature']}"
    )

    print(
        f"   Patient value: "
        f"{row['Patient_Value']}"
    )


# ---------------------------------------------------------
# INTERPRETATION
# ---------------------------------------------------------

print("\n----------------------------------------")
print("INTERPRETATION")
print("----------------------------------------")


if cancer_prediction == 1:

    print(
        "\nThe trained machine-learning model identified "
        "a pattern associated with a positive cervical "
        "cancer classification."
    )

    print(
        "\nRecommended next step:"
        "\nFurther clinical evaluation by a gynecologist "
        "is recommended."
    )

    print(
        "\nDepending on the patient's clinical findings, "
        "additional diagnostic evaluation may be required."
    )

else:

    print(
        "\nThe trained machine-learning model identified "
        "a pattern associated with a negative cervical "
        "cancer classification."
    )

    print(
        "\nRecommended next step:"
        "\nContinue appropriate routine cervical screening "
        "and clinical follow-up as advised by a healthcare "
        "professional."
    )


print(
    "\nImportant note:"
    "\nThis output is an AI-assisted prediction and "
    "explanation. It is not a confirmed medical diagnosis."
)


print("\n" + "=" * 72)
print("END OF CERVIXAI REPORT")
print("=" * 72)