import 'package:flutter/material.dart';

import '../session.dart';
import '../theme.dart';
import 'home_screen.dart';
import 'history_screen.dart';
import 'image_screening_screen.dart';
import 'profile_screen.dart';

/// The signed-in app shell: a bottom-navigation frame around the four
/// main sections. Replacing the original's flat "push a new full-screen
/// route for everything" navigation with tabs is one of the bigger
/// "make this feel like a real product" changes.
class ShellScreen extends StatefulWidget {
  const ShellScreen({super.key});
  @override
  State<ShellScreen> createState() => _ShellScreenState();
}

class _ShellScreenState extends State<ShellScreen> {
  int _index = 0;

  static const _tabs = [
    HomeScreen(),
    HistoryScreen(),
    ImageScreeningScreen(),
    ProfileScreen(),
  ];

  @override
  Widget build(BuildContext context) => Scaffold(
        // Listens to Session so the dashboard greeting / profile tab refresh
        // immediately after an edit, instead of waiting for the next full
        // navigation. _tabs is a const list, so the tab widgets themselves
        // (and their internal State, e.g. History's fetched list) are
        // unaffected by this outer rebuild.
        body: AnimatedBuilder(
          animation: Session.i,
          builder: (context, _) => IndexedStack(index: _index, children: _tabs),
        ),
        bottomNavigationBar: NavigationBarTheme(
          data: NavigationBarThemeData(
            indicatorColor: AppColors.blue.withValues(alpha: .14),
            labelTextStyle: WidgetStateProperty.resolveWith((states) => TextStyle(
                  fontSize: 12,
                  fontWeight: states.contains(WidgetState.selected) ? FontWeight.w700 : FontWeight.w500,
                  color: states.contains(WidgetState.selected) ? AppColors.blue : AppColors.muted,
                )),
          ),
          child: NavigationBar(
            selectedIndex: _index,
            onDestinationSelected: (i) => setState(() => _index = i),
            backgroundColor: Colors.white,
            elevation: 3,
            destinations: const [
              NavigationDestination(icon: Icon(Icons.dashboard_outlined), selectedIcon: Icon(Icons.dashboard_rounded), label: 'Dashboard'),
              NavigationDestination(icon: Icon(Icons.history_outlined), selectedIcon: Icon(Icons.history_rounded), label: 'History'),
              NavigationDestination(icon: Icon(Icons.image_search_outlined), selectedIcon: Icon(Icons.image_search_rounded), label: 'Screening'),
              NavigationDestination(icon: Icon(Icons.person_outline_rounded), selectedIcon: Icon(Icons.person_rounded), label: 'Profile'),
            ],
          ),
        ),
      );
}
