# Cervical Cancer XAI

An Explainable Artificial Intelligence (XAI) project for cervical cancer risk prediction using machine learning.

## Overview

This project applies machine learning techniques to cervical cancer risk-factor data and uses Explainable AI methods to help interpret model predictions.

The project includes:

- Data preprocessing and exploratory data analysis
- Machine learning model training and evaluation
- Cervical cancer risk prediction
- HPV, biopsy, cytology, and Schiller-related models
- Model evaluation using cross-validation
- Threshold tuning
- Feature importance analysis
- SHAP explanations
- LIME explanations
- FastAPI-based prediction API

## Dataset

This project uses the Cervical Cancer (Risk Factors) dataset from the UCI Machine Learning Repository.

The dataset contains demographic information, habits, medical history, and cervical cancer risk factors. The prediction targets include Hinselmann, Schiller, Cytology, and Biopsy.

Dataset source: UCI Machine Learning Repository.

> The dataset is used for educational and research purposes. No personally identifiable patient information is included in this repository.

## Project Structure

```text
Cervical_Cancer_XAI/
│
├── dataset/          # Dataset files
├── models/           # Trained machine learning models
├── notebooks/        # Jupyter notebooks
├── results/          # Evaluation and XAI results
├── src/              # Python source code
├── .gitignore
├── README.md
└── requirements.txt