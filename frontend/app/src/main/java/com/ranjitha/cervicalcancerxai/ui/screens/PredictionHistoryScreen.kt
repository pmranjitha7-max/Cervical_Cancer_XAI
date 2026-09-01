package com.ranjitha.cervicalcancerxai.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
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
fun PredictionHistoryScreen(
    navController: NavHostController
) {

    val background = Brush.verticalGradient(
        colors = listOf(
            Color(0xFFF8FBFF),
            Color(0xFFEAF3FF)
        )
    )

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(background)
            .padding(20.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {

        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {

            TextButton(
                onClick = {
                    navController.popBackStack()
                }
            ) {
                Text("← Back")
            }

            Spacer(modifier = Modifier.weight(1f))
        }

        Text(
            text = "Prediction History",
            fontSize = 30.sp,
            fontWeight = FontWeight.Bold,
            color = Color(0xFF1565D8)
        )

        Spacer(modifier = Modifier.height(30.dp))

        Card(
            modifier = Modifier.fillMaxWidth(),
            colors = CardDefaults.cardColors(
                containerColor = MaterialTheme.colorScheme.surface
            )
        ) {

            Column(
                modifier = Modifier.padding(24.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {

                Text(
                    text = "📋",
                    fontSize = 50.sp
                )

                Spacer(modifier = Modifier.height(16.dp))

                Text(
                    text = "No Prediction History",
                    fontSize = 22.sp,
                    fontWeight = FontWeight.Bold
                )

                Spacer(modifier = Modifier.height(10.dp))

                Text(
                    text = "Your previous cervical cancer prediction results will appear here after you complete patient assessments.",
                    fontSize = 16.sp,
                    color = Color.Gray
                )
            }
        }

        Spacer(modifier = Modifier.height(30.dp))

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
