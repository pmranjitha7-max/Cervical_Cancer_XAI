import json
import os
import joblib
import numpy as np
import pandas as pd
import shap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score

from image_features import FEATURE_NAMES

DATA = "/tmp/claude-0/-home-claude/2fa1290e-a201-5aa5-914c-697dea275e6e/scratchpad/cervical_image_dataset.csv"
OUTDIR = "/tmp/claude-0/-home-claude/2fa1290e-a201-5aa5-914c-697dea275e6e/scratchpad/artifacts"
os.makedirs(OUTDIR, exist_ok=True)

df = pd.read_csv(DATA)
train = df[df.split == "train"].reset_index(drop=True)
test = df[df.split == "test"].reset_index(drop=True)

NORMAL_CLASSES = {"normal_columnar", "normal_intermediate", "normal_superficiel"}

# ---------------------------------------------------------------
# Primary model: 7-class cell-pattern classifier (richer signal,
# still fully explainable via SHAP). Binary Normal/Abnormal and a
# severity band are both derived from this at report time.
# ---------------------------------------------------------------
X_train, y_train = train[FEATURE_NAMES], train["cell_type"]
X_test, y_test = test[FEATURE_NAMES], test["cell_type"]

model = RandomForestClassifier(
    n_estimators=150, max_depth=10, class_weight="balanced",
    random_state=42, n_jobs=-1
)
model.fit(X_train, y_train)
classes = list(model.classes_)

proba_test = model.predict_proba(X_test)
pred_class = np.array(classes)[proba_test.argmax(axis=1)]
pred_binary = np.array(["Normal" if c in NORMAL_CLASSES else "Abnormal" for c in pred_class])
true_binary = test["label"].values

acc_multiclass = accuracy_score(y_test, pred_class)
acc_binary = accuracy_score(true_binary, pred_binary)
f1_binary = f1_score(true_binary, pred_binary, pos_label="Abnormal")
cm_binary = confusion_matrix(true_binary, pred_binary, labels=["Normal", "Abnormal"])
report_multiclass = classification_report(y_test, pred_class)

print("7-class accuracy:", acc_multiclass)
print("Binary (derived) accuracy:", acc_binary, "F1(Abnormal):", f1_binary)
print(report_multiclass)
print("Binary confusion matrix [Normal,Abnormal]:\n", cm_binary)

joblib.dump(model, os.path.join(OUTDIR, "image_screening_model.pkl"))
joblib.dump(FEATURE_NAMES, os.path.join(OUTDIR, "image_screening_features.pkl"))
joblib.dump(classes, os.path.join(OUTDIR, "image_screening_classes.pkl"))

with open(os.path.join(OUTDIR, "image_screening_eval.json"), "w") as f:
    json.dump({
        "multiclass_accuracy": acc_multiclass,
        "binary_accuracy": acc_binary,
        "binary_f1_abnormal": f1_binary,
        "binary_confusion_matrix": cm_binary.tolist(),
        "binary_labels": ["Normal", "Abnormal"],
        "multiclass_classification_report": report_multiclass,
        "classes": classes,
        "n_train": len(train),
        "n_test": len(test),
    }, f, indent=2)

# Feature importance plot
importances = pd.Series(model.feature_importances_, index=FEATURE_NAMES).sort_values()
plt.figure(figsize=(8, 6))
importances.plot(kind="barh", color="#276ef1")
plt.title("Image screening model — feature importance")
plt.xlabel("Importance")
plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "image_feature_importance.png"), dpi=140)
plt.close()

# SHAP summary — averaged absolute impact across the 4 abnormal classes,
# which is what the live report uses to explain an Abnormal result.
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)
abnormal_idx = [i for i, c in enumerate(classes) if c not in NORMAL_CLASSES]
if isinstance(shap_values, list):
    sv = np.mean([np.abs(shap_values[i]) for i in abnormal_idx], axis=0)
else:
    sv = np.mean([np.abs(shap_values[:, :, i]) for i in abnormal_idx], axis=0)
plt.figure()
shap.summary_plot(sv, X_test, feature_names=FEATURE_NAMES, show=False, plot_type="bar")
plt.title("Average impact toward an Abnormal screening result")
plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "image_shap_summary.png"), dpi=140)
plt.close()

# NOTE: the SHAP TreeExplainer itself is not persisted — it is rebuilt
# from the (much smaller) saved model at API startup, which takes well
# under a second and avoids shipping a large duplicate artifact.

print("Saved artifacts to", OUTDIR)
