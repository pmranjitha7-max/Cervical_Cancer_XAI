package com.ranjitha.cervicalcancerxai.ui.screens

import android.content.Context
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavHostController
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import java.security.MessageDigest

@Composable
fun ChangePasswordScreen(
    navController: NavHostController
) {

    val context = LocalContext.current

    val preferences = context.getSharedPreferences(
        "cervixai_auth",
        Context.MODE_PRIVATE
    )

    val coroutineScope = rememberCoroutineScope()

    var currentPassword by remember {
        mutableStateOf("")
    }

    var newPassword by remember {
        mutableStateOf("")
    }

    var confirmPassword by remember {
        mutableStateOf("")
    }

    var currentPasswordVisible by remember {
        mutableStateOf(false)
    }

    var newPasswordVisible by remember {
        mutableStateOf(false)
    }

    var confirmPasswordVisible by remember {
        mutableStateOf(false)
    }

    var errorMessage by remember {
        mutableStateOf<String?>(null)
    }

    var successMessage by remember {
        mutableStateOf<String?>(null)
    }

    val backgroundGradient = Brush.verticalGradient(
        colors = listOf(
            Color(0xFFF9FCFF),
            Color(0xFFEFF6FF),
            Color(0xFFE5F0FF)
        )
    )

    val fieldColors = OutlinedTextFieldDefaults.colors(
        focusedTextColor = Color(0xFF102A4C),
        unfocusedTextColor = Color(0xFF102A4C),

        focusedContainerColor = Color.White,
        unfocusedContainerColor = Color.White,

        cursorColor = Color(0xFF1565D8),

        focusedBorderColor = Color(0xFF1565D8),
        unfocusedBorderColor = Color(0xFF7B8CA8),

        focusedLabelColor = Color(0xFF1565D8),
        unfocusedLabelColor = Color(0xFF526A8F)
    )

    fun hashPassword(password: String): String {

        val bytes = MessageDigest
            .getInstance("SHA-256")
            .digest(password.toByteArray())

        return bytes.joinToString("") { byte ->
            "%02x".format(byte)
        }
    }

    fun isStrongPassword(password: String): Boolean {

        val hasUppercase =
            password.any { it.isUpperCase() }

        val hasLowercase =
            password.any { it.isLowerCase() }

        val hasNumber =
            password.any { it.isDigit() }

        val hasSpecialCharacter =
            password.any { !it.isLetterOrDigit() }

        return password.length >= 8 &&
                hasUppercase &&
                hasLowercase &&
                hasNumber &&
                hasSpecialCharacter
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(backgroundGradient)
            .padding(horizontal = 24.dp)
    ) {

        Spacer(
            modifier = Modifier.height(28.dp)
        )

        TextButton(
            onClick = {
                navController.popBackStack()
            }
        ) {
            Text(
                text = "← Back",
                color = Color(0xFF1565D8),
                fontSize = 16.sp
            )
        }

        Spacer(
            modifier = Modifier.height(18.dp)
        )

        Text(
            text = "Change Password",
            fontSize = 32.sp,
            fontWeight = FontWeight.Bold,
            color = Color(0xFF173A68)
        )

        Spacer(
            modifier = Modifier.height(8.dp)
        )

        Text(
            text = "Keep your CerviXAI account secure by updating your password.",
            fontSize = 15.sp,
            color = Color(0xFF526A8F),
            lineHeight = 21.sp
        )

        Spacer(
            modifier = Modifier.height(32.dp)
        )

        OutlinedTextField(
            value = currentPassword,
            onValueChange = {
                currentPassword = it
                errorMessage = null
            },
            label = {
                Text("Current Password")
            },
            singleLine = true,
            colors = fieldColors,
            visualTransformation =
                if (currentPasswordVisible) {
                    VisualTransformation.None
                } else {
                    PasswordVisualTransformation()
                },
            trailingIcon = {

                TextButton(
                    onClick = {
                        currentPasswordVisible =
                            !currentPasswordVisible
                    }
                ) {
                    Text(
                        text =
                            if (currentPasswordVisible) {
                                "HIDE"
                            } else {
                                "SHOW"
                            },
                        color = Color(0xFF1565D8),
                        fontWeight = FontWeight.Bold
                    )
                }
            },
            modifier = Modifier.fillMaxWidth()
        )

        Spacer(
            modifier = Modifier.height(18.dp)
        )

        OutlinedTextField(
            value = newPassword,
            onValueChange = {
                newPassword = it
                errorMessage = null
            },
            label = {
                Text("New Password")
            },
            singleLine = true,
            colors = fieldColors,
            visualTransformation =
                if (newPasswordVisible) {
                    VisualTransformation.None
                } else {
                    PasswordVisualTransformation()
                },
            trailingIcon = {

                TextButton(
                    onClick = {
                        newPasswordVisible =
                            !newPasswordVisible
                    }
                ) {
                    Text(
                        text =
                            if (newPasswordVisible) {
                                "HIDE"
                            } else {
                                "SHOW"
                            },
                        color = Color(0xFF1565D8),
                        fontWeight = FontWeight.Bold
                    )
                }
            },
            modifier = Modifier.fillMaxWidth()
        )

        Spacer(
            modifier = Modifier.height(8.dp)
        )

        Text(
            text = "Use at least 8 characters with uppercase, lowercase, number and special character.",
            fontSize = 13.sp,
            color = Color(0xFF526A8F)
        )

        Spacer(
            modifier = Modifier.height(18.dp)
        )

        OutlinedTextField(
            value = confirmPassword,
            onValueChange = {
                confirmPassword = it
                errorMessage = null
            },
            label = {
                Text("Confirm New Password")
            },
            singleLine = true,
            colors = fieldColors,
            visualTransformation =
                if (confirmPasswordVisible) {
                    VisualTransformation.None
                } else {
                    PasswordVisualTransformation()
                },
            trailingIcon = {

                TextButton(
                    onClick = {
                        confirmPasswordVisible =
                            !confirmPasswordVisible
                    }
                ) {
                    Text(
                        text =
                            if (confirmPasswordVisible) {
                                "HIDE"
                            } else {
                                "SHOW"
                            },
                        color = Color(0xFF1565D8),
                        fontWeight = FontWeight.Bold
                    )
                }
            },
            modifier = Modifier.fillMaxWidth()
        )

        errorMessage?.let {

            Spacer(
                modifier = Modifier.height(16.dp)
            )

            Text(
                text = it,
                color = Color(0xFFB3261E),
                fontWeight = FontWeight.Medium
            )
        }

        successMessage?.let {

            Spacer(
                modifier = Modifier.height(16.dp)
            )

            Text(
                text = it,
                color = Color(0xFF137A3F),
                fontWeight = FontWeight.Bold
            )
        }

        Spacer(
            modifier = Modifier.height(30.dp)
        )

        Button(
            onClick = {

                errorMessage = null
                successMessage = null

                val savedPasswordHash =
                    preferences.getString(
                        "password_hash",
                        null
                    )

                when {

                    currentPassword.isBlank() -> {
                        errorMessage =
                            "Please enter your current password."
                    }

                    newPassword.isBlank() -> {
                        errorMessage =
                            "Please enter a new password."
                    }

                    confirmPassword.isBlank() -> {
                        errorMessage =
                            "Please confirm your new password."
                    }

                    savedPasswordHash == null -> {
                        errorMessage =
                            "Password information was not found."
                    }

                    hashPassword(currentPassword)
                            != savedPasswordHash -> {

                        errorMessage =
                            "Current password is incorrect."
                    }

                    !isStrongPassword(newPassword) -> {

                        errorMessage =
                            "New password must contain at least 8 characters, uppercase, lowercase, number and special character."
                    }

                    newPassword != confirmPassword -> {

                        errorMessage =
                            "New password and confirm password do not match."
                    }

                    hashPassword(newPassword)
                            == savedPasswordHash -> {

                        errorMessage =
                            "New password cannot be the same as your current password."
                    }

                    else -> {

                        preferences.edit()
                            .putString(
                                "password_hash",
                                hashPassword(newPassword)
                            )
                            .apply()

                        currentPassword = ""
                        newPassword = ""
                        confirmPassword = ""

                        successMessage =
                            "Password updated successfully."

                        coroutineScope.launch {

                            delay(1500)

                            navController.popBackStack()
                        }
                    }
                }
            },
            modifier = Modifier
                .fillMaxWidth()
                .height(56.dp),
            shape = RoundedCornerShape(18.dp),
            colors = ButtonDefaults.buttonColors(
                containerColor = Color(0xFF1565D8)
            )
        ) {

            Text(
                text = "UPDATE PASSWORD",
                fontSize = 16.sp,
                fontWeight = FontWeight.Bold,
                color = Color.White
            )
        }

        Spacer(
            modifier = Modifier.height(14.dp)
        )

        OutlinedButton(
            onClick = {
                navController.popBackStack()
            },
            modifier = Modifier
                .fillMaxWidth()
                .height(54.dp),
            shape = RoundedCornerShape(18.dp)
        ) {

            Text(
                text = "CANCEL",
                color = Color(0xFF1565D8),
                fontWeight = FontWeight.Bold
            )
        }
    }
}