# ConvertAnything - Production Setup Guide

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)
```bash
# Run the automated setup script
python run_local.py
```

### Option 2: Manual Setup

1. **Install Python Dependencies**
   ```bash
   pip install -r requirements-backend.txt
   ```

2. **Start Backend API**
   ```bash
   python app.py
   ```

3. **Start Frontend (in another terminal)**
   ```bash
   python -m http.server 8000
   ```

4. **Open Browser**
   Navigate to: http://localhost:8000

## 🔧 System Requirements

- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 2GB free space (for AI models)
- **OS**: Windows, macOS, or Linux

## 📦 Dependencies

### Core Dependencies (Required)
- `flask` - Web API framework
- `flask-cors` - Cross-origin resource sharing
- `openai-whisper` - AI speech recognition
- `torch` - PyTorch deep learning framework

### Optional Dependencies (Enhanced Features)
- `pyannote.audio` - Advanced speaker diarization
- `ffmpeg-python` - Audio file processing
- `speechbrain` - Additional AI models

## 🎯 Production Features

### ✅ Removed Demo Code
- Eliminated all demo/fallback functionality
- Direct integration with Python backend
- Real-time API communication

### ✅ Enhanced Error Handling
- Comprehensive input validation
- Network timeout handling
- User-friendly error notifications
- Graceful degradation

### ✅ Production Optimizations
- File size and type validation
- Request timeout controls
- Progress tracking
- Memory management
- Clean error recovery

### ✅ Professional UI/UX
- Toast notification system
- Loading states and animations
- Responsive design
- Accessibility features

## 🔑 Configuration

### Environment Variables (Optional)
```bash
# For advanced speaker separation
export HF_TOKEN=your_hugging_face_token

# Custom API port
export API_PORT=5000

# Custom frontend port  
export FRONTEND_PORT=8000
```

### Hugging Face Token Setup
1. Visit: https://huggingface.co/settings/tokens
2. Create a free account and generate a token
3. Set the environment variable: `export HF_TOKEN=your_token_here`
4. This enables advanced speaker diarization features

## 📊 API Endpoints

### Health Check
```
GET /api/health
Response: {"status": "healthy", "timestamp": "..."}
```

### Transcribe Audio
```
POST /api/transcribe
Form Data:
  - audio: File (required)
  - model: String (tiny|base|small|medium|large)
  - speaker_separation: Boolean
  - speaker_count: Integer (2-5)

Response: {
  "success": true,
  "result": {
    "text": "Full transcription...",
    "duration": 123.45,
    "language": "en",
    "segments": [...]
  }
}
```

### Available Models
```
GET /api/models
Response: {"models": [...], "default": "base"}
```

## 🎵 Supported Audio Formats

- **MP3** (.mp3) - Most common format
- **WAV** (.wav) - Uncompressed audio
- **M4A** (.m4a) - Apple format
- **FLAC** (.flac) - Lossless compression
- **OGG** (.ogg) - Open source format
- **MP4** (.mp4) - Video files with audio

## 📈 Performance Guidelines

### File Size Limits
- **Maximum**: 100MB per file
- **Recommended**: Under 50MB for best performance
- **Processing Time**: ~1-3 minutes per 10MB

### Model Selection
- **Tiny**: Fastest, lower accuracy (~39 MB)
- **Base**: Recommended balance (~74 MB) ⭐
- **Small**: Better accuracy (~244 MB)
- **Medium**: High accuracy (~769 MB)
- **Large**: Best accuracy (~1550 MB)

## 🔍 Troubleshooting

### Common Issues

1. **Backend API not available**
   - Ensure `python app.py` is running
   - Check port 5000 is not in use
   - Verify dependencies are installed

2. **Speaker separation not working**
   - Install `pyannote.audio`: `pip install pyannote.audio`
   - Set HF_TOKEN environment variable
   - Check internet connection for model downloads

3. **Large files failing**
   - Reduce file size or split audio
   - Check available RAM (models need 2-4GB)
   - Increase timeout in browser settings

4. **Poor transcription quality**
   - Try a larger model (medium/large)
   - Ensure audio is clear and not too quiet
   - Check audio format compatibility

### Performance Optimization

1. **First Run Setup**
   - Models download automatically (1-2GB)
   - Subsequent runs are much faster
   - Keep models cached for best performance

2. **Memory Management**
   - Close other applications when processing large files
   - Use smaller models for longer files
   - Process files individually, not in batches

## 🛡️ Security Notes

- Application runs locally only
- No data sent to external servers (except model downloads)
- Audio files processed entirely on your machine
- Temporary files automatically cleaned up

## 📱 Browser Compatibility

- **Chrome**: Full support ✅
- **Firefox**: Full support ✅
- **Safari**: Full support ✅
- **Edge**: Full support ✅

## 🚀 Production Deployment

For production deployment beyond localhost:

1. **Configure CORS** in `app.py` for your domain
2. **Set up HTTPS** for secure file uploads
3. **Configure reverse proxy** (nginx/apache)
4. **Set up process management** (systemd/supervisor)
5. **Monitor resource usage** (RAM/CPU)

## 📞 Support

If you encounter issues:

1. Check this setup guide
2. Review console logs in browser (F12)
3. Check backend logs in terminal
4. Verify all dependencies are installed
5. Try with a smaller test file first

## 🎯 Success Indicators

You'll know everything is working when:

- ✅ Backend API starts without errors
- ✅ Frontend loads at http://localhost:8000
- ✅ File upload shows green success message
- ✅ Transcription completes with results
- ✅ Export functions work properly

---

**🎵 ConvertAnything v1.0 - Production Ready**

Made with ❤️ for seamless AI audio transcription.
