package com.ranjitha.cervicalcancerxai.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavHostController

@Composable
fun PatientAssessmentScreen(
    navController: NavHostController
) {

    var patientId by remember {
        mutableStateOf("")
    }

    var errorMessage by remember {
        mutableStateOf("")
    }

    val backgroundGradient = Brush.verticalGradient(
        colors = listOf(
            Color(0xFFF9FCFF),
            Color(0xFFEFF6FF),
            Color(0xFFE5F0FF)
        )
    )

    val titleColor = Color(0xFF173A68)
    val primaryBlue = Color(0xFF1565D8)
    val normalTextColor = Color(0xFF243B62)
    val secondaryTextColor = Color(0xFF526A8F)

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(backgroundGradient)
            .verticalScroll(rememberScrollState())
            .padding(24.dp)
    ) {

        Spacer(modifier = Modifier.height(25.dp))

        Text(
            text = "New Patient Assessment",
            fontSize = 30.sp,
            fontWeight = FontWeight.Bold,
            color = primaryBlue
        )

        Spacer(modifier = Modifier.height(10.dp))

        Text(
            text = "Enter the Patient ID to retrieve the patient record and run prediction.",
            fontSize = 16.sp,
            color = secondaryTextColor,
            lineHeight = 22.sp
        )

        Spacer(modifier = Modifier.height(35.dp))

        OutlinedTextField(
            value = patientId,
            onValueChange = {
                patientId = it
                errorMessage = ""
            },
            label = {
                Text(
                    text = "Patient ID",
                    color = secondaryTextColor
                )
            },
            singleLine = true,
            keyboardOptions = KeyboardOptions(
                keyboardType = KeyboardType.Number
            ),
            colors = OutlinedTextFieldDefaults.colors(
                focusedTextColor = normalTextColor,
                unfocusedTextColor = normalTextColor,
                focusedBorderColor = primaryBlue,
                unfocusedBorderColor = Color(0xFF8AA4C8),
                cursorColor = primaryBlue,
                focusedContainerColor = Color.White,
                unfocusedContainerColor = Color.White
            ),
            modifier = Modifier.fillMaxWidth()
        )

        Spacer(modifier = Modifier.height(16.dp))

        if (errorMessage.isNotEmpty()) {

            Text(
                text = errorMessage,
                color = MaterialTheme.colorScheme.error,
                fontSize = 14.sp
            )

            Spacer(modifier = Modifier.height(10.dp))
        }

        Spacer(modifier = Modifier.height(18.dp))

        Button(
            onClick = {

                val id = patientId.toIntOrNull()

                when {

                    patientId.isBlank() -> {
                        errorMessage =
                            "Please enter Patient ID."
                    }

                    id == null || id < 0 -> {
                        errorMessage =
                            "Please enter a valid numeric Patient ID."
                    }

                    else -> {

                        navController.navigate(
                            "prediction/$id"
                        )
                    }
                }
            },
            modifier = Modifier
                .fillMaxWidth()
                .height(58.dp),
            colors = ButtonDefaults.buttonColors(
                containerColor = primaryBlue,
                contentColor = Color.White
            )
        ) {

            Text(
                text = "CONTINUE",
                fontSize = 17.sp,
                fontWeight = FontWeight.Bold,
                color = Color.White
            )
        }

        Spacer(modifier = Modifier.height(30.dp))

        Text(
            text = "The current demo uses the selected Patient ID to retrieve the corresponding record from the existing cervical cancer dataset.",
            fontSize = 14.sp,
            color = secondaryTextColor,
            lineHeight = 20.sp
        )
    }
}