import 'dart:ui';

import 'package:flutter/material.dart';

import '../theme.dart';

/// Soft gradient backdrop used behind every screen.
class Bg extends StatelessWidget {
  const Bg(this.child, {super.key});
  final Widget child;

  @override
  Widget build(BuildContext context) => DecoratedBox(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [Color(0xfff7fbff), Color(0xffe8f0ff), Color(0xffe7f8f3)],
          ),
        ),
        child: Stack(
          children: [
            Positioned(top: -110, right: -90, child: _orb(AppColors.cyan)),
            Positioned(bottom: -140, left: -100, child: _orb(AppColors.blue)),
            SafeArea(child: child),
          ],
        ),
      );

  static Widget _orb(Color c) => Container(
        width: 280,
        height: 280,
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          color: c.withValues(alpha: .12),
        ),
      );
}

/// Frosted-glass card, the app's signature surface treatment.
class Glass extends StatelessWidget {
  const Glass(this.child, {this.pad = const EdgeInsets.all(20), super.key});
  final Widget child;
  final EdgeInsets pad;

  @override
  Widget build(BuildContext context) => ClipRRect(
        borderRadius: BorderRadius.circular(AppRadius.card),
        child: BackdropFilter(
          filter: ImageFilter.blur(sigmaX: 16, sigmaY: 16),
          child: Container(
            padding: pad,
            decoration: BoxDecoration(
              color: Colors.white.withValues(alpha: .72),
              borderRadius: BorderRadius.circular(AppRadius.card),
              border: Border.all(color: Colors.white.withValues(alpha: .9)),
              boxShadow: const [
                BoxShadow(color: Color(0x14102a43), blurRadius: 28, offset: Offset(0, 12)),
              ],
            ),
            child: child,
          ),
        ),
      );
}

/// App wordmark + icon, drawn from the generated brand asset with a
/// graceful fallback if the asset isn't bundled yet.
class Brand extends StatelessWidget {
  const Brand({this.big = false, super.key});
  final bool big;

  @override
  Widget build(BuildContext context) {
    final size = big ? 62.0 : 44.0;
    return Row(mainAxisSize: MainAxisSize.min, children: [
      ClipRRect(
        borderRadius: BorderRadius.circular(size * 0.32),
        child: Image.asset(
          'assets/images/app_logo.png',
          width: size,
          height: size,
          fit: BoxFit.cover,
          errorBuilder: (_, __, ___) => Container(
            width: size,
            height: size,
            decoration: BoxDecoration(
              gradient: const LinearGradient(colors: [AppColors.blue, AppColors.cyan]),
              borderRadius: BorderRadius.circular(size * 0.32),
            ),
            child: Icon(Icons.biotech_rounded, color: Colors.white, size: size * 0.56),
          ),
        ),
      ),
      const SizedBox(width: 12),
      Text(
        'CerviXAI',
        style: TextStyle(
          fontSize: big ? 30 : 22,
          fontWeight: FontWeight.w800,
          color: AppColors.navy,
        ),
      ),
    ]);
  }
}

/// Standard sub-page scaffold: back button + title + optional actions,
/// on the shared [Bg].
class AppPage extends StatelessWidget {
  const AppPage(this.title, this.child, {this.actions = const [], super.key});
  final String title;
  final Widget child;
  final List<Widget> actions;

  @override
  Widget build(BuildContext context) => Scaffold(
        body: Bg(Column(children: [
          Padding(
            padding: const EdgeInsets.fromLTRB(14, 10, 14, 4),
            child: Row(children: [
              IconButton.filledTonal(
                onPressed: () => Navigator.pop(context),
                icon: const Icon(Icons.arrow_back_rounded),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: Text(title, style: Theme.of(context).textTheme.titleLarge),
              ),
              ...actions,
            ]),
          ),
          Expanded(child: child),
        ])),
      );
}

Widget appField(
  TextEditingController controller,
  String label,
  IconData icon, {
  bool secret = false,
  TextInputType? type,
}) =>
    TextField(
      controller: controller,
      obscureText: secret,
      keyboardType: type,
      decoration: InputDecoration(labelText: label, prefixIcon: Icon(icon, color: AppColors.muted)),
    );

Widget sectionCard(BuildContext context, String title, IconData icon, Widget child) => Glass(
      Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Row(children: [
          Icon(icon, color: AppColors.blue),
          const SizedBox(width: 10),
          Expanded(child: Text(title, style: Theme.of(context).textTheme.titleMedium)),
        ]),
        const SizedBox(height: 14),
        child,
      ]),
    );

/// Inline error/notice banner used under forms.
class InlineNotice extends StatelessWidget {
  const InlineNotice(this.text, {this.isError = true, super.key});
  final String text;
  final bool isError;

  @override
  Widget build(BuildContext context) => Padding(
        padding: const EdgeInsets.only(top: 12),
        child: Container(
          width: double.infinity,
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(
            color: (isError ? AppColors.red : AppColors.success).withValues(alpha: .1),
            borderRadius: BorderRadius.circular(14),
          ),
          child: Row(children: [
            Icon(isError ? Icons.error_outline_rounded : Icons.check_circle_outline_rounded,
                color: isError ? AppColors.red : AppColors.success, size: 20),
            const SizedBox(width: 8),
            Expanded(
              child: Text(text,
                  style: TextStyle(
                      color: isError ? AppColors.red : AppColors.success,
                      fontWeight: FontWeight.w600)),
            ),
          ]),
        ),
      );
}

class EmptyState extends StatelessWidget {
  const EmptyState({required this.icon, required this.text, super.key});
  final IconData icon;
  final String text;

  @override
  Widget build(BuildContext context) => Center(
        child: Column(mainAxisSize: MainAxisSize.min, children: [
          Icon(icon, size: 52, color: AppColors.muted.withValues(alpha: .7)),
          const SizedBox(height: 12),
          Text(text, style: const TextStyle(color: AppColors.muted)),
        ]),
      );
}

class BusySpinner extends StatelessWidget {
  const BusySpinner({this.size = 18, this.color = Colors.white, super.key});
  final double size;
  final Color color;

  @override
  Widget build(BuildContext context) => SizedBox.square(
        dimension: size,
        child: CircularProgressIndicator(strokeWidth: 2.2, color: color),
      );
}

void showSnack(BuildContext context, String message) {
  ScaffoldMessenger.of(context)
    ..hideCurrentSnackBar()
    ..showSnackBar(SnackBar(content: Text(message)));
}
