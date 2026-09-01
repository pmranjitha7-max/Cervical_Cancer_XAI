package com.ranjitha.cervicalcancerxai.ui.screens

import android.widget.Toast
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.ranjitha.cervicalcancerxai.report.PdfReportGenerator
import com.ranjitha.cervicalcancerxai.viewmodel.PredictionViewModel
import java.io.File


@Composable
fun PredictionScreen(
    patientId: Int,
    predictionViewModel: PredictionViewModel = viewModel()
) {

    val prediction by predictionViewModel.prediction.collectAsState()
    val isLoading by predictionViewModel.isLoading.collectAsState()
    val errorMessage by predictionViewModel.errorMessage.collectAsState()

    val context = LocalContext.current

    var pendingPdfFile by remember {
        mutableStateOf<File?>(null)
    }


    // =====================================================
    // PDF SAVE LAUNCHER
    // =====================================================

    val pdfSaveLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.CreateDocument(
            "application/pdf"
        )
    ) { uri ->

        if (uri != null) {

            val sourceFile = pendingPdfFile

            if (sourceFile != null) {

                try {

                    sourceFile.inputStream().use { inputStream ->

                        context.contentResolver
                            .openOutputStream(uri)
                            ?.use { outputStream ->

                                inputStream.copyTo(
                                    outputStream
                                )
                            }
                    }

                    Toast.makeText(
                        context,
                        "PDF report saved successfully.",
                        Toast.LENGTH_LONG
                    ).show()

                } catch (e: Exception) {

                    Toast.makeText(
                        context,
                        "Unable to save PDF: ${e.message}",
                        Toast.LENGTH_LONG
                    ).show()
                }
            }

            pendingPdfFile = null
        }
    }


    // =====================================================
    // COLORS
    // =====================================================

    val backgroundColor = Color(0xFFF4F8FC)
    val cardColor = Color.White

    val primaryBlue = Color(0xFF0D47A1)

    val titleColor = Color(0xFF163A5F)
    val normalTextColor = Color(0xFF263746)
    val secondaryTextColor = Color(0xFF60758A)

    val positiveColor = Color(0xFFB3261E)
    val negativeColor = Color(0xFF18794E)

    val warningBackground = Color(0xFFFFF7E6)
    val errorBackground = Color(0xFFFFEBEE)


    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(backgroundColor)
            .verticalScroll(
                rememberScrollState()
            )
            .padding(20.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {


        // =================================================
        // PAGE TITLE
        // =================================================

        Spacer(
            modifier = Modifier.height(20.dp)
        )

        Text(
            text = "CerviXAI",
            fontSize = 30.sp,
            fontWeight = FontWeight.Bold,
            color = primaryBlue,
            modifier = Modifier.fillMaxWidth()
        )

        Spacer(
            modifier = Modifier.height(4.dp)
        )

        Text(
            text = "Explainable Cervical Cancer Risk Assessment",
            fontSize = 18.sp,
            fontWeight = FontWeight.SemiBold,
            color = titleColor,
            modifier = Modifier.fillMaxWidth()
        )

        Spacer(
            modifier = Modifier.height(8.dp)
        )

        Text(
            text = "Machine-learning prediction with SHAP-based explanation",
            fontSize = 14.sp,
            color = secondaryTextColor,
            modifier = Modifier.fillMaxWidth()
        )


        Spacer(
            modifier = Modifier.height(28.dp)
        )


        // =================================================
        // PATIENT INFORMATION
        // =================================================

        Card(
            modifier = Modifier.fillMaxWidth(),
            shape = RoundedCornerShape(16.dp),
            colors = CardDefaults.cardColors(
                containerColor = cardColor
            ),
            elevation = CardDefaults.cardElevation(
                defaultElevation = 3.dp
            )
        ) {

            Column(
                modifier = Modifier.padding(20.dp)
            ) {

                Text(
                    text = "Patient Information",
                    fontSize = 19.sp,
                    fontWeight = FontWeight.Bold,
                    color = titleColor
                )

                Spacer(
                    modifier = Modifier.height(12.dp)
                )

                Text(
                    text = "Patient ID: $patientId",
                    fontSize = 18.sp,
                    fontWeight = FontWeight.SemiBold,
                    color = normalTextColor
                )

                Spacer(
                    modifier = Modifier.height(6.dp)
                )

                Text(
                    text = "The assessment uses the patient record associated with this ID.",
                    fontSize = 14.sp,
                    color = secondaryTextColor,
                    lineHeight = 20.sp
                )
            }
        }


        Spacer(
            modifier = Modifier.height(22.dp)
        )


        // =================================================
        // ASSESSMENT BUTTON
        // =================================================

        Button(
            onClick = {

                predictionViewModel.predict(
                    patientId
                )

            },
            enabled = !isLoading,
            modifier = Modifier
                .fillMaxWidth()
                .height(56.dp),
            colors = ButtonDefaults.buttonColors(
                containerColor = primaryBlue,
                contentColor = Color.White
            ),
            shape = RoundedCornerShape(12.dp)
        ) {

            if (isLoading) {

                CircularProgressIndicator(
                    color = Color.White,
                    modifier = Modifier.height(24.dp)
                )

            } else {

                Text(
                    text = "RUN CANCER ASSESSMENT",
                    fontSize = 16.sp,
                    fontWeight = FontWeight.Bold
                )
            }
        }


        // =================================================
        // ERROR
        // =================================================

        errorMessage?.let { message ->

            Spacer(
                modifier = Modifier.height(18.dp)
            )

            Card(
                modifier = Modifier.fillMaxWidth(),
                colors = CardDefaults.cardColors(
                    containerColor = errorBackground
                ),
                shape = RoundedCornerShape(12.dp)
            ) {

                Text(
                    text = message,
                    color = positiveColor,
                    fontSize = 14.sp,
                    lineHeight = 20.sp,
                    modifier = Modifier.padding(16.dp)
                )
            }
        }


        // =================================================
        // COMPLETE REPORT
        // =================================================

        prediction?.let { result ->

            val cancerResult =
                result.overall_cancer_prediction.prediction

            val cancerPositive =
                cancerResult.contains(
                    "POSITIVE",
                    ignoreCase = true
                )

            val resultColor =
                if (cancerPositive) {
                    positiveColor
                } else {
                    negativeColor
                }


            Spacer(
                modifier = Modifier.height(30.dp)
            )


            // =================================================
            // REPORT TITLE
            // =================================================

            Text(
                text = "Assessment Report",
                fontSize = 24.sp,
                fontWeight = FontWeight.Bold,
                color = primaryBlue,
                modifier = Modifier.fillMaxWidth()
            )


            Spacer(
                modifier = Modifier.height(16.dp)
            )


            // =================================================
            // OVERALL CANCER ASSESSMENT
            // =================================================

            Card(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(16.dp),
                colors = CardDefaults.cardColors(
                    containerColor = cardColor
                ),
                elevation = CardDefaults.cardElevation(
                    defaultElevation = 4.dp
                )
            ) {

                Column(
                    modifier = Modifier.padding(20.dp)
                ) {

                    Text(
                        text = "Overall Cervical Cancer Classification",
                        fontSize = 19.sp,
                        fontWeight = FontWeight.Bold,
                        color = titleColor
                    )


                    Spacer(
                        modifier = Modifier.height(18.dp)
                    )


                    Text(
                        text = cancerResult,
                        fontSize = 25.sp,
                        fontWeight = FontWeight.Bold,
                        color = resultColor
                    )


                    Spacer(
                        modifier = Modifier.height(18.dp)
                    )


                    Text(
                        text = "Cancer probability",
                        fontSize = 14.sp,
                        color = secondaryTextColor
                    )

                    Text(
                        text =
                            "${result.overall_cancer_prediction.cancer_probability_percent}%",
                        fontSize = 22.sp,
                        fontWeight = FontWeight.Bold,
                        color = positiveColor
                    )


                    Spacer(
                        modifier = Modifier.height(12.dp)
                    )


                    Text(
                        text = "No-cancer probability",
                        fontSize = 14.sp,
                        color = secondaryTextColor
                    )

                    Text(
                        text =
                            "${result.overall_cancer_prediction.no_cancer_probability_percent}%",
                        fontSize = 22.sp,
                        fontWeight = FontWeight.Bold,
                        color = negativeColor
                    )


                    Spacer(
                        modifier = Modifier.height(14.dp)
                    )


                    HorizontalDivider()


                    Spacer(
                        modifier = Modifier.height(14.dp)
                    )


                    Text(
                        text =
                            "Classification threshold: " +
                                    "${result.overall_cancer_prediction.classification_threshold_percent}%",
                        fontSize = 14.sp,
                        color = secondaryTextColor
                    )
                }
            }


            Spacer(
                modifier = Modifier.height(24.dp)
            )


            // =================================================
            // SUPPORTING MODEL RESULTS
            // =================================================

            Text(
                text = "Supporting Model Results",
                fontSize = 21.sp,
                fontWeight = FontWeight.Bold,
                color = titleColor,
                modifier = Modifier.fillMaxWidth()
            )


            Spacer(
                modifier = Modifier.height(14.dp)
            )


            // =================================================
            // BIOPSY
            // =================================================

            Card(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(14.dp),
                colors = CardDefaults.cardColors(
                    containerColor = cardColor
                ),
                elevation = CardDefaults.cardElevation(
                    defaultElevation = 2.dp
                )
            ) {

                Column(
                    modifier = Modifier.padding(18.dp)
                ) {

                    Text(
                        text = "Biopsy Assessment",
                        fontSize = 18.sp,
                        fontWeight = FontWeight.Bold,
                        color = titleColor
                    )

                    Spacer(
                        modifier = Modifier.height(10.dp)
                    )

                    Text(
                        text =
                            "Result: ${result.supporting_predictions.biopsy.prediction}",
                        fontSize = 17.sp,
                        fontWeight = FontWeight.SemiBold,
                        color = normalTextColor
                    )

                    Spacer(
                        modifier = Modifier.height(6.dp)
                    )

                    Text(
                        text =
                            "Positive probability: " +
                                    "${result.supporting_predictions.biopsy.positive_probability_percent}%",
                        fontSize = 15.sp,
                        color = secondaryTextColor
                    )
                }
            }


            Spacer(
                modifier = Modifier.height(14.dp)
            )


            // =================================================
            // HPV
            // =================================================

            Card(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(14.dp),
                colors = CardDefaults.cardColors(
                    containerColor = cardColor
                ),
                elevation = CardDefaults.cardElevation(
                    defaultElevation = 2.dp
                )
            ) {

                Column(
                    modifier = Modifier.padding(18.dp)
                ) {

                    Text(
                        text = "HPV Assessment",
                        fontSize = 18.sp,
                        fontWeight = FontWeight.Bold,
                        color = titleColor
                    )

                    Spacer(
                        modifier = Modifier.height(10.dp)
                    )

                    Text(
                        text =
                            "Result: ${result.supporting_predictions.hpv.prediction}",
                        fontSize = 17.sp,
                        fontWeight = FontWeight.SemiBold,
                        color = normalTextColor
                    )

                    Spacer(
                        modifier = Modifier.height(6.dp)
                    )

                    Text(
                        text =
                            "Positive probability: " +
                                    "${result.supporting_predictions.hpv.positive_probability_percent}%",
                        fontSize = 15.sp,
                        color = secondaryTextColor
                    )
                }
            }


            Spacer(
                modifier = Modifier.height(28.dp)
            )


            // =================================================
            // XAI EXPLANATION
            // =================================================

            Text(
                text = "Explainable AI Analysis",
                fontSize = 21.sp,
                fontWeight = FontWeight.Bold,
                color = primaryBlue,
                modifier = Modifier.fillMaxWidth()
            )


            Spacer(
                modifier = Modifier.height(8.dp)
            )


            Text(
                text =
                    "Explanation method: ${result.xai_explanation.method}",
                fontSize = 15.sp,
                fontWeight = FontWeight.SemiBold,
                color = normalTextColor,
                modifier = Modifier.fillMaxWidth()
            )


            Spacer(
                modifier = Modifier.height(6.dp)
            )


            Text(
                text = result.xai_explanation.explanation,
                fontSize = 14.sp,
                color = secondaryTextColor,
                lineHeight = 20.sp,
                modifier = Modifier.fillMaxWidth()
            )


            Spacer(
                modifier = Modifier.height(16.dp)
            )


            result.xai_explanation
                .top_supporting_factors
                .forEach { factor ->

                    Card(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(
                                bottom = 12.dp
                            ),
                        shape = RoundedCornerShape(14.dp),
                        colors = CardDefaults.cardColors(
                            containerColor = cardColor
                        ),
                        elevation = CardDefaults.cardElevation(
                            defaultElevation = 2.dp
                        )
                    ) {

                        Column(
                            modifier = Modifier.padding(16.dp)
                        ) {

                            Text(
                                text =
                                    "${factor.rank}. ${factor.factor}",
                                fontSize = 17.sp,
                                fontWeight = FontWeight.Bold,
                                color = titleColor
                            )


                            Spacer(
                                modifier = Modifier.height(7.dp)
                            )


                            Text(
                                text =
                                    "Patient value: ${factor.patient_value}",
                                fontSize = 15.sp,
                                color = normalTextColor
                            )


                            Spacer(
                                modifier = Modifier.height(7.dp)
                            )


                            Text(
                                text = factor.xai_result,
                                fontSize = 14.sp,
                                color = secondaryTextColor,
                                lineHeight = 20.sp
                            )
                        }
                    }
                }


            Spacer(
                modifier = Modifier.height(18.dp)
            )


            // =================================================
            // INTERPRETATION
            // =================================================

            Card(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(16.dp),
                colors = CardDefaults.cardColors(
                    containerColor = cardColor
                ),
                elevation = CardDefaults.cardElevation(
                    defaultElevation = 2.dp
                )
            ) {

                Column(
                    modifier = Modifier.padding(18.dp)
                ) {

                    Text(
                        text = "Interpretation",
                        fontSize = 19.sp,
                        fontWeight = FontWeight.Bold,
                        color = titleColor
                    )


                    Spacer(
                        modifier = Modifier.height(10.dp)
                    )


                    Text(
                        text = result.interpretation,
                        fontSize = 15.sp,
                        color = normalTextColor,
                        lineHeight = 22.sp
                    )
                }
            }


            Spacer(
                modifier = Modifier.height(16.dp)
            )


            // =================================================
            // RECOMMENDED NEXT STEP
            // =================================================

            Card(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(16.dp),
                colors = CardDefaults.cardColors(
                    containerColor = warningBackground
                ),
                elevation = CardDefaults.cardElevation(
                    defaultElevation = 2.dp
                )
            ) {

                Column(
                    modifier = Modifier.padding(18.dp)
                ) {

                    Text(
                        text = "Recommended Next Step",
                        fontSize = 19.sp,
                        fontWeight = FontWeight.Bold,
                        color = titleColor
                    )


                    Spacer(
                        modifier = Modifier.height(10.dp)
                    )


                    Text(
                        text = result.recommended_next_step,
                        fontSize = 15.sp,
                        color = normalTextColor,
                        lineHeight = 22.sp
                    )
                }
            }


            Spacer(
                modifier = Modifier.height(16.dp)
            )


            // =================================================
            // IMPORTANT NOTE
            // =================================================

            Card(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(14.dp),
                colors = CardDefaults.cardColors(
                    containerColor = Color(0xFFE8F1FA)
                )
            ) {

                Column(
                    modifier = Modifier.padding(16.dp)
                ) {

                    Text(
                        text = "Important Note",
                        fontSize = 16.sp,
                        fontWeight = FontWeight.Bold,
                        color = titleColor
                    )


                    Spacer(
                        modifier = Modifier.height(6.dp)
                    )


                    Text(
                        text = result.important_note,
                        fontSize = 13.sp,
                        color = secondaryTextColor,
                        lineHeight = 19.sp
                    )
                }
            }


            Spacer(
                modifier = Modifier.height(24.dp)
            )


            // =================================================
            // DOWNLOAD PDF REPORT
            // =================================================

            Button(
                onClick = {

                    try {

                        val generatedFile =
                            PdfReportGenerator.generateReport(
                                context = context,
                                result = result
                            )

                        pendingPdfFile =
                            generatedFile

                        pdfSaveLauncher.launch(
                            "CerviXAI_Report_Patient_${result.patient_id}.pdf"
                        )

                    } catch (e: Exception) {

                        Toast.makeText(
                            context,
                            "PDF generation failed: ${e.message}",
                            Toast.LENGTH_LONG
                        ).show()
                    }
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(58.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = Color(0xFF176B55),
                    contentColor = Color.White
                ),
                shape = RoundedCornerShape(12.dp)
            ) {

                Text(
                    text = "DOWNLOAD PDF REPORT",
                    fontSize = 16.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color.White
                )
            }


            Spacer(
                modifier = Modifier.height(12.dp)
            )


            Text(
                text = "The PDF contains the prediction, supporting model results, SHAP explanation, interpretation and recommended next step.",
                fontSize = 12.sp,
                color = secondaryTextColor,
                lineHeight = 18.sp,
                modifier = Modifier.fillMaxWidth()
            )


            Spacer(
                modifier = Modifier.height(40.dp)
            )
        }
    }
}