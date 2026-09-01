package com.ranjitha.cervicalcancerxai.ui.navigation

import androidx.compose.runtime.Composable
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument

import com.ranjitha.cervicalcancerxai.ui.screens.ForgotPasswordScreen
import com.ranjitha.cervicalcancerxai.ui.screens.AboutCervixAIScreen
import com.ranjitha.cervicalcancerxai.ui.screens.ChangePasswordScreen
import com.ranjitha.cervicalcancerxai.ui.screens.HomeScreen
import com.ranjitha.cervicalcancerxai.ui.screens.LoginScreen
import com.ranjitha.cervicalcancerxai.ui.screens.MyProfileScreen
import com.ranjitha.cervicalcancerxai.ui.screens.PatientAssessmentScreen
import com.ranjitha.cervicalcancerxai.ui.screens.PredictionHistoryScreen
import com.ranjitha.cervicalcancerxai.ui.screens.PredictionScreen
import com.ranjitha.cervicalcancerxai.ui.screens.RegisterScreen
import com.ranjitha.cervicalcancerxai.ui.screens.SplashScreen

@Composable
fun AppNavigation() {

    val navController = rememberNavController()

    NavHost(
        navController = navController,
        startDestination = "splash"
    ) {

        composable("splash") {
            SplashScreen(navController)
        }

        composable("login") {
            LoginScreen(navController)
        }

        composable("register") {
            RegisterScreen(navController)
        }

        composable("forgot_password") {
            ForgotPasswordScreen(navController)
        }

        composable("home") {
            HomeScreen(navController)
        }

        composable("assessment") {
            PatientAssessmentScreen(navController)
        }

        composable("profile") {
            MyProfileScreen(navController)
        }

        composable("predictionHistory") {
            PredictionHistoryScreen(navController)
        }

        composable("aboutCervixAI") {
            AboutCervixAIScreen(navController)
        }

        composable("changePassword") {
            ChangePasswordScreen(navController)
        }

        composable(
            route = "prediction/{patientId}",
            arguments = listOf(
                navArgument("patientId") {
                    type = NavType.IntType
                }
            )
        ) { backStackEntry ->

            val patientId =
                backStackEntry.arguments?.getInt("patientId") ?: 0

            PredictionScreen(
                patientId = patientId
            )
        }
    }
}