import 'dart:convert';
import 'dart:typed_data';

import 'package:http/http.dart' as http;

import '../models.dart';

const kApiBaseUrl = String.fromEnvironment(
  'API_BASE_URL',
  defaultValue: 'http://10.206.116.238:8000',
);

class ApiException implements Exception {
  ApiException(this.message);
  final String message;
  @override
  String toString() => message;
}

/// Thin wrapper around the CerviXAI FastAPI backend. Every call throws an
/// [ApiException] with a human-readable message on failure, so screens can
/// show `e.toString()` directly without re-parsing errors.
class ApiService {
  ApiService({this.token});

  /// Bearer token for the signed-in user, or null when signed out. When
  /// set, /cancer-report and /image-screening also save to that user's
  /// server-side history automatically.
  String? token;

  Map<String, String> get _authHeaders =>
      token == null ? {} : {'Authorization': 'Bearer $token'};

  Uri _uri(String path, [Map<String, dynamic>? query]) => Uri.parse('$kApiBaseUrl$path').replace(
        queryParameters: query?.map((k, v) => MapEntry(k, '$v')),
      );

  String _extractError(http.Response r) {
    try {
      final body = jsonDecode(r.body);
      if (body is Map && body['detail'] != null) return body['detail'].toString();
    } catch (_) {/* fall through */}
    return 'Server returned ${r.statusCode}. Please try again.';
  }

  Future<Map<String, dynamic>> _postJson(String path, Map<String, dynamic> body, {bool auth = false}) async {
    final http.Response r;
    try {
      r = await http
          .post(
            _uri(path),
            headers: {
              'Content-Type': 'application/json',
              if (auth) ..._authHeaders,
            },
            body: jsonEncode(body),
          )
          .timeout(const Duration(seconds: 20));
    } catch (_) {
      throw ApiException('Could not reach the server. Check your connection and the backend address.');
    }
    if (r.statusCode >= 200 && r.statusCode < 300) {
      return jsonDecode(r.body) as Map<String, dynamic>;
    }
    throw ApiException(_extractError(r));
  }

  Future<Map<String, dynamic>> _getJson(String path, {Map<String, dynamic>? query, bool auth = false}) async {
    final http.Response r;
    try {
      r = await http.get(_uri(path, query), headers: auth ? _authHeaders : null).timeout(const Duration(seconds: 30));
    } catch (_) {
      throw ApiException('Could not reach the server. Check your connection and the backend address.');
    }
    if (r.statusCode >= 200 && r.statusCode < 300) {
      return jsonDecode(r.body) as Map<String, dynamic>;
    }
    throw ApiException(_extractError(r));
  }

  Future<void> _delete(String path) async {
    final http.Response r;
    try {
      r = await http.delete(_uri(path), headers: _authHeaders).timeout(const Duration(seconds: 15));
    } catch (_) {
      throw ApiException('Could not reach the server. Check your connection and the backend address.');
    }
    if (r.statusCode < 200 || r.statusCode >= 300) {
      throw ApiException(_extractError(r));
    }
  }

  // ---------------------------------------------------------------
  // Auth
  // ---------------------------------------------------------------

  Future<(String, AppUser)> register({
    required String name,
    required String username,
    required String email,
    required String password,
  }) async {
    final j = await _postJson('/auth/register', {
      'name': name,
      'username': username,
      'email': email,
      'password': password,
    });
    return (j['token'] as String, AppUser.fromJson(j['user'] as Map<String, dynamic>));
  }

  Future<(String, AppUser)> login({required String username, required String password}) async {
    final j = await _postJson('/auth/login', {'username': username, 'password': password});
    return (j['token'] as String, AppUser.fromJson(j['user'] as Map<String, dynamic>));
  }

  Future<void> logout() async {
    try {
      await _postJson('/auth/logout', {}, auth: true);
    } catch (_) {
      // Logging out locally should always succeed even if the network call fails.
    }
  }

  // ---------------------------------------------------------------
  // Profile
  // ---------------------------------------------------------------

  Future<AppUser> fetchProfile() async {
    final j = await _getJson('/profile', auth: true);
    return AppUser.fromJson(j);
  }

  Future<AppUser> updateProfile({required String name, required String email}) async {
    final http.Response r;
    try {
      r = await http
          .put(
            _uri('/profile'),
            headers: {'Content-Type': 'application/json', ..._authHeaders},
            body: jsonEncode({'name': name, 'email': email}),
          )
          .timeout(const Duration(seconds: 15));
    } catch (_) {
      throw ApiException('Could not reach the server. Check your connection and the backend address.');
    }
    if (r.statusCode >= 200 && r.statusCode < 300) {
      return AppUser.fromJson(jsonDecode(r.body) as Map<String, dynamic>);
    }
    throw ApiException(_extractError(r));
  }

  Future<void> changePassword({required String currentPassword, required String newPassword}) =>
      _postJson('/auth/change-password', {
        'current_password': currentPassword,
        'new_password': newPassword,
      }, auth: true);

  // ---------------------------------------------------------------
  // Assessments
  // ---------------------------------------------------------------

  Future<AssessmentReport> runAssessment(int patientId) async {
    final j = await _getJson('/cancer-report', query: {'patient_id': patientId}, auth: true);
    return AssessmentReport.fromJson(j);
  }
  Future<Uint8List> downloadCancerReportPdf(int patientId) async {
  final http.Response r;

  try {
    r = await http
        .get(
          _uri('/cancer-report/pdf', {'patient_id': patientId}),
          headers: _authHeaders,
        )
        .timeout(const Duration(seconds: 30));
  } catch (_) {
    throw ApiException(
      'Could not reach the server. Check your connection and the backend address.',
    );
  }

  if (r.statusCode >= 200 && r.statusCode < 300) {
    return r.bodyBytes;
  }

  throw ApiException(_extractError(r));
}

  Future<ImageScreeningReport> runImageScreening(Uint8List bytes, String filename) async {
    final uri = _uri('/image-screening');
    final request = http.MultipartRequest('POST', uri)
      ..headers.addAll(_authHeaders)
      ..files.add(http.MultipartFile.fromBytes('file', bytes, filename: filename));
    http.StreamedResponse streamed;
    try {
      streamed = await request.send().timeout(const Duration(seconds: 40));
    } catch (_) {
      throw ApiException('Could not reach the server. Check your connection and the backend address.');
    }
    final r = await http.Response.fromStream(streamed);
    if (r.statusCode >= 200 && r.statusCode < 300) {
      return ImageScreeningReport.fromJson(jsonDecode(r.body) as Map<String, dynamic>);
    }
    throw ApiException(_extractError(r));
  }

  // ---------------------------------------------------------------
  // History
  // ---------------------------------------------------------------

  Future<List<HistoryEntry>> fetchHistory() async {
    final j = await _getJson('/history', auth: true);
    final list = j['history'] as List? ?? [];
    return list.whereType<Map<String, dynamic>>().map(HistoryEntry.fromJson).toList();
  }

  Future<void> clearHistory() => _delete('/history');

  Future<void> deleteHistoryEntry(int id) => _delete('/history/$id');

Future<Uint8List> downloadImageScreeningPdf(
  Uint8List imageBytes,
  String filename,
) async {
  final request = http.MultipartRequest(
    'POST',
    _uri('/image-screening/pdf'),
  );

  request.headers.addAll(_authHeaders);

  request.files.add(
    http.MultipartFile.fromBytes(
      'file',
      imageBytes,
      filename: filename,
    ),
  );

  try {
    final streamedResponse =
        await request.send().timeout(const Duration(seconds: 30));

    final response = await http.Response.fromStream(streamedResponse);

    if (response.statusCode >= 200 && response.statusCode < 300) {
      return response.bodyBytes;
    }

    throw ApiException(_extractError(response));
  } catch (e) {
    if (e is ApiException) rethrow;

    throw ApiException(
      'Could not reach the server. Check your connection and the backend address.',
    );
  }
}
}
