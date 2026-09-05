import 'package:flutter/material.dart';

import '../services/api_service.dart';
import '../session.dart';
import '../widgets/common.dart';

/// This screen is the actual fix for "profile edit not working" — the
/// original app only had a read-only profile view with no way to change
/// anything. Saving here calls PUT /profile, so the change is persisted
/// server-side and is still there after signing out or reinstalling.
class EditProfileScreen extends StatefulWidget {
  const EditProfileScreen({super.key});
  @override
  State<EditProfileScreen> createState() => _EditProfileScreenState();
}

class _EditProfileScreenState extends State<EditProfileScreen> {
  late final TextEditingController _name;
  late final TextEditingController _email;
  String? _error;
  bool _busy = false;

  @override
  void initState() {
    super.initState();
    final user = Session.i.user;
    _name = TextEditingController(text: user?.name ?? '');
    _email = TextEditingController(text: user?.email ?? '');
  }

  @override
  void dispose() {
    _name.dispose();
    _email.dispose();
    super.dispose();
  }

  Future<void> _save() async {
    if (_name.text.trim().length < 2 || !_email.text.contains('@')) {
      setState(() => _error = 'Enter your full name and a valid email address.');
      return;
    }
    setState(() {
      _busy = true;
      _error = null;
    });
    try {
      final updated = await Session.i.api.updateProfile(
        name: _name.text.trim(),
        email: _email.text.trim(),
      );
      Session.i.updateUser(updated);
      if (mounted) {
        Navigator.pop(context);
        showSnack(context, 'Profile updated.');
      }
    } on ApiException catch (e) {
      setState(() => _error = e.message);
    } finally {
      if (mounted) setState(() => _busy = false);
    }
  }

  @override
  Widget build(BuildContext context) => AppPage(
        'Edit profile',
        ListView(padding: const EdgeInsets.all(20), children: [
          Glass(Column(children: [
            appField(_name, 'Full name', Icons.badge_outlined),
            const SizedBox(height: 12),
            appField(_email, 'Email address', Icons.mail_outline_rounded, type: TextInputType.emailAddress),
            if (_error != null) InlineNotice(_error!),
            const SizedBox(height: 16),
            FilledButton(
              onPressed: _busy ? null : _save,
              child: _busy ? const BusySpinner() : const Text('SAVE CHANGES'),
            ),
          ])),
        ]),
      );
}
