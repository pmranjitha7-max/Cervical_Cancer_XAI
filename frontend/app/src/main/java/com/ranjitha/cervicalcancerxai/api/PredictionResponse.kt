package com.ranjitha.cervicalcancerxai.api

data class PredictionResponse(

    val patient_id: Int,

    val overall_cancer_prediction: OverallCancerPrediction,

    val supporting_predictions: SupportingPredictions,

    val xai_explanation: XaiExplanation,

    val interpretation: String,

    val recommended_next_step: String,

    val important_note: String
)


data class OverallCancerPrediction(

    val prediction: String,

    val cancer_probability_percent: Double,

    val no_cancer_probability_percent: Double,

    val classification_threshold_percent: Double
)


data class SupportingPredictions(

    val biopsy: BiopsyPrediction,

    val hpv: HpvPrediction
)


data class BiopsyPrediction(

    val prediction: String,

    val positive_probability_percent: Double
)


data class HpvPrediction(

    val prediction: String,

    val positive_probability_percent: Double
)


data class XaiExplanation(

    val method: String,

    val explanation: String,

    val top_supporting_factors: List<XaiFactor>
)


data class XaiFactor(

    val rank: Int,

    val factor: String,

    val patient_value: String,

    val xai_result: String
)