import 'dart:io';

import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

import '../services/api_service.dart';
import '../session.dart';
import '../theme.dart';
import '../widgets/common.dart';
import 'image_screening_result_screen.dart';

class ImageScreeningScreen extends StatefulWidget {
  const ImageScreeningScreen({super.key});
  @override
  State<ImageScreeningScreen> createState() => _ImageScreeningScreenState();
}

class _ImageScreeningScreenState extends State<ImageScreeningScreen> {
  XFile? _picked;
  bool _busy = false;
  String? _error;

  Future<void> _pick(ImageSource source) async {
    try {
      final file = await ImagePicker().pickImage(source: source, imageQuality: 92);
      if (file != null) setState(() {
        _picked = file;
        _error = null;
      });
    } catch (e) {
      setState(() => _error = 'Could not open the image picker on this device.');
    }
  }

  Future<void> _analyse() async {
    final picked = _picked;
    if (picked == null) return;
    setState(() {
      _busy = true;
      _error = null;
    });
    try {
      final bytes = await picked.readAsBytes();
      final report = await Session.i.api.runImageScreening(bytes, picked.name);
      Session.i.markHistoryChanged();
      if (mounted) {
        Navigator.push(context, MaterialPageRoute(builder: (_) => ImageScreeningResultScreen(report, picked)));
      }
    } on ApiException catch (e) {
      setState(() => _error = e.message);
    } finally {
      if (mounted) setState(() => _busy = false);
    }
  }

  @override
  Widget build(BuildContext context) => Bg(SafeArea(
        child: ListView(padding: const EdgeInsets.fromLTRB(20, 16, 20, 20), children: [
          Text('Cell image screening', style: Theme.of(context).textTheme.titleLarge),
          const SizedBox(height: 4),
          const Text(
            'Upload a cervical cytology cell image. The AI screens it and turns the result into a '
            'plain-language report — not just raw image output — so it makes sense to a patient, '
            'not only a doctor.',
            style: TextStyle(color: AppColors.muted),
          ),
          const SizedBox(height: 18),
          Glass(Column(children: [
            AspectRatio(
              aspectRatio: 1.3,
              child: ClipRRect(
                borderRadius: BorderRadius.circular(18),
                child: _picked == null
                    ? Container(
                        color: AppColors.surfaceAlt,
                        child: const Center(
                          child: Icon(Icons.image_outlined, size: 54, color: AppColors.muted),
                        ),
                      )
                    : Image.file(File(_picked!.path), fit: BoxFit.cover),
              ),
            ),
            const SizedBox(height: 16),
            Row(children: [
              Expanded(
                child: OutlinedButton.icon(
                  onPressed: _busy ? null : () => _pick(ImageSource.gallery),
                  icon: const Icon(Icons.photo_library_outlined),
                  label: const Text('Gallery'),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: OutlinedButton.icon(
                  onPressed: _busy ? null : () => _pick(ImageSource.camera),
                  icon: const Icon(Icons.photo_camera_outlined),
                  label: const Text('Camera'),
                ),
              ),
            ]),
            if (_error != null) InlineNotice(_error!),
            const SizedBox(height: 16),
            FilledButton.icon(
              onPressed: (_picked == null || _busy) ? null : _analyse,
              icon: _busy ? const BusySpinner() : const Icon(Icons.auto_awesome_rounded),
              label: Text(_busy ? 'SCREENING...' : 'RUN SCREENING'),
            ),
          ])),
          const SizedBox(height: 14),
          Glass(Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
            const Icon(Icons.shield_outlined, color: AppColors.blue),
            const SizedBox(width: 10),
            const Expanded(
              child: Text(
                'This screening tool supports triage and education. It does not replace a laboratory '
                'Pap smear or a pathologist\'s reading.',
                style: TextStyle(color: AppColors.muted),
              ),
            ),
          ])),
        ]),
      ));
}
