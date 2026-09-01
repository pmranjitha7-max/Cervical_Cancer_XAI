package com.ranjitha.cervicalcancerxai.api

import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

object RetrofitClient {

    // Use 10.0.2.2 if running on Android Emulator
    // Use your computer's IP if running on a physical phone

    val apiService: ApiService by lazy {

        Retrofit.Builder()
            .baseUrl(ApiConfig.BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(ApiService::class.java)

    }
}