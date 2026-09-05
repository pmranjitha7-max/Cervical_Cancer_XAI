import 'package:shared_preferences/shared_preferences.dart';

/// Persists only the auth token (and a light cache of the signed-in user's
/// name/email for instant display) on-device, so the app can stay signed
/// in across restarts. The actual profile and history data always come
/// live from the backend — this is not a local data store for that.
class SessionStore {
  SessionStore._();
  static const _tokenKey = 'auth_token';
  static const _nameKey = 'cached_name';
  static const _emailKey = 'cached_email';

  static Future<void> save({
    required String token,
    required String name,
    required String email,
  }) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_tokenKey, token);
    await prefs.setString(_nameKey, name);
    await prefs.setString(_emailKey, email);
  }

  static Future<String?> readToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_tokenKey);
  }

  static Future<String?> readCachedName() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_nameKey);
  }

  static Future<void> updateCachedName(String name, String email) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_nameKey, name);
    await prefs.setString(_emailKey, email);
  }

  static Future<void> clear() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_tokenKey);
    await prefs.remove(_nameKey);
    await prefs.remove(_emailKey);
  }
}
