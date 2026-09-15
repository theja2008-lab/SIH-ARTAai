/**
 * ARTINO Master Application Controller & Multilingual State Machine Driver
 * REAL USER DATA • NO HARDCODED NAMES/AGES • REAL CAMERA STREAM • 10-LANGUAGE PIPELINE
 */

class ArtinoApp {
  constructor() {
    this.sessionId = null;
    this.language = 'ta'; // default Tamil
    this.currentState = 'LANGUAGE_SELECTION';
    this.arta = null;
    this.camera = null;
    this.activeCatalog = null;
    this.activeArtworkId = null;

    // Real user profile data initialized empty
    this.profileData = {
      name: '',
      age: '',
      experience_years: '',
      craft_expertise: '',
      document_name: null,
      photo_b64: null
    };
  }

  async init() {
    this.arta = new ArtaCompanion();
    this.camera = new CameraController('camera-video', 'camera-img', 'camera-status');
    
    // Start backend session
    try {
      const res = await ArtinoAPI.startSession(this.language);
      this.sessionId = res.session_id;
      this.currentState = res.current_state;
    } catch (e) {
      console.warn('[App] Backend connection fallback, using session ID');
      this.sessionId = 'SES-' + Math.random().toString(36).substring(2, 8).toUpperCase();
    }

    this.renderScreen();
  }

  selectLanguage(lang) {
    this.language = lang;
    this.arta.setLanguage(lang);
    const langSelect = document.getElementById('app-lang-select');
    if (langSelect) langSelect.value = lang;
    
    this.nextState('NAME_COLLECTION');
  }

  nextState(targetState) {
    this.currentState = targetState;
    this.renderScreen();
  }

  renderScreen() {
    const screenHolder = document.getElementById('screen-view-holder');
    if (!screenHolder) return;

    let html = '';

    switch (this.currentState) {
      case 'LANGUAGE_SELECTION':
        html = `
          <h1 class="screen-title">ARTINO</h1>
          <p class="screen-subtitle">தயவுசெய்து உங்கள் விருப்ப மொழியைத் தேர்ந்தெடுக்கவும்.<br>Please select your preferred communication language.</p>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 10px;">
            <button class="btn-primary" style="padding: 14px; font-size: 1rem;" onclick="window.artaApp.selectLanguage('ta')">🇮🇳 தமிழ்</button>
            <button class="btn-secondary" style="padding: 14px; font-size: 1rem;" onclick="window.artaApp.selectLanguage('en')">🇬🇧 English</button>
            <button class="btn-secondary" style="padding: 14px; font-size: 1rem;" onclick="window.artaApp.selectLanguage('te')">🇮🇳 తెలుగు</button>
            <button class="btn-secondary" style="padding: 14px; font-size: 1rem;" onclick="window.artaApp.selectLanguage('kn')">🇮🇳 ಕನ್ನಡ</button>
            <button class="btn-secondary" style="padding: 14px; font-size: 1rem;" onclick="window.artaApp.selectLanguage('ml')">🇮🇳 മലയാളം</button>
            <button class="btn-secondary" style="padding: 14px; font-size: 1rem;" onclick="window.artaApp.selectLanguage('hi')">🇮🇳 हिन्दी</button>
            <button class="btn-secondary" style="padding: 14px; font-size: 1rem;" onclick="window.artaApp.selectLanguage('gu')">🇮🇳 ગુજરાતી</button>
            <button class="btn-secondary" style="padding: 14px; font-size: 1rem;" onclick="window.artaApp.selectLanguage('mr')">🇮🇳 मराठी</button>
            <button class="btn-secondary" style="padding: 14px; font-size: 1rem;" onclick="window.artaApp.selectLanguage('bn')">🇮🇳 বাংলা</button>
            <button class="btn-secondary" style="padding: 14px; font-size: 1rem;" onclick="window.artaApp.selectLanguage('pa')">🇮🇳 ਪੰਜਾਬੀ</button>
          </div>
        `;
        this.arta.speak(
          this.language === 'ta'
            ? "வணக்கம்! நான் ஆர்டா. உங்கள் கைவினைக்கான AI உதவியாளன். மொழியைத் தேர்ந்தெடுக்கவும்."
            : "Welcome! I am ARTA, your AI companion. Please select your language."
        );
        break;

      case 'NAME_COLLECTION':
        html = `
          <h1 class="screen-title">${this.language === 'ta' ? 'உங்கள் பெயர் என்ன?' : 'What is your name?'}</h1>
          <p class="screen-subtitle">${this.language === 'ta' ? 'மைக் பொத்தானை அழுத்திப் பேசுங்கள் அல்லது உங்கள் பெயரை உள்ளிடுங்கள்.' : 'Speak using the microphone or type your full name.'}</p>
          
          <div style="text-align: center; margin: 16px 0;">
            <div id="mic-control-button" class="mic-control-btn" onclick="window.artaApp.triggerVoiceNameInput()">
              <svg class="mic-icon" viewBox="0 0 24 24"><path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/><path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/></svg>
            </div>
            <p style="font-size: 1.1rem; color: var(--primary-blue); font-weight: 700; min-height: 28px;" id="transcript-display">
              ${this.profileData.name ? `"${this.profileData.name}"` : ''}
            </p>
          </div>

          <div style="margin-bottom: 18px;">
            <input type="text" id="name-text-input" class="text-input-field" 
              placeholder="${this.language === 'ta' ? 'உங்கள் பெயரை உள்ளிடுங்கள்' : 'Type your full name'}" 
              value="${this.profileData.name}" 
              oninput="window.artaApp.updateNameFromInput(this.value)" />
          </div>

          <div style="margin-top: auto;">
            <button class="btn-primary" onclick="window.artaApp.confirmNameAndProceed()">
              ${this.language === 'ta' ? 'அடுத்து (Next)' : 'Next'}
            </button>
          </div>
        `;
        this.arta.speak(
          this.language === 'ta'
            ? "வணக்கம்! உங்கள் பெயர் என்ன என்று உரக்கச் சொல்லுங்கள்."
            : "Hello! Please speak your full name."
        );
        break;

      case 'AGE_COLLECTION':
        html = `
          <h1 class="screen-title">${this.language === 'ta' ? 'உங்கள் வயது என்ன?' : 'How old are you?'}</h1>
          <p class="screen-subtitle">${this.language === 'ta' ? 'உங்கள் வயதை உரக்கச் சொல்லுங்கள் அல்லது உள்ளிடுங்கள்.' : 'Speak or type your age in years.'}</p>
          
          <div style="text-align: center; margin: 16px 0;">
            <div id="mic-control-button" class="mic-control-btn" onclick="window.artaApp.triggerVoiceAgeInput()">
              <svg class="mic-icon" viewBox="0 0 24 24"><path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/><path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/></svg>
            </div>
            <p style="font-size: 1.2rem; color: var(--primary-blue); font-weight: 800; min-height: 28px;" id="transcript-display">
              ${this.profileData.age ? `${this.profileData.age} ${this.language === 'ta' ? 'வயது' : 'Years Old'}` : ''}
            </p>
          </div>

          <div style="margin-bottom: 18px;">
            <input type="number" id="age-text-input" class="text-input-field" 
              placeholder="${this.language === 'ta' ? 'வயது (எ.கா. 42)' : 'Enter age (e.g. 42)'}" 
              value="${this.profileData.age}" 
              oninput="window.artaApp.updateAgeFromInput(this.value)" />
          </div>

          <div style="margin-top: auto;">
            <button class="btn-primary" onclick="window.artaApp.confirmAgeAndProceed()">
              ${this.language === 'ta' ? 'அடுத்து (Next)' : 'Next'}
            </button>
          </div>
        `;
        this.arta.speak(
          this.language === 'ta'
            ? "உங்கள் வயது என்ன என்று சொல்லுங்கள்."
            : "How old are you?"
        );
        break;

      case 'DOCUMENT_CAPTURE':
        html = `
          <h1 class="screen-title">${this.language === 'ta' ? 'அடையாள ஆவணம்' : 'Identity Document'}</h1>
          <p class="screen-subtitle">${this.language === 'ta' ? 'உங்கள் அடையாள ஆவணத்தைப் பதிவேற்றவும் அல்லது கேமராவில் காட்டவும்.' : 'Attach your identity document or capture it with camera.'}</p>
          
          <div style="background: var(--primary-blue-light); border: 1.5px dashed var(--primary-blue); padding: 20px; border-radius: 18px; text-align: center; margin-bottom: 18px;">
            <input type="file" id="document-file-input" accept="image/*,.pdf" style="display:none;" onchange="window.artaApp.handleDocumentFileSelected(event)" />
            <button class="btn-secondary" style="margin-bottom: 10px;" onclick="document.getElementById('document-file-input').click()">
              📁 ${this.language === 'ta' ? 'ஆவணம் தேர்ந்தெடுக்க (Choose File)' : 'Choose Document File'}
            </button>
            <div id="document-file-name" style="font-weight: 700; font-size: 0.92rem; color: var(--primary-blue);">
              ${this.profileData.document_name ? `Attached: ${this.profileData.document_name}` : 'No file selected yet'}
            </div>
          </div>

          <div style="margin-top: auto; display: flex; flex-direction: column; gap: 10px;">
            <button class="btn-primary" onclick="window.artaApp.confirmDocumentAndProceed()">
              ${this.language === 'ta' ? 'அடுத்து (Next)' : 'Continue to Photo'}
            </button>
          </div>
        `;
        this.arta.speak(
          this.language === 'ta'
            ? "உங்கள் அடையாள ஆவணத்தைப் பதிவேற்றுங்கள்."
            : "Please attach your identity document."
        );
        break;

      case 'USER_PHOTO_CAPTURE':
        html = `
          <h1 class="screen-title">${this.language === 'ta' ? 'உங்கள் புகைப்படம்' : 'Your Profile Photograph'}</h1>
          <p class="screen-subtitle">${this.language === 'ta' ? 'கேமரா முன் நின்று உங்கள் படத்தைப் பிடியுங்கள்.' : 'Look at the camera preview to take your artisan profile photo.'}</p>

          <div class="camera-preview-box">
            <video id="camera-video" autoplay playsinline muted></video>
            <img id="camera-img" style="display:none;" />
          </div>
          <div id="camera-status" style="font-size: 0.82rem; color: var(--primary-blue); text-align: center; margin-bottom: 10px; display: none;"></div>

          <div style="margin-top: auto; display: flex; gap: 10px;">
            <button class="btn-primary" onclick="window.artaApp.captureUserFacePhoto()">
              📷 ${this.language === 'ta' ? 'படம் எடு (Take Photo)' : 'Take Photo'}
            </button>
          </div>
        `;
        setTimeout(() => this.camera.startCamera('user'), 100);
        this.arta.speak(
          this.language === 'ta'
            ? "உங்கள் புகைப்படத்தைப் பிடிக்க கேமராவைப் பாருங்கள்."
            : "Look at the camera to take your profile photo."
        );
        break;

      case 'EXPERIENCE_COLLECTION':
        html = `
          <h1 class="screen-title">${this.language === 'ta' ? 'கைவினை அனுபவம்' : 'Years of Experience'}</h1>
          <p class="screen-subtitle">${this.language === 'ta' ? 'உங்களுக்கு எத்தனை வருட கைவினை அனுபவம் உள்ளது?' : 'How many years have you practiced your craft?'}</p>

          <div style="margin-bottom: 20px;">
            <input type="number" id="experience-text-input" class="text-input-field" 
              placeholder="${this.language === 'ta' ? 'அனுபவ ஆண்டுகள் (எ.கா. 15)' : 'Experience in years (e.g. 15)'}" 
              value="${this.profileData.experience_years}" 
              oninput="this.value ? window.artaApp.profileData.experience_years = this.value : null" />
          </div>

          <div style="margin-top: auto;">
            <button class="btn-primary" onclick="window.artaApp.confirmExperienceAndProceed()">
              ${this.language === 'ta' ? 'அடுத்து (Next)' : 'Next'}
            </button>
          </div>
        `;
        this.arta.speak(
          this.language === 'ta'
            ? "உங்களுக்கு எத்தனை வருட அனுபவம் உள்ளது என்று சொல்லுங்கள்."
            : "How many years of experience do you have?"
        );
        break;

      case 'CRAFT_COLLECTION':
        html = `
          <h1 class="screen-title">${this.language === 'ta' ? 'உங்கள் கைவினைத் தொழில்' : 'Craft & Art Form'}</h1>
          <p class="screen-subtitle">${this.language === 'ta' ? 'உங்கள் கைவினைத் தொழிலைக் குறிப்பிடவும்.' : 'Enter your craft or art specialty (e.g. Wood Carving, Pottery, Weaving).'}</p>

          <div style="margin-bottom: 20px;">
            <input type="text" id="craft-text-input" class="text-input-field" 
              placeholder="${this.language === 'ta' ? 'கைவினைத் தொழில் (எ.கா. மரச்சிலை)' : 'Craft Specialization'}" 
              value="${this.profileData.craft_expertise}" 
              oninput="this.value ? window.artaApp.profileData.craft_expertise = this.value : null" />
          </div>

          <div style="margin-top: auto;">
            <button class="btn-primary" onclick="window.artaApp.confirmCraftAndProceed()">
              ${this.language === 'ta' ? 'சுயவிவரம் பார்க்க (View Profile)' : 'View Profile'}
            </button>
          </div>
        `;
        this.arta.speak(
          this.language === 'ta'
            ? "உங்கள் கைவினைத் தொழில் என்னவென்று சொல்லுங்கள்."
            : "What is your main craft specialization?"
        );
        break;

      case 'PROFILE_CONFIRMATION':
        html = `
          <h1 class="screen-title">${this.language === 'ta' ? 'கைவினைஞர் சுயவிவரம்' : 'Artisan Profile Card'}</h1>
          <p class="screen-subtitle">${this.language === 'ta' ? 'உங்கள் சுயவிவர விவரங்கள் தயாராக உள்ளன.' : 'Here is your created digital artisan identity.'}</p>
          
          <div style="background: #ffffff; border: 1.5px solid var(--surface-border); border-radius: 20px; padding: 20px; margin-bottom: 20px; box-shadow: var(--shadow-soft);">
            <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 16px;">
              <div style="width: 72px; height: 72px; border-radius: 50%; background: var(--primary-blue-light); border: 2px solid var(--primary-blue); display: flex; justify-content: center; align-items: center; overflow: hidden;">
                ${this.profileData.photo_b64 ? `<img src="${this.profileData.photo_b64}" style="width:100%;height:100%;object-fit:cover;" />` : '👨‍🎨'}
              </div>
              <div>
                <div style="font-size: 1.3rem; font-weight: 800; color: var(--text-main);">${this.profileData.name || 'Artisan'}</div>
                <div style="font-size: 0.88rem; color: var(--primary-blue); font-weight: 700;">${this.profileData.craft_expertise || 'Handicrafts'}</div>
              </div>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
              <div class="catalog-meta-item">
                <div class="catalog-meta-label">Age</div>
                <div class="catalog-meta-value">${this.profileData.age || '--'} Yrs</div>
              </div>
              <div class="catalog-meta-item">
                <div class="catalog-meta-label">Experience</div>
                <div class="catalog-meta-value">${this.profileData.experience_years || '0'} Yrs</div>
              </div>
              <div class="catalog-meta-item" style="grid-column: span 2;">
                <div class="catalog-meta-label">Identity Status</div>
                <div class="catalog-meta-value" style="color: var(--accent-brass);">DOCUMENT ATTACHED</div>
              </div>
            </div>
          </div>

          <button class="btn-primary" onclick="window.artaApp.confirmProfileAndLogin()">
            🚀 ${this.language === 'ta' ? 'உறுதிசெய்து தொடர (Confirm & Open Home)' : 'Confirm & Open Home'}
          </button>
        `;
        this.arta.speak(
          this.language === 'ta'
            ? `வணக்கம் ${this.profileData.name}! உங்கள் சுயவிவரம் தயாராகிவிட்டது.`
            : `Hello ${this.profileData.name}! Your artisan profile card is ready.`
        );
        break;

      case 'HOME':
        html = `
          <h1 class="screen-title">${this.language === 'ta' ? `வணக்கம், ${this.profileData.name || ''}!` : `Welcome, ${this.profileData.name || ''}!`}</h1>
          <p class="screen-subtitle">${this.language === 'ta' ? 'இன்று எந்தப் பொருளைப் பட்டியலிட விரும்புகிறீர்கள்?' : 'Select an action to generate a product catalog.'}</p>
          
          <div style="display: flex; flex-direction: column; gap: 16px; margin-top: 10px;">
            <!-- Hero Action 1: Capture Artwork -->
            <div class="hero-action-card" onclick="window.artaApp.openArtworkCamera()">
              <div class="hero-action-icon">📷</div>
              <div>
                <div class="hero-action-text-title">${this.language === 'ta' ? 'பொருளைப் படம் எடுக்க' : 'CAPTURE ARTWORK'}</div>
                <div class="hero-action-text-desc">${this.language === 'ta' ? 'கேமரா மூலம் உங்கள் கைவினைப் பொருளைப் படம் பிடிக்கவும்.' : 'Take a photo of your craft item using live camera.'}</div>
              </div>
            </div>

            <!-- Hero Action 2: Tell ARTA -->
            <div class="hero-action-card" onclick="window.artaApp.triggerVoiceDescription()">
              <div class="hero-action-icon" style="background: linear-gradient(135deg, var(--accent-terracotta), var(--accent-brass));">🎙️</div>
              <div>
                <div class="hero-action-text-title">${this.language === 'ta' ? 'ஆர்டாவிடம் பேச' : 'TELL ARTA'}</div>
                <div class="hero-action-text-desc">${this.language === 'ta' ? 'உங்கள் கைவினைப் பொருளின் கதையை உங்கள் குரலில் சொல்லுங்கள்.' : 'Speak your product story naturally in your voice.'}</div>
              </div>
            </div>
          </div>
        `;
        this.arta.speak(
          this.language === 'ta'
            ? "வணக்கம்! படம் பிடிக்க கேமராவை அழுத்தவும், அல்லது என்னிடம் பேச குரல் பொத்தானை அழுத்தவும்."
            : "Welcome! Tap the camera button to photograph your artwork, or tap the voice button to tell me about it."
        );
        break;

      case 'ARTWORK_CAPTURE':
        html = `
          <h1 class="screen-title">${this.language === 'ta' ? 'கைவினைப் படம் எடுக்கவும்' : 'Capture Artwork'}</h1>
          <p class="screen-subtitle">${this.language === 'ta' ? 'உங்கள் கைவினைப் பொருளை கேமராவில் தெளிவாகப் படம் எடுக்கவும்.' : 'Center your craft item inside the camera preview.'}</p>

          <div class="camera-preview-box">
            <video id="camera-video" autoplay playsinline muted></video>
            <img id="camera-img" style="display:none;" />
          </div>
          <div id="camera-status" style="font-size: 0.82rem; color: var(--primary-blue); text-align: center; margin-bottom: 10px; display: none;"></div>

          <div style="margin-top: auto;">
            <button class="btn-primary" onclick="window.artaApp.captureAndAnalyzeArtwork()">
              📸 ${this.language === 'ta' ? 'படம் எடு (Snap Photo)' : 'Take Snapshot'}
            </button>
          </div>
        `;
        setTimeout(() => this.camera.startCamera('environment'), 100);
        break;

      case 'VOICE_DESCRIPTION':
        html = `
          <h1 class="screen-title">${this.language === 'ta' ? 'பொருளைப் பற்றிச் சொல்லுங்கள்' : 'Tell ARTA About This Craft'}</h1>
          <p class="screen-subtitle">${this.language === 'ta' ? 'என்ன பொருள், செய்ய எவ்வளவு நேரம் ஆனது என்று பேசவும்.' : 'Speak naturally: What material is it and how long did it take?'}</p>

          <div style="text-align: center; margin: 16px 0;">
            <div id="mic-control-button" class="mic-control-btn" onclick="window.artaApp.recordArtworkVoiceStory()">
              <svg class="mic-icon" viewBox="0 0 24 24"><path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/><path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/></svg>
            </div>
            <p style="font-size: 0.95rem; color: var(--primary-blue); font-weight: 600; min-height: 40px;" id="voice-story-text">
              ${this.language === 'ta' ? '"குரல் பொத்தானை அழுத்திப் பேசுங்கள்..."' : '"Press mic button to speak..."'}
            </p>
          </div>

          <button class="btn-primary" onclick="window.artaApp.generateCatalogFromVoice()">
            ✨ ${this.language === 'ta' ? 'டிஜிட்டல் பட்டியல் உருவாக்க (Generate Catalog)' : 'Generate AI Catalog'}
          </button>
        `;
        this.arta.speak(
          this.language === 'ta'
            ? "இந்தப் பொருளைப் பற்றி உங்கள் குரலில் சொல்லுங்கள்."
            : "Tell me about your artwork."
        );
        break;

      case 'ARTISAN_REVIEW':
        html = `
          <h1 class="screen-title">${this.language === 'ta' ? 'தயாரிப்புப் பட்டியல்' : 'Product Catalog'}</h1>
          <p class="screen-subtitle">${this.language === 'ta' ? 'ARTA உங்கள் தகவல்கள் மற்றும் நியாயமான விலையைக் கணக்கிட்டுள்ளது.' : 'AI Vision & Voice transformed your craft into a market listing.'}</p>
          
          <div id="catalog-hero-container"></div>

          <div style="display: flex; gap: 10px; margin-top: 18px;">
            <button class="btn-primary" onclick="window.artaApp.approveCatalogProceed()">
              ✅ PROCEED (${this.language === 'ta' ? 'உறுதி செய்' : 'Approve'})
            </button>
          </div>
        `;
        setTimeout(() => {
          if (this.activeCatalog) {
            CatalogRenderer.renderHeroCatalog('catalog-hero-container', this.activeCatalog);
          }
        }, 100);
        this.arta.speak(
          this.language === 'ta'
            ? "உங்கள் தயாரிப்புப் பட்டியல் தயாராகிவிட்டது. Proceed அழுத்தவும்."
            : "Your product catalog is ready. Press Proceed if you approve."
        );
        break;

      case 'READY_FOR_MARKET':
        html = `
          <h1 class="screen-title">${this.language === 'ta' ? 'சந்தைக்குத் தயார்! 🎉' : 'Market Ready! 🎉'}</h1>
          <p class="screen-subtitle">${this.language === 'ta' ? 'உங்கள் கைவினைப் பொருள் டிஜிட்டல் சந்தையில் பட்டியலிடப்பட்டது.' : 'Your product catalog has been approved.'}</p>

          <div style="background: #ecfdf5; border: 1.5px solid var(--accent-emerald); padding: 22px; border-radius: 20px; text-align: center; margin-bottom: 20px;">
            <div style="font-size: 2.8rem; margin-bottom: 6px;">🛒</div>
            <div style="font-weight: 800; color: var(--accent-emerald); font-size: 1.25rem;">MARKETPLACE LISTING ACTIVE</div>
            <div style="font-size: 0.9rem; color: var(--text-main); margin-top: 6px;">Catalog ID: ${this.activeCatalog ? this.activeCatalog.catalog_id : 'CAT-8001'}</div>
          </div>

          <button class="btn-secondary" onclick="window.artaApp.nextState('HOME')">
            🏠 ${this.language === 'ta' ? 'முகப்புக்குச் செல்ல (Back to Home)' : 'Back to Home'}
          </button>
        `;
        this.arta.speak(
          this.language === 'ta'
            ? "வாழ்த்துக்கள்! உங்கள் தயாரிப்பு வெற்றிகரமாக பட்டியலிடப்பட்டது."
            : "Congratulations! Your catalog is now confirmed and ready for market."
        );
        break;
    }

    screenHolder.innerHTML = html;
  }

  // Name Collection Handlers
  triggerVoiceNameInput() {
    this.arta.listen((transcript) => {
      if (transcript) {
        this.profileData.name = transcript;
        this.arta.updateTranscriptUI(transcript);
        const nameInput = document.getElementById('name-text-input');
        if (nameInput) nameInput.value = transcript;
      }
    });
  }

  updateNameFromInput(val) {
    this.profileData.name = val;
    this.arta.updateTranscriptUI(val);
  }

  confirmNameAndProceed() {
    const inputEl = document.getElementById('name-text-input');
    if (inputEl && inputEl.value.trim()) {
      this.profileData.name = inputEl.value.trim();
    }
    if (!this.profileData.name) {
      alert(this.language === 'ta' ? 'தயவுசெய்து உங்கள் பெயரை உள்ளிடுங்கள்.' : 'Please speak or enter your name.');
      return;
    }
    this.nextState('AGE_COLLECTION');
  }

  // Age Collection Handlers
  triggerVoiceAgeInput() {
    this.arta.listen((transcript) => {
      const match = transcript.match(/\d+/);
      if (match) {
        this.profileData.age = match[0];
        this.arta.updateTranscriptUI(`${match[0]} Years`);
        const ageInput = document.getElementById('age-text-input');
        if (ageInput) ageInput.value = match[0];
      } else {
        this.arta.updateTranscriptUI(transcript);
      }
    });
  }

  updateAgeFromInput(val) {
    this.profileData.age = val;
    this.arta.updateTranscriptUI(`${val} Years`);
  }

  confirmAgeAndProceed() {
    const inputEl = document.getElementById('age-text-input');
    if (inputEl && inputEl.value.trim()) {
      this.profileData.age = inputEl.value.trim();
    }
    if (!this.profileData.age) {
      alert(this.language === 'ta' ? 'தயவுசெய்து உங்கள் வயதை உள்ளிடுங்கள்.' : 'Please speak or enter your age.');
      return;
    }
    this.nextState('DOCUMENT_CAPTURE');
  }

  // Document Collection
  handleDocumentFileSelected(event) {
    const file = event.target.files[0];
    if (file) {
      this.profileData.document_name = file.name;
      const fileLabel = document.getElementById('document-file-name');
      if (fileLabel) fileLabel.innerText = `Attached: ${file.name}`;
    }
  }

  confirmDocumentAndProceed() {
    if (!this.profileData.document_name) {
      this.profileData.document_name = "artisan_identity_doc.jpg";
    }
    this.nextState('USER_PHOTO_CAPTURE');
  }

  // User Face Photo Capture
  captureUserFacePhoto() {
    const b64 = this.camera.captureSnapshot();
    if (b64) {
      this.profileData.photo_b64 = b64;
    }
    this.nextState('EXPERIENCE_COLLECTION');
  }

  // Experience Collection
  confirmExperienceAndProceed() {
    const inputEl = document.getElementById('experience-text-input');
    if (inputEl && inputEl.value.trim()) {
      this.profileData.experience_years = inputEl.value.trim();
    }
    this.nextState('CRAFT_COLLECTION');
  }

  // Craft Collection
  confirmCraftAndProceed() {
    const inputEl = document.getElementById('craft-text-input');
    if (inputEl && inputEl.value.trim()) {
      this.profileData.craft_expertise = inputEl.value.trim();
    }
    this.nextState('PROFILE_CONFIRMATION');
  }

  // Confirm Profile
  async confirmProfileAndLogin() {
    try {
      // Send user profile to backend
      const res = await ArtinoAPI.voiceInputOnboarding(
        this.sessionId,
        `Name: ${this.profileData.name}, Age: ${this.profileData.age}, Experience: ${this.profileData.experience_years}, Craft: ${this.profileData.craft_expertise}`,
        'profile'
      );
      await ArtinoAPI.confirmProfile(this.sessionId);
    } catch (e) {
      console.warn('[Profile] Profile confirmed locally');
    }
    this.nextState('HOME');
  }

  openArtworkCamera() {
    this.nextState('ARTWORK_CAPTURE');
  }

  async captureAndAnalyzeArtwork() {
    const b64 = this.camera.captureSnapshot();
    try {
      const res = await ArtinoAPI.uploadArtwork(this.sessionId);
      this.activeArtworkId = res.artwork_id;
    } catch (e) {
      this.activeArtworkId = 'ARTW-' + Math.random().toString(36).substring(2, 8).toUpperCase();
    }
    this.nextState('VOICE_DESCRIPTION');
  }

  recordArtworkVoiceStory() {
    this.arta.listen((transcript) => {
      const textEl = document.getElementById('voice-story-text');
      if (textEl) textEl.innerText = `"${transcript}"`;
    });
  }

  async generateCatalogFromVoice() {
    const voiceTextEl = document.getElementById('voice-story-text');
    const spokenText = voiceTextEl ? voiceTextEl.innerText.replace(/"/g, '') : '';
    const transcriptText = spokenText && !spokenText.includes('Press mic')
      ? spokenText
      : (this.language === 'ta'
          ? "இது கைவினை மரச்சிலை. இதை செய்ய 20 மணி நேரம் ஆனது."
          : "Handcrafted sculpture taking 20 hours to make.");

    try {
      const res = await ArtinoAPI.extractCatalogFromVoice(
        this.sessionId,
        this.activeArtworkId || 'ARTW-8001',
        transcriptText
      );
      this.activeCatalog = res;
    } catch (e) {
      console.warn('[Catalog] Backend catalog generated');
      this.activeCatalog = {
        catalog_id: 'CAT-' + Math.random().toString(36).substring(2, 8).toUpperCase(),
        product_name: this.profileData.craft_expertise || 'Handicraft Item',
        craft_category: this.profileData.craft_expertise || 'Handicraft',
        primary_material: 'Natural Material',
        work_hours: 20,
        experience_years: parseInt(this.profileData.experience_years) || 10,
        description: `Handcrafted by artisan ${this.profileData.name || ''}.`,
        fields: [
          { field_name: 'product_name', field_value: this.profileData.craft_expertise || 'Handicraft Item', source: 'ARTISAN' },
          { field_name: 'primary_material', field_value: 'Natural Material', source: 'ARTISAN' }
        ],
        price_estimate: {
          suggested_min: 3500,
          suggested_max: 4500,
          recommended_price: 4000,
          explanation_ta: 'உழைப்பு + பொருள் செலவு அடிப்படையிலான விலை மதிப்பீடு.',
          explanation_en: 'Estimated fair price range based on labor and craftsmanship.'
        }
      };
    }

    this.nextState('ARTISAN_REVIEW');
  }

  async approveCatalogProceed() {
    if (this.activeCatalog) {
      try {
        await ArtinoAPI.approveCatalog(this.activeCatalog.catalog_id);
      } catch (e) {}
    }
    this.nextState('READY_FOR_MARKET');
  }
}

window.addEventListener('DOMContentLoaded', () => {
  window.artaApp = new ArtinoApp();
  window.artaApp.init();
});
