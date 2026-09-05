import 'package:flutter/material.dart';

import '../models.dart';
import '../theme.dart';
import '../widgets/common.dart';

class PredictionResultScreen extends StatelessWidget {
  const PredictionResultScreen(this.report, {super.key});
  final AssessmentReport report;

  @override
  Widget build(BuildContext context) {
    final positive = report.isPositive;
    final color = positive ? AppColors.red : AppColors.success;
    return AppPage(
      'Assessment result',
      ListView(padding: const EdgeInsets.all(20), children: [
        Glass(Column(children: [
          Row(children: [
            Text('PATIENT #${report.patientId}',
                style: const TextStyle(color: AppColors.muted, fontWeight: FontWeight.bold)),
            const Spacer(),
            Icon(positive ? Icons.warning_amber_rounded : Icons.verified_rounded, color: color),
          ]),
          const SizedBox(height: 15),
          Text(report.result,
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 25, fontWeight: FontWeight.w800, color: color)),
          const SizedBox(height: 16),
          Row(children: [
            Expanded(child: _metric('Cancer', report.riskPercent, color)),
            const SizedBox(width: 10),
            Expanded(child: _metric('No cancer', report.safePercent, AppColors.cyan)),
          ]),
          const SizedBox(height: 9),
          Text('Classification threshold: ${report.thresholdPercent.toStringAsFixed(1)}%',
              style: const TextStyle(color: AppColors.muted)),
        ])),
        const SizedBox(height: 14),
        sectionCard(
          context,
          'Supporting models',
          Icons.hub_outlined,
          Column(children: [
            _support('Biopsy', report.biopsyResult, report.biopsyRisk),
            const Divider(height: 24),
            _support('HPV', report.hpvResult, report.hpvRisk),
          ]),
        ),
        const SizedBox(height: 14),
        sectionCard(
          context,
          '${report.method} explanation',
          Icons.auto_awesome_outlined,
          Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text(report.explanation),
            const SizedBox(height: 12),
            ...report.factors.map((f) => Container(
                  width: double.infinity,
                  margin: const EdgeInsets.only(bottom: 9),
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: AppColors.blue.withValues(alpha: .06),
                    borderRadius: BorderRadius.circular(14),
                  ),
                  child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    Text('${f.rank}. ${f.name}', style: const TextStyle(fontWeight: FontWeight.bold)),
                    if (f.value != null)
                      Text('Patient value: ${f.value}', style: const TextStyle(color: AppColors.muted)),
                    Text(f.text),
                  ]),
                )),
          ]),
        ),
        const SizedBox(height: 14),
        sectionCard(context, 'Clinical interpretation', Icons.fact_check_outlined, Text(report.interpretation)),
        const SizedBox(height: 14),
        sectionCard(context, 'Recommended next step', Icons.arrow_circle_right_outlined, Text(report.nextStep)),
        const SizedBox(height: 14),
        sectionCard(context, 'Important clinical note', Icons.shield_outlined,
            Text(report.note, style: const TextStyle(color: AppColors.muted))),
      ]),
    );
  }

  Widget _metric(String label, double value, Color c) => Container(
        padding: const EdgeInsets.all(13),
        decoration: BoxDecoration(color: c.withValues(alpha: .1), borderRadius: BorderRadius.circular(16)),
        child: Column(children: [
          Text('${value.toStringAsFixed(1)}%',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.w800, color: c)),
          Text(label),
        ]),
      );

  Widget _support(String label, String prediction, double value) => Row(children: [
        Expanded(
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text(label, style: const TextStyle(fontWeight: FontWeight.bold)),
            Text(prediction, style: const TextStyle(color: AppColors.muted)),
          ]),
        ),
        Text('${value.toStringAsFixed(1)}%',
            style: const TextStyle(fontSize: 17, fontWeight: FontWeight.bold, color: AppColors.blue)),
      ]);
}
