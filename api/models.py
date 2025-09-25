def handler(request):
    """Get available models endpoint for Vercel"""
    
    if request.method == 'GET':
        # For serverless deployment, we'll use cloud AI services
        # These models represent what's available through external APIs
        models = [
            {
                'id': 'whisper-1', 
                'name': 'Whisper-1 (OpenAI)', 
                'description': 'OpenAI Whisper API - Best accuracy and speed'
            },
            {
                'id': 'base', 
                'name': 'Base', 
                'description': 'Balanced performance (fallback mode)'
            },
            {
                'id': 'small', 
                'name': 'Small', 
                'description': 'Better accuracy (fallback mode)'
            },
            {
                'id': 'medium', 
                'name': 'Medium', 
                'description': 'High accuracy (fallback mode)'
            }
        ]
        
        return {
            'models': models,
            'default': 'whisper-1',
            'environment': 'vercel_serverless',
            'note': 'Using cloud AI services for serverless deployment'
        }
    
    return {'error': 'Method not allowed'}, 405
