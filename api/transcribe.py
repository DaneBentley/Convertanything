from http.server import BaseHTTPRequestHandler
import json
import os
import tempfile
import cgi
from datetime import datetime
import traceback
from io import BytesIO

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Set CORS headers
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            # Parse multipart form data
            content_type = self.headers.get('Content-Type', '')
            if not content_type.startswith('multipart/form-data'):
                self._send_error(400, 'Content-Type must be multipart/form-data')
                return
                
            # Get content length
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self._send_error(400, 'No data received')
                return
                
            # Read the POST data
            post_data = self.rfile.read(content_length)
            
            # Parse form data
            form_data = cgi.FieldStorage(
                fp=BytesIO(post_data),
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )
            
            # Check if audio file is present
            if 'audio' not in form_data:
                self._send_error(400, 'No audio file provided')
                return
                
            audio_file = form_data['audio']
            if not audio_file.filename:
                self._send_error(400, 'No file selected')
                return
            
            # Get parameters
            model_size = form_data.getvalue('model', 'base')
            speaker_separation = form_data.getvalue('speaker_separation', 'false').lower() == 'true'
            speaker_count = int(form_data.getvalue('speaker_count', '2'))
            
            # Validate file type
            allowed_extensions = {'mp3', 'wav', 'm4a', 'flac', 'ogg', 'mp4'}
            filename_lower = audio_file.filename.lower()
            if not any(filename_lower.endswith('.' + ext) for ext in allowed_extensions):
                self._send_error(400, 'File type not supported')
                return
            
            # Check file size (Vercel has limits)
            max_size = int(os.getenv('MAX_FILE_SIZE', '10')) * 1024 * 1024  # Default 10MB
            file_content = audio_file.file.read()
            
            if len(file_content) > max_size:
                self._send_error(400, f'File too large for serverless processing. Maximum size: {max_size // (1024*1024)}MB')
                return
            
            # Process transcription
            if os.getenv('OPENAI_API_KEY'):
                result = self._transcribe_with_openai_api(file_content, audio_file.filename, model_size, speaker_separation)
            else:
                result = self._transcribe_fallback(audio_file.filename, model_size, speaker_separation)
            
            # Send successful response
            response = {
                'success': True,
                'result': result,
                'metadata': {
                    'filename': audio_file.filename,
                    'model': model_size,
                    'speaker_separation': speaker_separation,
                    'processed_at': datetime.now().isoformat(),
                    'environment': 'vercel_serverless'
                }
            }
            
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            print(f"Transcription error: {str(e)}")
            print(traceback.format_exc())
            self._send_error(500, f'Transcription failed: {str(e)}')
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def _send_error(self, code, message):
        """Send error response"""
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        error_response = {
            'success': False,
            'error': message
        }
        self.wfile.write(json.dumps(error_response).encode())
    
    def _transcribe_with_openai_api(self, file_content, filename, model_size, speaker_separation):
        """Use OpenAI API for transcription"""
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            
            # Save file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{filename.split(".")[-1]}') as tmp_file:
                tmp_file.write(file_content)
                tmp_file.flush()
                
                # Use OpenAI Whisper API
                with open(tmp_file.name, 'rb') as audio_file:
                    transcript = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        response_format="verbose_json"
                    )
                
                # Clean up temp file
                os.unlink(tmp_file.name)
            
            # Format response to match our expected structure
            result = {
                'text': transcript.text,
                'duration': getattr(transcript, 'duration', 0),
                'language': getattr(transcript, 'language', 'unknown'),
                'segments': []
            }
            
            # Convert OpenAI segments to our format
            if hasattr(transcript, 'segments') and transcript.segments:
                for i, segment in enumerate(transcript.segments):
                    formatted_segment = {
                        'start': segment.get('start', 0),
                        'end': segment.get('end', 0),
                        'text': segment.get('text', ''),
                        'speaker': f'Speaker {(i % 2) + 1}' if speaker_separation else 'Speaker 1'
                    }
                    result['segments'].append(formatted_segment)
            else:
                # Create basic segments if not provided
                words = result['text'].split()
                segment_size = max(10, len(words) // 5)
                
                for i in range(0, len(words), segment_size):
                    segment_words = words[i:i + segment_size]
                    result['segments'].append({
                        'start': i * 2,
                        'end': (i + len(segment_words)) * 2,
                        'text': ' '.join(segment_words),
                        'speaker': f'Speaker {(i // segment_size % 2) + 1}' if speaker_separation else 'Speaker 1'
                    })
            
            return result
            
        except Exception as e:
            raise Exception(f"OpenAI API transcription failed: {str(e)}")
    
    def _transcribe_fallback(self, filename, model_size, speaker_separation):
        """Fallback transcription for demonstration purposes"""
        return {
            'text': f'Transcription placeholder for file: {filename}. To enable real transcription, configure OPENAI_API_KEY environment variable in Vercel dashboard.',
            'duration': 60,
            'language': 'en',
            'segments': [
                {
                    'start': 0,
                    'end': 30,
                    'text': f'This is a placeholder transcription for {filename}.',
                    'speaker': 'Speaker 1'
                },
                {
                    'start': 30,
                    'end': 60,
                    'text': 'Configure OpenAI API key in Vercel dashboard for real transcription.',
                    'speaker': 'Speaker 2' if speaker_separation else 'Speaker 1'
                }
            ]
        }