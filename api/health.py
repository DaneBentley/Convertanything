import json
from datetime import datetime

def handler(request):
    """Health check endpoint for Vercel"""
    
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': ''
        }
    
    # Health check response
    if request.method == 'GET':
        response = {
            'status': 'healthy',
            'message': 'ConvertAnything API is running on Vercel',
            'timestamp': datetime.now().isoformat(),
            'environment': 'production',
            'version': '1.0.0'
        }
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(response)
        }
    
    # Method not allowed
    return {
        'statusCode': 405,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({'error': 'Method not allowed'})
    }
