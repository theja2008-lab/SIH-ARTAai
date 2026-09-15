import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/app_state.dart';

class LanguageSelectionScreen extends StatelessWidget {
  const LanguageSelectionScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(24.0),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const SizedBox(height: 20),
          const Text(
            'ARTINO',
            style: TextStyle(fontSize: 32, fontWeight: FontWeight.bold, color: Colors.blue),
          ),
          const SizedBox(height: 8),
          const Text(
            'தயவுசெய்து உங்கள் விருப்ப மொழியைத் தேர்ந்தெடுக்கவும்.\nPlease select your preferred communication language.',
            textAlign: TextAlign.center,
            style: TextStyle(fontSize: 16, color: Colors.grey),
          ),
          const SizedBox(height: 32),
          GridView.count(
            crossAxisCount: 2,
            childAspectRatio: 2.5,
            shrinkWrap: true, // Fix for unbounded height in Column
            physics: const NeverScrollableScrollPhysics(), // Let SingleChildScrollView handle scrolling
            mainAxisSpacing: 10,
            crossAxisSpacing: 10,
            children: [
              _buildLangBtn(context, 'ta', '🇮🇳 தமிழ்'),
              _buildLangBtn(context, 'en', '🇬🇧 English'),
              _buildLangBtn(context, 'te', '🇮🇳 తెలుగు'),
              _buildLangBtn(context, 'kn', '🇮🇳 ಕನ್ನಡ'),
              _buildLangBtn(context, 'ml', '🇮🇳 മലയാളം'),
              _buildLangBtn(context, 'hi', '🇮🇳 हिन्दी'),
              _buildLangBtn(context, 'gu', '🇮🇳 ગુજરાતી'),
              _buildLangBtn(context, 'mr', '🇮🇳 मराठी'),
              _buildLangBtn(context, 'bn', '🇮🇳 বাংলা'),
              _buildLangBtn(context, 'pa', '🇮🇳 ਪੰਜਾਬੀ'),
            ],
          ),
          const SizedBox(height: 20),
        ],
      ),
    );
  }

  Widget _buildLangBtn(BuildContext context, String code, String label) {
    return ElevatedButton(
      style: ElevatedButton.styleFrom(
        backgroundColor: code == 'ta' ? Colors.blue : Colors.grey.shade200,
        foregroundColor: code == 'ta' ? Colors.white : Colors.black87,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      ),
      onPressed: () {
        context.read<AppState>().setLanguage(code);
      },
      child: Text(label, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
    );
  }
}

class NameCollectionScreen extends StatelessWidget {
  const NameCollectionScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final state = context.watch<AppState>();
    final isTamil = state.language == 'ta';

    return CustomScrollView(
      slivers: [
        SliverFillRemaining(
          hasScrollBody: false,
          child: Padding(
            padding: const EdgeInsets.all(24.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const SizedBox(height: 20),
                Text(
                  isTamil ? 'உங்கள் பெயர் என்ன?' : 'What is your name?',
                  style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 8),
                Text(
                  isTamil ? 'மைக் பொத்தானை அழுத்திப் பேசுங்கள் அல்லது உங்கள் பெயரை உள்ளிடுங்கள்.' : 'Speak using the microphone or type your full name.',
                  style: const TextStyle(fontSize: 16, color: Colors.grey),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 40),
                GestureDetector(
                  onTap: () {
                    ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Voice input triggered...')));
                  },
                  child: Container(
                    height: 80,
                    width: 80,
                    decoration: BoxDecoration(
                      color: Colors.blue.shade100,
                      shape: BoxShape.circle,
                    ),
                    alignment: Alignment.center,
                    child: const Icon(Icons.mic, size: 40, color: Colors.blue),
                  ),
                ),
                const SizedBox(height: 24),
                TextField(
                  decoration: InputDecoration(
                    hintText: isTamil ? 'உங்கள் பெயரை உள்ளிடுங்கள்' : 'Type your full name',
                    border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                    filled: true,
                    fillColor: Colors.grey.shade100,
                  ),
                  onChanged: (val) => context.read<AppState>().updateName(val),
                ),
                const SizedBox(height: 40),
                const Expanded(child: SizedBox()), // Replaces Spacer for SliverFillRemaining
                ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    backgroundColor: Colors.blue,
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                  ),
                  onPressed: () => context.read<AppState>().confirmName(),
                  child: Text(isTamil ? 'அடுத்து (Next)' : 'Next', style: const TextStyle(fontSize: 18, color: Colors.white)),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }
}

class AgeCollectionScreen extends StatelessWidget {
  const AgeCollectionScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final state = context.watch<AppState>();
    final isTamil = state.language == 'ta';

    return CustomScrollView(
      slivers: [
        SliverFillRemaining(
          hasScrollBody: false,
          child: Padding(
            padding: const EdgeInsets.all(24.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const SizedBox(height: 20),
                Text(
                  isTamil ? 'உங்கள் வயது என்ன?' : 'How old are you?',
                  style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 8),
                Text(
                  isTamil ? 'உங்கள் வயதை உரக்கச் சொல்லுங்கள் அல்லது உள்ளிடுங்கள்.' : 'Speak or type your age in years.',
                  style: const TextStyle(fontSize: 16, color: Colors.grey),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 40),
                GestureDetector(
                  onTap: () {
                    ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Voice input triggered...')));
                  },
                  child: Container(
                    height: 80,
                    width: 80,
                    decoration: BoxDecoration(
                      color: Colors.blue.shade100,
                      shape: BoxShape.circle,
                    ),
                    alignment: Alignment.center,
                    child: const Icon(Icons.mic, size: 40, color: Colors.blue),
                  ),
                ),
                const SizedBox(height: 24),
                TextField(
                  keyboardType: TextInputType.number,
                  decoration: InputDecoration(
                    hintText: isTamil ? 'வயது (எ.கா. 42)' : 'Enter age (e.g. 42)',
                    border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                    filled: true,
                    fillColor: Colors.grey.shade100,
                  ),
                  onChanged: (val) => context.read<AppState>().updateAge(val),
                ),
                const SizedBox(height: 40),
                const Expanded(child: SizedBox()),
                ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    backgroundColor: Colors.blue,
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                  ),
                  onPressed: () => context.read<AppState>().confirmAge(),
                  child: Text(isTamil ? 'அடுத்து (Next)' : 'Next', style: const TextStyle(fontSize: 18, color: Colors.white)),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }
}

class DocumentCaptureScreen extends StatelessWidget {
  const DocumentCaptureScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final state = context.watch<AppState>();
    final isTamil = state.language == 'ta';

    return CustomScrollView(
      slivers: [
        SliverFillRemaining(
          hasScrollBody: false,
          child: Padding(
            padding: const EdgeInsets.all(24.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const SizedBox(height: 20),
                Text(
                  isTamil ? 'அடையாள ஆவணம்' : 'Identity Document',
                  style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 8),
                Text(
                  isTamil ? 'உங்கள் அடையாள ஆவணத்தைப் பதிவேற்றவும் அல்லது கேமராவில் காட்டவும்.' : 'Attach your identity document or capture it with camera.',
                  style: const TextStyle(fontSize: 16, color: Colors.grey),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 40),
                GestureDetector(
                  onTap: () {
                    ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('File picker triggered...')));
                  },
                  child: Container(
                    padding: const EdgeInsets.all(32),
                    decoration: BoxDecoration(
                      color: Colors.blue.shade50,
                      border: Border.all(color: Colors.blue, width: 2, style: BorderStyle.solid),
                      borderRadius: BorderRadius.circular(16),
                    ),
                    child: Column(
                      children: [
                        const Icon(Icons.folder, size: 48, color: Colors.blue),
                        const SizedBox(height: 8),
                        Text(
                          isTamil ? 'ஆவணம் தேர்ந்தெடுக்க (Choose File)' : 'Choose Document File',
                          style: const TextStyle(color: Colors.blue, fontWeight: FontWeight.bold),
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 40),
                const Expanded(child: SizedBox()),
                ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    backgroundColor: Colors.blue,
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                  ),
                  onPressed: () => context.read<AppState>().confirmDocument(),
                  child: Text(isTamil ? 'அடுத்து (Next)' : 'Continue to Photo', style: const TextStyle(fontSize: 18, color: Colors.white)),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }
}

class PhotoCaptureScreen extends StatelessWidget {
  const PhotoCaptureScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final state = context.watch<AppState>();
    final isTamil = state.language == 'ta';

    return CustomScrollView(
      slivers: [
        SliverFillRemaining(
          hasScrollBody: false,
          child: Padding(
            padding: const EdgeInsets.all(24.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const SizedBox(height: 20),
                Text(
                  isTamil ? 'உங்கள் புகைப்படம்' : 'Your Profile Photograph',
                  style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 8),
                Text(
                  isTamil ? 'கேமரா முன் நின்று உங்கள் படத்தைப் பிடியுங்கள்.' : 'Look at the camera preview to take your artisan profile photo.',
                  style: const TextStyle(fontSize: 16, color: Colors.grey),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 40),
                Container(
                  height: 300,
                  decoration: BoxDecoration(
                    color: Colors.black12,
                    borderRadius: BorderRadius.circular(16),
                  ),
                  alignment: Alignment.center,
                  child: const Icon(Icons.camera_alt, size: 64, color: Colors.black45),
                ),
                const SizedBox(height: 40),
                const Expanded(child: SizedBox()),
                ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    backgroundColor: Colors.blue,
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                  ),
                  onPressed: () => context.read<AppState>().confirmPhoto(),
                  child: Text(isTamil ? 'படம் எடு (Take Photo)' : 'Take Photo', style: const TextStyle(fontSize: 18, color: Colors.white)),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }
}

class ConfirmationScreen extends StatelessWidget {
  const ConfirmationScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final isTamil = context.watch<AppState>().language == 'ta';
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.check_circle, color: Colors.green, size: 80),
            const SizedBox(height: 24),
            Text(
              isTamil ? 'சுயவிவரம் உறுதிப்படுத்தப்பட்டது!' : 'Profile Confirmed!',
              style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 16),
            Text(
              isTamil ? 'உங்கள் விவரங்கள் வெற்றிகரமாக சமர்ப்பிக்கப்பட்டன.' : 'Your details have been successfully submitted.',
              style: const TextStyle(fontSize: 16, color: Colors.grey),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }
}
