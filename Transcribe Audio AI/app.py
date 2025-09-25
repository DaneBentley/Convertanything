#!/usr/bin/env python3
"""
Flask API backend for ConvertAnything web application
Connects the web UI to the Python transcription scripts
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import sys
import tempfile
import json
from pathlib import Path
from datetime import datetime
import traceback

# Import our transcription modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'Transcribe Audio AI'))
from transcribe_audio import transcribe_audio, save_transcription
from transcribe_with_speakers import transcribe_with_speakers, save_speaker_transcription

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Configuration
UPLOAD_FOLDER = 'temp_uploads'
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'm4a', 'flac', 'ogg', 'mp4', 'avi', 'mov'}

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_duration(filepath):
    """Get audio duration using ffmpeg-python or fallback"""
    try:
        import ffmpeg
        probe = ffmpeg.probe(filepath)
        duration = float(probe['streams'][0]['duration'])
        return duration
    except:
        # Fallback - estimate based on file size (very rough)
        file_size = os.path.getsize(filepath)
        # Rough estimate: 1MB per minute for compressed audio
        return file_size / (1024 * 1024) * 60

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'ConvertAnything API is running',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/transcribe', methods=['POST'])
def transcribe_audio_api():
    """Main transcription endpoint"""
    try:
        # Check if file is present
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        file = request.files['audio']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not supported'}), 400
        
        # Get parameters
        model_size = request.form.get('model', 'base')
        speaker_separation = request.form.get('speaker_separation', 'false').lower() == 'true'
        speaker_count = int(request.form.get('speaker_count', '2'))
        
        # Save uploaded file temporarily
        temp_filename = f"temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        temp_filepath = os.path.join(UPLOAD_FOLDER, temp_filename)
        file.save(temp_filepath)
        
        try:
            # Get file duration
            duration = get_file_duration(temp_filepath)
            
            if speaker_separation:
                # Use speaker separation
                print(f"Starting transcription with speaker separation: {temp_filepath}")
                result = transcribe_with_speakers(
                    temp_filepath, 
                    model_size, 
                    speaker_count
                )
            else:
                # Regular transcription
                print(f"Starting regular transcription: {temp_filepath}")
                result = transcribe_audio(temp_filepath, model_size)
                
                # Convert to speaker format for consistency
                if 'segments' not in result:
                    # Create segments from full text (simple splitting)
                    words = result['text'].split()
                    segment_length = len(words) // 5  # 5 segments
                    segments = []
                    
                    for i in range(0, len(words), max(1, segment_length)):
                        segment_words = words[i:i + segment_length]
                        segment_text = ' '.join(segment_words)
                        segments.append({
                            'start': i * 2,  # Rough timing
                            'end': (i + len(segment_words)) * 2,
                            'text': segment_text,
                            'speaker': 'Speaker 1'
                        })
                    
                    result['segments'] = segments
                else:
                    # Add speaker labels to existing segments
                    for segment in result['segments']:
                        if 'speaker' not in segment:
                            segment['speaker'] = 'Speaker 1'
            
            # Ensure we have duration
            if 'duration' not in result:
                result['duration'] = duration
            
            # Format response
            response = {
                'success': True,
                'result': {
                    'text': result.get('text', ''),
                    'duration': result.get('duration', duration),
                    'language': result.get('language', 'unknown'),
                    'segments': result.get('segments', [])
                },
                'metadata': {
                    'filename': file.filename,
                    'model': model_size,
                    'speaker_separation': speaker_separation,
                    'processed_at': datetime.now().isoformat()
                }
            }
            
            return jsonify(response)
            
        finally:
            # Clean up temporary file
            try:
                os.remove(temp_filepath)
            except:
                pass
                
    except Exception as e:
        print(f"Transcription error: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': f'Transcription failed: {str(e)}'
        }), 500

@app.route('/api/models', methods=['GET'])
def get_available_models():
    """Get list of available Whisper models"""
    models = [
        {'id': 'tiny', 'name': 'Tiny', 'description': 'Fastest, lower accuracy (~39 MB)'},
        {'id': 'base', 'name': 'Base', 'description': 'Recommended balance (~74 MB)'},
        {'id': 'small', 'name': 'Small', 'description': 'Better accuracy (~244 MB)'},
        {'id': 'medium', 'name': 'Medium', 'description': 'High accuracy (~769 MB)'},
        {'id': 'large', 'name': 'Large', 'description': 'Best accuracy (~1550 MB)'}
    ]
    
    return jsonify({
        'models': models,
        'default': 'base'
    })

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({'error': 'File too large. Maximum size is 100MB.'}), 413

@app.errorhandler(500)
def internal_error(e):
    """Handle internal server errors"""
    return jsonify({'error': 'Internal server error. Please try again.'}), 500

if __name__ == '__main__':
    print("Starting ConvertAnything API server...")
    print("Available endpoints:")
    print("  GET  /api/health - Health check")
    print("  POST /api/transcribe - Transcribe audio file")
    print("  GET  /api/models - Available models")
    print()
    print("Frontend should be served separately (e.g., with 'python -m http.server')")
    print("Make sure to install dependencies: pip install flask flask-cors")
    print()
    
    # Check if required modules are available
    try:
        import whisper
        print("✓ OpenAI Whisper is available")
    except ImportError:
        print("✗ OpenAI Whisper not found. Install with: pip install openai-whisper")
    
    try:
        from pyannote.audio import Pipeline
        print("✓ Pyannote Audio is available")
    except ImportError:
        print("✗ Pyannote Audio not found. Install with: pip install pyannote.audio")
    
    print("\nStarting server on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
