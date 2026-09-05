import 'package:flutter/material.dart';

import 'theme.dart';
import 'screens/splash_screen.dart';
import 'screens/login_screen.dart';
import 'screens/register_screen.dart';
import 'screens/forgot_password_screen.dart';
import 'screens/shell_screen.dart';
import 'screens/assessment_screen.dart';
import 'screens/edit_profile_screen.dart';
import 'screens/change_password_screen.dart';
import 'screens/about_screen.dart';

void main() => runApp(const CervixAiApp());

class CervixAiApp extends StatelessWidget {
  const CervixAiApp({super.key});

  @override
  Widget build(BuildContext context) => MaterialApp(
        debugShowCheckedModeBanner: false,
        title: 'CerviXAI',
        theme: buildAppTheme(),
        initialRoute: '/',
        routes: {
          '/': (_) => const SplashScreen(),
          '/login': (_) => const LoginScreen(),
          '/register': (_) => const RegisterScreen(),
          '/forgot': (_) => const ForgotPasswordScreen(),
          '/shell': (_) => const ShellScreen(),
          '/assessment': (_) => const AssessmentScreen(),
          '/edit-profile': (_) => const EditProfileScreen(),
          '/change-password': (_) => const ChangePasswordScreen(),
          '/about': (_) => const AboutScreen(),
        },
      );
}
