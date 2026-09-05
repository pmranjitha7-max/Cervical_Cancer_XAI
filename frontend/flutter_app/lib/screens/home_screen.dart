import 'package:flutter/material.dart';

import '../session.dart';
import '../theme.dart';
import '../widgets/common.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final name = Session.i.user?.name.isNotEmpty == true ? Session.i.user!.name : 'there';
    return Bg(ListView(padding: const EdgeInsets.fromLTRB(20, 16, 20, 20), children: [
      const Brand(),
      const SizedBox(height: 26),
      Text('Good day, $name', style: Theme.of(context).textTheme.headlineSmall),
      const Text('What would you like to review today?', style: TextStyle(color: AppColors.muted)),
      const SizedBox(height: 20),
      Glass(Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        const Icon(Icons.biotech_rounded, size: 40, color: AppColors.blue),
        const SizedBox(height: 14),
        Text('New patient assessment', style: Theme.of(context).textTheme.titleLarge),
        const Text(
          'Request an explainable AI risk classification using a patient ID from the clinical dataset.',
          style: TextStyle(color: AppColors.muted),
        ),
        const SizedBox(height: 18),
        FilledButton.icon(
          onPressed: () => Navigator.pushNamed(context, '/assessment'),
          icon: const Icon(Icons.add_rounded),
          label: const Text('START ASSESSMENT'),
        ),
      ])),
      const SizedBox(height: 16),
      Glass(Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        const Icon(Icons.image_search_rounded, size: 40, color: AppColors.mint),
        const SizedBox(height: 14),
        Text('Cell image screening', style: Theme.of(context).textTheme.titleLarge),
        const Text(
          'Upload a cervical cytology cell image for an AI screening flag with a plain-language report.',
          style: TextStyle(color: AppColors.muted),
        ),
      ])),
      const SizedBox(height: 16),
      Glass(Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
        const Icon(Icons.shield_outlined, color: AppColors.blue),
        const SizedBox(width: 10),
        Expanded(
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            const Text(
              'Clinical support only. Interpret results with screening data, examination findings and professional judgement.',
              style: TextStyle(color: AppColors.muted),
            ),
            Align(
              alignment: Alignment.centerRight,
              child: TextButton(
                onPressed: () => Navigator.pushNamed(context, '/about'),
                child: const Text('About CerviXAI'),
              ),
            ),
          ]),
        ),
      ])),
    ]));
  }
}
