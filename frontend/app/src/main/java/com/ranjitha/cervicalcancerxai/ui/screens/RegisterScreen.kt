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
import androidx.compose.runtime.rememberCoroutineScope
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
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import java.security.MessageDigest

@Composable
fun RegisterScreen(
    navController: NavHostController
) {
    var fullName by remember { mutableStateOf("") }
    var username by remember { mutableStateOf("") }
    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var confirmPassword by remember { mutableStateOf("") }

    var passwordVisible by remember { mutableStateOf(false) }
    var confirmPasswordVisible by remember { mutableStateOf(false) }

    var fullNameError by remember { mutableStateOf<String?>(null) }
    var usernameError by remember { mutableStateOf<String?>(null) }
    var emailError by remember { mutableStateOf<String?>(null) }
    var passwordError by remember { mutableStateOf<String?>(null) }
    var confirmPasswordError by remember { mutableStateOf<String?>(null) }

    var registrationMessage by remember { mutableStateOf<String?>(null) }

    val context = LocalContext.current
    val coroutineScope = rememberCoroutineScope()

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
        unfocusedLabelColor = Color(0xFF526A8F),
        focusedPlaceholderColor = Color(0xFF8A97AA),
        unfocusedPlaceholderColor = Color(0xFF8A97AA)
    )

    fun isStrongPassword(value: String): Boolean {
        val hasUppercase = value.any { it.isUpperCase() }
        val hasLowercase = value.any { it.isLowerCase() }
        val hasNumber = value.any { it.isDigit() }
        val hasSpecialCharacter = value.any { !it.isLetterOrDigit() }

        return value.length >= 8 &&
                hasUppercase &&
                hasLowercase &&
                hasNumber &&
                hasSpecialCharacter
    }

    fun hashPassword(value: String): String {
        val bytes = MessageDigest
            .getInstance("SHA-256")
            .digest(value.toByteArray())

        return bytes.joinToString("") { byte ->
            "%02x".format(byte)
        }
    }

    fun validateRegistration(): Boolean {
        fullNameError = null
        usernameError = null
        emailError = null
        passwordError = null
        confirmPasswordError = null
        registrationMessage = null

        var isValid = true

        if (fullName.trim().length < 3) {
            fullNameError = "Enter your full name."
            isValid = false
        }

        if (username.trim().length < 4) {
            usernameError = "Username must contain at least 4 characters."
            isValid = false
        }

        if (!Patterns.EMAIL_ADDRESS.matcher(email.trim()).matches()) {
            emailError = "Enter a valid email address."
            isValid = false
        }

        if (!isStrongPassword(password)) {
            passwordError =
                "Use 8+ characters with uppercase, lowercase, number and special character."
            isValid = false
        }

        if (confirmPassword.isBlank()) {
            confirmPasswordError = "Confirm your password."
            isValid = false
        } else if (password != confirmPassword) {
            confirmPasswordError = "Passwords do not match."
            isValid = false
        }

        return isValid
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(backgroundGradient)
            .verticalScroll(rememberScrollState())
            .padding(horizontal = 26.dp, vertical = 40.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Top
    ) {
        Text(
            text = "Create Account",
            fontSize = 34.sp,
            fontWeight = FontWeight.Bold,
            color = Color(0xFF1565D8)
        )

        Spacer(modifier = Modifier.height(8.dp))

        Text(
            text = "Doctor / Hospital Staff Registration",
            fontSize = 17.sp,
            fontWeight = FontWeight.Medium,
            color = Color(0xFF243B62),
            textAlign = TextAlign.Center
        )

        Spacer(modifier = Modifier.height(28.dp))

        OutlinedTextField(
            value = fullName,
            onValueChange = {
                fullName = it
                fullNameError = null
            },
            label = { Text("Full Name") },
            placeholder = { Text("Enter your full name") },
            singleLine = true,
            isError = fullNameError != null,
            supportingText = {
                fullNameError?.let {
                    Text(it, color = MaterialTheme.colorScheme.error)
                }
            },
            colors = fieldColors,
            modifier = Modifier.fillMaxWidth()
        )

        Spacer(modifier = Modifier.height(10.dp))

        OutlinedTextField(
            value = username,
            onValueChange = {
                username = it
                usernameError = null
            },
            label = { Text("Username") },
            placeholder = { Text("Create a username") },
            singleLine = true,
            isError = usernameError != null,
            supportingText = {
                usernameError?.let {
                    Text(it, color = MaterialTheme.colorScheme.error)
                }
            },
            keyboardOptions = KeyboardOptions(
                keyboardType = KeyboardType.Text
            ),
            colors = fieldColors,
            modifier = Modifier.fillMaxWidth()
        )

        Spacer(modifier = Modifier.height(10.dp))

        OutlinedTextField(
            value = email,
            onValueChange = {
                email = it
                emailError = null
            },
            label = { Text("Email ID") },
            placeholder = { Text("Enter your email address") },
            singleLine = true,
            isError = emailError != null,
            supportingText = {
                emailError?.let {
                    Text(it, color = MaterialTheme.colorScheme.error)
                }
            },
            keyboardOptions = KeyboardOptions(
                keyboardType = KeyboardType.Email
            ),
            colors = fieldColors,
            modifier = Modifier.fillMaxWidth()
        )

        Spacer(modifier = Modifier.height(10.dp))

        OutlinedTextField(
            value = password,
            onValueChange = {
                password = it
                passwordError = null
            },
            label = { Text("Password") },
            placeholder = { Text("Create a strong password") },
            singleLine = true,
            isError = passwordError != null,
            visualTransformation = if (passwordVisible) {
                VisualTransformation.None
            } else {
                PasswordVisualTransformation()
            },
            trailingIcon = {
                TextButton(
                    onClick = {
                        passwordVisible = !passwordVisible
                    }
                ) {
                    Text(
                        text = if (passwordVisible) "HIDE" else "SHOW",
                        fontSize = 12.sp,
                        fontWeight = FontWeight.Bold
                    )
                }
            },
            supportingText = {
                if (passwordError != null) {
                    Text(
                        text = passwordError!!,
                        color = MaterialTheme.colorScheme.error
                    )
                } else {
                    Text(
                        text = "Minimum 8 characters, uppercase, lowercase, number and special character.",
                        color = Color(0xFF526A8F)
                    )
                }
            },
            keyboardOptions = KeyboardOptions(
                keyboardType = KeyboardType.Password
            ),
            colors = fieldColors,
            modifier = Modifier.fillMaxWidth()
        )

        Spacer(modifier = Modifier.height(10.dp))

        OutlinedTextField(
            value = confirmPassword,
            onValueChange = {
                confirmPassword = it
                confirmPasswordError = null
            },
            label = { Text("Confirm Password") },
            placeholder = { Text("Re-enter your password") },
            singleLine = true,
            isError = confirmPasswordError != null,
            visualTransformation = if (confirmPasswordVisible) {
                VisualTransformation.None
            } else {
                PasswordVisualTransformation()
            },
            trailingIcon = {
                TextButton(
                    onClick = {
                        confirmPasswordVisible = !confirmPasswordVisible
                    }
                ) {
                    Text(
                        text = if (confirmPasswordVisible) "HIDE" else "SHOW",
                        fontSize = 12.sp,
                        fontWeight = FontWeight.Bold
                    )
                }
            },
            supportingText = {
                confirmPasswordError?.let {
                    Text(it, color = MaterialTheme.colorScheme.error)
                }
            },
            keyboardOptions = KeyboardOptions(
                keyboardType = KeyboardType.Password
            ),
            colors = fieldColors,
            modifier = Modifier.fillMaxWidth()
        )

        registrationMessage?.let {
            Spacer(modifier = Modifier.height(12.dp))

            Text(
                text = it,
                color = Color(0xFF137A3F),
                fontWeight = FontWeight.SemiBold,
                textAlign = TextAlign.Center
            )
        }

        Spacer(modifier = Modifier.height(22.dp))

        Button(
            onClick = {
                if (validateRegistration()) {
                    val preferences = context.getSharedPreferences(
                        "cervixai_auth",
                        Context.MODE_PRIVATE
                    )

                    val savedUsername = preferences.getString(
                        "username",
                        null
                    )

                    val savedEmail = preferences.getString(
                        "email",
                        null
                    )

                    when {
                        savedUsername.equals(
                            username.trim(),
                            ignoreCase = true
                        ) -> {
                            usernameError = "This username already exists."
                        }

                        savedEmail.equals(
                            email.trim(),
                            ignoreCase = true
                        ) -> {
                            emailError =
                                "An account already exists with this email."
                        }

                        else -> {
                            preferences.edit()
                                .putString(
                                    "full_name",
                                    fullName.trim()
                                )
                                .putString(
                                    "username",
                                    username.trim()
                                )
                                .putString(
                                    "email",
                                    email.trim()
                                )
                                .putString(
                                    "password_hash",
                                    hashPassword(password)
                                )
                                .apply()

                            registrationMessage =
                                "Account created successfully."

                            coroutineScope.launch {
                                delay(1500)

                                navController.navigate("login") {
                                    popUpTo("register") {
                                        inclusive = true
                                    }
                                }
                            }
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
                text = "CREATE ACCOUNT",
                fontSize = 16.sp,
                fontWeight = FontWeight.Bold
            )
        }

        Spacer(modifier = Modifier.height(12.dp))

        TextButton(
            onClick = {
                navController.popBackStack()
            }
        ) {
            Text(
                text = "Already have an account? Login",
                fontSize = 15.sp,
                fontWeight = FontWeight.Bold
            )
        }

        Spacer(modifier = Modifier.height(30.dp))
    }
}