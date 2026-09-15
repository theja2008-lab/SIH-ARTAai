import 'package:flutter/material.dart';
import 'package:flutter_tts/flutter_tts.dart';

class ArtaCompanionWidget extends StatefulWidget {
  final String textToSpeak;
  final String language;

  const ArtaCompanionWidget({
    Key? key,
    required this.textToSpeak,
    required this.language,
  }) : super(key: key);

  @override
  _ArtaCompanionWidgetState createState() => _ArtaCompanionWidgetState();
}

class _ArtaCompanionWidgetState extends State<ArtaCompanionWidget> with SingleTickerProviderStateMixin {
  late FlutterTts flutterTts;
  bool isSpeaking = false;
  late AnimationController _animationController;

  @override
  void initState() {
    super.initState();
    flutterTts = FlutterTts();
    _animationController = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 1),
    )..repeat(reverse: true);
    
    _speak();
  }

  @override
  void didUpdateWidget(covariant ArtaCompanionWidget oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.textToSpeak != widget.textToSpeak || oldWidget.language != widget.language) {
      _speak();
    }
  }

  Future<void> _speak() async {
    if (widget.textToSpeak.isEmpty) return;
    
    await flutterTts.setLanguage(widget.language == 'ta' ? 'ta-IN' : 'en-US');
    await flutterTts.setPitch(1.0);
    await flutterTts.setSpeechRate(0.5); // Adjust rate to sound natural

    flutterTts.setStartHandler(() {
      setState(() {
        isSpeaking = true;
      });
    });

    flutterTts.setCompletionHandler(() {
      setState(() {
        isSpeaking = false;
      });
    });

    flutterTts.setErrorHandler((msg) {
      setState(() {
        isSpeaking = false;
      });
    });

    await flutterTts.speak(widget.textToSpeak);
  }

  @override
  void dispose() {
    flutterTts.stop();
    _animationController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      decoration: BoxDecoration(
        color: Colors.blue.shade50,
        borderRadius: const BorderRadius.vertical(top: Radius.circular(24)),
        boxShadow: const [
          BoxShadow(
            color: Colors.black12,
            blurRadius: 10,
            offset: Offset(0, -2),
          ),
        ],
      ),
      child: Row(
        children: [
          AnimatedBuilder(
            animation: _animationController,
            builder: (context, child) {
              return Transform.scale(
                scale: isSpeaking ? 1.0 + (_animationController.value * 0.1) : 1.0,
                child: Container(
                  width: 48,
                  height: 48,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    gradient: const LinearGradient(
                      colors: [Colors.blue, Colors.purple],
                    ),
                    boxShadow: isSpeaking
                        ? [
                            BoxShadow(
                              color: Colors.blue.withOpacity(0.5),
                              blurRadius: 10,
                              spreadRadius: 2,
                            )
                          ]
                        : null,
                  ),
                  child: const Icon(Icons.psychology, color: Colors.white, size: 28),
                ),
              );
            },
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Text(
              widget.textToSpeak,
              style: const TextStyle(
                fontSize: 14,
                fontWeight: FontWeight.w600,
                color: Colors.blue,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
