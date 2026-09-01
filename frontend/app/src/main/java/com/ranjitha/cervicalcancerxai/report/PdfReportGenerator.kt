package com.ranjitha.cervicalcancerxai.report

import android.content.Context
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.Typeface
import android.graphics.pdf.PdfDocument
import android.os.Environment
import com.ranjitha.cervicalcancerxai.api.PredictionResponse
import java.io.File
import java.io.FileOutputStream
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

object PdfReportGenerator {

    fun generateReport(
        context: Context,
        result: PredictionResponse
    ): File {

        val pdfDocument = PdfDocument()

        val pageWidth = 595
        val pageHeight = 842

        val marginLeft = 48f
        val marginRight = 48f
        val contentWidth = pageWidth - marginLeft - marginRight

        var pageNumber = 1
        var currentPage: PdfDocument.Page? = null
        var currentCanvas: Canvas? = null
        var y = 0f

        val titlePaint = Paint().apply {
            color = Color.rgb(20, 66, 114)
            textSize = 25f
            typeface = Typeface.create(
                Typeface.DEFAULT,
                Typeface.BOLD
            )
            isAntiAlias = true
        }

        val headingPaint = Paint().apply {
            color = Color.rgb(25, 73, 120)
            textSize = 16f
            typeface = Typeface.create(
                Typeface.DEFAULT,
                Typeface.BOLD
            )
            isAntiAlias = true
        }

        val bodyPaint = Paint().apply {
            color = Color.rgb(45, 55, 65)
            textSize = 11f
            typeface = Typeface.create(
                Typeface.DEFAULT,
                Typeface.NORMAL
            )
            isAntiAlias = true
        }

        val boldPaint = Paint(bodyPaint).apply {
            typeface = Typeface.create(
                Typeface.DEFAULT,
                Typeface.BOLD
            )
        }

        val mutedPaint = Paint(bodyPaint).apply {
            color = Color.rgb(95, 105, 115)
            textSize = 10f
        }

        val positivePaint = Paint().apply {
            color = Color.rgb(180, 35, 35)
            textSize = 18f
            typeface = Typeface.create(
                Typeface.DEFAULT,
                Typeface.BOLD
            )
            isAntiAlias = true
        }

        val negativePaint = Paint().apply {
            color = Color.rgb(20, 125, 85)
            textSize = 18f
            typeface = Typeface.create(
                Typeface.DEFAULT,
                Typeface.BOLD
            )
            isAntiAlias = true
        }

        val linePaint = Paint().apply {
            color = Color.rgb(205, 212, 220)
            strokeWidth = 1f
        }

        fun startPage() {

            val pageInfo = PdfDocument.PageInfo.Builder(
                pageWidth,
                pageHeight,
                pageNumber
            ).create()

            currentPage = pdfDocument.startPage(pageInfo)
            currentCanvas = currentPage?.canvas

            val canvas = currentCanvas ?: return

            canvas.drawColor(Color.WHITE)

            y = 50f

            canvas.drawText(
                "CerviXAI",
                marginLeft,
                y,
                titlePaint
            )

            y += 22f

            canvas.drawText(
                "Explainable Cervical Cancer Risk Assessment",
                marginLeft,
                y,
                boldPaint
            )

            y += 18f

            canvas.drawText(
                "Machine-Learning Prediction with SHAP-Based Explanation",
                marginLeft,
                y,
                mutedPaint
            )

            y += 18f

            canvas.drawLine(
                marginLeft,
                y,
                pageWidth - marginRight,
                y,
                linePaint
            )

            y += 28f
        }

        fun finishPage() {

            val page = currentPage ?: return
            val canvas = currentCanvas ?: return

            canvas.drawLine(
                marginLeft,
                pageHeight - 40f,
                pageWidth - marginRight,
                pageHeight - 40f,
                linePaint
            )

            canvas.drawText(
                "CerviXAI | AI-Assisted Assessment Report",
                marginLeft,
                pageHeight - 23f,
                mutedPaint
            )

            val pageText = "Page $pageNumber"

            canvas.drawText(
                pageText,
                pageWidth - marginRight -
                        mutedPaint.measureText(pageText),
                pageHeight - 23f,
                mutedPaint
            )

            pdfDocument.finishPage(page)

            currentPage = null
            currentCanvas = null

            pageNumber++
        }

        fun ensureSpace(requiredSpace: Float) {

            if (y + requiredSpace > pageHeight - 65f) {
                finishPage()
                startPage()
            }
        }

        fun drawWrappedText(
            text: String,
            paint: Paint = bodyPaint,
            indent: Float = 0f,
            lineSpacing: Float = 16f
        ) {

            val words = text.split(" ")
            var line = ""

            for (word in words) {

                val testLine =
                    if (line.isEmpty()) {
                        word
                    } else {
                        "$line $word"
                    }

                if (
                    paint.measureText(testLine) >
                    contentWidth - indent
                ) {

                    if (line.isNotEmpty()) {

                        ensureSpace(lineSpacing)

                        currentCanvas?.drawText(
                            line,
                            marginLeft + indent,
                            y,
                            paint
                        )

                        y += lineSpacing
                    }

                    line = word

                } else {

                    line = testLine
                }
            }

            if (line.isNotEmpty()) {

                ensureSpace(lineSpacing)

                currentCanvas?.drawText(
                    line,
                    marginLeft + indent,
                    y,
                    paint
                )

                y += lineSpacing
            }
        }

        fun sectionTitle(title: String) {

            ensureSpace(40f)

            y += 8f

            currentCanvas?.drawText(
                title,
                marginLeft,
                y,
                headingPaint
            )

            y += 10f

            currentCanvas?.drawLine(
                marginLeft,
                y,
                pageWidth - marginRight,
                y,
                linePaint
            )

            y += 20f
        }

        // =================================================
        // START REPORT
        // =================================================

        startPage()

        // =================================================
        // ASSESSMENT INFORMATION
        // =================================================

        sectionTitle("Assessment Information")

        drawWrappedText(
            "Patient ID: ${result.patient_id}",
            boldPaint
        )

        val dateFormat = SimpleDateFormat(
            "dd MMMM yyyy, hh:mm a",
            Locale.getDefault()
        )

        drawWrappedText(
            "Report generated: ${dateFormat.format(Date())}",
            mutedPaint
        )

        // =================================================
        // OVERALL CANCER CLASSIFICATION
        // =================================================

        sectionTitle(
            "Overall Cervical Cancer Classification"
        )

        val isPositive =
            result.overall_cancer_prediction.prediction
                .contains(
                    "POSITIVE",
                    ignoreCase = true
                )

        val resultPaint =
            if (isPositive) {
                positivePaint
            } else {
                negativePaint
            }

        ensureSpace(30f)

        currentCanvas?.drawText(
            result.overall_cancer_prediction.prediction,
            marginLeft,
            y,
            resultPaint
        )

        y += 28f

        drawWrappedText(
            "Cancer probability: " +
                    "${result.overall_cancer_prediction.cancer_probability_percent}%"
        )

        drawWrappedText(
            "No-cancer probability: " +
                    "${result.overall_cancer_prediction.no_cancer_probability_percent}%"
        )

        drawWrappedText(
            "Classification threshold: " +
                    "${result.overall_cancer_prediction.classification_threshold_percent}%"
        )

        // =================================================
        // SUPPORTING MODEL RESULTS
        // =================================================

        sectionTitle("Supporting Model Results")

        drawWrappedText(
            "Biopsy Assessment",
            boldPaint
        )

        drawWrappedText(
            "Result: ${result.supporting_predictions.biopsy.prediction}"
        )

        drawWrappedText(
            "Positive probability: " +
                    "${result.supporting_predictions.biopsy.positive_probability_percent}%"
        )

        y += 8f

        drawWrappedText(
            "HPV Assessment",
            boldPaint
        )

        drawWrappedText(
            "Result: ${result.supporting_predictions.hpv.prediction}"
        )

        drawWrappedText(
            "Positive probability: " +
                    "${result.supporting_predictions.hpv.positive_probability_percent}%"
        )

        // =================================================
        // XAI ANALYSIS
        // =================================================

        sectionTitle("Explainable AI Analysis")

        drawWrappedText(
            "Explanation method: ${result.xai_explanation.method}",
            boldPaint
        )

        y += 4f

        drawWrappedText(
            result.xai_explanation.explanation
        )

        y += 8f

        result.xai_explanation
            .top_supporting_factors
            .forEach { factor ->

                ensureSpace(65f)

                drawWrappedText(
                    "${factor.rank}. ${factor.factor}",
                    boldPaint
                )

                drawWrappedText(
                    "Patient value: ${factor.patient_value}",
                    bodyPaint,
                    indent = 12f
                )

                drawWrappedText(
                    factor.xai_result,
                    mutedPaint,
                    indent = 12f
                )

                y += 9f
            }

        // =================================================
        // INTERPRETATION
        // =================================================

        sectionTitle("Interpretation")

        drawWrappedText(
            result.interpretation
        )

        // =================================================
        // RECOMMENDATION
        // =================================================

        sectionTitle("Recommended Next Step")

        drawWrappedText(
            result.recommended_next_step
        )

        // =================================================
        // IMPORTANT NOTE
        // =================================================

        sectionTitle("Important Clinical Note")

        drawWrappedText(
            result.important_note,
            mutedPaint
        )

        y += 8f

        drawWrappedText(
            "The output of CerviXAI should be interpreted together with appropriate clinical examination, screening results and professional medical judgement.",
            mutedPaint
        )

        finishPage()

        // =================================================
        // SAVE PDF
        // =================================================

        val reportsDirectory = File(
            context.getExternalFilesDir(
                Environment.DIRECTORY_DOCUMENTS
            ),
            "CerviXAI"
        )

        if (!reportsDirectory.exists()) {
            reportsDirectory.mkdirs()
        }

        val file = File(
            reportsDirectory,
            "CerviXAI_Report_Patient_${result.patient_id}.pdf"
        )

        FileOutputStream(file).use { outputStream ->
            pdfDocument.writeTo(outputStream)
        }

        pdfDocument.close()

        return file
    }
}