from io import BytesIO
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
)


def create_cancer_pdf(report):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        spaceAfter=8,
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=10,
        textColor=colors.grey,
        spaceAfter=18,
    )

    heading_style = ParagraphStyle(
        "Heading",
        parent=styles["Heading2"],
        fontSize=13,
        spaceBefore=12,
        spaceAfter=8,
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=14,
    )

    story = []

    # =====================================================
    # HEADER
    # =====================================================

    story.append(
        Paragraph("CerviXAI", title_style)
    )

    story.append(
        Paragraph(
            "Cervical Cancer Risk Assessment Report",
            subtitle_style,
        )
    )

    # =====================================================
    # REPORT INFORMATION
    # =====================================================

    story.append(
        Paragraph(
            "Report Information",
            heading_style,
        )
    )

    report_date = datetime.now().strftime(
        "%d %B %Y, %I:%M %p"
    )

    patient_id = report.get(
        "patient_id",
        "N/A",
    )

    info_data = [
        ["Patient ID", str(patient_id)],
        ["Report Date", report_date],
        ["Report Type", "AI-Assisted Risk Assessment"],
    ]

    info_table = Table(
        info_data,
        colWidths=[
            55 * mm,
            115 * mm,
        ],
    )

    info_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#EAF2F8"),
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (0, -1),
                    "Helvetica-Bold",
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )

    story.append(info_table)

    # =====================================================
    # OVERALL PREDICTION
    # =====================================================

    overall = report.get(
        "overall_cancer_prediction",
        {},
    )

    prediction = overall.get(
        "prediction",
        "N/A",
    )

    cancer_probability = overall.get(
        "cancer_probability_percent",
        0,
    )

    no_cancer_probability = overall.get(
        "no_cancer_probability_percent",
        0,
    )

    threshold = overall.get(
        "classification_threshold_percent",
        0,
    )

    story.append(
        Paragraph(
            "Overall Prediction",
            heading_style,
        )
    )

    prediction_data = [
        [
            "Prediction",
            str(prediction),
        ],
        [
            "Cancer Probability",
            f"{cancer_probability:.2f}%",
        ],
        [
            "No-Cancer Probability",
            f"{no_cancer_probability:.2f}%",
        ],
        [
            "Classification Threshold",
            f"{threshold:.2f}%",
        ],
    ]

    prediction_table = Table(
        prediction_data,
        colWidths=[
            75 * mm,
            95 * mm,
        ],
    )

    prediction_table.setStyle(
        TableStyle(
            [
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (0, -1),
                    "Helvetica-Bold",
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
            ]
        )
    )

    story.append(prediction_table)

    # =====================================================
    # SUPPORTING PREDICTIONS
    # =====================================================

    supporting = report.get(
        "supporting_predictions",
        {},
    )

    biopsy = supporting.get(
        "biopsy",
        {},
    )

    hpv = supporting.get(
        "hpv",
        {},
    )

    story.append(
        Paragraph(
            "Supporting Predictions",
            heading_style,
        )
    )

    supporting_data = [
        [
            "Test",
            "Prediction",
            "Positive Probability",
        ],
        [
            "Biopsy",
            str(
                biopsy.get(
                    "prediction",
                    "N/A",
                )
            ),
            f"{float(biopsy.get('positive_probability_percent', 0)):.2f}%",
        ],
        [
            "HPV",
            str(
                hpv.get(
                    "prediction",
                    "N/A",
                )
            ),
            f"{float(hpv.get('positive_probability_percent', 0)):.2f}%",
        ],
    ]

    supporting_table = Table(
        supporting_data,
        colWidths=[
            45 * mm,
            55 * mm,
            70 * mm,
        ],
    )

    supporting_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#EAF2F8"),
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )

    story.append(supporting_table)

    # =====================================================
    # XAI EXPLANATION
    # =====================================================

    xai = report.get(
        "xai_explanation",
        {},
    )

    story.append(
        Paragraph(
            "Explainable AI Analysis",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            f"<b>Method:</b> {xai.get('method', 'SHAP')}",
            body_style,
        )
    )

    story.append(Spacer(1, 5))

    story.append(
        Paragraph(
            str(
                xai.get(
                    "explanation",
                    "No explanation available.",
                )
            ),
            body_style,
        )
    )

    # =====================================================
    # TOP XAI FACTORS
    # =====================================================

    factors = xai.get(
        "top_supporting_factors",
        [],
    )

    if factors:

        story.append(
            Paragraph(
                "Top Contributing Factors",
                heading_style,
            )
        )

        factor_rows = [
            [
                "Rank",
                "Factor",
                "Patient Value",
                "XAI Interpretation",
            ]
        ]

        for factor in factors:

            factor_rows.append(
                [
                    str(
                        factor.get(
                            "rank",
                            "",
                        )
                    ),
                    str(
                        factor.get(
                            "factor",
                            "",
                        )
                    ),
                    str(
                        factor.get(
                            "patient_value",
                            "",
                        )
                    ),
                    str(
                        factor.get(
                            "xai_result",
                            "",
                        )
                    ),
                ]
            )

        factor_table = Table(
            factor_rows,
            colWidths=[
                15 * mm,
                45 * mm,
                35 * mm,
                75 * mm,
            ],
            repeatRows=1,
        )

        factor_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#EAF2F8"),
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold",
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey,
                    ),
                    (
                        "FONTSIZE",
                        (0, 0),
                        (-1, -1),
                        7.5,
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP",
                    ),
                    (
                        "PADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                ]
            )
        )

        story.append(factor_table)

    # =====================================================
    # INTERPRETATION
    # =====================================================

    story.append(
        Paragraph(
            "Clinical Interpretation",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            str(
                report.get(
                    "interpretation",
                    "No interpretation available.",
                )
            ),
            body_style,
        )
    )

    # =====================================================
    # RECOMMENDED NEXT STEP
    # =====================================================

    story.append(
        Paragraph(
            "Recommended Next Step",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            str(
                report.get(
                    "recommended_next_step",
                    "Please consult a qualified healthcare professional.",
                )
            ),
            body_style,
        )
    )

    # =====================================================
    # IMPORTANT NOTE
    # =====================================================

    story.append(
        Paragraph(
            "Important Note",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            str(
                report.get(
                    "important_note",
                    "This report is not a confirmed medical diagnosis.",
                )
            ),
            body_style,
        )
    )

    # =====================================================
    # FOOTER / DISCLAIMER
    # =====================================================

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "<b>Disclaimer:</b> This report is generated by "
            "an artificial intelligence system for screening "
            "and informational purposes. It is not a medical "
            "diagnosis and should not replace professional "
            "medical evaluation, laboratory testing, "
            "histopathology, or advice from a qualified "
            "healthcare professional.",
            body_style,
        )
    )

    doc.build(story)

    buffer.seek(0)

    return buffer

def create_image_screening_pdf(report, image_bytes, patient_id):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ImageReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        spaceAfter=8,
    )

    subtitle_style = ParagraphStyle(
        "ImageReportSubtitle",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=10,
        textColor=colors.grey,
        spaceAfter=18,
    )

    heading_style = ParagraphStyle(
        "ImageReportHeading",
        parent=styles["Heading2"],
        fontSize=13,
        spaceBefore=12,
        spaceAfter=8,
    )

    body_style = ParagraphStyle(
        "ImageReportBody",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=14,
    )

    story = []

    # =====================================================
    # HEADER
    # =====================================================

    story.append(
        Paragraph("CerviXAI", title_style)
    )

    story.append(
        Paragraph(
            "Cervical Cell Image Screening Report",
            subtitle_style,
        )
    )

    # =====================================================
    # REPORT INFORMATION
    # =====================================================

    story.append(
        Paragraph(
            "Report Information",
            heading_style,
        )
    )

    report_date = datetime.now().strftime(
        "%d %B %Y, %I:%M %p"
    )

    info_data = [
        ["Patient ID", str(patient_id)],
        ["Report Date", report_date],
        ["Report Type", "AI-Assisted Image Screening"],
    ]

    info_table = Table(
        info_data,
        colWidths=[
            55 * mm,
            115 * mm,
        ],
    )

    info_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#EAF2F8"),
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (0, -1),
                    "Helvetica-Bold",
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )

    story.append(info_table)

    # =====================================================
    # SCREENING IMAGE
    # =====================================================

    story.append(
        Paragraph(
            "Screening Image",
            heading_style,
        )
    )

    image_reader = ImageReader(BytesIO(image_bytes))
    image_width, image_height = image_reader.getSize()

    max_width = 170 * mm
    max_height = 90 * mm

    scale = min(
        max_width / image_width,
        max_height / image_height,
        1,
    )

    screening_image = Image(
        image_reader,
        width=image_width * scale,
        height=image_height * scale,
    )

    story.append(screening_image)
    story.append(Spacer(1, 8))

    # =====================================================
    # SCREENING RESULT
    # =====================================================

    screening_result = report.get(
        "screening_result",
        "N/A",
    )

    abnormal_probability = report.get(
        "abnormal_probability_percent",
        0,
    )

    normal_probability = report.get(
        "normal_probability_percent",
        0,
    )

    likely_pattern = report.get(
        "likely_pattern",
        "N/A",
    )

    confidence = report.get(
        "confidence_percent",
        0,
    )

    story.append(
        Paragraph(
            "Screening Result",
            heading_style,
        )
    )

    result_data = [
        ["Screening Result", str(screening_result)],
        ["Likely Pattern", str(likely_pattern)],
        ["Abnormal Probability", f"{float(abnormal_probability):.2f}%"],
        ["Normal Probability", f"{float(normal_probability):.2f}%"],
        ["Model Confidence", f"{float(confidence):.2f}%"],
    ]

    result_table = Table(
        result_data,
        colWidths=[
            75 * mm,
            95 * mm,
        ],
    )

    result_table.setStyle(
        TableStyle(
            [
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (0, -1),
                    "Helvetica-Bold",
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )

    story.append(result_table)

    # =====================================================
    # PLAIN LANGUAGE SUMMARY
    # =====================================================

    story.append(
        Paragraph(
            "In Plain Language",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            str(
                report.get(
                    "plain_language_summary",
                    "No summary available.",
                )
            ),
            body_style,
        )
    )

    # =====================================================
    # VISUAL FACTORS
    # =====================================================

    factors = report.get(
        "top_visual_factors",
        [],
    )

    if factors:
        story.append(
            Paragraph(
                "What the AI Noticed",
                heading_style,
            )
        )

        factor_rows = [
            [
                "Rank",
                "Visual Factor",
                "Observation",
            ]
        ]

        for factor in factors:
            factor_rows.append(
                [
                    str(factor.get("rank", "")),
                    str(factor.get("factor", "")),
                    str(factor.get("observation", "")),
                ]
            )

        factor_table = Table(
            factor_rows,
            colWidths=[
                15 * mm,
                55 * mm,
                100 * mm,
            ],
            repeatRows=1,
        )

        factor_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#EAF2F8"),
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold",
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey,
                    ),
                    (
                        "FONTSIZE",
                        (0, 0),
                        (-1, -1),
                        8,
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP",
                    ),
                    (
                        "PADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                ]
            )
        )

        story.append(factor_table)

    # =====================================================
    # RECOMMENDED NEXT STEP
    # =====================================================

    story.append(
        Paragraph(
            "Recommended Next Step",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            str(
                report.get(
                    "recommended_next_step",
                    "Please consult a qualified healthcare professional.",
                )
            ),
            body_style,
        )
    )

    # =====================================================
    # IMPORTANT NOTE
    # =====================================================

    story.append(
        Paragraph(
            "Important Note",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            str(
                report.get(
                    "important_note",
                    "This report is not a confirmed medical diagnosis.",
                )
            ),
            body_style,
        )
    )

    # =====================================================
    # DISCLAIMER
    # =====================================================

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "<b>Disclaimer:</b> This report is generated by "
            "an artificial intelligence system for screening "
            "and informational purposes. It is not a confirmed "
            "cytology or pathology diagnosis and should not "
            "replace professional medical evaluation.",
            body_style,
        )
    )

    doc.build(story)

    buffer.seek(0)

    return buffer

def create_image_screening_pdf(report, image_bytes):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ImageReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        spaceAfter=8,
    )

    subtitle_style = ParagraphStyle(
        "ImageReportSubtitle",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=10,
        textColor=colors.grey,
        spaceAfter=18,
    )

    heading_style = ParagraphStyle(
        "ImageReportHeading",
        parent=styles["Heading2"],
        fontSize=13,
        spaceBefore=12,
        spaceAfter=8,
    )

    body_style = ParagraphStyle(
        "ImageReportBody",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=14,
    )

    story = []

    # =====================================================
    # HEADER
    # =====================================================

    story.append(
        Paragraph("CerviXAI", title_style)
    )

    story.append(
        Paragraph(
            "Cervical Cell Image Screening Report",
            subtitle_style,
        )
    )

    # =====================================================
    # REPORT INFORMATION
    # =====================================================

    story.append(
        Paragraph(
            "Report Information",
            heading_style,
        )
    )

    report_date = datetime.now().strftime(
        "%d %B %Y, %I:%M %p"
    )

    info_data = [
        ["Report Date", report_date],
        ["Report Type", "AI-Assisted Image Screening"],
    ]

    info_table = Table(
        info_data,
        colWidths=[
            55 * mm,
            115 * mm,
        ],
    )

    info_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#EAF2F8"),
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (0, -1),
                    "Helvetica-Bold",
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )

    story.append(info_table)

    # =====================================================
    # SCREENING IMAGE
    # =====================================================

    story.append(
        Paragraph(
            "Screening Image",
            heading_style,
        )
    )

    try:
        image = Image(
            BytesIO(image_bytes),
            width=150 * mm,
            height=100 * mm,
        )
        image.hAlign = "CENTER"
        story.append(image)
    except Exception:
        story.append(
            Paragraph(
                "Screening image could not be embedded in the PDF.",
                body_style,
            )
        )

    # =====================================================
    # SCREENING RESULT
    # =====================================================

    screening_result = report.get(
        "screening_result",
        "N/A",
    )

    abnormal_probability = report.get(
        "abnormal_probability_percent",
        0,
    )

    normal_probability = report.get(
        "normal_probability_percent",
        0,
    )

    likely_pattern = report.get(
        "likely_pattern",
        "N/A",
    )

    confidence = report.get(
        "confidence_percent",
        0,
    )

    story.append(
        Paragraph(
            "AI Screening Result",
            heading_style,
        )
    )

    result_data = [
        ["Screening Result", str(screening_result)],
        ["Likely Pattern", str(likely_pattern)],
        ["Abnormal Probability", f"{float(abnormal_probability):.2f}%"],
        ["Normal Probability", f"{float(normal_probability):.2f}%"],
        ["Model Confidence", f"{float(confidence):.2f}%"],
    ]

    result_table = Table(
        result_data,
        colWidths=[
            75 * mm,
            95 * mm,
        ],
    )

    result_table.setStyle(
        TableStyle(
            [
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (0, -1),
                    "Helvetica-Bold",
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )

    story.append(result_table)

    # =====================================================
    # PLAIN LANGUAGE SUMMARY
    # =====================================================

    story.append(
        Paragraph(
            "In Plain Language",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            str(
                report.get(
                    "plain_language_summary",
                    "No summary available.",
                )
            ),
            body_style,
        )
    )

    # =====================================================
    # VISUAL FACTORS
    # =====================================================

    factors = report.get(
        "top_visual_factors",
        [],
    )

    if factors:

        story.append(
            Paragraph(
                "What the AI Noticed",
                heading_style,
            )
        )

        factor_rows = [
            ["Rank", "Visual Factor", "Observation"]
        ]

        for factor in factors:
            factor_rows.append(
                [
                    str(factor.get("rank", "")),
                    str(factor.get("factor", "")),
                    str(factor.get("observation", "")),
                ]
            )

        factor_table = Table(
            factor_rows,
            colWidths=[
                15 * mm,
                55 * mm,
                100 * mm,
            ],
            repeatRows=1,
        )

        factor_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#EAF2F8"),
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold",
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey,
                    ),
                    (
                        "FONTSIZE",
                        (0, 0),
                        (-1, -1),
                        8,
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP",
                    ),
                    (
                        "PADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                ]
            )
        )

        story.append(factor_table)

    # =====================================================
    # RECOMMENDED NEXT STEP
    # =====================================================

    story.append(
        Paragraph(
            "Recommended Next Step",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            str(
                report.get(
                    "recommended_next_step",
                    "Please consult a qualified healthcare professional.",
                )
            ),
            body_style,
        )
    )

    # =====================================================
    # IMPORTANT NOTE
    # =====================================================

    story.append(
        Paragraph(
            "Important Note",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            str(
                report.get(
                    "important_note",
                    "This report is not a confirmed medical diagnosis.",
                )
            ),
            body_style,
        )
    )

    # =====================================================
    # DISCLAIMER
    # =====================================================

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "<b>Disclaimer:</b> This report is generated by "
            "an artificial intelligence system for screening "
            "and informational purposes. It is not a medical "
            "diagnosis and should not replace professional "
            "medical evaluation, laboratory testing, "
            "histopathology, or advice from a qualified "
            "healthcare professional.",
            body_style,
        )
    )

    doc.build(story)

    buffer.seek(0)

    return buffer