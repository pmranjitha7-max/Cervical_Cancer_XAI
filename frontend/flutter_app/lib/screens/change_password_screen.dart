import 'package:flutter/material.dart';

import '../services/api_service.dart';
import '../session.dart';
import '../widgets/common.dart';

class ChangePasswordScreen extends StatefulWidget {
  const ChangePasswordScreen({super.key});
  @override
  State<ChangePasswordScreen> createState() => _ChangePasswordScreenState();
}

class _ChangePasswordScreenState extends State<ChangePasswordScreen> {
  final _current = TextEditingController();
  final _next = TextEditingController();
  final _confirm = TextEditingController();
  String? _error;
  bool _busy = false;

  @override
  void dispose() {
    _current.dispose();
    _next.dispose();
    _confirm.dispose();
    super.dispose();
  }

  Future<void> _save() async {
    if (_next.text.length < 8 || _next.text != _confirm.text) {
      setState(() => _error = 'New passwords must match and contain 8+ characters.');
      return;
    }
    setState(() {
      _busy = true;
      _error = null;
    });
    try {
      await Session.i.api.changePassword(currentPassword: _current.text, newPassword: _next.text);
      if (mounted) {
        Navigator.pop(context);
        showSnack(context, 'Password updated successfully.');
      }
    } on ApiException catch (e) {
      setState(() => _error = e.message);
    } finally {
      if (mounted) setState(() => _busy = false);
    }
  }

  @override
  Widget build(BuildContext context) => AppPage(
        'Change password',
        ListView(padding: const EdgeInsets.all(20), children: [
          Glass(Column(children: [
            appField(_current, 'Current password', Icons.lock_outline_rounded, secret: true),
            const SizedBox(height: 11),
            appField(_next, 'New password', Icons.password_rounded, secret: true),
            const SizedBox(height: 11),
            appField(_confirm, 'Confirm new password', Icons.verified_user_outlined, secret: true),
            if (_error != null) InlineNotice(_error!),
            const SizedBox(height: 15),
            FilledButton(
              onPressed: _busy ? null : _save,
              child: _busy ? const BusySpinner() : const Text('UPDATE PASSWORD'),
            ),
          ])),
        ]),
      );
}
