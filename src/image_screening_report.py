"""
Turns an uploaded cervical cytology cell image into a plain-language
screening report instead of a raw image / raw model dump — the whole
point being that a patient (not just a doctor) can read the result.
"""
from __future__ import annotations

import io
import numpy as np
import pandas as pd
import joblib
from PIL import Image

from .image_features import extract_feature_vector, FEATURE_NAMES, FEATURE_LABELS

NORMAL_CLASSES = {"normal_columnar", "normal_intermediate", "normal_superficiel"}

CELL_TYPE_LABELS = {
    "normal_superficiel": "Normal superficial squamous cells",
    "normal_intermediate": "Normal intermediate squamous cells",
    "normal_columnar": "Normal columnar cells",
    "light_dysplastic": "Mild cell changes (consistent with mild/low-grade dysplasia)",
    "moderate_dysplastic": "Moderate cell changes (consistent with moderate dysplasia)",
    "severe_dysplastic": "Marked cell changes (consistent with severe/high-grade dysplasia)",
    "carcinoma_in_situ": "Cell changes consistent with carcinoma in situ (high-grade)",
}

FEATURE_EXPLANATIONS = {
    "nucleus_cytoplasm_ratio": (
        "The cell's nucleus takes up an unusually large share of the cell, which is a classic sign screeners look for in abnormal cells.",
        "The cell's nucleus is a normal, small share of the cell, as expected in healthy cells.",
    ),
    "nucleus_area_fraction": (
        "The nucleus is enlarged relative to the whole cell.",
        "The nucleus size is within the normal range.",
    ),
    "nucleus_mean_intensity": (
        "The nucleus stains darker (hyperchromatic) than typical of a healthy cell.",
        "The nucleus staining is in the normal, lighter range.",
    ),
    "nucleus_intensity_std": (
        "The staining inside the nucleus is uneven, a pattern sometimes seen with abnormal chromatin.",
        "The staining inside the nucleus is even and uniform.",
    ),
    "nucleus_mean_saturation": (
        "The nucleus colour intensity is atypical compared with normal cells.",
        "The nucleus colour intensity looks typical.",
    ),
    "cytoplasm_mean_intensity": (
        "The cytoplasm brightness differs from the pattern seen in normal cells.",
        "The cytoplasm brightness is typical of a normal cell.",
    ),
    "cell_eccentricity": (
        "The cell outline is more elongated/irregular than a typical round healthy cell.",
        "The cell shape is regular, as expected in healthy cells.",
    ),
    "cell_solidity": (
        "The cell boundary is less smooth than expected, which can indicate an irregular cell shape.",
        "The cell boundary is smooth and regular.",
    ),
    "cell_area_fraction": (
        "The overall cell size is atypical compared with a normal reference cell.",
        "The overall cell size is within the normal range.",
    ),
    "texture_contrast": (
        "The internal texture of the cell shows more contrast/irregularity than usual.",
        "The internal texture of the cell is smooth and uniform, as expected.",
    ),
    "texture_homogeneity": (
        "The cell surface is less uniform than typical of a healthy cell.",
        "The cell surface is uniform, as expected in a healthy cell.",
    ),
    "texture_energy": (
        "The cell's texture pattern is less orderly than in a typical healthy cell.",
        "The cell's texture pattern is orderly, as expected.",
    ),
    "texture_correlation": (
        "The texture pattern is less consistent across the cell than expected.",
        "The texture pattern is consistent across the cell, as expected.",
    ),
    "edge_density": (
        "The cell shows sharper internal edges than typical, which can reflect irregular chromatin.",
        "The cell shows soft, typical internal edges.",
    ),
}


class ImageScreeningModel:
    """Loads the trained artifacts once and serves screening reports."""

    def __init__(self, model_path, features_path, classes_path, explainer_path=None):
        self.model = joblib.load(model_path)
        self.feature_names = joblib.load(features_path)
        self.classes = joblib.load(classes_path)
        self._explainer = None
        self._explainer_path = explainer_path

    @property
    def explainer(self):
        if self._explainer is None:
            import shap
            if self._explainer_path:
                try:
                    self._explainer = joblib.load(self._explainer_path)
                    return self._explainer
                except Exception:
                    pass
            self._explainer = shap.TreeExplainer(self.model)
        return self._explainer

    def screen(self, image_bytes: bytes) -> dict:
        img = Image.open(io.BytesIO(image_bytes))
        vector = extract_feature_vector(img)
        x = pd.DataFrame([vector], columns=self.feature_names)

        proba = self.model.predict_proba(x)[0]
        class_proba = dict(zip(self.classes, proba))
        abnormal_prob = sum(p for c, p in class_proba.items() if c not in NORMAL_CLASSES)
        normal_prob = 1.0 - abnormal_prob
        top_class = max(class_proba, key=class_proba.get)
        overall = "Abnormal" if abnormal_prob >= 0.5 else "Normal"

        # SHAP explanation for whichever bucket the image fell into.
        shap_raw = self.explainer.shap_values(x)
        bucket_classes = [c for c in self.classes if (c not in NORMAL_CLASSES) == (overall == "Abnormal")]
        idxs = [list(self.classes).index(c) for c in bucket_classes]
        if isinstance(shap_raw, list):
            sv = np.mean([shap_raw[i][0] for i in idxs], axis=0)
        else:
            arr = np.asarray(shap_raw)
            sv = np.mean([arr[0, :, i] for i in idxs], axis=0)

        order = np.argsort(-np.abs(sv))[:5]
        factors = []
        for rank, i in enumerate(order, start=1):
            fname = self.feature_names[i]
            positive_direction = sv[i] > 0  # pushes toward this bucket
            texts = FEATURE_EXPLANATIONS.get(fname, (
                f"This visual feature contributed to the {overall.lower()} result.",
                f"This visual feature was typical of a {overall.lower()} result.",
            ))
            explanation = texts[0] if (positive_direction == (overall == "Abnormal")) else texts[1]
            factors.append({
                "rank": rank,
                "factor": FEATURE_LABELS.get(fname, fname),
                "observation": explanation,
            })

        if overall == "Abnormal":
            interpretation = (
                "The visual pattern of this cell image is more consistent with abnormal "
                "cervical cells than with normal ones. "
                f"The closest matching pattern is: {CELL_TYPE_LABELS.get(top_class, top_class)}."
            )
            next_step = (
                "This screening flag should be reviewed by a pathologist or gynaecologist "
                "together with a proper laboratory-prepared slide and clinical history. "
                "It does not replace a formal Pap smear / biopsy reading."
            )
        else:
            interpretation = (
                "The visual pattern of this cell image is consistent with normal cervical "
                f"cells ({CELL_TYPE_LABELS.get(top_class, top_class)})."
            )
            next_step = (
                "Continue routine cervical screening as advised by a healthcare professional. "
                "This tool is a screening aid, not a substitute for a laboratory Pap smear reading."
            )

        return {
            "screening_result": overall,
            "abnormal_probability_percent": round(abnormal_prob * 100, 2),
            "normal_probability_percent": round(normal_prob * 100, 2),
            "likely_pattern": CELL_TYPE_LABELS.get(top_class, top_class),
            "confidence_percent": round(class_proba[top_class] * 100, 2),
            "plain_language_summary": interpretation,
            "top_visual_factors": factors,
            "recommended_next_step": next_step,
            "important_note": (
                "This is an AI-assisted image screening aid intended for education and "
                "triage support. It is not a confirmed cytology or pathology diagnosis."
            ),
        }
