import 'dart:io';

import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

import '../models.dart';
import '../theme.dart';
import '../widgets/common.dart';

class ImageScreeningResultScreen extends StatelessWidget {
  const ImageScreeningResultScreen(this.report, this.image, {super.key});
  final ImageScreeningReport report;
  final XFile image;

  @override
  Widget build(BuildContext context) {
    final abnormal = report.isAbnormal;
    final color = abnormal ? AppColors.red : AppColors.success;
    return AppPage(
      'Screening report',
      ListView(padding: const EdgeInsets.all(20), children: [
        Glass(Column(children: [
          ClipRRect(
            borderRadius: BorderRadius.circular(16),
            child: Image.file(File(image.path), height: 150, width: double.infinity, fit: BoxFit.cover),
          ),
          const SizedBox(height: 16),
          Icon(abnormal ? Icons.warning_amber_rounded : Icons.verified_rounded, color: color, size: 34),
          const SizedBox(height: 8),
          Text(
            abnormal ? 'Abnormal pattern detected' : 'Normal pattern',
            textAlign: TextAlign.center,
            style: TextStyle(fontSize: 23, fontWeight: FontWeight.w800, color: color),
          ),
          const SizedBox(height: 6),
          Text(report.likelyPattern, textAlign: TextAlign.center, style: const TextStyle(color: AppColors.muted)),
          const SizedBox(height: 16),
          Row(children: [
            Expanded(child: _metric('Abnormal', report.abnormalPercent, AppColors.red)),
            const SizedBox(width: 10),
            Expanded(child: _metric('Normal', report.normalPercent, AppColors.cyan)),
          ]),
          const SizedBox(height: 9),
          Text('Model confidence: ${report.confidencePercent.toStringAsFixed(1)}%',
              style: const TextStyle(color: AppColors.muted)),
        ])),
        const SizedBox(height: 14),
        sectionCard(context, 'In plain language', Icons.forum_outlined, Text(report.summary)),
        const SizedBox(height: 14),
        sectionCard(
          context,
          'What the AI noticed',
          Icons.visibility_outlined,
          Column(crossAxisAlignment: CrossAxisAlignment.start, children: report.factors
              .map((f) => Container(
                    width: double.infinity,
                    margin: const EdgeInsets.only(bottom: 9),
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: AppColors.mint.withValues(alpha: .08),
                      borderRadius: BorderRadius.circular(14),
                    ),
                    child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                      Text('${f.rank}. ${f.name}', style: const TextStyle(fontWeight: FontWeight.bold)),
                      Text(f.text),
                    ]),
                  ))
              .toList()),
        ),
        const SizedBox(height: 14),
        sectionCard(context, 'Recommended next step', Icons.arrow_circle_right_outlined, Text(report.nextStep)),
        const SizedBox(height: 14),
        sectionCard(context, 'Important note', Icons.shield_outlined,
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
}
