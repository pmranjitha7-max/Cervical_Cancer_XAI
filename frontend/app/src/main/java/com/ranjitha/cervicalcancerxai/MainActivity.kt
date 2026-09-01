package com.ranjitha.cervicalcancerxai

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import com.ranjitha.cervicalcancerxai.ui.navigation.AppNavigation
import com.ranjitha.cervicalcancerxai.ui.theme.CervicalCancerXAITheme

class MainActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContent {
            CervicalCancerXAITheme {
                AppNavigation()
            }
        }
    }
}