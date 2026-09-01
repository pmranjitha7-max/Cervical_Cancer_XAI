package com.ranjitha.cervicalcancerxai.ui.screens

import android.content.Context
import android.util.Patterns
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavHostController
import java.security.MessageDigest


@Composable
fun ForgotPasswordScreen(
    navController: NavHostController
) {

    var email by remember {
        mutableStateOf("")
    }

    var newPassword by remember {
        mutableStateOf("")
    }

    var confirmPassword by remember {
        mutableStateOf("")
    }

    var newPasswordVisible by remember {
        mutableStateOf(false)
    }

    var confirmPasswordVisible by remember {
        mutableStateOf(false)
    }

    var emailVerified by remember {
        mutableStateOf(false)
    }

    var emailError by remember {
        mutableStateOf<String?>(null)
    }

    var newPasswordError by remember {
        mutableStateOf<String?>(null)
    }

    var confirmPasswordError by remember {
        mutableStateOf<String?>(null)
    }

    var successMessage by remember {
        mutableStateOf<String?>(null)
    }

    val context = LocalContext.current


    val backgroundGradient = Brush.verticalGradient(
        colors = listOf(
            Color(0xFFF9FCFF),
            Color(0xFFEAF4FF),
            Color(0xFFDCEBFF)
        )
    )


    val fieldColors = OutlinedTextFieldDefaults.colors(
        focusedTextColor = Color(0xFF102A4C),
        unfocusedTextColor = Color(0xFF102A4C),

        cursorColor = Color(0xFF1565D8),

        focusedBorderColor = Color(0xFF1565D8),
        unfocusedBorderColor = Color(0xFF7B8CA8),

        focusedLabelColor = Color(0xFF1565D8),
        unfocusedLabelColor = Color(0xFF526A8F)
    )


    fun hashPassword(value: String): String {

        val bytes = MessageDigest
            .getInstance("SHA-256")
            .digest(
                value.toByteArray()
            )

        return bytes.joinToString("") { byte ->
            "%02x".format(byte)
        }
    }


    fun isStrongPassword(
        value: String
    ): Boolean {

        val hasUppercase =
            value.any {
                it.isUpperCase()
            }

        val hasLowercase =
            value.any {
                it.isLowerCase()
            }

        val hasNumber =
            value.any {
                it.isDigit()
            }

        val hasSpecialCharacter =
            value.any {
                !it.isLetterOrDigit()
            }

        return (
                value.length >= 8 &&
                        hasUppercase &&
                        hasLowercase &&
                        hasNumber &&
                        hasSpecialCharacter
                )
    }


    fun verifyEmail() {

        emailError = null
        successMessage = null

        val enteredEmail =
            email.trim()

        if (
            !Patterns.EMAIL_ADDRESS
                .matcher(
                    enteredEmail
                )
                .matches()
        ) {

            emailError =
                "Enter a valid email address."

            return
        }


        val preferences =
            context.getSharedPreferences(
                "cervixai_auth",
                Context.MODE_PRIVATE
            )


        val savedEmail =
            preferences.getString(
                "email",
                null
            )


        if (
            savedEmail != null &&
            savedEmail.equals(
                enteredEmail,
                ignoreCase = true
            )
        ) {

            emailVerified = true

            successMessage =
                "Email verified. Create a new password."

        } else {

            emailVerified = false

            emailError =
                "No registered account found with this email."
        }
    }


    fun resetPassword() {

        newPasswordError = null
        confirmPasswordError = null
        successMessage = null


        if (
            !isStrongPassword(
                newPassword
            )
        ) {

            newPasswordError =
                "Use 8+ characters with uppercase, lowercase, number and special character."

            return
        }


        if (
            confirmPassword.isBlank()
        ) {

            confirmPasswordError =
                "Confirm your new password."

            return
        }


        if (
            newPassword != confirmPassword
        ) {

            confirmPasswordError =
                "Passwords do not match."

            return
        }


        val preferences =
            context.getSharedPreferences(
                "cervixai_auth",
                Context.MODE_PRIVATE
            )


        preferences.edit()
            .putString(
                "password_hash",
                hashPassword(
                    newPassword
                )
            )
            .putBoolean(
                "remember_me",
                false
            )
            .putBoolean(
                "is_logged_in",
                false
            )
            .apply()


        successMessage =
            "Password reset successfully."


        navController.navigate(
            "login"
        ) {

            popUpTo(
                "forgot_password"
            ) {
                inclusive = true
            }
        }
    }


    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(
                backgroundGradient
            )
            .verticalScroll(
                rememberScrollState()
            )
            .padding(
                horizontal = 26.dp,
                vertical = 40.dp
            ),

        horizontalAlignment =
            Alignment.CenterHorizontally,

        verticalArrangement =
            Arrangement.Top
    ) {


        Text(
            text = "Reset Password",
            fontSize = 34.sp,
            fontWeight = FontWeight.Bold,
            color = Color(0xFF1565D8)
        )


        Spacer(
            modifier =
                Modifier.height(8.dp)
        )


        Text(
            text =
                "Verify your registered email and create a new password.",
            fontSize = 16.sp,
            color = Color(0xFF243B62),
            textAlign = TextAlign.Center
        )


        Spacer(
            modifier =
                Modifier.height(28.dp)
        )


        OutlinedTextField(
            value = email,

            onValueChange = {

                email = it

                emailError = null

                if (emailVerified) {
                    emailVerified = false
                    newPassword = ""
                    confirmPassword = ""
                }
            },

            label = {
                Text(
                    "Registered Email"
                )
            },

            placeholder = {
                Text(
                    "Enter your registered email"
                )
            },

            singleLine = true,

            enabled = !emailVerified,

            isError =
                emailError != null,

            supportingText = {

                emailError?.let {

                    Text(
                        text = it,
                        color =
                            MaterialTheme
                                .colorScheme
                                .error
                    )
                }
            },

            keyboardOptions =
                KeyboardOptions(
                    keyboardType =
                        KeyboardType.Email
                ),

            colors =
                fieldColors,

            modifier =
                Modifier.fillMaxWidth()
        )


        Spacer(
            modifier =
                Modifier.height(12.dp)
        )


        if (!emailVerified) {

            Button(
                onClick = {
                    verifyEmail()
                },

                modifier =
                    Modifier
                        .fillMaxWidth()
                        .height(54.dp),

                shape =
                    RoundedCornerShape(
                        16.dp
                    ),

                colors =
                    ButtonDefaults
                        .buttonColors(
                            containerColor =
                                Color(
                                    0xFF1565D8
                                )
                        )
            ) {

                Text(
                    text = "VERIFY EMAIL",
                    fontSize = 16.sp,
                    fontWeight =
                        FontWeight.Bold
                )
            }
        }


        successMessage?.let {

            Spacer(
                modifier =
                    Modifier.height(14.dp)
            )

            Text(
                text = it,
                color =
                    Color(0xFF137A3F),

                fontWeight =
                    FontWeight.SemiBold,

                textAlign =
                    TextAlign.Center
            )
        }


        if (emailVerified) {

            Spacer(
                modifier =
                    Modifier.height(22.dp)
            )


            OutlinedTextField(
                value =
                    newPassword,

                onValueChange = {

                    newPassword = it
                    newPasswordError = null
                },

                label = {
                    Text(
                        "New Password"
                    )
                },

                placeholder = {
                    Text(
                        "Enter new password"
                    )
                },

                singleLine = true,

                isError =
                    newPasswordError != null,

                visualTransformation =
                    if (
                        newPasswordVisible
                    ) {

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
                                if (
                                    newPasswordVisible
                                ) {
                                    "HIDE"
                                } else {
                                    "SHOW"
                                },

                            fontSize =
                                12.sp,

                            fontWeight =
                                FontWeight.Bold
                        )
                    }
                },

                supportingText = {

                    if (
                        newPasswordError != null
                    ) {

                        Text(
                            text =
                                newPasswordError!!,

                            color =
                                MaterialTheme
                                    .colorScheme
                                    .error
                        )

                    } else {

                        Text(
                            text =
                                "Minimum 8 characters with uppercase, lowercase, number and special character.",

                            color =
                                Color(
                                    0xFF526A8F
                                )
                        )
                    }
                },

                keyboardOptions =
                    KeyboardOptions(
                        keyboardType =
                            KeyboardType.Password
                    ),

                colors =
                    fieldColors,

                modifier =
                    Modifier.fillMaxWidth()
            )


            Spacer(
                modifier =
                    Modifier.height(12.dp)
            )


            OutlinedTextField(
                value =
                    confirmPassword,

                onValueChange = {

                    confirmPassword = it
                    confirmPasswordError = null
                },

                label = {
                    Text(
                        "Confirm New Password"
                    )
                },

                placeholder = {
                    Text(
                        "Re-enter new password"
                    )
                },

                singleLine = true,

                isError =
                    confirmPasswordError != null,

                visualTransformation =
                    if (
                        confirmPasswordVisible
                    ) {

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
                                if (
                                    confirmPasswordVisible
                                ) {
                                    "HIDE"
                                } else {
                                    "SHOW"
                                },

                            fontSize =
                                12.sp,

                            fontWeight =
                                FontWeight.Bold
                        )
                    }
                },

                supportingText = {

                    confirmPasswordError
                        ?.let {

                            Text(
                                text = it,

                                color =
                                    MaterialTheme
                                        .colorScheme
                                        .error
                            )
                        }
                },

                keyboardOptions =
                    KeyboardOptions(
                        keyboardType =
                            KeyboardType.Password
                    ),

                colors =
                    fieldColors,

                modifier =
                    Modifier.fillMaxWidth()
            )


            Spacer(
                modifier =
                    Modifier.height(22.dp)
            )


            Button(
                onClick = {
                    resetPassword()
                },

                modifier =
                    Modifier
                        .fillMaxWidth()
                        .height(56.dp),

                shape =
                    RoundedCornerShape(
                        18.dp
                    ),

                colors =
                    ButtonDefaults
                        .buttonColors(
                            containerColor =
                                Color(
                                    0xFF1565D8
                                )
                        )
            ) {

                Text(
                    text = "RESET PASSWORD",
                    fontSize = 16.sp,
                    fontWeight =
                        FontWeight.Bold
                )
            }
        }


        Spacer(
            modifier =
                Modifier.height(18.dp)
        )


        TextButton(
            onClick = {

                navController
                    .popBackStack()
            }
        ) {

            Text(
                text = "Back to Login",
                fontSize = 15.sp,
                fontWeight =
                    FontWeight.Bold
            )
        }
    }
}