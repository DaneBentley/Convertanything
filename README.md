# ConvertAnything - AI Audio Transcription

A modern, minimalist web application for AI-powered audio transcription with speaker separation capabilities.

## 🚀 Features

- **AI-Powered Transcription**: Uses OpenAI Whisper for high-accuracy speech recognition
- **Speaker Separation**: Automatically identifies and separates different speakers using Pyannote AI
- **Multiple Export Formats**: Export transcriptions as TXT, JSON, CSV, SRT subtitles, or PDF
- **Modern UI**: Clean, responsive interface with dark mode support
- **Drag & Drop**: Easy file upload with drag-and-drop functionality
- **Real-time Progress**: Live progress tracking during transcription
- **Multiple Views**: View transcripts by speaker, timeline, or raw text

## 🎯 Live Demo

Visit the live application: [https://danebentley.github.io/Convertanything](https://danebentley.github.io/Convertanything)

## 📱 Screenshots

### Upload Interface
Clean, modern upload area with drag-and-drop support for audio files.

### Processing View
Real-time progress tracking with animated visualizations during transcription.

### Results Dashboard
Comprehensive results with speaker separation, timeline view, and export options.

## 🛠️ Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **AI Models**: OpenAI Whisper, Pyannote Audio
- **Styling**: Modern CSS with CSS Grid and Flexbox
- **Icons**: Font Awesome
- **PDF Export**: jsPDF library
- **Hosting**: GitHub Pages

## 📁 Supported Audio Formats

- MP3 (.mp3)
- WAV (.wav)
- M4A (.m4a)
- FLAC (.flac)
- OGG (.ogg)

## 🎨 Export Options

1. **Text (.txt)**: Clean text format with speaker labels and timestamps
2. **JSON (.json)**: Structured data with metadata and segment information
3. **CSV (.csv)**: Spreadsheet-compatible format for analysis
4. **SRT (.srt)**: Standard subtitle format for video editing
5. **PDF (.pdf)**: Professional document format with formatting

## 🚀 Getting Started

### Online Usage
Simply visit [https://danebentley.github.io/Convertanything](https://danebentley.github.io/Convertanything) and start transcribing!

### Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/DaneBentley/Convertanything.git
   cd Convertanything
   ```

2. **Serve locally**:
   ```bash
   # Using Python
   python -m http.server 8000
   
   # Using Node.js
   npx serve .
   
   # Or any other static server
   ```

3. **Open in browser**:
   Navigate to `http://localhost:8000`

## 🔧 Backend Integration

The current version runs in demo mode. To integrate with the Python backend:

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Hugging Face token** (for speaker diarization):
   ```bash
   export HF_TOKEN=your_hugging_face_token
   ```

3. **Create API endpoint** (example structure):
   ```python
   from flask import Flask, request, jsonify
   from transcribe_with_speakers import transcribe_with_speakers
   
   app = Flask(__name__)
   
   @app.route('/api/transcribe', methods=['POST'])
   def transcribe():
       audio_file = request.files['audio']
       model = request.form.get('model', 'base')
       speaker_separation = request.form.get('speaker_separation') == 'true'
       
       result = transcribe_with_speakers(audio_file, model)
       return jsonify(result)
   ```

4. **Update frontend configuration**:
   Set `demoMode = false` in `script.js` and configure API endpoints.

## 🎯 Model Options

### Whisper Models
- **Tiny**: Fastest, lower accuracy (~39 MB)
- **Base**: Recommended balance (~74 MB)
- **Small**: Better accuracy (~244 MB)
- **Medium**: High accuracy (~769 MB)
- **Large**: Best accuracy (~1550 MB)

### Speaker Diarization
- Automatic speaker detection and separation
- Configurable expected speaker count
- Fallback to simple detection if advanced models unavailable

## 📊 Performance

- **Processing Speed**: Varies by model size and audio length
- **File Size Limit**: 100MB (configurable)
- **Accuracy**: Up to 95%+ with large models
- **Languages**: 99+ languages supported by Whisper

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) for speech recognition
- [Pyannote Audio](https://github.com/pyannote/pyannote-audio) for speaker diarization
- [Font Awesome](https://fontawesome.com/) for icons
- [jsPDF](https://github.com/parallax/jsPDF) for PDF generation

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/DaneBentley/Convertanything/issues) page
2. Create a new issue if needed
3. Provide detailed information about your problem

## 🔮 Future Enhancements

- [ ] Real-time transcription
- [ ] Batch processing
- [ ] Custom vocabulary support
- [ ] Integration with cloud storage
- [ ] Mobile app versions
- [ ] Advanced speaker analytics
- [ ] Multi-language detection
- [ ] Noise reduction preprocessing

---

**Made with ❤️ by [Dane Bentley](https://github.com/DaneBentley)**
