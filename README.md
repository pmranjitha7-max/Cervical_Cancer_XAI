# CerviXAI

An Explainable Artificial Intelligence (XAI) project for cervical cancer risk prediction, plus a cell-image AI screening aid, with a FastAPI backend and a Flutter mobile client.

## Overview

This project applies machine learning to cervical cancer risk-factor data and to cervical cytology cell images, and uses Explainable AI methods so predictions come with a plain-language explanation instead of a raw model score.

The project includes:

- Data preprocessing and exploratory data analysis
- Machine learning model training and evaluation (HPV, biopsy, cytology, Schiller-related, and overall cancer risk models)
- Model evaluation using cross-validation and threshold tuning
- Feature importance, SHAP, and LIME explanations
- A cervical cytology **cell-image screening** model with a plain-language report (see below)
- A FastAPI backend with accounts, profiles, and server-side assessment history
- A Flutter client (`frontend/flutter_app`)

## Image screening (new)

In addition to the structured-data risk models, the project includes an image-based screening path:

- `src/build_image_dataset.py` extracts a set of human-meaningful cytology features (nucleus-to-cytoplasm ratio, nucleus staining, cell shape/texture, etc. — the same criteria a cytotechnologist looks at) from a labelled cervical cell image dataset (Herlev-style: normal vs. dysplastic/carcinoma-in-situ cell images) into `dataset/cervical_image_dataset.csv`.
- `src/train_image_model.py` trains a Random Forest classifier on those features (`models/image_screening_model.pkl`) and saves evaluation results and SHAP plots to `results/`.
- `src/image_screening_report.py` turns a new uploaded image into a **plain-language screening report** (Normal/Abnormal, a confidence score, and a short explanation of what visually stood out) rather than raw pixels or a bare probability — the point being that a patient, not only a doctor, can read the result. It is a screening aid, not a diagnosis.
- `dataset/sample_cytology_images/` has a few sample images (one per cell type) for trying the feature out without needing the full dataset.
- The API exposes this at `POST /image-screening` (multipart image upload).

## Accounts, profile, and history

Accounts, profile edits, and assessment history are now stored server-side (SQLite, see `src/db.py`), not only in the app's memory. That means:

- Editing your profile actually saves (`PUT /profile`).
- History survives closing the app, logging out, and reinstalling, because it's tied to your account on the backend, not kept in memory on the device.

## Dataset

This project uses the Cervical Cancer (Risk Factors) dataset from the UCI Machine Learning Repository for the structured-data models, and a Herlev-style labelled cervical cytology cell image dataset for the image screening model.

The dataset contains demographic information, habits, medical history, and cervical cancer risk factors. The prediction targets include Hinselmann, Schiller, Cytology, and Biopsy.

> The dataset is used for educational and research purposes. No personally identifiable patient information is included in this repository.

## Project structure

```text
Cervical_Cancer_XAI/
│
├── dataset/          # Dataset files (+ sample_cytology_images/ for the image feature)
├── models/           # Trained machine learning models
├── results/          # Evaluation and XAI results
├── src/              # Python source code (FastAPI backend + training scripts)
├── frontend/
│   └── flutter_app/  # Flutter mobile client
├── data/             # Runtime SQLite database (accounts/history) — not committed
├── .gitignore
├── README.md
└── requirements.txt
```

## Running the backend

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
python -m uvicorn src.api:app --host 0.0.0.0 --port 8000
```

Interactive API docs: `http://127.0.0.1:8000/docs`

## Running the Flutter app

```bash
cd frontend/flutter_app
flutter pub get
flutter run --dart-define=API_BASE_URL=http://<your-backend-host>:8000
```

If you're testing on a physical device over USB, `adb reverse tcp:8000 tcp:8000` lets the device reach a backend running on `127.0.0.1:8000` on your computer.
