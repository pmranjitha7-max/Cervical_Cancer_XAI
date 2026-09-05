"""
Handcrafted cytology-style feature extraction for cervical cell images.

These features mirror the criteria cytotechnologists actually look at when
reading a Pap smear / liquid-based cytology slide (nucleus size, the
nucleus-to-cytoplasm ratio, how dark/irregular the nucleus staining is,
and how irregular the cell boundary is). Using human-meaningful features
(rather than raw CNN pixel features) is what lets the screening report
explain a result in plain language instead of an unreadable image.
"""
from __future__ import annotations

import numpy as np
from PIL import Image
from skimage.feature import graycomatrix, graycoprops
from skimage.filters import threshold_otsu
from skimage.measure import label as sk_label, regionprops
from skimage.color import rgb2gray, rgb2hsv

FEATURE_NAMES = [
    "cell_area_fraction",
    "nucleus_area_fraction",
    "nucleus_cytoplasm_ratio",
    "nucleus_mean_intensity",
    "nucleus_intensity_std",
    "nucleus_mean_saturation",
    "cytoplasm_mean_intensity",
    "cell_eccentricity",
    "cell_solidity",
    "texture_contrast",
    "texture_homogeneity",
    "texture_energy",
    "texture_correlation",
    "edge_density",
]

FEATURE_LABELS = {
    "cell_area_fraction": "Cell size relative to the image frame",
    "nucleus_area_fraction": "Nucleus size relative to the whole cell",
    "nucleus_cytoplasm_ratio": "Nucleus-to-cytoplasm (N:C) ratio",
    "nucleus_mean_intensity": "Nucleus darkness (staining intensity)",
    "nucleus_intensity_std": "Evenness of nucleus staining",
    "nucleus_mean_saturation": "Nucleus colour intensity (saturation)",
    "cytoplasm_mean_intensity": "Cytoplasm brightness",
    "cell_eccentricity": "Cell shape elongation",
    "cell_solidity": "Cell boundary regularity",
    "texture_contrast": "Surface texture contrast",
    "texture_homogeneity": "Surface texture smoothness",
    "texture_energy": "Surface texture uniformity",
    "texture_correlation": "Texture pattern consistency",
    "edge_density": "Sharpness of internal edges",
}


def _largest_component_mask(mask: np.ndarray) -> np.ndarray:
    lbl = sk_label(mask)
    if lbl.max() == 0:
        return mask
    props = regionprops(lbl)
    biggest = max(props, key=lambda p: p.area)
    return lbl == biggest.label


def extract_features(pil_image: Image.Image) -> dict:
    """Extract a fixed-length, human-meaningful feature vector from a single
    cell image. Works best on single-cell crops (e.g. Herlev-style images)
    but degrades gracefully on other cervical cytology / colposcopy images.
    """
    img = pil_image.convert("RGB")
    # Cap size for speed; aspect ratio doesn't matter for these stats.
    img.thumbnail((512, 512))
    arr = np.asarray(img).astype(np.float64) / 255.0
    gray = rgb2gray(arr)
    hsv = rgb2hsv(arr)

    h, w = gray.shape

    # --- Cell (foreground) mask: Herlev-style images have a light/white
    # background, so the cell is the darker region. Otsu handles this well.
    try:
        thresh = threshold_otsu(gray)
    except ValueError:
        thresh = float(np.mean(gray))
    cell_mask = gray < thresh
    if cell_mask.sum() < 20:
        cell_mask = gray < np.percentile(gray, 60)
    cell_mask = _largest_component_mask(cell_mask)
    cell_area = int(cell_mask.sum())
    cell_area_fraction = cell_area / (h * w)

    # --- Nucleus mask: within the cell, the nucleus stains darkest/most
    # saturated (classic haematoxylin-eosin / Papanicolaou staining cue).
    if cell_area > 20:
        cell_gray_vals = gray[cell_mask]
        try:
            nuc_thresh = threshold_otsu(cell_gray_vals)
        except ValueError:
            nuc_thresh = float(np.percentile(cell_gray_vals, 30))
        nucleus_mask = cell_mask & (gray < nuc_thresh)
    else:
        nucleus_mask = np.zeros_like(cell_mask)
    nucleus_area = int(nucleus_mask.sum())
    nucleus_area_fraction = nucleus_area / max(cell_area, 1)
    cytoplasm_mask = cell_mask & ~nucleus_mask
    nc_ratio = nucleus_area / max(cell_area - nucleus_area, 1)

    nucleus_mean_intensity = float(gray[nucleus_mask].mean()) if nucleus_area > 5 else float(gray[cell_mask].mean())
    nucleus_intensity_std = float(gray[nucleus_mask].std()) if nucleus_area > 5 else 0.0
    nucleus_mean_saturation = float(hsv[..., 1][nucleus_mask].mean()) if nucleus_area > 5 else float(hsv[..., 1][cell_mask].mean())
    cytoplasm_mean_intensity = float(gray[cytoplasm_mask].mean()) if cytoplasm_mask.sum() > 5 else nucleus_mean_intensity

    # --- Shape descriptors of the cell outline.
    eccentricity, solidity = 0.0, 1.0
    lbl = sk_label(cell_mask)
    if lbl.max() > 0:
        props = regionprops(lbl)
        biggest = max(props, key=lambda p: p.area)
        eccentricity = float(biggest.eccentricity)
        solidity = float(biggest.solidity)

    # --- Texture (GLCM) computed on the cell region only.
    gray_u8 = (gray * 255).astype(np.uint8)
    masked = np.where(cell_mask, gray_u8, 0)
    glcm = graycomatrix(masked, distances=[1], angles=[0], levels=256, symmetric=True, normed=True)
    texture_contrast = float(graycoprops(glcm, "contrast")[0, 0])
    texture_homogeneity = float(graycoprops(glcm, "homogeneity")[0, 0])
    texture_energy = float(graycoprops(glcm, "energy")[0, 0])
    texture_correlation = float(graycoprops(glcm, "correlation")[0, 0])
    if np.isnan(texture_correlation):
        texture_correlation = 0.0

    # --- Edge density inside the cell (boundary/chromatin irregularity).
    gy, gx = np.gradient(gray)
    grad_mag = np.hypot(gx, gy)
    edge_thresh = np.percentile(grad_mag, 90)
    edge_density = float((grad_mag[cell_mask] > edge_thresh).mean()) if cell_area > 5 else 0.0

    return {
        "cell_area_fraction": cell_area_fraction,
        "nucleus_area_fraction": nucleus_area_fraction,
        "nucleus_cytoplasm_ratio": nc_ratio,
        "nucleus_mean_intensity": nucleus_mean_intensity,
        "nucleus_intensity_std": nucleus_intensity_std,
        "nucleus_mean_saturation": nucleus_mean_saturation,
        "cytoplasm_mean_intensity": cytoplasm_mean_intensity,
        "cell_eccentricity": eccentricity,
        "cell_solidity": solidity,
        "texture_contrast": texture_contrast,
        "texture_homogeneity": texture_homogeneity,
        "texture_energy": texture_energy,
        "texture_correlation": texture_correlation,
        "edge_density": edge_density,
    }


def extract_feature_vector(pil_image: Image.Image) -> list:
    feats = extract_features(pil_image)
    return [feats[name] for name in FEATURE_NAMES]
