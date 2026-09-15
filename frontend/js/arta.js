/**
 * ARTA Companion Controller
 * Speech Recognition (STT) + Speech Synthesis (TTS) Engine for 10 Indic & Global Languages.
 * Manages Browser Autoplay Audio Unlocking, Voice Matching, Waveform Visualizer,
 * and Circular Avatar State Machine (IDLE, LISTENING, THINKING, SPEAKING, ERROR).
 */

class ArtaCompanion {
  constructor() {
    this.language = 'ta'; // 'ta', 'en', 'te', 'kn', 'ml', 'hi', 'gu', 'mr', 'bn', 'pa'
    this.state = 'IDLE'; // IDLE, LISTENING, THINKING, SPEAKING, ERROR
    this.recognition = null;
    this.synthesis = window.speechSynthesis;
    this.currentUtterance = null;
    this.lastSpokenText = "";
    this.audioUnlocked = false;
    this.availableVoices = [];

    this.initVoices();
    this.initSpeechRecognition();
    this.setupAudioUnlockListeners();
  }

  initVoices() {
    if (this.synthesis) {
      const loadVoices = () => {
        this.availableVoices = this.synthesis.getVoices();
      };
      loadVoices();
      if (this.synthesis.onvoiceschanged !== undefined) {
        this.synthesis.onvoiceschanged = loadVoices;
      }
    }
  }

  setupAudioUnlockListeners() {
    const unlock = () => {
      if (!this.audioUnlocked) {
        this.audioUnlocked = true;
        if (this.synthesis && this.synthesis.resume) {
          this.synthesis.resume();
        }
      }
    };
    window.addEventListener('click', unlock, { once: false });
    window.addEventListener('touchstart', unlock, { once: false });
  }

  getLocaleCode(lang) {
    const locales = {
      ta: 'ta-IN',
      en: 'en-IN',
      te: 'te-IN',
      kn: 'kn-IN',
      ml: 'ml-IN',
      hi: 'hi-IN',
      gu: 'gu-IN',
      mr: 'mr-IN',
      bn: 'bn-IN',
      pa: 'pa-IN'
    };
    return locales[lang] || 'ta-IN';
  }

  initSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      this.recognition = new SpeechRecognition();
      this.recognition.continuous = false;
      this.recognition.interimResults = true;
      this.recognition.lang = this.getLocaleCode(this.language);

      this.recognition.onstart = () => {
        this.setState('LISTENING');
      };

      this.recognition.onresult = (event) => {
        let transcript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          transcript += event.results[i][0].transcript;
        }
        this.updateTranscriptUI(transcript);
        if (event.results[0].isFinal && this.onSpeechResultCallback) {
          this.setState('THINKING');
          this.onSpeechResultCallback(transcript);
        }
      };

      this.recognition.onerror = (event) => {
        console.warn('[ARTA STT] Recognition error:', event.error);
        if (event.error === 'not-allowed') {
          this.setState('ERROR');
          this.updateUI(
            this.language === 'ta'
              ? "மைக் அனுமதி தேவை. தயவுசெய்து அனுமதிக்கவும்."
              : "Microphone permission required. Please allow access."
          );
        } else {
          this.setState('ERROR');
          this.speak(
            this.language === 'ta'
              ? "மன்னிக்கவும், தெளிவாகக் கேட்கவில்லை. மீண்டும் சொல்லுங்கள்."
              : "I didn't catch that clearly. Could you speak again?"
          );
        }
      };

      this.recognition.onend = () => {
        if (this.state === 'LISTENING') {
          this.setState('IDLE');
        }
      };
    }
  }

  setLanguage(lang) {
    this.language = lang;
    if (this.recognition) {
      this.recognition.lang = this.getLocaleCode(lang);
    }
  }

  listen(onResult) {
    this.onSpeechResultCallback = onResult;
    if (this.recognition) {
      try {
        this.recognition.continuous = false;
        this.recognition.lang = this.getLocaleCode(this.language);
        this.recognition.start();
      } catch (e) {
        console.warn('[ARTA STT] Restarting recognition session:', e);
      }
    } else {
      const promptTitle = this.language === 'ta'
        ? "உங்கள் பதிலைப் பேசுங்கள் அல்லது உள்ளிடுங்கள்:"
        : "Speak or enter your response:";
      const input = prompt(promptTitle, "");
      if (input && onResult) {
        onResult(input);
      }
    }
  }

  listenExtended(onResult, durationSeconds = 18) {
    this.onSpeechResultCallback = onResult;
    let accumulatedTranscript = '';
    let recordingTimer = null;

    if (this.recognition) {
      try {
        this.recognition.continuous = true;
        this.recognition.interimResults = true;
        this.recognition.lang = this.getLocaleCode(this.language);

        const stopAndFinalize = () => {
          if (recordingTimer) clearTimeout(recordingTimer);
          try {
            this.recognition.stop();
          } catch (e) {}
          this.setState('THINKING');
          const finalResult = accumulatedTranscript.trim();
          if (onResult) {
            onResult(finalResult || (this.language === 'ta' ? 'பாரம்பரிய கைவினைப் பொருள்' : 'Traditional handcrafted artwork'));
          }
        };

        this.recognition.onresult = (event) => {
          let interim = '';
          for (let i = event.resultIndex; i < event.results.length; i++) {
            if (event.results[i].isFinal) {
              accumulatedTranscript += ' ' + event.results[i][0].transcript;
            } else {
              interim += event.results[i][0].transcript;
            }
          }
          const currentText = (accumulatedTranscript + ' ' + interim).trim();
          this.updateTranscriptUI(currentText);
        };

        this.recognition.onend = () => {
          if (this.state === 'LISTENING' && accumulatedTranscript.length > 0) {
            stopAndFinalize();
          }
        };

        // Start continuous 15-20s session
        this.recognition.start();
        this.setState('LISTENING');

        // Set hard limit duration
        recordingTimer = setTimeout(() => {
          stopAndFinalize();
        }, durationSeconds * 1000);

      } catch (e) {
        console.warn('[ARTA Extended STT] Continuous session error:', e);
        this.listen(onResult);
      }
    } else {
      const promptTitle = this.language === 'ta'
        ? "உங்கள் படைப்பைப் பற்றி 15-20 வினாடிகள் விவரிக்கவும்:"
        : "Describe your artwork (15-20 seconds):";
      const input = prompt(promptTitle, "");
      if (input && onResult) {
        onResult(input);
      }
    }
  }

  speak(text, onEnd) {
    if (!text) return;
    this.lastSpokenText = text;
    this.updateUI(text);

    if (this.synthesis) {
      try {
        // STOP PREVIOUS AUDIO FIRST
        this.synthesis.cancel();
        
        const utterance = new SpeechSynthesisUtterance(text);
        const targetLocale = this.getLocaleCode(this.language);
        utterance.lang = targetLocale;
        utterance.rate = 0.92;

        if (this.availableVoices.length === 0) {
          this.availableVoices = this.synthesis.getVoices();
        }

        const matchedVoice = this.availableVoices.find(v => v.lang === targetLocale || v.lang.startsWith(this.language));
        if (matchedVoice) {
          utterance.voice = matchedVoice;
        }

        utterance.onstart = () => {
          this.setState('SPEAKING');
        };

        utterance.onend = () => {
          this.setState('IDLE');
          if (onEnd) onEnd();
        };

        utterance.onerror = (e) => {
          console.warn('[ARTA TTS] Speech synthesis error:', e);
          this.setState('IDLE');
          if (onEnd) onEnd();
        };

        this.currentUtterance = utterance;
        this.synthesis.speak(utterance);
      } catch (err) {
        console.warn('[ARTA TTS] Audio playback exception:', err);
        this.setState('IDLE');
        if (onEnd) onEnd();
      }
    } else {
      if (onEnd) onEnd();
    }
  }

  replayLastSpeech() {
    if (this.lastSpokenText) {
      this.speak(this.lastSpokenText);
    }
  }

  setState(newState) {
    this.state = newState;
    const avatarEl = document.getElementById('arta-avatar-element');
    const micBtn = document.getElementById('mic-control-button');
    const statusTextEl = document.getElementById('arta-status-text');
    const waveformEl = document.getElementById('arta-waveform-bars');

    if (avatarEl) {
      avatarEl.className = `arta-avatar ${newState.toLowerCase()}`;
    }

    if (statusTextEl) {
      const labels = {
        IDLE: 'ARTA • AI COMPANION',
        LISTENING: '🔴 LISTENING... Speak now',
        THINKING: '◌ THINKING... Understanding',
        SPEAKING: '🔊 ARTA IS SPEAKING...',
        ERROR: '⚠️ PLEASE REPEAT'
      };
      statusTextEl.innerText = labels[newState] || 'ARTA • AI COMPANION';
    }

    if (waveformEl) {
      if (newState === 'SPEAKING' || newState === 'LISTENING') {
        waveformEl.style.display = 'flex';
      } else {
        waveformEl.style.display = 'none';
      }
    }

    if (micBtn) {
      if (newState === 'LISTENING') {
        micBtn.classList.add('listening');
      } else {
        micBtn.classList.remove('listening');
      }
    }
  }

  updateUI(text) {
    const textEl = document.getElementById('arta-speech-text');
    if (textEl) {
      textEl.innerText = text;
    }
  }

  updateTranscriptUI(transcript) {
    const disp = document.getElementById('transcript-display');
    if (disp) {
      disp.innerText = `"${transcript}"`;
    }
  }
}

window.ArtaCompanion = ArtaCompanion;
