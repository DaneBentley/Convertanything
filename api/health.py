from datetime import datetime

def handler(request):
    """Health check endpoint for Vercel"""
    
    if request.method == 'GET':
        return {
            'status': 'healthy',
            'message': 'ConvertAnything API is running on Vercel',
            'timestamp': datetime.now().isoformat(),
            'environment': 'production',
            'version': '1.0.0'
        }
    
    return {'error': 'Method not allowed'}, 405
