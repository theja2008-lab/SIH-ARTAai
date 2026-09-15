/**
 * ARTINO Camera Controller
 * Manages Web MediaDevices API stream capture, live video rendering,
 * canvas frame capture, and camera state machine:
 * CAMERA_IDLE | CAMERA_REQUESTING | CAMERA_ACTIVE | CAMERA_READY | CAMERA_CAPTURED | CAMERA_ERROR
 */

class CameraController {
  constructor(videoElementId, imageElementId, statusElementId) {
    this.videoEl = document.getElementById(videoElementId);
    this.imageEl = document.getElementById(imageElementId);
    this.statusEl = document.getElementById(statusElementId);
    this.stream = null;
    this.capturedDataUrl = null;
    this.state = 'CAMERA_IDLE';
  }

  setState(newState, message = '') {
    this.state = newState;
    console.log(`[Camera State] ${newState}: ${message}`);
    if (this.statusEl) {
      if (message) {
        this.statusEl.innerText = message;
        this.statusEl.style.display = 'block';
      } else {
        this.statusEl.style.display = 'none';
      }
    }
  }

  async startCamera(facingMode = 'user') {
    this.videoEl = this.videoEl || document.getElementById('camera-video');
    this.imageEl = this.imageEl || document.getElementById('camera-img');
    
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      this.setState('CAMERA_ERROR', 'Camera access is not supported by your browser.');
      return false;
    }

    this.stopCamera();
    this.setState('CAMERA_REQUESTING', 'Requesting camera access...');

    try {
      this.stream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: facingMode,
          width: { ideal: 1280 },
          height: { ideal: 720 }
        },
        audio: false
      });

      if (this.videoEl) {
        this.videoEl.srcObject = this.stream;
        this.videoEl.muted = true;
        this.videoEl.playsInline = true;
        
        await new Promise((resolve) => {
          this.videoEl.onloadedmetadata = () => {
            this.videoEl.play()
              .then(resolve)
              .catch(err => {
                console.warn('[Camera] Autoplay error, trying silent play:', err);
                resolve();
              });
          };
        });

        this.videoEl.style.display = 'block';
        if (this.imageEl) this.imageEl.style.display = 'none';
        this.setState('CAMERA_READY', 'Live camera stream active.');
        return true;
      }
    } catch (err) {
      console.error('[Camera Error]', err);
      let userMsg = 'Camera permission denied or camera unavailable.';
      if (err.name === 'NotAllowedError') {
        userMsg = 'Please grant camera permission in your browser to take photos.';
      } else if (err.name === 'NotFoundError') {
        userMsg = 'No camera device found on your device.';
      }
      this.setState('CAMERA_ERROR', userMsg);
      return false;
    }
    return false;
  }

  captureSnapshot() {
    this.videoEl = this.videoEl || document.getElementById('camera-video');
    this.imageEl = this.imageEl || document.getElementById('camera-img');

    if (this.videoEl && this.videoEl.videoWidth > 0) {
      const canvas = document.createElement('canvas');
      canvas.width = this.videoEl.videoWidth;
      canvas.height = this.videoEl.videoHeight;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(this.videoEl, 0, 0, canvas.width, canvas.height);
      
      this.capturedDataUrl = canvas.toDataURL('image/jpeg', 0.88);
      this.stopCamera();

      if (this.imageEl) {
        this.imageEl.src = this.capturedDataUrl;
        this.imageEl.style.display = 'block';
      }
      if (this.videoEl) {
        this.videoEl.style.display = 'none';
      }
      this.setState('CAMERA_CAPTURED', 'Photo captured.');
      return this.capturedDataUrl;
    } else {
      this.setState('CAMERA_ERROR', 'Unable to capture frame from video feed.');
      return null;
    }
  }

  stopCamera() {
    if (this.stream) {
      this.stream.getTracks().forEach(track => track.stop());
      this.stream = null;
    }
    if (this.videoEl) {
      this.videoEl.style.display = 'none';
    }
    if (this.state !== 'CAMERA_CAPTURED') {
      this.setState('CAMERA_IDLE');
    }
  }
}

window.CameraController = CameraController;
