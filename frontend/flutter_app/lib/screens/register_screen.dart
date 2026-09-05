import 'package:flutter/material.dart';

import '../services/api_service.dart';
import '../session.dart';
import '../widgets/common.dart';

class RegisterScreen extends StatefulWidget {
  const RegisterScreen({super.key});
  @override
  State<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  final _name = TextEditingController();
  final _username = TextEditingController();
  final _email = TextEditingController();
  final _password = TextEditingController();
  final _confirm = TextEditingController();
  String? _error;
  bool _busy = false;

  @override
  void dispose() {
    _name.dispose();
    _username.dispose();
    _email.dispose();
    _password.dispose();
    _confirm.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    if (_name.text.trim().length < 2 ||
        _username.text.trim().length < 4 ||
        !_email.text.contains('@') ||
        _password.text.length < 8 ||
        _password.text != _confirm.text) {
      setState(() => _error =
          'Complete all fields. Matching passwords require at least 8 characters.');
      return;
    }
    setState(() {
      _busy = true;
      _error = null;
    });
    try {
      final (token, user) = await Session.i.api.register(
        name: _name.text.trim(),
        username: _username.text.trim(),
        email: _email.text.trim(),
        password: _password.text,
      );
      await Session.i.signInWith(token, user);
      if (mounted) {
        Navigator.pushNamedAndRemoveUntil(context, '/shell', (_) => false);
        showSnack(context, 'Account created — welcome to CerviXAI.');
      }
    } on ApiException catch (e) {
      setState(() => _error = e.message);
    } finally {
      if (mounted) setState(() => _busy = false);
    }
  }

  @override
  Widget build(BuildContext context) => AppPage(
        'Create account',
        ListView(padding: const EdgeInsets.all(20), children: [
          Glass(Column(children: [
            appField(_name, 'Full name', Icons.badge_outlined),
            const SizedBox(height: 11),
            appField(_username, 'Username', Icons.person_outline_rounded),
            const SizedBox(height: 11),
            appField(_email, 'Email address', Icons.mail_outline_rounded,
                type: TextInputType.emailAddress),
            const SizedBox(height: 11),
            appField(_password, 'Password', Icons.lock_outline_rounded, secret: true),
            const SizedBox(height: 11),
            appField(_confirm, 'Confirm password', Icons.verified_user_outlined, secret: true),
            if (_error != null) InlineNotice(_error!),
            const SizedBox(height: 16),
            FilledButton(
              onPressed: _busy ? null : _submit,
              child: _busy ? const BusySpinner() : const Text('CREATE ACCOUNT'),
            ),
          ])),
        ]),
      );
}
