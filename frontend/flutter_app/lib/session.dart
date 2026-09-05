import 'package:flutter/foundation.dart';

import 'models.dart';
import 'services/api_service.dart';
import 'services/session_store.dart';

/// Single in-memory source of truth for "who is signed in right now" plus
/// the shared [ApiService] instance. Screens read `Session.i.user` and
/// call `Session.i.signIn(...)` / `Session.i.signOut()`; the actual
/// profile and history data always comes fresh from the backend, so
/// restarting the app (or switching devices, once signed back in) never
/// loses it — only the convenience of staying signed in is cached
/// on-device, via [SessionStore].
///
/// Extends [ChangeNotifier] so screens that show cached user info (e.g. the
/// dashboard greeting) can rebuild immediately when the profile is edited,
/// instead of showing a stale name until the next full navigation.
class Session extends ChangeNotifier {
  Session._();
  static final Session i = Session._();

  final api = ApiService();
  AppUser? user;

  /// Bumped whenever a new assessment/screening is saved to history, so
  /// HistoryScreen can auto-refresh itself without a manual pull.
  int historyVersion = 0;

  bool get isSignedIn => user != null && api.token != null;

  /// Attempts to restore a previous session using the token saved on this
  /// device. Returns true if the app can go straight to the dashboard.
  Future<bool> tryRestore() async {
    final token = await SessionStore.readToken();
    if (token == null) return false;
    api.token = token;
    try {
      user = await api.fetchProfile();
      return true;
    } catch (_) {
      // Token is stale/invalid (e.g. server data was reset) — fall back
      // to the sign-in screen instead of getting stuck.
      api.token = null;
      await SessionStore.clear();
      return false;
    }
  }

  Future<void> signInWith(String token, AppUser signedInUser) async {
    api.token = token;
    user = signedInUser;
    await SessionStore.save(token: token, name: signedInUser.name, email: signedInUser.email);
    notifyListeners();
  }

  void updateUser(AppUser updated) {
    user = updated;
    SessionStore.updateCachedName(updated.name, updated.email);
    notifyListeners();
  }

  void markHistoryChanged() {
    historyVersion++;
    notifyListeners();
  }

  Future<void> signOut() async {
    await api.logout();
    api.token = null;
    user = null;
    await SessionStore.clear();
    notifyListeners();
  }
}
