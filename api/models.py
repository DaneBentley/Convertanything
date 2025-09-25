import json

def handler(request):
    """Available models endpoint for Vercel"""
    
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': ''
        }
    
    if request.method == 'GET':
        models = [
            {'id': 'tiny', 'name': 'Tiny', 'description': 'Fastest, lower accuracy (~39 MB)'},
            {'id': 'base', 'name': 'Base', 'description': 'Recommended balance (~74 MB)'},
            {'id': 'small', 'name': 'Small', 'description': 'Better accuracy (~244 MB)'},
            {'id': 'medium', 'name': 'Medium', 'description': 'High accuracy (~769 MB)'},
            {'id': 'large', 'name': 'Large', 'description': 'Best accuracy (~1550 MB)'}
        ]
        
        response = {
            'models': models,
            'default': 'base'
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