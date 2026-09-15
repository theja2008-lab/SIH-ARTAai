import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/app_state.dart';
import '../widgets/arta_companion_widget.dart';
import 'onboarding_screens.dart';

class MainScreen extends StatefulWidget {
  const MainScreen({Key? key}) : super(key: key);

  @override
  _MainScreenState createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<AppState>().initializeSession();
    });
  }

  Widget _buildCurrentScreen(AppScreen screen) {
    switch (screen) {
      case AppScreen.languageSelection:
        return const LanguageSelectionScreen();
      case AppScreen.nameCollection:
        return const NameCollectionScreen();
      case AppScreen.ageCollection:
        return const AgeCollectionScreen();
      case AppScreen.documentCapture:
        return const DocumentCaptureScreen();
      case AppScreen.userPhotoCapture:
        return const PhotoCaptureScreen();
      case AppScreen.confirmation:
        return const ConfirmationScreen();
      default:
        return const SizedBox.shrink();
    }
  }

  String _getArtaText(AppScreen screen, String lang) {
    final isTamil = lang == 'ta';
    switch (screen) {
      case AppScreen.languageSelection:
        return isTamil 
            ? "வணக்கம்! நான் ஆர்டா. உங்கள் கைவினைக்கான AI உதவியாளன். மொழியைத் தேர்ந்தெடுக்கவும்." 
            : "Welcome! I am ARTA, your AI companion. Please select your language.";
      case AppScreen.nameCollection:
        return isTamil
            ? "வணக்கம்! உங்கள் பெயர் என்ன என்று உரக்கச் சொல்லுங்கள்."
            : "Hello! Please speak your full name.";
      case AppScreen.ageCollection:
        return isTamil
            ? "உங்கள் வயது என்ன என்று சொல்லுங்கள்."
            : "How old are you?";
      case AppScreen.documentCapture:
        return isTamil
            ? "உங்கள் அடையாள ஆவணத்தைப் பதிவேற்றுங்கள்."
            : "Please attach your identity document.";
      case AppScreen.userPhotoCapture:
        return isTamil
            ? "தயவுசெய்து கேமராவைப் பார்த்து ஒரு புகைப்படம் எடுக்கவும்."
            : "Please look at the camera to take a photo.";
      case AppScreen.confirmation:
        return isTamil
            ? "மிக அருமை! உங்கள் சுயவிவரம் உருவாக்கப்பட்டது."
            : "Excellent! Your profile has been created.";
      default:
        return "";
    }
  }

  @override
  Widget build(BuildContext context) {
    final state = context.watch<AppState>();

    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: LayoutBuilder(
          builder: (context, constraints) {
            // Fix for Flutter Web startup tiny viewport bug
            if (constraints.maxHeight < 100 || constraints.maxWidth < 100) {
              return const SizedBox.shrink();
            }
            return Column(
              children: [
                Expanded(
                  child: AnimatedSwitcher(
                    duration: const Duration(milliseconds: 300),
                    layoutBuilder: (Widget? currentChild, List<Widget> previousChildren) {
                      return Stack(
                        fit: StackFit.expand,
                        alignment: Alignment.center,
                        children: <Widget>[
                          ...previousChildren,
                          if (currentChild != null) currentChild,
                        ],
                      );
                    },
                    child: _buildCurrentScreen(state.currentScreen),
                  ),
                ),
                ArtaCompanionWidget(
                  textToSpeak: _getArtaText(state.currentScreen, state.language),
                  language: state.language,
                ),
              ],
            );
          },
        ),
      ),
    );
  }
}
