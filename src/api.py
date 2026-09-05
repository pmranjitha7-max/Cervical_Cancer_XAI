import os

from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import shap

from . import db
from . import auth
from .image_screening_report import ImageScreeningModel

# api.py lives in <project_root>/src/, but dataset/ and models/ are
# siblings of src/ at the project root — so go up two levels.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def path(*parts):
    return os.path.join(BASE_DIR, *parts)


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="CerviXAI - Cervical Cancer Prediction API",
    description=(
        "Explainable AI based cervical cancer risk "
        "classification API using Random Forest and SHAP."
    ),
    version="5.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def _startup():
    db.init_db()


# =========================================================
# LOAD DATASET
# =========================================================

df = pd.read_csv(
    path("dataset", "cleaned_cervical_cancer.csv")
)


# =========================================================
# LOAD SUPPORTING MODELS
# =========================================================

biopsy_model = joblib.load(
    path("models", "biopsy_model.pkl")
)

hpv_model = joblib.load(
    path("models", "hpv_model.pkl")
)


# =========================================================
# LOAD FINAL CANCER MODEL
# =========================================================

cancer_model = joblib.load(
    path("models", "cancer_model.pkl")
)

cancer_features = joblib.load(
    path("models", "cancer_features.pkl")
)

cancer_threshold = joblib.load(
    path("models", "cancer_threshold.pkl")
)


# =========================================================
# CREATE SHAP EXPLAINER
# =========================================================

cancer_explainer = shap.TreeExplainer(
    cancer_model
)


# =========================================================
# LOAD IMAGE SCREENING MODEL (optional — the API still runs
# fine without it, /image-screening just reports unavailable)
# =========================================================

try:
    image_screening_model = ImageScreeningModel(
        path("models", "image_screening_model.pkl"),
        path("models", "image_screening_features.pkl"),
        path("models", "image_screening_classes.pkl"),
    )
except Exception as _e:  # pragma: no cover - defensive only
    image_screening_model = None


# =========================================================
# FRIENDLY FEATURE NAMES
# =========================================================

FEATURE_LABELS = {

    "Age":
        "Age",

    "Number of sexual partners":
        "Number of sexual partners",

    "First sexual intercourse":
        "Age at first sexual intercourse",

    "Num of pregnancies":
        "Number of pregnancies",

    "Smokes":
        "Smoking history",

    "Smokes (years)":
        "Smoking duration",

    "Smokes (packs/year)":
        "Smoking exposure",

    "Hormonal Contraceptives":
        "Hormonal contraceptive use",

    "Hormonal Contraceptives (years)":
        "Hormonal contraceptive duration",

    "IUD":
        "IUD use",

    "IUD (years)":
        "IUD duration",

    "STDs":
        "History of sexually transmitted diseases",

    "STDs (number)":
        "Number of sexually transmitted diseases",

    "STDs:condylomatosis":
        "Condylomatosis history",

    "STDs:cervical condylomatosis":
        "Cervical condylomatosis history",

    "STDs:vaginal condylomatosis":
        "Vaginal condylomatosis history",

    "STDs:vulvo-perineal condylomatosis":
        "Vulvo-perineal condylomatosis history",

    "STDs:syphilis":
        "Syphilis history",

    "STDs:pelvic inflammatory disease":
        "Pelvic inflammatory disease history",

    "STDs:genital herpes":
        "Genital herpes history",

    "STDs:molluscum contagiosum":
        "Molluscum contagiosum history",

    "STDs:AIDS":
        "AIDS history",

    "STDs:HIV":
        "HIV history",

    "STDs:Hepatitis B":
        "Hepatitis B history",

    "STDs:HPV":
        "HPV-related STD history",

    "STDs: Number of diagnosis":
        "Number of STD diagnoses"
}


# =========================================================
# VALIDATE PATIENT ID
# =========================================================

def validate_patient_id(patient_id: int):

    if patient_id < 0 or patient_id >= len(df):

        raise HTTPException(
            status_code=404,
            detail=(
                f"Invalid Patient ID. "
                f"Enter an ID between 0 and {len(df) - 1}."
            )
        )


# =========================================================
# GET SHAP VALUES FOR POSITIVE CLASS
# =========================================================

def get_positive_class_shap_values(patient):

    shap_output = cancer_explainer.shap_values(
        patient
    )

    # Older SHAP format
    if isinstance(shap_output, list):

        return np.array(
            shap_output[1][0]
        )

    shap_array = np.array(
        shap_output
    )

    # Newer SHAP format:
    # (1, features, 2)
    if shap_array.ndim == 3:

        return shap_array[
            0,
            :,
            1
        ]

    # Possible format:
    # (1, features)
    if shap_array.ndim == 2:

        return shap_array[0]

    return shap_array


# =========================================================
# HUMAN-READABLE PATIENT VALUE
# =========================================================

def format_patient_value(
    raw_feature,
    patient_value
):

    if "(years)" in raw_feature:

        return f"{patient_value} years"

    elif raw_feature == "Age":

        return f"{patient_value} years"

    elif raw_feature == "First sexual intercourse":

        return f"{patient_value} years of age"

    elif raw_feature in [
        "Smokes",
        "IUD",
        "Hormonal Contraceptives",
        "STDs"
    ]:

        return (
            "Yes"
            if patient_value == 1
            else "No"
        )

    elif raw_feature.startswith("STDs:"):

        return (
            "Present"
            if patient_value == 1
            else "Not present"
        )

    else:

        return str(patient_value)


# =========================================================
# HOME ENDPOINT
# =========================================================

@app.get("/")
def home():

    return {

        "application":
            "CerviXAI",

        "message":
            (
                "Cervical Cancer Prediction API "
                "is running successfully!"
            ),

        "version":
            "5.0",

        "cancer_classification_threshold":
            float(cancer_threshold),

        "available_endpoints": [
            "/predict",
            "/cancer-report",
            "/image-screening",
            "/auth/register",
            "/auth/login",
            "/profile",
            "/history",
            "/docs"
        ]
    }


# =========================================================
# BIOPSY + HPV SUPPORTING PREDICTION ENDPOINT
# =========================================================

@app.get("/predict")
def predict(
    patient_id: int = 0
):

    validate_patient_id(
        patient_id
    )


    # -----------------------------------------------------
    # BIOPSY
    # -----------------------------------------------------

    biopsy_X = df.drop(
        "Biopsy",
        axis=1
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


    if biopsy_prediction == 1:

        biopsy_result = "Positive"

        biopsy_recommendation = (
            "Further gynecological evaluation "
            "is recommended."
        )

    else:

        biopsy_result = "Negative"

        biopsy_recommendation = (
            "Continue appropriate routine "
            "cervical screening."
        )


    # -----------------------------------------------------
    # HPV
    # -----------------------------------------------------

    hpv_X = df.drop(
        "Dx:HPV",
        axis=1
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


    if hpv_prediction == 1:

        hpv_result = "Positive"

        hpv_recommendation = (
            "Further HPV evaluation "
            "is recommended."
        )

    else:

        hpv_result = "Negative"

        hpv_recommendation = (
            "Low HPV risk predicted by "
            "the current model."
        )


    # -----------------------------------------------------
    # RESPONSE
    # -----------------------------------------------------

    return {

        "patient_id":
            patient_id,

        "biopsy_prediction":
            biopsy_result,

        "biopsy_negative_probability":
            round(
                float(
                    biopsy_probability[0]
                ),
                4
            ),

        "biopsy_positive_probability":
            round(
                float(
                    biopsy_probability[1]
                ),
                4
            ),

        "biopsy_recommendation":
            biopsy_recommendation,

        "hpv_prediction":
            hpv_result,

        "hpv_negative_probability":
            round(
                float(
                    hpv_probability[0]
                ),
                4
            ),

        "hpv_positive_probability":
            round(
                float(
                    hpv_probability[1]
                ),
                4
            ),

        "hpv_recommendation":
            hpv_recommendation
    }


# =========================================================
# COMPLETE CANCER + XAI REPORT ENDPOINT
# =========================================================

@app.get("/cancer-report")
def cancer_report(
    patient_id: int = 0,
    current_user=Depends(auth.get_optional_user),
):

    validate_patient_id(
        patient_id
    )


    # =====================================================
    # PATIENT DATA
    # =====================================================

    patient_row = df.iloc[
        [patient_id]
    ]

    cancer_patient = patient_row[
        cancer_features
    ]


    # =====================================================
    # MAIN CANCER PROBABILITY
    # =====================================================

    cancer_probability = cancer_model.predict_proba(
        cancer_patient
    )[0]

    cancer_negative_probability = float(
        cancer_probability[0]
    )

    cancer_positive_probability = float(
        cancer_probability[1]
    )


    # =====================================================
    # FINAL CANCER CLASSIFICATION USING SAVED THRESHOLD
    # =====================================================

    cancer_prediction = (
        1
        if cancer_positive_probability >= cancer_threshold
        else 0
    )


    cancer_result = (
        "CANCER POSITIVE"
        if cancer_prediction == 1
        else "CANCER NEGATIVE"
    )


    # =====================================================
    # BIOPSY SUPPORTING PREDICTION
    # =====================================================

    biopsy_X = df.drop(
        "Biopsy",
        axis=1
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


    biopsy_result = (
        "Positive"
        if biopsy_prediction == 1
        else "Negative"
    )


    # =====================================================
    # HPV SUPPORTING PREDICTION
    # =====================================================

    hpv_X = df.drop(
        "Dx:HPV",
        axis=1
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


    hpv_result = (
        "Positive"
        if hpv_prediction == 1
        else "Negative"
    )


    # =====================================================
    # SHAP XAI
    # =====================================================

    shap_values = get_positive_class_shap_values(
        cancer_patient
    )


    xai_data = pd.DataFrame(
        {

            "Feature":
                cancer_features,

            "Patient_Value":
                cancer_patient.iloc[0].values,

            "SHAP_Value":
                shap_values
        }
    )


    xai_data[
        "Absolute_Impact"
    ] = (

        xai_data[
            "SHAP_Value"
        ].abs()
    )


    xai_data = xai_data.sort_values(
        by="Absolute_Impact",
        ascending=False
    )


    # =====================================================
    # SELECT FACTORS SUPPORTING FINAL CLASSIFICATION
    # =====================================================

    if cancer_prediction == 1:

        supporting_factors = xai_data[
            xai_data["SHAP_Value"] > 0
        ].head(5)

    else:

        supporting_factors = xai_data[
            xai_data["SHAP_Value"] < 0
        ].head(5)


    # =====================================================
    # FORMAT XAI FACTORS
    # =====================================================

    xai_factors = []


    for rank, (_, row) in enumerate(
        supporting_factors.iterrows(),
        start=1
    ):

        raw_feature = str(
            row["Feature"]
        )

        friendly_name = FEATURE_LABELS.get(
            raw_feature,
            raw_feature
        )

        patient_value = round(
            float(
                row["Patient_Value"]
            ),
            4
        )


        display_value = format_patient_value(
            raw_feature,
            patient_value
        )


        if row["SHAP_Value"] > 0:

            xai_result = (
                "This factor supported the model's "
                "CANCER-POSITIVE classification."
            )

        else:

            xai_result = (
                "This factor supported the model's "
                "CANCER-NEGATIVE classification."
            )


        xai_factors.append(
            {

                "rank":
                    rank,

                "factor":
                    friendly_name,

                "patient_value":
                    display_value,

                "xai_result":
                    xai_result
            }
        )


    # =====================================================
    # INTERPRETATION + RECOMMENDATION
    # =====================================================

    if cancer_prediction == 1:

        interpretation = (
            "The trained machine-learning model identified "
            "a patient pattern associated with the "
            "CANCER-POSITIVE classification."
        )

        recommendation = (
            "Further clinical evaluation by a gynecologist "
            "is recommended. Additional diagnostic testing "
            "may be required depending on the patient's "
            "clinical findings."
        )

    else:

        interpretation = (
            "The trained machine-learning model identified "
            "a patient pattern associated with the "
            "CANCER-NEGATIVE classification."
        )

        recommendation = (
            "Continue appropriate routine cervical "
            "screening and clinical follow-up as advised "
            "by a healthcare professional."
        )


    # =====================================================
    # COMPLETE RESPONSE
    # =====================================================

    response = {

        "patient_id":
            patient_id,


        "overall_cancer_prediction": {

            "prediction":
                cancer_result,

            "cancer_probability_percent":
                round(
                    cancer_positive_probability * 100,
                    2
                ),

            "no_cancer_probability_percent":
                round(
                    cancer_negative_probability * 100,
                    2
                ),

            "classification_threshold_percent":
                round(
                    float(cancer_threshold) * 100,
                    2
                )
        },


        "supporting_predictions": {

            "biopsy": {

                "prediction":
                    biopsy_result,

                "positive_probability_percent":
                    round(
                        float(
                            biopsy_probability[1]
                        ) * 100,
                        2
                    )
            },


            "hpv": {

                "prediction":
                    hpv_result,

                "positive_probability_percent":
                    round(
                        float(
                            hpv_probability[1]
                        ) * 100,
                        2
                    )
            }
        },


        "xai_explanation": {

            "method":
                "SHAP",

            "explanation":
                (
                    "These factors had the strongest "
                    "influence on this patient's "
                    "model classification."
                ),

            "top_supporting_factors":
                xai_factors
        },


        "interpretation":
            interpretation,


        "recommended_next_step":
            recommendation,


        "important_note":
            (
                "This is an AI-assisted cervical cancer "
                "risk classification and XAI explanation. "
                "It is not a confirmed medical diagnosis."
            )
    }

    if current_user is not None:
        db.add_history_entry(
            user_id=current_user["id"],
            kind="assessment",
            title=f"Patient #{patient_id}",
            result=cancer_result,
            risk_percent=response["overall_cancer_prediction"]["cancer_probability_percent"],
            details=response,
        )

    return response


# =========================================================
# IMAGE SCREENING ENDPOINT
# =========================================================

@app.post("/image-screening")
async def image_screening(
    file: UploadFile = File(...),
    current_user=Depends(auth.get_optional_user),
):
    if image_screening_model is None:
        raise HTTPException(
            status_code=503,
            detail="The image screening model is not available on this server.",
        )

    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="No image data received.")

    try:
        report = image_screening_model.screen(contents)
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Could not read this image. Please upload a clear JPG/PNG cell image. ({exc})",
        )

    if current_user is not None:
        db.add_history_entry(
            user_id=current_user["id"],
            kind="image_screening",
            title=file.filename or "Cell image",
            result=report["screening_result"],
            risk_percent=report["abnormal_probability_percent"],
            details=report,
        )

    return report


# =========================================================
# AUTH ENDPOINTS
# =========================================================

class RegisterRequest(BaseModel):
    name: str
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class ProfileUpdateRequest(BaseModel):
    name: str
    email: str


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str


def _user_public(user) -> dict:
    return {
        "id": user["id"],
        "name": user["name"],
        "username": user["username"],
        "email": user["email"],
    }


@app.post("/auth/register")
def register(body: RegisterRequest):
    name, username, email = body.name.strip(), body.username.strip(), body.email.strip().lower()
    auth.validate_registration(name, username, email, body.password)

    if db.get_user_by_username(username):
        raise HTTPException(409, "That username is already taken.")
    if db.get_user_by_email(email):
        raise HTTPException(409, "An account with that email already exists.")

    password_hash, salt = auth.hash_password(body.password)
    user = db.create_user(name, username, email, password_hash, salt)
    token = db.create_session(user["id"])
    return {"token": token, "user": _user_public(user)}


@app.post("/auth/login")
def login(body: LoginRequest):
    username = body.username.strip()
    user = db.get_user_by_username(username) or db.get_user_by_email(username.lower())
    if user is None or not auth.verify_password(body.password, user["password_hash"], user["password_salt"]):
        raise HTTPException(401, "Incorrect username or password.")
    token = db.create_session(user["id"])
    return {"token": token, "user": _user_public(user)}


@app.post("/auth/logout")
def logout(authorization: str | None = Header(default=None), current_user=Depends(auth.get_current_user)):
    token = authorization.split(" ", 1)[1].strip()
    db.delete_session(token)
    return {"message": "Signed out."}


@app.get("/profile")
def get_profile(current_user=Depends(auth.get_current_user)):
    return _user_public(current_user)


@app.put("/profile")
def update_profile(body: ProfileUpdateRequest, current_user=Depends(auth.get_current_user)):
    name, email = body.name.strip(), body.email.strip().lower()
    if len(name) < 2:
        raise HTTPException(400, "Please enter your full name.")
    if not auth.EMAIL_RE.match(email):
        raise HTTPException(400, "Please enter a valid email address.")
    existing = db.get_user_by_email(email)
    if existing is not None and existing["id"] != current_user["id"]:
        raise HTTPException(409, "That email is already used by another account.")
    updated = db.update_user_profile(current_user["id"], name, email)
    return _user_public(updated)


@app.post("/auth/change-password")
def change_password(body: ChangePasswordRequest, current_user=Depends(auth.get_current_user)):
    if not auth.verify_password(body.current_password, current_user["password_hash"], current_user["password_salt"]):
        raise HTTPException(400, "Current password is incorrect.")
    if len(body.new_password) < 8:
        raise HTTPException(400, "New password must be at least 8 characters.")
    password_hash, salt = auth.hash_password(body.new_password)
    db.update_user_password(current_user["id"], password_hash, salt)
    return {"message": "Password updated successfully."}


# =========================================================
# HISTORY ENDPOINTS
# =========================================================

@app.get("/history")
def get_history(current_user=Depends(auth.get_current_user)):
    return {"history": db.list_history(current_user["id"])}


@app.delete("/history")
def clear_history(current_user=Depends(auth.get_current_user)):
    db.clear_history(current_user["id"])
    return {"message": "History cleared."}


@app.delete("/history/{entry_id}")
def delete_history_entry(entry_id: int, current_user=Depends(auth.get_current_user)):
    db.delete_history_entry(current_user["id"], entry_id)
    return {"message": "Entry deleted."}
