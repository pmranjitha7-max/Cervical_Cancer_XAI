package com.ranjitha.cervicalcancerxai.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavHostController

@Composable
fun AboutCervixAIScreen(
    navController: NavHostController
) {

    val background = Brush.verticalGradient(
        listOf(
            Color(0xFFF8FBFF),
            Color(0xFFEAF3FF)
        )
    )

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(background)
            .verticalScroll(rememberScrollState())
            .padding(20.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {

        TextButton(
            onClick = {
                navController.popBackStack()
            },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("← Back")
        }

        Text(
            text = "About CervixAI",
            fontSize = 30.sp,
            fontWeight = FontWeight.Bold,
            color = Color(0xFF1565D8)
        )

        Spacer(modifier = Modifier.height(24.dp))

        Card(
            modifier = Modifier.fillMaxWidth(),
            colors = CardDefaults.cardColors(
                containerColor = Color.White
            )
        ) {

            Column(
                modifier = Modifier.padding(20.dp)
            ) {

                Text(
                    text = "CervixAI-XAI",
                    fontSize = 22.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color(0xFF1565D8)
                )

                Spacer(modifier = Modifier.height(12.dp))

                Text(
                    text =
                        "CervixAI-XAI is an Explainable Artificial Intelligence (XAI) based mobile application developed to assist healthcare professionals in cervical cancer prediction. The application combines machine learning with explainable AI techniques to provide accurate predictions along with understandable explanations for clinical decision support.",
                    fontSize = 16.sp
                )

                Spacer(modifier = Modifier.height(20.dp))

                Text(
                    text = "Project Features",
                    fontSize = 20.sp,
                    fontWeight = FontWeight.Bold
                )

                Spacer(modifier = Modifier.height(10.dp))

                Text("• Doctor Login & Registration")
                Text("• Patient Assessment")
                Text("• AI Prediction")
                Text("• Explainable AI Results")
                Text("• Prediction History")
                Text("• Doctor Profile Management")

                Spacer(modifier = Modifier.height(20.dp))

                Text(
                    text = "Version 1.0",
                    fontWeight = FontWeight.Bold
                )
            }
        }

        Spacer(modifier = Modifier.height(24.dp))

        Button(
            onClick = {
                navController.popBackStack()
            },
            modifier = Modifier.fillMaxWidth(),
            colors = ButtonDefaults.buttonColors(
                containerColor = Color(0xFF1565D8)
            )
        ) {
            Text("Back to Dashboard")
        }
    }
}