import 'package:flutter/material.dart';

import '../session.dart';
import '../theme.dart';
import '../widgets/common.dart';

class ProfileScreen extends StatefulWidget {
  const ProfileScreen({super.key});
  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  bool _signingOut = false;

  Future<void> _signOut() async {
    setState(() => _signingOut = true);
    await Session.i.signOut();
    if (mounted) Navigator.pushNamedAndRemoveUntil(context, '/login', (_) => false);
  }

  @override
  Widget build(BuildContext context) {
    final user = Session.i.user;
    return Bg(SafeArea(
      child: ListView(padding: const EdgeInsets.fromLTRB(20, 20, 20, 20), children: [
        Text('My profile', style: Theme.of(context).textTheme.titleLarge),
        const SizedBox(height: 16),
        Glass(Column(children: [
          const CircleAvatar(
            radius: 38,
            backgroundColor: AppColors.surfaceAlt,
            child: Icon(Icons.person_rounded, size: 40, color: AppColors.blue),
          ),
          const SizedBox(height: 12),
          Text(user?.name.isNotEmpty == true ? user!.name : 'Healthcare professional',
              textAlign: TextAlign.center, style: Theme.of(context).textTheme.titleLarge),
          Text(user?.email ?? '', style: const TextStyle(color: AppColors.muted)),
          if (user != null) ...[
            const SizedBox(height: 4),
            Text('@${user.username}', style: const TextStyle(color: AppColors.muted, fontSize: 12)),
          ],
        ])),
        const SizedBox(height: 14),
        Glass(
          pad: EdgeInsets.zero,
          Column(children: [
            ListTile(
              leading: const Icon(Icons.edit_outlined),
              title: const Text('Edit profile'),
              trailing: const Icon(Icons.chevron_right_rounded),
              onTap: () async {
                await Navigator.pushNamed(context, '/edit-profile');
                setState(() {});
              },
            ),
            const Divider(height: 1),
            ListTile(
              leading: const Icon(Icons.lock_outline_rounded),
              title: const Text('Change password'),
              trailing: const Icon(Icons.chevron_right_rounded),
              onTap: () => Navigator.pushNamed(context, '/change-password'),
            ),
            const Divider(height: 1),
            ListTile(
              leading: const Icon(Icons.info_outline_rounded),
              title: const Text('About CerviXAI'),
              trailing: const Icon(Icons.chevron_right_rounded),
              onTap: () => Navigator.pushNamed(context, '/about'),
            ),
          ]),
        ),
        const SizedBox(height: 14),
        OutlinedButton.icon(
          onPressed: _signingOut ? null : _signOut,
          icon: _signingOut ? const BusySpinner(color: AppColors.navy) : const Icon(Icons.logout_rounded),
          label: const Text('SIGN OUT'),
        ),
      ]),
    ));
  }
}
