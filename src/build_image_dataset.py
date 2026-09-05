import os
import csv
import sys
from PIL import Image
from image_features import extract_features, FEATURE_NAMES

ROOT = "/tmp/cciw/Herlev Dataset"
OUT = "/tmp/claude-0/-home-claude/2fa1290e-a201-5aa5-914c-697dea275e6e/scratchpad/cervical_image_dataset.csv"

NORMAL_CLASSES = {"normal_columnar", "normal_intermediate", "normal_superficiel"}
ABNORMAL_SEVERITY = {
    "light_dysplastic": "mild",
    "moderate_dysplastic": "moderate",
    "severe_dysplastic": "severe",
    "carcinoma_in_situ": "carcinoma_in_situ",
}

rows = []
image_id = 0
for split in ["Train", "Test"]:
    split_dir = os.path.join(ROOT, split)
    for cls in sorted(os.listdir(split_dir)):
        cls_dir = os.path.join(split_dir, cls)
        if not os.path.isdir(cls_dir):
            continue
        binary_label = "Normal" if cls in NORMAL_CLASSES else "Abnormal"
        severity = "none" if cls in NORMAL_CLASSES else ABNORMAL_SEVERITY.get(cls, "abnormal")
        files = sorted(os.listdir(cls_dir))
        for fname in files:
            fpath = os.path.join(cls_dir, fname)
            try:
                im = Image.open(fpath)
                feats = extract_features(im)
            except Exception as e:
                print("SKIP", fpath, e, file=sys.stderr)
                continue
            row = {
                "image_id": image_id,
                "split": split.lower(),
                "cell_type": cls,
                "label": binary_label,
                "severity": severity,
            }
            row.update(feats)
            rows.append(row)
            image_id += 1
        print(f"{split}/{cls}: {len(files)} images done", file=sys.stderr)

fieldnames = ["image_id", "split", "cell_type", "label", "severity"] + FEATURE_NAMES
with open(OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(rows)

print(f"Wrote {len(rows)} rows to {OUT}")
