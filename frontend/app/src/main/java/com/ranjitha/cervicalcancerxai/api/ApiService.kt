package com.ranjitha.cervicalcancerxai.api

import retrofit2.http.GET
import retrofit2.http.Query

interface ApiService {

    @GET("cancer-report")
    suspend fun predictPatient(
        @Query("patient_id") patientId: Int
    ): PredictionResponse
}