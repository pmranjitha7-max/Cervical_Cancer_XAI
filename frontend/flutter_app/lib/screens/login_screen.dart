import 'package:flutter/material.dart';

import '../services/api_service.dart';
import '../session.dart';
import '../widgets/common.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});
  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _username = TextEditingController();
  final _password = TextEditingController();
  String? _error;
  bool _busy = false;

  @override
  void dispose() {
    _username.dispose();
    _password.dispose();
    super.dispose();
  }

  Future<void> _signIn() async {
    if (_username.text.trim().isEmpty || _password.text.isEmpty) {
      setState(() => _error = 'Enter your username and password.');
      return;
    }
    setState(() {
      _busy = true;
      _error = null;
    });
    try {
      final (token, user) = await Session.i.api.login(
        username: _username.text.trim(),
        password: _password.text,
      );
      await Session.i.signInWith(token, user);
      if (mounted) Navigator.pushNamedAndRemoveUntil(context, '/shell', (_) => false);
    } on ApiException catch (e) {
      setState(() => _error = e.message);
    } finally {
      if (mounted) setState(() => _busy = false);
    }
  }

  @override
  Widget build(BuildContext context) => Scaffold(
        body: Bg(ListView(padding: const EdgeInsets.all(24), children: [
          const SizedBox(height: 18),
          const Center(child: Brand(big: true)),
          const SizedBox(height: 30),
          Glass(Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text('Welcome back', style: Theme.of(context).textTheme.headlineSmall),
            const Text('Secure access for healthcare professionals',
                style: TextStyle(color: Color(0xff5b7186))),
            const SizedBox(height: 22),
            appField(_username, 'Username or email', Icons.person_outline_rounded),
            const SizedBox(height: 12),
            appField(_password, 'Password', Icons.lock_outline_rounded, secret: true),
            if (_error != null) InlineNotice(_error!),
            const SizedBox(height: 16),
            Align(
              alignment: Alignment.centerRight,
              child: TextButton(
                onPressed: () => Navigator.pushNamed(context, '/forgot'),
                child: const Text('Forgot password?'),
              ),
            ),
            FilledButton(
              onPressed: _busy ? null : _signIn,
              child: _busy ? const BusySpinner() : const Text('SIGN IN'),
            ),
            const SizedBox(height: 6),
            Center(
              child: TextButton(
                onPressed: () => Navigator.pushNamed(context, '/register'),
                child: const Text('Create a professional account'),
              ),
            ),
          ])),
        ])),
      );
}
