import 'package:flutter/material.dart';

/// CerviXAI brand palette + shared theme. Centralising this (instead of
/// scattering `Color(0xff...)` literals through every screen) is what
/// makes the "professional" pass maintainable — one place to retune the
/// whole app's look.
class AppColors {
  AppColors._();

  static const navy = Color(0xff0b2545);
  static const navyLight = Color(0xff17395f);
  static const blue = Color(0xff2d6cdf);
  static const blueDeep = Color(0xff1f4fb0);
  static const cyan = Color(0xff1fb6c8);
  static const mint = Color(0xff2fbf9f);
  static const red = Color(0xffd8455f);
  static const amber = Color(0xffe0a52c);
  static const muted = Color(0xff5b7186);
  static const surface = Color(0xfff6f9fd);
  static const surfaceAlt = Color(0xffeef4fb);
  static const success = Color(0xff12876f);
}

class AppSpacing {
  AppSpacing._();
  static const xs = 6.0;
  static const sm = 10.0;
  static const md = 16.0;
  static const lg = 22.0;
  static const xl = 30.0;
}

class AppRadius {
  AppRadius._();
  static const card = 22.0;
  static const field = 16.0;
  static const chip = 30.0;
}

ThemeData buildAppTheme() {
  final scheme = ColorScheme.fromSeed(
    seedColor: AppColors.blue,
    brightness: Brightness.light,
  ).copyWith(
    primary: AppColors.blue,
    secondary: AppColors.cyan,
    error: AppColors.red,
    surface: Colors.white,
  );

  return ThemeData(
    useMaterial3: true,
    colorScheme: scheme,
    scaffoldBackgroundColor: AppColors.surface,
    fontFamily: 'Roboto',
    textTheme: const TextTheme(
      headlineSmall: TextStyle(
        fontWeight: FontWeight.w800,
        color: AppColors.navy,
        height: 1.2,
      ),
      titleLarge: TextStyle(
        fontWeight: FontWeight.w700,
        color: AppColors.navy,
      ),
      titleMedium: TextStyle(
        fontWeight: FontWeight.w700,
        color: AppColors.navy,
      ),
      bodyMedium: TextStyle(color: AppColors.navy, height: 1.4),
      labelLarge: TextStyle(fontWeight: FontWeight.w700, letterSpacing: .3),
    ),
    inputDecorationTheme: InputDecorationTheme(
      filled: true,
      fillColor: Colors.white,
      contentPadding:
          const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(AppRadius.field),
        borderSide: BorderSide(color: Colors.black.withValues(alpha: .06)),
      ),
      enabledBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(AppRadius.field),
        borderSide: BorderSide(color: Colors.black.withValues(alpha: .06)),
      ),
      focusedBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(AppRadius.field),
        borderSide: const BorderSide(color: AppColors.blue, width: 1.6),
      ),
      errorBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(AppRadius.field),
        borderSide: const BorderSide(color: AppColors.red, width: 1.3),
      ),
      labelStyle: const TextStyle(color: AppColors.muted),
    ),
    filledButtonTheme: FilledButtonThemeData(
      style: FilledButton.styleFrom(
        backgroundColor: AppColors.blue,
        foregroundColor: Colors.white,
        minimumSize: const Size.fromHeight(54),
        textStyle: const TextStyle(fontWeight: FontWeight.w700, letterSpacing: .3),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(AppRadius.field),
        ),
      ),
    ),
    outlinedButtonTheme: OutlinedButtonThemeData(
      style: OutlinedButton.styleFrom(
        minimumSize: const Size.fromHeight(54),
        foregroundColor: AppColors.navy,
        side: BorderSide(color: Colors.black.withValues(alpha: .12)),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(AppRadius.field),
        ),
      ),
    ),
    textButtonTheme: TextButtonThemeData(
      style: TextButton.styleFrom(foregroundColor: AppColors.blue),
    ),
    snackBarTheme: SnackBarThemeData(
      behavior: SnackBarBehavior.floating,
      backgroundColor: AppColors.navy,
      contentTextStyle: const TextStyle(color: Colors.white),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(14),
      ),
    ),
    dividerTheme: DividerThemeData(color: Colors.black.withValues(alpha: .06)),
  );
}
