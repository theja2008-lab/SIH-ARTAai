import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;

class ApiService {
  // Use 127.0.0.1 for Web, and 10.0.2.2 for Android emulator. 
  static String get baseUrl {
    if (kIsWeb) return 'http://127.0.0.1:8000/api/v1';
    return 'http://10.0.2.2:8000/api/v1';
  }

  static Future<Map<String, dynamic>> startSession({String language = 'ta'}) async {
    final response = await http.post(
      Uri.parse('$baseUrl/session/start'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'language': language}),
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to start session');
    }
  }

  static Future<Map<String, dynamic>> submitVoiceInput(
      String sessionId, String transcript, {String? fieldTarget}) async {
    final response = await http.post(
      Uri.parse('$baseUrl/onboarding/voice-input'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'session_id': sessionId,
        'transcript': transcript,
        'field_target': fieldTarget,
      }),
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to submit voice input');
    }
  }

  static Future<Map<String, dynamic>> verifyDemoIdentity(
      String sessionId, {String documentType = 'aadhaar_demo', String? imageB64}) async {
    final response = await http.post(
      Uri.parse('$baseUrl/identity/verify-demo'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'session_id': sessionId,
        'document_type': documentType,
        'image_b64': imageB64,
      }),
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to verify identity');
    }
  }

  static Future<Map<String, dynamic>> confirmProfile(String sessionId) async {
    final response = await http.post(
      Uri.parse('$baseUrl/onboarding/confirm-profile?session_id=$sessionId'),
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to confirm profile');
    }
  }

  static Future<Map<String, dynamic>> uploadArtwork(String sessionId, {String? filePath}) async {
    var request = http.MultipartRequest('POST', Uri.parse('$baseUrl/artworks/upload'));
    request.fields['session_id'] = sessionId;
    if (filePath != null) {
      request.files.add(await http.MultipartFile.fromPath('file', filePath));
    }
    
    var streamedResponse = await request.send();
    var response = await http.Response.fromStream(streamedResponse);
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to upload artwork');
    }
  }

  static Future<Map<String, dynamic>> extractCatalogFromVoice(
      String sessionId, String artworkId, String transcript) async {
    final response = await http.post(
      Uri.parse('$baseUrl/catalogs/extract-from-voice'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'session_id': sessionId,
        'artwork_id': artworkId,
        'transcript': transcript,
      }),
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to extract catalog');
    }
  }

  static Future<Map<String, dynamic>> correctCatalogField(
      String catalogId, String fieldName, String newValue) async {
    final response = await http.post(
      Uri.parse('$baseUrl/catalogs/$catalogId/correct'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'catalog_id': catalogId,
        'field_name': fieldName,
        'new_value': newValue,
        'source': 'ARTISAN',
      }),
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to correct field');
    }
  }

  static Future<Map<String, dynamic>> approveCatalog(String catalogId) async {
    final response = await http.post(
      Uri.parse('$baseUrl/catalogs/$catalogId/approve'),
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to approve catalog');
    }
  }
}
