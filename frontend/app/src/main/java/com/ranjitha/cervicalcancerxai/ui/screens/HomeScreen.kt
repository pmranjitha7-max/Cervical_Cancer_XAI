package com.ranjitha.cervicalcancerxai.ui.screens

import android.content.Context
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavHostController

@Composable
fun HomeScreen(
    navController: NavHostController
) {
    val context = LocalContext.current

    val preferences = context.getSharedPreferences(
        "cervixai_auth",
        Context.MODE_PRIVATE
    )

    val doctorName = preferences.getString(
        "full_name",
        "Doctor"
    ) ?: "Doctor"

    val background = Brush.verticalGradient(
        colors = listOf(
            Color(0xFFF9FCFF),
            Color(0xFFEFF6FF),
            Color(0xFFE6F1FF)
        )
    )

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(background)
            .padding(20.dp)
    ) {
        Spacer(modifier = Modifier.height(30.dp))

        Text(
            text = "CerviXAI",
            fontSize = 34.sp,
            fontWeight = FontWeight.Bold,
            color = Color(0xFF1565D8)
        )

        Spacer(modifier = Modifier.height(6.dp))

        Text(
            text = "Clinical Decision Support System",
            fontSize = 16.sp,
            color = Color(0xFF526A8F)
        )

        Spacer(modifier = Modifier.height(28.dp))

        Text(
            text = "Welcome,",
            fontSize = 18.sp,
            color = Color(0xFF526A8F)
        )

        Text(
            text = doctorName,
            fontSize = 24.sp,
            fontWeight = FontWeight.Bold,
            color = Color(0xFF0E53B7)
        )

        Spacer(modifier = Modifier.height(28.dp))

        DashboardCard(
            icon = "🩺",
            title = "New Patient Assessment",
            subtitle = "Start a new cervical cancer assessment"
        ) {
            navController.navigate("assessment")
        }

        DashboardCard(
            icon = "📋",
            title = "Prediction History",
            subtitle = "View previous patient predictions"
        ) {
            navController.navigate("predictionHistory")
        }

        DashboardCard(
            icon = "ℹ️",
            title = "About CerviXAI",
            subtitle = "View application and project information"
        ) {
            navController.navigate("aboutCervixAI")
        }

        DashboardCard(
            icon = "👤",
            title = "My Profile",
            subtitle = "View doctor profile information"
        ) {
            navController.navigate("profile")
        }



        DashboardCard(
            icon = "🚪",
            title = "Logout",
            subtitle = "Sign out from CerviXAI"
        ) {
            preferences.edit()
                .putBoolean("is_logged_in", false)
                .putBoolean("remember_me", false)
                .apply()

            navController.navigate("login") {
                popUpTo("home") {
                    inclusive = true
                }
            }
        }

        Spacer(modifier = Modifier.weight(1f))

        Text(
            text = "Version 1.0",
            modifier = Modifier.align(Alignment.CenterHorizontally),
            color = Color(0xFF7B8CA8),
            fontSize = 13.sp
        )
    }
}

@Composable
fun DashboardCard(
    icon: String,
    title: String,
    subtitle: String,
    onClick: () -> Unit
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 7.dp)
            .clickable {
                onClick()
            },
        shape = RoundedCornerShape(18.dp),
        colors = CardDefaults.cardColors(
            containerColor = Color.White
        ),
        elevation = CardDefaults.cardElevation(
            defaultElevation = 6.dp
        )
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(18.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = icon,
                fontSize = 30.sp,
                modifier = Modifier.size(42.dp)
            )

            Spacer(modifier = Modifier.width(16.dp))

            Column(
                modifier = Modifier.weight(1f)
            ) {
                Text(
                    text = title,
                    fontSize = 18.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color(0xFF173A68)
                )

                Spacer(modifier = Modifier.height(4.dp))

                Text(
                    text = subtitle,
                    fontSize = 14.sp,
                    color = Color(0xFF6B7F9E)
                )
            }

            Text(
                text = "›",
                fontSize = 30.sp,
                color = Color(0xFF1565D8)
            )
        }
    }
}