package com.ranjitha.cervicalcancerxai.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.ranjitha.cervicalcancerxai.api.PredictionResponse
import com.ranjitha.cervicalcancerxai.api.RetrofitClient
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class PredictionViewModel : ViewModel() {

    private val _prediction =
        MutableStateFlow<PredictionResponse?>(null)

    val prediction: StateFlow<PredictionResponse?> =
        _prediction


    private val _isLoading =
        MutableStateFlow(false)

    val isLoading: StateFlow<Boolean> =
        _isLoading


    private val _errorMessage =
        MutableStateFlow<String?>(null)

    val errorMessage: StateFlow<String?> =
        _errorMessage


    fun predict(patientId: Int) {

        viewModelScope.launch {

            _isLoading.value = true
            _errorMessage.value = null
            _prediction.value = null

            try {

                val result =
                    RetrofitClient.apiService.predictPatient(patientId)

                _prediction.value = result

            } catch (e: Exception) {

                _errorMessage.value =
                    "Prediction failed: ${e.message}"

                e.printStackTrace()

            } finally {

                _isLoading.value = false
            }
        }
    }


    fun clearError() {
        _errorMessage.value = null
    }
}