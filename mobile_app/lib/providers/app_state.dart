import 'package:flutter/material.dart';
import '../services/api_service.dart';

enum AppScreen {
  languageSelection,
  nameCollection,
  ageCollection,
  documentCapture,
  userPhotoCapture,
  confirmation
}

class AppState extends ChangeNotifier {
  String? sessionId;
  String language = 'ta'; // default to Tamil
  AppScreen currentScreen = AppScreen.languageSelection;
  
  Map<String, dynamic> profileData = {
    'name': '',
    'age': '',
    'experience_years': '',
    'craft_expertise': '',
    'document_name': null,
    'photo_b64': null,
  };

  Future<void> initializeSession() async {
    try {
      final res = await ApiService.startSession(language: language);
      sessionId = res['session_id'];
      // The backend returns a current_state, but we will manage local state explicitly.
      // e.g. res['current_state'] == 'LANGUAGE_SELECTION'
      notifyListeners();
    } catch (e) {
      debugPrint('[App] Backend connection fallback, using local session ID');
      sessionId = 'SES-${DateTime.now().millisecondsSinceEpoch}';
      notifyListeners();
    }
  }

  void setLanguage(String lang) {
    language = lang;
    currentScreen = AppScreen.nameCollection;
    notifyListeners();
  }

  void updateName(String name) {
    profileData['name'] = name;
    notifyListeners();
  }

  void confirmName() {
    currentScreen = AppScreen.ageCollection;
    notifyListeners();
  }

  void updateAge(String age) {
    profileData['age'] = age;
    notifyListeners();
  }

  void confirmAge() {
    currentScreen = AppScreen.documentCapture;
    notifyListeners();
  }

  void setDocument(String docName, String b64Image) {
    profileData['document_name'] = docName;
    profileData['document_b64'] = b64Image;
    notifyListeners();
  }

  void confirmDocument() {
    currentScreen = AppScreen.userPhotoCapture;
    notifyListeners();
  }
  
  void setPhoto(String b64Image) {
    profileData['photo_b64'] = b64Image;
    notifyListeners();
  }
  
  void confirmPhoto() {
    currentScreen = AppScreen.confirmation;
    notifyListeners();
  }

  Future<void> submitVoiceData(String transcript, String fieldTarget) async {
    if (sessionId != null) {
      try {
        final res = await ApiService.submitVoiceInput(sessionId!, transcript, fieldTarget: fieldTarget);
        if (res['status'] == 'success') {
           if (fieldTarget == 'name' && res['parsed_data'] != null && res['parsed_data']['name'] != null) {
              updateName(res['parsed_data']['name']);
           }
           if (fieldTarget == 'age' && res['parsed_data'] != null && res['parsed_data']['age'] != null) {
              updateAge(res['parsed_data']['age'].toString());
           }
        }
      } catch (e) {
        debugPrint('Voice submission failed: $e');
      }
    }
  }
}
