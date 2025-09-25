import os
import tempfile
import json
from datetime import datetime
import traceback

def handler(request):
    """
    Transcription endpoint for Vercel
    
    Note: This is a serverless adaptation. For full AI functionality,
    consider using external AI services or a dedicated server.
    """
    
    if request.method != 'POST':
        return {'error': 'Method not allowed'}, 405
    
    try:
        # Check if file is present
        if 'audio' not in request.files:
            return {
                'success': False,
                'error': 'No audio file provided'
            }, 400
        
        file = request.files['audio']
        if file.filename == '':
            return {
                'success': False,
                'error': 'No file selected'
            }, 400
        
        # Get parameters
        model_size = request.form.get('model', 'base')
        speaker_separation = request.form.get('speaker_separation', 'false').lower() == 'true'
        speaker_count = int(request.form.get('speaker_count', '2'))
        
        # Validate file type
        allowed_extensions = {'mp3', 'wav', 'm4a', 'flac', 'ogg', 'mp4'}
        if not ('.' in file.filename and 
                file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
            return {
                'success': False,
                'error': 'File type not supported'
            }, 400
        
        # Check file size (Vercel has limits)
        max_size = int(os.getenv('MAX_FILE_SIZE', '10')) * 1024 * 1024  # Default 10MB
        
        # Read file content to check size
        file_content = file.read()
        if len(file_content) > max_size:
            return {
                'success': False,
                'error': f'File too large for serverless processing. Maximum size: {max_size // (1024*1024)}MB'
            }, 400
        
        file.seek(0)  # Reset file pointer after reading
        
        # For Vercel deployment, we'll use external AI services
        # Check if OpenAI API key is available
        if os.getenv('OPENAI_API_KEY'):
            result = transcribe_with_openai_api(file, model_size, speaker_separation)
        else:
            # Fallback for demonstration
            result = transcribe_fallback(file, model_size, speaker_separation)
        
        return {
            'success': True,
            'result': result,
            'metadata': {
                'filename': file.filename,
                'model': model_size,
                'speaker_separation': speaker_separation,
                'processed_at': datetime.now().isoformat(),
                'environment': 'vercel_serverless'
            }
        }
        
    except Exception as e:
        print(f"Transcription error: {str(e)}")
        print(traceback.format_exc())
        return {
            'success': False,
            'error': f'Transcription failed: {str(e)}'
        }, 500

def transcribe_with_openai_api(file, model_size, speaker_separation):
    """
    Use OpenAI API for transcription (recommended for Vercel)
    Requires OPENAI_API_KEY environment variable
    """
    from openai import OpenAI
    
    # Set up OpenAI client
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    if not os.getenv('OPENAI_API_KEY'):
        raise Exception("OpenAI API key not configured. Set OPENAI_API_KEY environment variable.")
    
    try:
        # Save file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file.filename.split(".")[-1]}') as tmp_file:
            file.save(tmp_file.name)
            
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
                'duration': transcript.get('duration', 0),
                'language': transcript.get('language', 'unknown'),
                'segments': []
            }
            
            # Convert OpenAI segments to our format
            if hasattr(transcript, 'segments'):
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

def transcribe_fallback(file, model_size, speaker_separation):
    """
    Fallback transcription for demonstration purposes
    In production, replace this with actual AI service integration
    """
    return {
        'text': f'Transcription placeholder for file: {file.filename}. To enable real transcription, configure an AI service API key.',
        'duration': 60,  # Placeholder duration
        'language': 'en',
        'segments': [
            {
                'start': 0,
                'end': 30,
                'text': f'This is a placeholder transcription for {file.filename}.',
                'speaker': 'Speaker 1'
            },
            {
                'start': 30,
                'end': 60,
                'text': 'Configure OpenAI API key or another AI service for real transcription.',
                'speaker': 'Speaker 2' if speaker_separation else 'Speaker 1'
            }
        ]
    }

# For local development testing
if __name__ == '__main__':
    print("This is a Vercel serverless function. Deploy to Vercel to test.")
