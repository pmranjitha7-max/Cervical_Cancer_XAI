/// Data models shared across the app. Kept separate from the screens so
/// the JSON shape of the backend response only has to be parsed in one
/// place.
library;

class AppUser {
  AppUser({
    required this.id,
    required this.name,
    required this.username,
    required this.email,
  });

  final int id;
  final String name;
  final String username;
  final String email;

  factory AppUser.fromJson(Map<String, dynamic> j) => AppUser(
        id: (j['id'] as num?)?.toInt() ?? 0,
        name: j['name']?.toString() ?? '',
        username: j['username']?.toString() ?? '',
        email: j['email']?.toString() ?? '',
      );
}

class Factor {
  Factor({required this.rank, required this.name, this.value, required this.text});
  final int rank;
  final String name;
  final String? value;
  final String text;

  factory Factor.fromTabularJson(Map<String, dynamic> j) => Factor(
        rank: (j['rank'] as num?)?.toInt() ?? 0,
        name: j['factor']?.toString() ?? 'Factor',
        value: j['patient_value']?.toString(),
        text: j['xai_result']?.toString() ?? '',
      );

  factory Factor.fromImageJson(Map<String, dynamic> j) => Factor(
        rank: (j['rank'] as num?)?.toInt() ?? 0,
        name: j['factor']?.toString() ?? 'Factor',
        value: null,
        text: j['observation']?.toString() ?? '',
      );
}

/// Result of a tabular patient assessment (/cancer-report).
class AssessmentReport {
  AssessmentReport({
    required this.patientId,
    required this.result,
    required this.riskPercent,
    required this.safePercent,
    required this.thresholdPercent,
    required this.biopsyResult,
    required this.biopsyRisk,
    required this.hpvResult,
    required this.hpvRisk,
    required this.method,
    required this.explanation,
    required this.factors,
    required this.interpretation,
    required this.nextStep,
    required this.note,
  });

  final int patientId;
  final String result;
  final double riskPercent, safePercent, thresholdPercent, biopsyRisk, hpvRisk;
  final String biopsyResult, hpvResult, method, explanation, interpretation, nextStep, note;
  final List<Factor> factors;

  bool get isPositive => result.toLowerCase().contains('positive');

  factory AssessmentReport.fromJson(Map<String, dynamic> j) {
    final overall = j['overall_cancer_prediction'] as Map<String, dynamic>? ?? {};
    final support = j['supporting_predictions'] as Map<String, dynamic>? ?? {};
    final biopsy = support['biopsy'] as Map<String, dynamic>? ?? {};
    final hpv = support['hpv'] as Map<String, dynamic>? ?? {};
    final xai = j['xai_explanation'] as Map<String, dynamic>? ?? {};
    double num_(v) => (v as num?)?.toDouble() ?? 0;
    final factorsJson = xai['top_supporting_factors'] as List? ?? [];

    return AssessmentReport(
      patientId: (j['patient_id'] as num?)?.toInt() ?? 0,
      result: overall['prediction']?.toString() ?? 'Unknown',
      riskPercent: num_(overall['cancer_probability_percent']),
      safePercent: num_(overall['no_cancer_probability_percent']),
      thresholdPercent: num_(overall['classification_threshold_percent']),
      biopsyResult: biopsy['prediction']?.toString() ?? 'Unknown',
      biopsyRisk: num_(biopsy['positive_probability_percent']),
      hpvResult: hpv['prediction']?.toString() ?? 'Unknown',
      hpvRisk: num_(hpv['positive_probability_percent']),
      method: xai['method']?.toString() ?? 'Explainable AI',
      explanation: xai['explanation']?.toString() ?? '',
      factors: factorsJson
          .whereType<Map<String, dynamic>>()
          .map(Factor.fromTabularJson)
          .toList(),
      interpretation: j['interpretation']?.toString() ?? '',
      nextStep: j['recommended_next_step']?.toString() ?? '',
      note: j['important_note']?.toString() ?? '',
    );
  }
}

/// Result of an image screening (/image-screening) — deliberately plain
/// language so a patient (not just a clinician) can read it.
class ImageScreeningReport {
  ImageScreeningReport({
    required this.result,
    required this.abnormalPercent,
    required this.normalPercent,
    required this.likelyPattern,
    required this.confidencePercent,
    required this.summary,
    required this.factors,
    required this.nextStep,
    required this.note,
  });

  final String result;
  final double abnormalPercent, normalPercent, confidencePercent;
  final String likelyPattern, summary, nextStep, note;
  final List<Factor> factors;

  bool get isAbnormal => result.toLowerCase() == 'abnormal';

  factory ImageScreeningReport.fromJson(Map<String, dynamic> j) {
    double num_(v) => (v as num?)?.toDouble() ?? 0;
    final factorsJson = j['top_visual_factors'] as List? ?? [];
    return ImageScreeningReport(
      result: j['screening_result']?.toString() ?? 'Unknown',
      abnormalPercent: num_(j['abnormal_probability_percent']),
      normalPercent: num_(j['normal_probability_percent']),
      likelyPattern: j['likely_pattern']?.toString() ?? '',
      confidencePercent: num_(j['confidence_percent']),
      summary: j['plain_language_summary']?.toString() ?? '',
      factors: factorsJson
          .whereType<Map<String, dynamic>>()
          .map(Factor.fromImageJson)
          .toList(),
      nextStep: j['recommended_next_step']?.toString() ?? '',
      note: j['important_note']?.toString() ?? '',
    );
  }
}

/// One row in the persisted assessment history (from GET /history).
class HistoryEntry {
  HistoryEntry({
    required this.id,
    required this.kind,
    required this.title,
    required this.result,
    required this.riskPercent,
    required this.createdAt,
  });

  final int id;
  final String kind; // "assessment" or "image_screening"
  final String title;
  final String result;
  final double? riskPercent;
  final DateTime createdAt;

  bool get isPositive => result.toLowerCase().contains('positive') ||
      result.toLowerCase() == 'abnormal';

  bool get isImage => kind == 'image_screening';

  factory HistoryEntry.fromJson(Map<String, dynamic> j) => HistoryEntry(
        id: (j['id'] as num?)?.toInt() ?? 0,
        kind: j['kind']?.toString() ?? 'assessment',
        title: j['title']?.toString() ?? '',
        result: j['result']?.toString() ?? '',
        riskPercent: (j['risk_percent'] as num?)?.toDouble(),
        createdAt: DateTime.tryParse(j['created_at']?.toString() ?? '') ??
            DateTime.now(),
      );
}
