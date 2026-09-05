import 'package:flutter/material.dart';

import '../services/api_service.dart';
import '../session.dart';
import '../theme.dart';
import '../widgets/common.dart';
import 'prediction_result_screen.dart';

class AssessmentScreen extends StatefulWidget {
  const AssessmentScreen({super.key});
  @override
  State<AssessmentScreen> createState() => _AssessmentScreenState();
}

class _AssessmentScreenState extends State<AssessmentScreen> {
  final _id = TextEditingController();
  bool _busy = false;
  String? _error;

  @override
  void dispose() {
    _id.dispose();
    super.dispose();
  }

  Future<void> _run() async {
    final n = int.tryParse(_id.text.trim());
    if (n == null || n < 0) {
      setState(() => _error = 'Enter a valid numeric patient ID.');
      return;
    }
    setState(() {
      _busy = true;
      _error = null;
    });
    try {
      final report = await Session.i.api.runAssessment(n);
      Session.i.markHistoryChanged();
      if (mounted) {
        Navigator.push(context, MaterialPageRoute(builder: (_) => PredictionResultScreen(report)));
      }
    } on ApiException catch (e) {
      setState(() => _error = e.message);
    } finally {
      if (mounted) setState(() => _busy = false);
    }
  }

  @override
  Widget build(BuildContext context) => AppPage(
        'Patient assessment',
        ListView(padding: const EdgeInsets.all(20), children: [
          Glass(Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            const Icon(Icons.manage_search_rounded, size: 44, color: AppColors.blue),
            const SizedBox(height: 15),
            Text('Find patient record', style: Theme.of(context).textTheme.titleLarge),
            const Text(
              'Enter the dataset patient ID used by the prediction service.',
              style: TextStyle(color: AppColors.muted),
            ),
            const SizedBox(height: 19),
            appField(_id, 'Patient ID', Icons.tag_rounded, type: TextInputType.number),
            if (_error != null) InlineNotice(_error!),
            const SizedBox(height: 18),
            FilledButton.icon(
              onPressed: _busy ? null : _run,
              icon: _busy ? const BusySpinner() : const Icon(Icons.auto_awesome_rounded),
              label: Text(_busy ? 'ANALYSING...' : 'GENERATE ASSESSMENT'),
            ),
          ])),
        ]),
      );
}
