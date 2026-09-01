package com.ranjitha.cervicalcancerxai.ui.screens

import android.content.Context
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Checkbox
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
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavHostController
import java.security.MessageDigest

@Composable
fun LoginScreen(
    navController: NavHostController
) {
    var loginIdentifier by remember {
        mutableStateOf("")
    }

    var password by remember {
        mutableStateOf("")
    }

    var passwordVisible by remember {
        mutableStateOf(false)
    }

    var rememberMe by remember {
        mutableStateOf(false)
    }

    var loginIdentifierError by remember {
        mutableStateOf<String?>(null)
    }

    var passwordError by remember {
        mutableStateOf<String?>(null)
    }

    var loginError by remember {
        mutableStateOf<String?>(null)
    }

    val context = LocalContext.current
    val focusManager = LocalFocusManager.current
    val scrollState = rememberScrollState()

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

    fun hashPassword(value: String): String {
        val bytes = MessageDigest
            .getInstance("SHA-256")
            .digest(value.toByteArray(Charsets.UTF_8))

        return bytes.joinToString("") { byte ->
            "%02x".format(byte)
        }
    }

    fun validateAndLogin() {
        loginIdentifierError = null
        passwordError = null
        loginError = null

        val enteredLogin = loginIdentifier.trim()

        if (enteredLogin.isBlank()) {
            loginIdentifierError =
                "Please enter your username or email."
            return
        }

        if (password.isBlank()) {
            passwordError = "Please enter your password."
            return
        }

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

        val savedPasswordHash = preferences.getString(
            "password_hash",
            null
        )

        if (
            savedUsername == null ||
            savedEmail == null ||
            savedPasswordHash == null
        ) {
            loginError =
                "No account found. Please create an account first."
            return
        }

        val usernameMatches = savedUsername.equals(
            enteredLogin,
            ignoreCase = true
        )

        val emailMatches = savedEmail.equals(
            enteredLogin,
            ignoreCase = true
        )

        val enteredPasswordHash = hashPassword(password)
        val passwordMatches =
            savedPasswordHash == enteredPasswordHash

        if (
            (usernameMatches || emailMatches) &&
            passwordMatches
        ) {
            preferences.edit()
                .putBoolean(
                    "remember_me",
                    rememberMe
                )
                .putBoolean(
                    "is_logged_in",
                    rememberMe
                )
                .apply()

            navController.navigate("home") {
                popUpTo("login") {
                    inclusive = true
                }

                launchSingleTop = true
            }
        } else {
            loginError = "Incorrect username/email or password."
        }
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(backgroundGradient)
            .verticalScroll(scrollState)
            .padding(
                horizontal = 28.dp,
                vertical = 40.dp
            ),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Top
    ) {
        Spacer(modifier = Modifier.height(24.dp))

        Text(
            text = "CerviXAI",
            fontSize = 40.sp,
            fontWeight = FontWeight.Bold,
            color = Color(0xFF1257C7)
        )

        Spacer(modifier = Modifier.height(8.dp))

        Text(
            text = "Doctor / Hospital Staff Login",
            fontSize = 19.sp,
            fontWeight = FontWeight.Medium,
            color = Color(0xFF243B62),
            textAlign = TextAlign.Center
        )

        Spacer(modifier = Modifier.height(36.dp))

        OutlinedTextField(
            value = loginIdentifier,
            onValueChange = {
                loginIdentifier = it
                loginIdentifierError = null
                loginError = null
            },
            label = {
                Text("Username or Email")
            },
            placeholder = {
                Text("Enter your username or email")
            },
            singleLine = true,
            isError = loginIdentifierError != null,
            supportingText = {
                loginIdentifierError?.let { error ->
                    Text(
                        text = error,
                        color = MaterialTheme.colorScheme.error
                    )
                }
            },
            keyboardOptions = KeyboardOptions(
                keyboardType = KeyboardType.Email,
                imeAction = ImeAction.Next
            ),
            colors = fieldColors,
            modifier = Modifier.fillMaxWidth()
        )

        Spacer(modifier = Modifier.height(12.dp))

        OutlinedTextField(
            value = password,
            onValueChange = {
                password = it
                passwordError = null
                loginError = null
            },
            label = {
                Text("Password")
            },
            placeholder = {
                Text("Enter your password")
            },
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
                        text = if (passwordVisible) {
                            "HIDE"
                        } else {
                            "SHOW"
                        },
                        fontSize = 12.sp,
                        fontWeight = FontWeight.Bold
                    )
                }
            },
            supportingText = {
                passwordError?.let { error ->
                    Text(
                        text = error,
                        color = MaterialTheme.colorScheme.error
                    )
                }
            },
            keyboardOptions = KeyboardOptions(
                keyboardType = KeyboardType.Password,
                imeAction = ImeAction.Done
            ),
            keyboardActions = KeyboardActions(
                onDone = {
                    focusManager.clearFocus()
                    validateAndLogin()
                }
            ),
            colors = fieldColors,
            modifier = Modifier.fillMaxWidth()
        )

        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Checkbox(
                checked = rememberMe,
                onCheckedChange = {
                    rememberMe = it
                }
            )

            Text(
                text = "Remember me",
                fontSize = 14.sp,
                color = Color(0xFF334E76)
            )

            Spacer(modifier = Modifier.weight(1f))

            TextButton(
                onClick = {
                    navController.navigate("forgot_password")
                }
            ) {
                Text("Forgot password?")
            }
        }

        loginError?.let { error ->
            Spacer(modifier = Modifier.height(8.dp))

            Text(
                text = error,
                color = MaterialTheme.colorScheme.error,
                fontWeight = FontWeight.Medium,
                textAlign = TextAlign.Center
            )
        }

        Spacer(modifier = Modifier.height(18.dp))

        Button(
            onClick = {
                focusManager.clearFocus()
                validateAndLogin()
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
                text = "LOGIN",
                fontSize = 17.sp,
                fontWeight = FontWeight.Bold
            )
        }

        Spacer(modifier = Modifier.height(24.dp))

        Text(
            text = "New doctor or hospital staff member?",
            fontSize = 14.sp,
            color = Color(0xFF526A8F),
            textAlign = TextAlign.Center
        )

        TextButton(
            onClick = {
                navController.navigate("register") {
                    launchSingleTop = true
                }
            }
        ) {
            Text(
                text = "CREATE NEW ACCOUNT",
                fontSize = 16.sp,
                fontWeight = FontWeight.Bold,
                color = Color(0xFF1565D8)
            )
        }

        Spacer(modifier = Modifier.height(30.dp))
    }
}