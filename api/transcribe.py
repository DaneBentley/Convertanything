import json
import os
import tempfile
from datetime import datetime
import traceback

def handler(request):
    """Transcription endpoint for Vercel"""
    
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': ''
        }
    
    if request.method != 'POST':
        return {
            'statusCode': 405,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'Method not allowed'})
        }
    
    try:
        # Check if OpenAI API key is configured
        if not os.getenv('OPENAI_API_KEY'):
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'success': False,
                    'error': 'OpenAI API key not configured. Please set OPENAI_API_KEY environment variable in Vercel dashboard.'
                })
            }
        
        # For now, return a placeholder response since we need multipart form handling
        # This would need proper multipart parsing for file uploads
        response = {
            'success': True,
            'result': {
                'text': 'Transcription service is configured and ready. To enable file uploads, please implement multipart form parsing.',
                'duration': 0,
                'language': 'en',
                'segments': []
            },
            'metadata': {
                'filename': 'placeholder',
                'model': 'whisper-1',
                'speaker_separation': False,
                'processed_at': datetime.now().isoformat(),
                'environment': 'vercel_serverless'
            }
        }
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(response)
        }
        
    except Exception as e:
        print(f"Transcription error: {str(e)}")
        print(traceback.format_exc())
        
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'success': False,
                'error': f'Transcription failed: {str(e)}'
            })
        }