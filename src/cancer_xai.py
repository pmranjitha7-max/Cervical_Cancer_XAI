import pandas as pd
import joblib
import shap
import numpy as np


print("=" * 70)
print("CERVICAL CANCER XAI EXPLANATION")
print("=" * 70)


# ---------------------------------------------------------
# 1. LOAD DATASET
# ---------------------------------------------------------

df = pd.read_csv(
    "dataset/cleaned_cervical_cancer.csv"
)


# ---------------------------------------------------------
# 2. LOAD TRAINED CANCER MODEL
# ---------------------------------------------------------

model = joblib.load(
    "models/cancer_model.pkl"
)


# ---------------------------------------------------------
# 3. LOAD EXACT FEATURES USED DURING TRAINING
# ---------------------------------------------------------

feature_names = joblib.load(
    "models/cancer_features.pkl"
)


# ---------------------------------------------------------
# 4. SELECT PATIENT
# ---------------------------------------------------------

patient_id = int(input("\nEnter Patient ID: "))

patient = df.loc[[patient_id], feature_names]


# ---------------------------------------------------------
# 5. MODEL PREDICTION
# ---------------------------------------------------------

prediction = model.predict(patient)[0]

probabilities = model.predict_proba(patient)[0]

negative_probability = float(probabilities[0])
positive_probability = float(probabilities[1])


print("\nPATIENT ID:", patient_id)

print(
    "ACTUAL Dx:Cancer:",
    int(df.loc[patient_id, "Dx:Cancer"])
)

print(
    "MODEL PREDICTION:",
    "Positive" if prediction == 1 else "Negative"
)

print(
    "CANCER POSITIVE PROBABILITY:",
    f"{positive_probability * 100:.2f}%"
)

print(
    "CANCER NEGATIVE PROBABILITY:",
    f"{negative_probability * 100:.2f}%"
)


# ---------------------------------------------------------
# 6. SHAP EXPLAINER
# ---------------------------------------------------------

print("\nGenerating SHAP explanation...")

explainer = shap.TreeExplainer(model)

shap_output = explainer.shap_values(patient)


# ---------------------------------------------------------
# 7. HANDLE DIFFERENT SHAP OUTPUT FORMATS
# ---------------------------------------------------------

if isinstance(shap_output, list):

    # Older SHAP versions:
    # [class_0_values, class_1_values]
    shap_values = shap_output[1][0]

else:

    shap_array = np.array(shap_output)

    # Possible shape:
    # (1, number_of_features, 2)
    if shap_array.ndim == 3:

        shap_values = shap_array[0, :, 1]

    # Possible shape:
    # (1, number_of_features)
    elif shap_array.ndim == 2:

        shap_values = shap_array[0]

    else:

        shap_values = shap_array


# ---------------------------------------------------------
# 8. CREATE PATIENT-SPECIFIC XAI TABLE
# ---------------------------------------------------------

xai_data = pd.DataFrame(
    {
        "Feature": feature_names,
        "Patient_Value": patient.iloc[0].values,
        "SHAP_Value": shap_values
    }
)


# Absolute importance is used only for ranking.
xai_data["Absolute_Impact"] = (
    xai_data["SHAP_Value"].abs()
)


# ---------------------------------------------------------
# 9. INTERPRET DIRECTION
# ---------------------------------------------------------

def explain_direction(value):

    if value > 0:
        return "Supports the CANCER-POSITIVE prediction"

    elif value < 0:
        return "Supports the CANCER-NEGATIVE prediction"

    else:
        return "Has very little influence on the prediction"


xai_data["Impact"] = (
    xai_data["SHAP_Value"]
    .apply(explain_direction)
)


# ---------------------------------------------------------
# 10. SORT MOST INFLUENTIAL FEATURES
# ---------------------------------------------------------

xai_data = xai_data.sort_values(
    by="Absolute_Impact",
    ascending=False
)


top_features = xai_data.head(10)


# ---------------------------------------------------------
# 11. DISPLAY EXPLANATION
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("TOP XAI FACTORS FOR THIS PATIENT")
print("=" * 70)


for rank, (_, row) in enumerate(
    top_features.iterrows(),
    start=1
):

    print(
        f"\n{rank}. {row['Feature']}"
    )

    print(
        f"   Patient value: {row['Patient_Value']}"
    )

    print(
        f"   SHAP impact: {row['SHAP_Value']:.6f}"
    )

    print(
        f"   Explanation: {row['Impact']}"
    )

# ---------------------------------------------------------
# 12. PATIENT-FRIENDLY XAI SUMMARY
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("FINAL CERVICAL CANCER PREDICTION REPORT")
print("=" * 70)

print(f"\nPatient ID: {patient_id}")

if prediction == 1:

    print("\nFINAL PREDICTION: CANCER POSITIVE")

    print(
        f"Cancer probability: "
        f"{positive_probability * 100:.2f}%"
    )

    print(
        f"No-cancer probability: "
        f"{negative_probability * 100:.2f}%"
    )

    positive_factors = xai_data[
        xai_data["SHAP_Value"] > 0
    ].head(5)

    print("\nMAIN FACTORS SUPPORTING THE POSITIVE PREDICTION:")

    for _, row in positive_factors.iterrows():

        print(
            f"- {row['Feature']}: "
            f"patient value = {row['Patient_Value']}"
        )

    print(
        "\nXAI INTERPRETATION:"
        "\nThe model identified the factors above as the "
        "strongest contributors to this patient's "
        "positive prediction."
    )

    print(
        "\nFINAL ASSESSMENT:"
        "\nBased on the trained machine-learning model, "
        "this patient is classified as CANCER POSITIVE."
    )

else:

    print("\nFINAL PREDICTION: CANCER NEGATIVE")

    print(
        f"Cancer probability: "
        f"{positive_probability * 100:.2f}%"
    )

    print(
        f"No-cancer probability: "
        f"{negative_probability * 100:.2f}%"
    )

    negative_factors = xai_data[
        xai_data["SHAP_Value"] < 0
    ].head(5)

    print("\nMAIN FACTORS SUPPORTING THE NEGATIVE PREDICTION:")

    for _, row in negative_factors.iterrows():

        print(
            f"- {row['Feature']}: "
            f"patient value = {row['Patient_Value']}"
        )

    print(
        "\nXAI INTERPRETATION:"
        "\nThe model identified the factors above as the "
        "strongest contributors to this patient's "
        "negative prediction."
    )

    print(
        "\nFINAL ASSESSMENT:"
        "\nBased on the trained machine-learning model, "
        "this patient is classified as CANCER NEGATIVE."
    )
# ---------------------------------------------------------
# 13. SAVE XAI RESULT
# ---------------------------------------------------------

top_features.to_csv(
    f"results/cancer_xai_patient_{patient_id}.csv",
    index=False
)


print(
    f"\nXAI explanation saved to:"
    f"\nresults/cancer_xai_patient_{patient_id}.csv"
)


print("\n" + "=" * 70)
print("XAI EXPLANATION COMPLETED")
print("=" * 70)