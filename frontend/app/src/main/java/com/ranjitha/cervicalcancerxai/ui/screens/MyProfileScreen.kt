package com.ranjitha.cervicalcancerxai.ui.screens

import android.content.Context
import android.net.Uri
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavHostController
import coil3.compose.rememberAsyncImagePainter

@Composable
fun MyProfileScreen(
    navController: NavHostController
) {
    val context = LocalContext.current

    val preferences = context.getSharedPreferences(
        "cervixai_auth",
        Context.MODE_PRIVATE
    )

    var fullName by remember {
        mutableStateOf(
            preferences.getString("full_name", "") ?: ""
        )
    }

    var username by remember {
        mutableStateOf(
            preferences.getString("username", "") ?: ""
        )
    }

    var email by remember {
        mutableStateOf(
            preferences.getString("email", "") ?: ""
        )
    }

    var phone by remember {
        mutableStateOf(
            preferences.getString("phone", "") ?: ""
        )
    }

    var age by remember {
        mutableStateOf(
            preferences.getString("age", "") ?: ""
        )
    }

    var gender by remember {
        mutableStateOf(
            preferences.getString("gender", "") ?: ""
        )
    }

    var dateOfBirth by remember {
        mutableStateOf(
            preferences.getString("date_of_birth", "") ?: ""
        )
    }

    var bloodGroup by remember {
        mutableStateOf(
            preferences.getString("blood_group", "") ?: ""
        )
    }

    var role by remember {
        mutableStateOf(
            preferences.getString(
                "role",
                "Doctor / Healthcare Professional"
            ) ?: "Doctor / Healthcare Professional"
        )
    }

    var specialization by remember {
        mutableStateOf(
            preferences.getString("specialization", "") ?: ""
        )
    }

    var qualification by remember {
        mutableStateOf(
            preferences.getString("qualification", "") ?: ""
        )
    }

    var hospital by remember {
        mutableStateOf(
            preferences.getString("hospital", "") ?: ""
        )
    }

    var registrationNumber by remember {
        mutableStateOf(
            preferences.getString("registration_number", "") ?: ""
        )
    }

    var experience by remember {
        mutableStateOf(
            preferences.getString("experience", "") ?: ""
        )
    }

    var city by remember {
        mutableStateOf(
            preferences.getString("city", "") ?: ""
        )
    }

    var country by remember {
        mutableStateOf(
            preferences.getString("country", "") ?: ""
        )
    }

    var bio by remember {
        mutableStateOf(
            preferences.getString("bio", "") ?: ""
        )
    }

    var profileImageUri by remember {
        mutableStateOf(
            preferences.getString("profile_image_uri", null)
        )
    }

    var isEditing by remember {
        mutableStateOf(false)
    }

    var message by remember {
        mutableStateOf<String?>(null)
    }

    val imagePickerLauncher =
        rememberLauncherForActivityResult(
            contract = ActivityResultContracts.GetContent()
        ) { uri: Uri? ->

            if (uri != null) {
                profileImageUri = uri.toString()

                preferences.edit()
                    .putString(
                        "profile_image_uri",
                        uri.toString()
                    )
                    .apply()
            }
        }

    val backgroundGradient = Brush.verticalGradient(
        colors = listOf(
            Color(0xFFF9FCFF),
            Color(0xFFEFF6FF),
            Color(0xFFE5F0FF)
        )
    )

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(backgroundGradient)
            .verticalScroll(rememberScrollState())
            .padding(horizontal = 20.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {

        Spacer(modifier = Modifier.height(20.dp))

        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            TextButton(
                onClick = {
                    if (isEditing) {
                        isEditing = false
                    } else {
                        navController.popBackStack()
                    }
                }
            ) {
                Text(
                    text = "← Back",
                    fontSize = 16.sp
                )
            }

            Spacer(modifier = Modifier.weight(1f))
        }

        Text(
            text = if (isEditing) {
                "Edit Profile"
            } else {
                "My Profile"
            },
            fontSize = 32.sp,
            fontWeight = FontWeight.Bold,
            color = Color(0xFF1565D8)
        )

        Spacer(modifier = Modifier.height(22.dp))

        if (profileImageUri != null) {
            Image(
                painter = rememberAsyncImagePainter(
                    model = profileImageUri
                ),
                contentDescription = "Profile Photo",
                modifier = Modifier
                    .size(130.dp)
                    .clip(CircleShape),
                contentScale = ContentScale.Crop
            )
        } else {
            Surface(
                modifier = Modifier.size(130.dp),
                shape = CircleShape,
                color = Color(0xFFDCEBFF)
            ) {
                Box(
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = "👤",
                        fontSize = 70.sp
                    )
                }
            }
        }

        Spacer(modifier = Modifier.height(12.dp))

        if (!isEditing) {
            Text(
                text = fullName.ifBlank { "Doctor" },
                fontSize = 24.sp,
                fontWeight = FontWeight.Bold,
                color = Color(0xFF173A68)
            )

            Spacer(modifier = Modifier.height(4.dp))

            Text(
                text = if (username.isBlank()) {
                    "@username"
                } else {
                    "@$username"
                },
                fontSize = 15.sp,
                color = Color(0xFF6B7F9E)
            )

            Spacer(modifier = Modifier.height(4.dp))

            Text(
                text = role,
                fontSize = 16.sp,
                fontWeight = FontWeight.Medium,
                color = Color(0xFF1565D8)
            )
        }

        Spacer(modifier = Modifier.height(24.dp))

        if (!isEditing) {

            ProfileSectionCard(
                title = "Personal Information"
            ) {
                ProfileInfoRow(
                    label = "Full Name",
                    value = fullName
                )

                ProfileInfoRow(
                    label = "Username",
                    value = username
                )

                ProfileInfoRow(
                    label = "Email",
                    value = email
                )

                ProfileInfoRow(
                    label = "Phone Number",
                    value = phone
                )

                ProfileInfoRow(
                    label = "Age",
                    value = age
                )

                ProfileInfoRow(
                    label = "Gender",
                    value = gender
                )

                ProfileInfoRow(
                    label = "Date of Birth",
                    value = dateOfBirth
                )

                ProfileInfoRow(
                    label = "Blood Group",
                    value = bloodGroup
                )
            }

            Spacer(modifier = Modifier.height(16.dp))

            ProfileSectionCard(
                title = "Professional Information"
            ) {
                ProfileInfoRow(
                    label = "Role",
                    value = role
                )

                ProfileInfoRow(
                    label = "Specialization",
                    value = specialization
                )

                ProfileInfoRow(
                    label = "Qualification",
                    value = qualification
                )

                ProfileInfoRow(
                    label = "Hospital / Clinic",
                    value = hospital
                )

                ProfileInfoRow(
                    label = "Medical Registration No.",
                    value = registrationNumber
                )

                ProfileInfoRow(
                    label = "Years of Experience",
                    value = experience
                )

                ProfileInfoRow(
                    label = "City",
                    value = city
                )

                ProfileInfoRow(
                    label = "Country",
                    value = country
                )
            }

            Spacer(modifier = Modifier.height(16.dp))

            ProfileSectionCard(
                title = "About Me"
            ) {
                Text(
                    text = bio.ifBlank {
                        "Not added"
                    },
                    fontSize = 15.sp,
                    color = Color(0xFF526A8F),
                    lineHeight = 22.sp
                )
            }

            Spacer(modifier = Modifier.height(16.dp))

            ProfileSectionCard(
                title = "Account Settings"
            ) {

                ProfileActionRow(
                    title = "✏️  Edit Profile"
                ) {
                    message = null
                    isEditing = true
                }

                HorizontalDivider()

                ProfileActionRow(
                    title = "🔒  Change Password"
                ) {
                    navController.navigate("changePassword")
                }

                HorizontalDivider()

                ProfileActionRow(
                    title = "📷  Change Profile Photo"
                ) {
                    imagePickerLauncher.launch("image/*")
                }
            }

        } else {

            Text(
                text = "Personal Information",
                fontSize = 20.sp,
                fontWeight = FontWeight.Bold,
                color = Color(0xFF173A68),
                modifier = Modifier.fillMaxWidth()
            )

            Spacer(modifier = Modifier.height(14.dp))

            ProfileEditField(
                label = "Full Name",
                value = fullName,
                onValueChange = {
                    fullName = it
                }
            )

            ProfileEditField(
                label = "Username",
                value = username,
                onValueChange = {
                    username = it
                }
            )

            ProfileEditField(
                label = "Email ID",
                value = email,
                onValueChange = {
                    email = it
                }
            )

            ProfileEditField(
                label = "Phone Number",
                value = phone,
                onValueChange = {
                    phone = it
                }
            )

            ProfileEditField(
                label = "Age",
                value = age,
                onValueChange = {
                    age = it
                }
            )

            ProfileEditField(
                label = "Gender",
                value = gender,
                onValueChange = {
                    gender = it
                }
            )

            ProfileEditField(
                label = "Date of Birth",
                value = dateOfBirth,
                onValueChange = {
                    dateOfBirth = it
                }
            )

            ProfileEditField(
                label = "Blood Group",
                value = bloodGroup,
                onValueChange = {
                    bloodGroup = it
                }
            )

            Spacer(modifier = Modifier.height(22.dp))

            Text(
                text = "Professional Information",
                fontSize = 20.sp,
                fontWeight = FontWeight.Bold,
                color = Color(0xFF173A68),
                modifier = Modifier.fillMaxWidth()
            )

            Spacer(modifier = Modifier.height(14.dp))

            ProfileEditField(
                label = "Role",
                value = role,
                onValueChange = {
                    role = it
                }
            )

            ProfileEditField(
                label = "Specialization",
                value = specialization,
                onValueChange = {
                    specialization = it
                }
            )

            ProfileEditField(
                label = "Qualification",
                value = qualification,
                onValueChange = {
                    qualification = it
                }
            )

            ProfileEditField(
                label = "Hospital / Clinic",
                value = hospital,
                onValueChange = {
                    hospital = it
                }
            )

            ProfileEditField(
                label = "Medical Registration Number",
                value = registrationNumber,
                onValueChange = {
                    registrationNumber = it
                }
            )

            ProfileEditField(
                label = "Years of Experience",
                value = experience,
                onValueChange = {
                    experience = it
                }
            )

            ProfileEditField(
                label = "City",
                value = city,
                onValueChange = {
                    city = it
                }
            )

            ProfileEditField(
                label = "Country",
                value = country,
                onValueChange = {
                    country = it
                }
            )

            Spacer(modifier = Modifier.height(22.dp))

            Text(
                text = "About Me",
                fontSize = 20.sp,
                fontWeight = FontWeight.Bold,
                color = Color(0xFF173A68),
                modifier = Modifier.fillMaxWidth()
            )

            Spacer(modifier = Modifier.height(14.dp))

            OutlinedTextField(
                value = bio,
                onValueChange = {
                    bio = it
                },
                label = {
                    Text("Professional Bio")
                },
                minLines = 4,
                maxLines = 6,
                modifier = Modifier.fillMaxWidth()
            )

            Spacer(modifier = Modifier.height(26.dp))

            Button(
                onClick = {

                    if (
                        fullName.isBlank() ||
                        username.isBlank() ||
                        email.isBlank()
                    ) {
                        message =
                            "Full name, username and email are required."
                    } else {

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
                                "phone",
                                phone.trim()
                            )
                            .putString(
                                "age",
                                age.trim()
                            )
                            .putString(
                                "gender",
                                gender.trim()
                            )
                            .putString(
                                "date_of_birth",
                                dateOfBirth.trim()
                            )
                            .putString(
                                "blood_group",
                                bloodGroup.trim()
                            )
                            .putString(
                                "role",
                                role.trim()
                            )
                            .putString(
                                "specialization",
                                specialization.trim()
                            )
                            .putString(
                                "qualification",
                                qualification.trim()
                            )
                            .putString(
                                "hospital",
                                hospital.trim()
                            )
                            .putString(
                                "registration_number",
                                registrationNumber.trim()
                            )
                            .putString(
                                "experience",
                                experience.trim()
                            )
                            .putString(
                                "city",
                                city.trim()
                            )
                            .putString(
                                "country",
                                country.trim()
                            )
                            .putString(
                                "bio",
                                bio.trim()
                            )
                            .apply()

                        isEditing = false

                        message =
                            "Profile updated successfully."
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
                    text = "SAVE CHANGES",
                    fontSize = 16.sp,
                    fontWeight = FontWeight.Bold
                )
            }

            Spacer(modifier = Modifier.height(12.dp))

            OutlinedButton(
                onClick = {
                    fullName =
                        preferences.getString(
                            "full_name",
                            ""
                        ) ?: ""

                    username =
                        preferences.getString(
                            "username",
                            ""
                        ) ?: ""

                    email =
                        preferences.getString(
                            "email",
                            ""
                        ) ?: ""

                    phone =
                        preferences.getString(
                            "phone",
                            ""
                        ) ?: ""

                    age =
                        preferences.getString(
                            "age",
                            ""
                        ) ?: ""

                    gender =
                        preferences.getString(
                            "gender",
                            ""
                        ) ?: ""

                    dateOfBirth =
                        preferences.getString(
                            "date_of_birth",
                            ""
                        ) ?: ""

                    bloodGroup =
                        preferences.getString(
                            "blood_group",
                            ""
                        ) ?: ""

                    role =
                        preferences.getString(
                            "role",
                            "Doctor / Healthcare Professional"
                        ) ?: "Doctor / Healthcare Professional"

                    specialization =
                        preferences.getString(
                            "specialization",
                            ""
                        ) ?: ""

                    qualification =
                        preferences.getString(
                            "qualification",
                            ""
                        ) ?: ""

                    hospital =
                        preferences.getString(
                            "hospital",
                            ""
                        ) ?: ""

                    registrationNumber =
                        preferences.getString(
                            "registration_number",
                            ""
                        ) ?: ""

                    experience =
                        preferences.getString(
                            "experience",
                            ""
                        ) ?: ""

                    city =
                        preferences.getString(
                            "city",
                            ""
                        ) ?: ""

                    country =
                        preferences.getString(
                            "country",
                            ""
                        ) ?: ""

                    bio =
                        preferences.getString(
                            "bio",
                            ""
                        ) ?: ""

                    isEditing = false
                    message = null
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(54.dp)
            ) {
                Text(
                    text = "CANCEL"
                )
            }
        }

        message?.let {
            Spacer(modifier = Modifier.height(16.dp))

            Text(
                text = it,
                color = Color(0xFF137A3F),
                fontWeight = FontWeight.SemiBold,
                textAlign = TextAlign.Center
            )
        }

        Spacer(modifier = Modifier.height(40.dp))
    }
}

@Composable
fun ProfileSectionCard(
    title: String,
    content: @Composable () -> Unit
) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(18.dp),
        colors = CardDefaults.cardColors(
            containerColor = Color.White
        ),
        elevation = CardDefaults.cardElevation(
            defaultElevation = 4.dp
        )
    ) {
        Column(
            modifier = Modifier.padding(18.dp)
        ) {
            Text(
                text = title,
                fontSize = 19.sp,
                fontWeight = FontWeight.Bold,
                color = Color(0xFF173A68)
            )

            Spacer(modifier = Modifier.height(14.dp))

            content()
        }
    }
}

@Composable
fun ProfileInfoRow(
    label: String,
    value: String
) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 8.dp)
    ) {
        Text(
            text = label,
            fontSize = 13.sp,
            color = Color(0xFF7B8CA8)
        )

        Spacer(modifier = Modifier.height(3.dp))

        Text(
            text = value.ifBlank {
                "Not added"
            },
            fontSize = 16.sp,
            fontWeight = FontWeight.Medium,
            color = Color(0xFF243B62)
        )
    }
}

@Composable
fun ProfileActionRow(
    title: String,
    onClick: () -> Unit
) {
    TextButton(
        onClick = onClick,
        modifier = Modifier.fillMaxWidth()
    ) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = title,
                fontSize = 16.sp,
                fontWeight = FontWeight.Medium,
                color = Color(0xFF243B62)
            )

            Spacer(modifier = Modifier.weight(1f))

            Text(
                text = "›",
                fontSize = 26.sp,
                color = Color(0xFF1565D8)
            )
        }
    }
}

@Composable
fun ProfileEditField(
    label: String,
    value: String,
    onValueChange: (String) -> Unit
) {
    OutlinedTextField(
        value = value,
        onValueChange = onValueChange,
        label = {
            Text(label)
        },
        singleLine = true,
        modifier = Modifier
            .fillMaxWidth()
            .padding(bottom = 12.dp)
    )
}