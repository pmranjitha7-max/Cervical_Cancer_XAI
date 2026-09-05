import 'package:flutter/material.dart';

import '../theme.dart';
import '../widgets/common.dart';

class ForgotPasswordScreen extends StatefulWidget {
  const ForgotPasswordScreen({super.key});
  @override
  State<ForgotPasswordScreen> createState() => _ForgotPasswordScreenState();
}

class _ForgotPasswordScreenState extends State<ForgotPasswordScreen> {
  final _email = TextEditingController();
  bool _sent = false;

  @override
  void dispose() {
    _email.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) => AppPage(
        'Reset password',
        ListView(padding: const EdgeInsets.all(20), children: [
          Glass(Column(children: [
            const Icon(Icons.mark_email_read_outlined, size: 54, color: AppColors.blue),
            const SizedBox(height: 14),
            Text(_sent ? 'Check your email' : 'Recover your account',
                style: Theme.of(context).textTheme.titleLarge),
            const SizedBox(height: 9),
            Text(
              _sent
                  ? 'If an account exists for that address, a reset link has been requested. '
                      'Contact your CerviXAI administrator if it does not arrive.'
                  : 'Enter the email associated with your account.',
              textAlign: TextAlign.center,
              style: const TextStyle(color: AppColors.muted),
            ),
            if (!_sent) ...[
              const SizedBox(height: 18),
              appField(_email, 'Email address', Icons.mail_outline_rounded,
                  type: TextInputType.emailAddress),
              const SizedBox(height: 16),
              FilledButton(
                onPressed: () => setState(() => _sent = _email.text.contains('@')),
                child: const Text('REQUEST RESET'),
              ),
            ] else ...[
              const SizedBox(height: 18),
              OutlinedButton(
                onPressed: () => Navigator.pop(context),
                child: const Text('BACK TO SIGN IN'),
              ),
            ],
          ])),
        ]),
      );
}
