# ConvertAnything - Local Setup Guide

This guide will help you set up ConvertAnything to run locally with real AI transcription capabilities.

## 🚀 Quick Start

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements-backend.txt
   ```

2. **Run the application**:
   ```bash
   python run_local.py
   ```

3. **Open your browser** to `http://localhost:8000`

That's it! The app will automatically connect to the local backend API.

## 📋 Detailed Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- At least 2GB of free disk space (for AI models)
- 4GB+ RAM recommended

### Step-by-Step Installation

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone https://github.com/DaneBentley/Convertanything.git
   cd Convertanything
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements-backend.txt
   ```

4. **Set up Hugging Face token** (for advanced speaker separation):
   ```bash
   # Get a free token from: https://huggingface.co/settings/tokens
   export HF_TOKEN=your_token_here
   
   # Or create a .env file:
   echo "HF_TOKEN=your_token_here" > .env
   ```

### Running the Application

#### Option 1: Quick Start (Recommended)
```bash
python run_local.py
```

This starts both the frontend and backend servers and opens your browser automatically.

#### Option 2: Manual Setup
If you prefer to run servers separately:

**Terminal 1 - Backend API:**
```bash
python app.py
```

**Terminal 2 - Frontend Server:**
```bash
python -m http.server 8000
```

Then visit `http://localhost:8000` in your browser.

## 🎯 Testing the Setup

1. **Upload an audio file** (MP3, WAV, M4A, etc.)
2. **Choose your settings**:
   - Model size (Base recommended for balance of speed/accuracy)
   - Enable speaker separation if you have multiple speakers
3. **Click "Start Transcription"**
4. **Wait for processing** (this may take a few minutes depending on file length)
5. **View and export results** in your preferred format

## 🔧 Configuration Options

### Model Sizes
- **Tiny**: Fastest, ~39MB download, good for quick tests
- **Base**: Recommended, ~74MB download, good balance
- **Small**: Better accuracy, ~244MB download
- **Medium**: High accuracy, ~769MB download
- **Large**: Best accuracy, ~1550MB download

### Speaker Separation
- **Enabled**: Uses Pyannote AI for speaker diarization (requires HF token)
- **Disabled**: Single speaker or manual separation
- **Fallback**: Simple speaker detection if Pyannote unavailable

## 🐛 Troubleshooting

### Common Issues

**"ModuleNotFoundError: No module named 'whisper'"**
```bash
pip install openai-whisper
```

**"Could not load model"**
- Check internet connection (models download on first use)
- Ensure you have enough disk space
- Try a smaller model size first

**"Speaker separation failed"**
- Set up your Hugging Face token
- Or disable speaker separation to use basic transcription

**"Port already in use"**
- Kill existing processes: `pkill -f "python.*app.py"`
- Or use different ports in the configuration

**"CORS errors in browser"**
- Make sure both servers are running
- Check that backend is on port 5000 and frontend on port 8000

### Performance Tips

1. **Use appropriate model size** for your needs
2. **Close other applications** to free up RAM
3. **Use shorter audio files** for faster processing
4. **Enable speaker separation** only when needed

## 📊 Expected Performance

| Model Size | Speed | Accuracy | RAM Usage |
|------------|-------|----------|-----------|
| Tiny       | ~10x  | Good     | ~1GB      |
| Base       | ~7x   | Better   | ~1GB      |
| Small      | ~4x   | High     | ~2GB      |
| Medium     | ~2x   | Higher   | ~5GB      |
| Large      | ~1x   | Best     | ~10GB     |

*Speed relative to audio length (e.g., 10x = 1 minute audio processed in 6 seconds)*

## 🔒 Privacy & Security

- All processing happens locally on your machine
- No audio data is sent to external servers
- Transcription results are stored temporarily and cleaned up automatically
- You have full control over your data

## 📞 Support

If you encounter issues:

1. Check this troubleshooting guide
2. Look at console output for error messages
3. Create an issue on GitHub with:
   - Your operating system
   - Python version
   - Error messages
   - Steps to reproduce

## 🚀 Next Steps

Once you have the basic setup working:

1. **Try different model sizes** to find the best balance for your needs
2. **Experiment with speaker separation** on multi-speaker audio
3. **Test various audio formats** and lengths
4. **Explore export options** for your workflow
5. **Consider deploying** to a server for team use

Happy transcribing! 🎵→📝
