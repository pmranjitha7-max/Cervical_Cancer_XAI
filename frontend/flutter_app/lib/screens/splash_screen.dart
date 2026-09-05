import 'package:flutter/material.dart';

import '../session.dart';
import '../widgets/common.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});
  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  @override
  void initState() {
    super.initState();
    _decide();
  }

  Future<void> _decide() async {
    final restored = await Session.i.tryRestore();
    // Small minimum splash time so the brand mark doesn't just flash by.
    await Future.delayed(const Duration(milliseconds: 900));
    if (!mounted) return;
    Navigator.pushReplacementNamed(context, restored ? '/shell' : '/login');
  }

  @override
  Widget build(BuildContext context) => Scaffold(
        body: Bg(Center(
          child: Padding(
            padding: const EdgeInsets.all(28),
            child: Glass(Column(mainAxisSize: MainAxisSize.min, children: [
              const Brand(big: true),
              const SizedBox(height: 24),
              Text('Clarity behind every prediction',
                  textAlign: TextAlign.center, style: Theme.of(context).textTheme.headlineSmall),
              const SizedBox(height: 9),
              const Text(
                'Explainable cervical cancer risk assessment for informed clinical decisions.',
                textAlign: TextAlign.center,
                style: TextStyle(color: Color(0xff5b7186), height: 1.5),
              ),
              const SizedBox(height: 25),
              const LinearProgressIndicator(),
            ])),
          ),
        )),
      );
}
