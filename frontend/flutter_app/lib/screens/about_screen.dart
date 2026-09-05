import 'package:flutter/material.dart';

import '../theme.dart';
import '../widgets/common.dart';

class AboutScreen extends StatelessWidget {
  const AboutScreen({super.key});

  @override
  Widget build(BuildContext context) => AppPage(
        'About CerviXAI',
        ListView(padding: const EdgeInsets.all(20), children: [
          Glass(Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            const Brand(big: true),
            const SizedBox(height: 20),
            Text('Explainable intelligence for clinical support', style: Theme.of(context).textTheme.headlineSmall),
            const SizedBox(height: 10),
            const Text(
              'CerviXAI combines machine-learning predictions with human-readable explanations to '
              'support cervical cancer risk assessment, including both structured patient records and '
              'cell image screening. It is designed for healthcare professionals and does not replace '
              'clinical judgement.',
            ),
          ])),
          const SizedBox(height: 14),
          sectionCard(
            context,
            'Core capabilities',
            Icons.stars_outlined,
            const Column(children: [
              _Feature(Icons.biotech_outlined, 'AI-assisted patient assessment'),
              _Feature(Icons.image_search_outlined, 'Cell image screening with plain-language reports'),
              _Feature(Icons.psychology_alt_outlined, 'Explainable supporting factors (SHAP)'),
              _Feature(Icons.history_rounded, 'Assessment history saved to your account'),
              _Feature(Icons.security_rounded, 'Professional access workflow'),
            ]),
          ),
          const SizedBox(height: 14),
          const Center(child: Text('Version 2.0.0 — Flutter edition', style: TextStyle(color: AppColors.muted))),
        ]),
      );
}

class _Feature extends StatelessWidget {
  const _Feature(this.icon, this.text);
  final IconData icon;
  final String text;

  @override
  Widget build(BuildContext context) => Padding(
        padding: const EdgeInsets.symmetric(vertical: 7),
        child: Row(children: [
          Icon(icon, color: AppColors.cyan),
          const SizedBox(width: 11),
          Expanded(child: Text(text)),
        ]),
      );
}
